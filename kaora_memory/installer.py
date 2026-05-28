"""Install the kaora-memory template into a target directory (ADR-006 v2).

Brownfield policy:
- `CANONICAL_MARKDOWN` (CLAUDE.md, AGENTS.md, AGENT_BRIEF.md):
  backup `.kaora-bak` + overwrite with placeholder substitution.
- `JSON_MERGE_FILES` (.claude/settings.json): intelligent merge via
  settings_merger.merge_claude_settings, backup `.kaora-bak`.
- Everything else: write only if missing (skip-conservative).
- `RENAME`: README.md.tpl → README.md.

CLI flags:
- `force=True`: overwrite everything without backup, skip JSON merge.
- `dry_run=True`: populate the report without touching disk.
"""
from __future__ import annotations

import datetime
import json
import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

from kaora_memory.settings_merger import merge_claude_settings
from kaora_memory.template_resolver import get_template_root


__all__ = [
    "InstallReport",
    "install_template",
    "CANONICAL_MARKDOWN",
    "JSON_MERGE_FILES",
    "RENAME",
    "BACKUP_SUFFIX",
]


CANONICAL_MARKDOWN: frozenset[str] = frozenset(
    {"CLAUDE.md", "AGENTS.md", "AGENT_BRIEF.md"}
)
JSON_MERGE_FILES: frozenset[str] = frozenset({".claude/settings.json"})
RENAME: dict[str, str] = {"README.md.tpl": "README.md"}
BACKUP_SUFFIX = ".kaora-bak"

_TEXT_SUFFIXES = frozenset({".md", ".sh", ".json", ".tpl", ".txt"})


@dataclass
class InstallReport:
    """Outcome of install_template, paths relative to the target."""

    created: list[Path] = field(default_factory=list)
    backed_up: list[Path] = field(default_factory=list)
    merged: list[Path] = field(default_factory=list)
    skipped: list[Path] = field(default_factory=list)
    warnings: list[tuple[Path, str]] = field(default_factory=list)


def install_template(
    target: Path,
    *,
    force: bool = False,
    dry_run: bool = False,
    year: int | None = None,
) -> InstallReport:
    """Install the kaora-memory template into `target`, applying ADR-006 v2 policy."""
    target = Path(target).resolve()
    if not dry_run:
        target.mkdir(parents=True, exist_ok=True)

    template_root = get_template_root()
    effective_year = year if year is not None else datetime.datetime.now().year
    placeholders: dict[str, str] = {
        "{{project_name}}": target.name,
        "{{project_path}}": str(target),
        "{{year}}": str(effective_year),
    }

    report = InstallReport()

    for src in _iter_template_files(template_root):
        src_rel = src.relative_to(template_root).as_posix()
        dest_rel_posix = RENAME.get(src_rel, src_rel)
        dest_rel = Path(dest_rel_posix)
        dest = target / dest_rel

        _process(
            src=src,
            dest=dest,
            rel=dest_rel,
            placeholders=placeholders,
            force=force,
            dry_run=dry_run,
            report=report,
        )

    return report


# ---------------------------------------------------------------------------
# Internals
# ---------------------------------------------------------------------------


def _iter_template_files(root: Path) -> Iterator[Path]:
    for path in sorted(root.rglob("*")):
        if path.is_file():
            yield path


def _process(
    *,
    src: Path,
    dest: Path,
    rel: Path,
    placeholders: dict[str, str],
    force: bool,
    dry_run: bool,
    report: InstallReport,
) -> None:
    rel_posix = rel.as_posix()

    if force:
        _write_fresh(src, dest, rel, placeholders, dry_run, report)
        return

    if not dest.exists():
        _write_fresh(src, dest, rel, placeholders, dry_run, report)
        return

    # dest exists, not force → apply ADR-006 v2 policy
    if rel_posix in CANONICAL_MARKDOWN:
        _backup_and_write(src, dest, rel, placeholders, dry_run, report)
    elif rel_posix in JSON_MERGE_FILES:
        _merge_and_write(src, dest, rel, dry_run, report)
    else:
        report.skipped.append(rel)


def _write_fresh(
    src: Path,
    dest: Path,
    rel: Path,
    placeholders: dict[str, str],
    dry_run: bool,
    report: InstallReport,
) -> None:
    if dry_run:
        report.created.append(rel)
        return

    dest.parent.mkdir(parents=True, exist_ok=True)
    _write_with_placeholders(src, dest, placeholders)
    _preserve_executable(src, dest)
    report.created.append(rel)


def _find_free_backup_path(dest: Path) -> Path:
    """Return a backup path that doesn't yet exist on disk.

    Tries ``<dest>.kaora-bak`` first. If it's already taken — typical of a
    second ``kaora init`` run where the original pre-kaora backup is still
    on disk — rotates incrementally to ``.kaora-bak.1``, ``.kaora-bak.2``,
    and so on. The original pre-kaora content is therefore never silently
    overwritten by a subsequent install (ADR-006 v2 + post-launch hardening).
    """
    base = dest.parent / (dest.name + BACKUP_SUFFIX)
    if not base.exists():
        return base
    i = 1
    while True:
        candidate = dest.parent / (dest.name + BACKUP_SUFFIX + f".{i}")
        if not candidate.exists():
            return candidate
        i += 1


def _backup_and_write(
    src: Path,
    dest: Path,
    rel: Path,
    placeholders: dict[str, str],
    dry_run: bool,
    report: InstallReport,
) -> None:
    if dry_run:
        report.backed_up.append(rel)
        return

    bak = _find_free_backup_path(dest)
    shutil.copy2(dest, bak)
    _write_with_placeholders(src, dest, placeholders)
    report.backed_up.append(rel)


def _merge_and_write(
    src: Path,
    dest: Path,
    rel: Path,
    dry_run: bool,
    report: InstallReport,
) -> None:
    try:
        template_dict = json.loads(src.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        report.skipped.append(rel)
        report.warnings.append(
            (rel, f"template settings.json is not valid JSON: {exc.msg}")
        )
        return

    merged, error = merge_claude_settings(dest, template_dict)
    if error is not None or merged is None:
        report.skipped.append(rel)
        if error:
            report.warnings.append(
                (
                    rel,
                    f"could not merge existing settings.json: {error}. "
                    "kaora hooks NOT installed — fix the JSON or merge manually.",
                )
            )
        return

    if dry_run:
        report.merged.append(rel)
        return

    bak = _find_free_backup_path(dest)
    shutil.copy2(dest, bak)
    dest.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")
    report.merged.append(rel)


def _write_with_placeholders(
    src: Path, dest: Path, placeholders: dict[str, str]
) -> None:
    if src.suffix in _TEXT_SUFFIXES:
        try:
            content = src.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            dest.write_bytes(src.read_bytes())
            return
        for key, value in placeholders.items():
            content = content.replace(key, value)
        dest.write_text(content, encoding="utf-8")
    else:
        dest.write_bytes(src.read_bytes())


def _preserve_executable(src: Path, dest: Path) -> None:
    if src.suffix == ".sh":
        try:
            os.chmod(dest, 0o755)
        except OSError:
            pass
