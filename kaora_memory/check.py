"""kaora-memory check — operating-memory integrity linter.

Diagnoses a project post-`kaora init` across 6 categories:
structure, adr005, adr_state, placeholders, hooks, settings.

Severity: error / warn / info / ok. Exit code 0 by default; --strict
promotes warn to 1. Output text or JSON via format_text() / format_json().
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Literal

Level = Literal["error", "warn", "info", "ok"]


@dataclass
class CheckResult:
    level: Level
    category: str
    message: str
    hint: str | None = None


@dataclass
class CheckReport:
    results: list[CheckResult] = field(default_factory=list)

    @property
    def errors(self) -> list[CheckResult]:
        return [r for r in self.results if r.level == "error"]

    @property
    def warnings(self) -> list[CheckResult]:
        return [r for r in self.results if r.level == "warn"]

    def exit_code(self, strict: bool = False) -> int:
        if self.errors:
            return 1
        if strict and self.warnings:
            return 1
        return 0


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def check_project(target: Path) -> CheckReport:
    report = CheckReport()
    _check_structure(target, report)
    _check_adr005(target, report)
    _check_adr_state(target, report)
    _check_placeholders(target, report)
    _check_hooks(target, report)
    _check_settings(target, report)
    return report


# ---------------------------------------------------------------------------
# 1. STRUCTURE
# ---------------------------------------------------------------------------

_REQUIRED_FILES = (
    "AGENTS.md",
    "CLAUDE.md",
    "docs/IDENTITY.md",
    "docs/DECISIONS.md",
)


def _check_structure(target: Path, report: CheckReport) -> None:
    for rel in _REQUIRED_FILES:
        if not (target / rel).is_file():
            report.results.append(CheckResult(
                level="error",
                category="structure",
                message=f"{rel} missing",
                hint="run `kaora init` or restore from .kaora-bak",
            ))

    settings = target / ".claude" / "settings.json"
    if settings.is_file():
        try:
            json.loads(settings.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            report.results.append(CheckResult(
                level="error",
                category="structure",
                message=f".claude/settings.json is not valid JSON: {exc.msg}",
            ))


# ---------------------------------------------------------------------------
# 2. ADR-005 — canonical AGENTS.md + @AGENTS.md import in CLAUDE.md
# ---------------------------------------------------------------------------

_AGENTS_MIN_LINES = 50


def _check_adr005(target: Path, report: CheckReport) -> None:
    claude = target / "CLAUDE.md"
    if claude.is_file() and "@AGENTS.md" not in claude.read_text(encoding="utf-8"):
        report.results.append(CheckResult(
            level="warn",
            category="adr005",
            message="CLAUDE.md does not contain @AGENTS.md directive (see ADR-005)",
            hint="add a line `@AGENTS.md` to import the canonical file",
        ))

    agents = target / "AGENTS.md"
    if agents.is_file():
        n_lines = len(agents.read_text(encoding="utf-8").splitlines())
        if n_lines < _AGENTS_MIN_LINES:
            report.results.append(CheckResult(
                level="warn",
                category="adr005",
                message=(
                    f"AGENTS.md looks mutilated ({n_lines} lines, "
                    f"expected at least {_AGENTS_MIN_LINES}) — populate the canonical sections"
                ),
            ))


# ---------------------------------------------------------------------------
# 3. ADR STATE — at least one Accepted, flag Proposed
# ---------------------------------------------------------------------------

_RE_ADR_ACCEPTED = re.compile(r"\*\*Status:\*\*\s*Accepted", re.IGNORECASE)
_RE_ADR_PROPOSED = re.compile(r"\*\*Status:\*\*\s*Proposed", re.IGNORECASE)
_RE_FENCED_CODE_BLOCK = re.compile(r"```.*?```", re.DOTALL)


def _strip_code_blocks(content: str) -> str:
    """Remove fenced code blocks to avoid matching template examples."""
    return _RE_FENCED_CODE_BLOCK.sub("", content)


def _check_adr_state(target: Path, report: CheckReport) -> None:
    decisions = target / "docs" / "DECISIONS.md"
    if not decisions.is_file():
        return  # error already logged in _check_structure

    content = _strip_code_blocks(decisions.read_text(encoding="utf-8"))
    n_accepted = len(_RE_ADR_ACCEPTED.findall(content))
    n_proposed = len(_RE_ADR_PROPOSED.findall(content))

    if n_accepted == 0:
        report.results.append(CheckResult(
            level="info",
            category="adr_state",
            message=f"no Accepted ADR in docs/DECISIONS.md (proposed: {n_proposed})",
        ))
    if n_proposed > 0:
        report.results.append(CheckResult(
            level="info",
            category="adr_state",
            message=f"{n_proposed} ADR(s) in Proposed state awaiting decision",
        ))


# ---------------------------------------------------------------------------
# 4. PLACEHOLDERS — structural (WARN) vs BOOTSTRAP (INFO)
# ---------------------------------------------------------------------------

_STRUCTURAL_PLACEHOLDERS = ("project_name", "project_path", "year")
_BOOTSTRAP_PLACEHOLDERS = (
    "owner_name",
    "owner_email",
    "project_oneliner",
    "communication_register",
    "communication_language",
)
_RE_BOOTSTRAP_MARKER = re.compile(r"<BOOTSTRAP[^>]*/?>", re.IGNORECASE)
_PLACEHOLDER_EXCLUDE_NAMES = {"PHILOSOPHY.md"}
_PLACEHOLDER_EXCLUDE_DIR_PARTS = {"archive"}


def _placeholder_scan_paths(target: Path) -> list[Path]:
    """All kaora-managed .md files: root + recursive docs/, excluding
    docs/archive/** and docs/PHILOSOPHY.md (narrative content, not subject
    to substitution)."""
    paths: list[Path] = sorted(target.glob("*.md"))
    docs = target / "docs"
    if docs.is_dir():
        for p in sorted(docs.rglob("*.md")):
            parts = p.relative_to(target).parts
            if _PLACEHOLDER_EXCLUDE_DIR_PARTS.intersection(parts):
                continue
            if p.name in _PLACEHOLDER_EXCLUDE_NAMES:
                continue
            paths.append(p)
    return paths


def _check_placeholders(target: Path, report: CheckReport) -> None:
    for path in _placeholder_scan_paths(target):
        rel = path.relative_to(target).as_posix()
        content = _strip_code_blocks(path.read_text(encoding="utf-8"))

        for ph in _STRUCTURAL_PLACEHOLDERS:
            token = "{{" + ph + "}}"
            if token in content:
                report.results.append(CheckResult(
                    level="warn",
                    category="placeholders",
                    message=f"structural placeholder {token} still open in {rel}",
                    hint="re-run `kaora init` or replace manually",
                ))

        for ph in _BOOTSTRAP_PLACEHOLDERS:
            token = "{{" + ph + "}}"
            if token in content:
                report.results.append(CheckResult(
                    level="info",
                    category="placeholders",
                    message=f"BOOTSTRAP placeholder {token} to fill in {rel}",
                ))

        for match in _RE_BOOTSTRAP_MARKER.finditer(content):
            report.results.append(CheckResult(
                level="info",
                category="placeholders",
                message=f"BOOTSTRAP marker to fill in {rel}: {match.group()}",
            ))


# ---------------------------------------------------------------------------
# 5. HOOKS — .claude/hooks/*.sh must be executable
# ---------------------------------------------------------------------------


def _check_hooks(target: Path, report: CheckReport) -> None:
    hooks_dir = target / ".claude" / "hooks"
    if not hooks_dir.is_dir():
        return
    for hook in sorted(hooks_dir.glob("*.sh")):
        if not os.access(hook, os.X_OK):
            rel = hook.relative_to(target).as_posix()
            report.results.append(CheckResult(
                level="warn",
                category="hooks",
                message=f"{rel} not executable",
                hint=f"chmod +x {rel}",
            ))


# ---------------------------------------------------------------------------
# 6. SETTINGS — .claude/settings.json references kaora hooks
# ---------------------------------------------------------------------------

_KAORA_HOOK_NAMES = ("protect-credentials.sh", "log-api-calls.sh")


def _check_settings(target: Path, report: CheckReport) -> None:
    settings = target / ".claude" / "settings.json"
    if not settings.is_file():
        return
    try:
        data = json.loads(settings.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return  # already logged by _check_structure

    if not _has_kaora_hook_command(data):
        report.results.append(CheckResult(
            level="info",
            category="settings",
            message=(
                ".claude/settings.json does not reference kaora hooks "
                f"({', '.join(_KAORA_HOOK_NAMES)})"
            ),
            hint="re-run `kaora init` to add the standard hooks",
        ))


def _has_kaora_hook_command(settings_data: object) -> bool:
    """Walk settings.json and look for a command that ends with a kaora hook.

    Expected Claude Code structure:
      settings["hooks"][<Event>] = [{"matcher": ..., "hooks": [{"command": "..."}, ...]}, ...]
    """
    if not isinstance(settings_data, dict):
        return False
    hooks_root = settings_data.get("hooks")
    if not isinstance(hooks_root, dict):
        return False
    for event_entries in hooks_root.values():
        if not isinstance(event_entries, list):
            continue
        for entry in event_entries:
            if not isinstance(entry, dict):
                continue
            for hook in entry.get("hooks", []) or []:
                if not isinstance(hook, dict):
                    continue
                command = hook.get("command", "")
                if isinstance(command, str) and any(
                    command.endswith(name) or f"/{name}" in command
                    for name in _KAORA_HOOK_NAMES
                ):
                    return True
    return False


# ---------------------------------------------------------------------------
# Formatters
# ---------------------------------------------------------------------------

_LEVEL_HEADER = {
    "error": "❌ ERROR",
    "warn": "⚠️  WARN",
    "info": "ℹ️  INFO",
    "ok": "✅ OK",
}


def format_text(report: CheckReport, quiet: bool = False) -> str:
    levels: tuple[Level, ...] = ("error",) if quiet else ("error", "warn", "info")
    lines: list[str] = []
    for lvl in levels:
        items = [r for r in report.results if r.level == lvl]
        if not items:
            continue
        lines.append(f"\n{_LEVEL_HEADER[lvl]}:")
        for r in items:
            line = f"  [{r.category}] {r.message}"
            if r.hint:
                line += f"\n      hint: {r.hint}"
            lines.append(line)
    if not lines:
        lines.append("✅ OK — all checks pass")
    return "\n".join(lines).lstrip("\n")


def format_json(report: CheckReport) -> str:
    payload = {
        "results": [asdict(r) for r in report.results],
        "exit_code": report.exit_code(),
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)
