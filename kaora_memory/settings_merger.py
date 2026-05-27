"""Intelligent merge for .claude/settings.json (ADR-006 v2).

Implements the brownfield policy defined in ADR-006 v2:
- permissions.allow / permissions.deny → deduplicated union, existing first
- hooks.<event> → array union grouped by `matcher`, dedup by `command`
- every other key from existing → preserved 1:1

Edge cases:
- malformed JSON → returns (None, message) without writing anything
- missing file → returns a copy of the template
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any


__all__ = ["merge_settings", "merge_claude_settings"]


_HOOK_EVENT_KEYS = ("PreToolUse", "PostToolUse", "Stop", "SubagentStop", "Notification")


def merge_settings(existing: dict[str, Any], template: dict[str, Any]) -> dict[str, Any]:
    """Pure merge between two settings.json dicts following ADR-006 v2."""
    merged: dict[str, Any] = copy.deepcopy(existing)

    for key, template_value in template.items():
        if key == "permissions":
            merged["permissions"] = _merge_permissions(
                merged.get("permissions"), template_value
            )
        elif key == "hooks":
            merged["hooks"] = _merge_hooks(merged.get("hooks"), template_value)
        else:
            if key not in merged:
                merged[key] = copy.deepcopy(template_value)

    return merged


def merge_claude_settings(
    existing_path: Path, template: dict[str, Any]
) -> tuple[dict[str, Any] | None, str | None]:
    """Load `existing_path`, run the merge, return (merged, error).

    - Missing file → (deepcopy(template), None)
    - Malformed JSON → (None, "JSON parse error: ...") with no writes
    - Success → (merged_dict, None)

    This function does NOT write to disk: writing (and the .kaora-bak backup)
    is the caller's responsibility (installer.py).
    """
    if not existing_path.exists():
        return copy.deepcopy(template), None

    try:
        raw = existing_path.read_text(encoding="utf-8")
        existing = json.loads(raw)
    except json.JSONDecodeError as exc:
        return None, f"JSON parse error in {existing_path}: {exc}"
    except OSError as exc:
        return None, f"Cannot read {existing_path}: {exc}"

    if not isinstance(existing, dict):
        return None, f"JSON root in {existing_path} must be an object, got {type(existing).__name__}"

    return merge_settings(existing, template), None


def _merge_permissions(
    existing: dict[str, Any] | None, template: dict[str, Any]
) -> dict[str, Any]:
    if existing is None:
        return copy.deepcopy(template)

    merged: dict[str, Any] = copy.deepcopy(existing)
    for bucket in ("allow", "deny"):
        existing_list = list(merged.get(bucket, []))
        template_list = list(template.get(bucket, []))
        merged[bucket] = _ordered_union(existing_list, template_list)

    for key, value in template.items():
        if key not in ("allow", "deny") and key not in merged:
            merged[key] = copy.deepcopy(value)

    return merged


def _merge_hooks(
    existing: dict[str, Any] | None, template: dict[str, Any]
) -> dict[str, Any]:
    if existing is None:
        return copy.deepcopy(template)

    merged: dict[str, Any] = copy.deepcopy(existing)

    for event, template_blocks in template.items():
        if event not in merged:
            merged[event] = copy.deepcopy(template_blocks)
            continue

        if not isinstance(merged[event], list) or not isinstance(template_blocks, list):
            continue

        merged[event] = _merge_hook_blocks(merged[event], template_blocks)

    return merged


def _merge_hook_blocks(
    existing_blocks: list[dict[str, Any]], template_blocks: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    result = [copy.deepcopy(b) for b in existing_blocks]
    index_by_matcher = {
        b.get("matcher"): i for i, b in enumerate(result) if isinstance(b, dict)
    }

    for tpl_block in template_blocks:
        if not isinstance(tpl_block, dict):
            continue
        matcher = tpl_block.get("matcher")
        tpl_hooks = tpl_block.get("hooks", [])
        if matcher in index_by_matcher:
            existing_block = result[index_by_matcher[matcher]]
            existing_hooks = list(existing_block.get("hooks", []))
            existing_block["hooks"] = _dedup_hook_commands(existing_hooks, tpl_hooks)
        else:
            new_block = copy.deepcopy(tpl_block)
            result.append(new_block)
            index_by_matcher[matcher] = len(result) - 1

    return result


def _dedup_hook_commands(
    existing_hooks: list[Any], template_hooks: list[Any]
) -> list[Any]:
    seen_commands = {
        h["command"]
        for h in existing_hooks
        if isinstance(h, dict) and "command" in h
    }
    result = [copy.deepcopy(h) for h in existing_hooks]
    for hook in template_hooks:
        if not isinstance(hook, dict):
            continue
        cmd = hook.get("command")
        if cmd is not None and cmd in seen_commands:
            continue
        result.append(copy.deepcopy(hook))
        if cmd is not None:
            seen_commands.add(cmd)
    return result


def _ordered_union(existing: list[Any], template: list[Any]) -> list[Any]:
    seen: set[Any] = set()
    result: list[Any] = []
    for item in list(existing) + list(template):
        # Hashable items only: for non-hashable items fall back to linear comparison
        try:
            if item in seen:
                continue
            seen.add(item)
        except TypeError:
            if item in result:
                continue
        result.append(item)
    return result
