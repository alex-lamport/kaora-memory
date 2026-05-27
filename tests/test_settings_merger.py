"""Tests for the ADR-006 v2 merge policy for .claude/settings.json.

Four minimal cases required by the Block 3 Goal:
1. permissions union (allow + deny dedup)
2. hooks matcher append (matcher not present in existing)
3. hooks matcher conflict dedup (existing matcher, duplicate hook command deduplicated)
4. malformed JSON fail-safe (existing unreadable, no writes, error returned)
"""
from pathlib import Path

import pytest

from kaora_memory.settings_merger import merge_settings, merge_claude_settings


# ---------------------------------------------------------------------------
# Case 1 — permissions union
# ---------------------------------------------------------------------------

def test_permissions_union_preserves_user_and_adds_kaora():
    existing = {
        "permissions": {
            "allow": ["Bash(ls:*)", "Read(*)"],
            "deny": ["Bash(rm -rf /:*)"],
        }
    }
    template = {
        "permissions": {
            "allow": ["Read(*)", "Bash(python -m pytest:*)"],
            "deny": ["Bash(rm -rf /:*)", "Write(/etc/**)"],
        }
    }

    merged = merge_settings(existing, template)

    assert set(merged["permissions"]["allow"]) == {
        "Bash(ls:*)",
        "Read(*)",
        "Bash(python -m pytest:*)",
    }
    assert set(merged["permissions"]["deny"]) == {
        "Bash(rm -rf /:*)",
        "Write(/etc/**)",
    }
    assert len(merged["permissions"]["allow"]) == 3
    assert len(merged["permissions"]["deny"]) == 2


def test_permissions_missing_in_existing_uses_template():
    existing = {"theme": "dark"}
    template = {"permissions": {"allow": ["Read(*)"], "deny": []}}

    merged = merge_settings(existing, template)

    assert merged["permissions"]["allow"] == ["Read(*)"]
    assert merged["theme"] == "dark"


# ---------------------------------------------------------------------------
# Case 2 — hooks matcher append (matcher not present in existing)
# ---------------------------------------------------------------------------

def test_hooks_matcher_append_adds_whole_block_when_matcher_new():
    existing = {
        "hooks": {
            "PreToolUse": [
                {
                    "matcher": "Read",
                    "hooks": [
                        {"type": "command", "command": ".claude/hooks/user-read.sh"}
                    ],
                }
            ]
        }
    }
    template = {
        "hooks": {
            "PreToolUse": [
                {
                    "matcher": "Write|Edit|MultiEdit",
                    "hooks": [
                        {
                            "type": "command",
                            "command": ".claude/hooks/protect-credentials.sh",
                        }
                    ],
                }
            ],
            "PostToolUse": [
                {
                    "matcher": "Bash",
                    "hooks": [
                        {"type": "command", "command": ".claude/hooks/log-api-calls.sh"}
                    ],
                }
            ],
        }
    }

    merged = merge_settings(existing, template)

    pre = merged["hooks"]["PreToolUse"]
    assert len(pre) == 2
    matchers = {block["matcher"] for block in pre}
    assert matchers == {"Read", "Write|Edit|MultiEdit"}

    user_block = next(b for b in pre if b["matcher"] == "Read")
    assert user_block["hooks"] == [
        {"type": "command", "command": ".claude/hooks/user-read.sh"}
    ]

    kaora_block = next(b for b in pre if b["matcher"] == "Write|Edit|MultiEdit")
    assert kaora_block["hooks"] == [
        {"type": "command", "command": ".claude/hooks/protect-credentials.sh"}
    ]

    assert merged["hooks"]["PostToolUse"][0]["matcher"] == "Bash"


# ---------------------------------------------------------------------------
# Case 3 — hooks matcher conflict dedup
# ---------------------------------------------------------------------------

def test_hooks_matcher_conflict_appends_new_commands_and_dedupes():
    existing = {
        "hooks": {
            "PreToolUse": [
                {
                    "matcher": "Write|Edit|MultiEdit",
                    "hooks": [
                        {"type": "command", "command": ".claude/hooks/user-pre.sh"},
                        {
                            "type": "command",
                            "command": ".claude/hooks/protect-credentials.sh",
                        },
                    ],
                }
            ]
        }
    }
    template = {
        "hooks": {
            "PreToolUse": [
                {
                    "matcher": "Write|Edit|MultiEdit",
                    "hooks": [
                        {
                            "type": "command",
                            "command": ".claude/hooks/protect-credentials.sh",
                        }
                    ],
                }
            ]
        }
    }

    merged = merge_settings(existing, template)

    pre = merged["hooks"]["PreToolUse"]
    assert len(pre) == 1
    block = pre[0]
    assert block["matcher"] == "Write|Edit|MultiEdit"

    commands = [h["command"] for h in block["hooks"]]
    assert commands.count(".claude/hooks/protect-credentials.sh") == 1
    assert ".claude/hooks/user-pre.sh" in commands
    assert len(commands) == 2


# ---------------------------------------------------------------------------
# Case 4 — malformed JSON fail-safe
# ---------------------------------------------------------------------------

def test_malformed_json_returns_error_and_leaves_file_untouched(tmp_path: Path):
    settings_path = tmp_path / "settings.json"
    raw = "{ this is not valid json"
    settings_path.write_text(raw, encoding="utf-8")

    template_dict = {"permissions": {"allow": ["Read(*)"], "deny": []}}

    merged, error = merge_claude_settings(settings_path, template_dict)

    assert merged is None
    assert error is not None and "json" in error.lower()
    assert settings_path.read_text(encoding="utf-8") == raw


def test_merge_claude_settings_happy_path_returns_merged_dict(tmp_path: Path):
    settings_path = tmp_path / "settings.json"
    settings_path.write_text(
        '{"permissions": {"allow": ["Read(*)"], "deny": []}}',
        encoding="utf-8",
    )
    template_dict = {
        "permissions": {"allow": ["Bash(python:*)"], "deny": ["Write(/etc/**)"]},
    }

    merged, error = merge_claude_settings(settings_path, template_dict)

    assert error is None
    assert merged is not None
    assert set(merged["permissions"]["allow"]) == {"Read(*)", "Bash(python:*)"}
    assert merged["permissions"]["deny"] == ["Write(/etc/**)"]


def test_merge_claude_settings_missing_file_returns_template_copy(tmp_path: Path):
    settings_path = tmp_path / "settings.json"
    template_dict = {"permissions": {"allow": ["Read(*)"], "deny": []}}

    merged, error = merge_claude_settings(settings_path, template_dict)

    assert error is None
    assert merged == template_dict
    assert not settings_path.exists()


# ---------------------------------------------------------------------------
# Bonus case — non-hooks keys preserved
# ---------------------------------------------------------------------------

def test_unknown_keys_preserved_from_existing():
    existing = {
        "statusLine": {"type": "command", "command": "my-statusline.sh"},
        "env": {"DEBUG": "1"},
        "theme": "dark",
    }
    template = {"permissions": {"allow": ["Read(*)"], "deny": []}}

    merged = merge_settings(existing, template)

    assert merged["statusLine"] == {
        "type": "command",
        "command": "my-statusline.sh",
    }
    assert merged["env"] == {"DEBUG": "1"}
    assert merged["theme"] == "dark"
    assert merged["permissions"]["allow"] == ["Read(*)"]
