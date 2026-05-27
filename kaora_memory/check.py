"""kaora-memory check — linter integrità memoria operativa.

Diagnostica un progetto post-`kaora init` su 6 categorie:
structure, adr005, adr_state, placeholders, hooks, settings.

Severità: error / warn / info / ok. Exit code 0 di default; --strict promuove
warn a 1. Output text o JSON via format_text() / format_json().
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
                message=f"{rel} mancante",
                hint="esegui `kaora init` o ripristina dal .kaora-bak",
            ))

    settings = target / ".claude" / "settings.json"
    if settings.is_file():
        try:
            json.loads(settings.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            report.results.append(CheckResult(
                level="error",
                category="structure",
                message=f".claude/settings.json non è JSON valido: {exc.msg}",
            ))


# ---------------------------------------------------------------------------
# 2. ADR-005 — canonico AGENTS.md + import @AGENTS.md in CLAUDE.md
# ---------------------------------------------------------------------------

_AGENTS_MIN_LINES = 50


def _check_adr005(target: Path, report: CheckReport) -> None:
    claude = target / "CLAUDE.md"
    if claude.is_file() and "@AGENTS.md" not in claude.read_text(encoding="utf-8"):
        report.results.append(CheckResult(
            level="warn",
            category="adr005",
            message="CLAUDE.md non contiene direttiva @AGENTS.md (vedi ADR-005)",
            hint="aggiungi una riga `@AGENTS.md` per importare il canonico",
        ))

    agents = target / "AGENTS.md"
    if agents.is_file():
        n_lines = len(agents.read_text(encoding="utf-8").splitlines())
        if n_lines < _AGENTS_MIN_LINES:
            report.results.append(CheckResult(
                level="warn",
                category="adr005",
                message=(
                    f"AGENTS.md sembra mutilato ({n_lines} righe, "
                    f"minimo atteso {_AGENTS_MIN_LINES}) — popola le sezioni canoniche"
                ),
            ))


# ---------------------------------------------------------------------------
# 3. ADR STATE — almeno una Accepted, segnala Proposed
# ---------------------------------------------------------------------------

_RE_ADR_ACCEPTED = re.compile(r"\*\*Stato:\*\*\s*Accepted", re.IGNORECASE)
_RE_ADR_PROPOSED = re.compile(r"\*\*Stato:\*\*\s*Proposed", re.IGNORECASE)
_RE_FENCED_CODE_BLOCK = re.compile(r"```.*?```", re.DOTALL)


def _strip_code_blocks(content: str) -> str:
    """Rimuove fenced code blocks per evitare di matchare esempi template."""
    return _RE_FENCED_CODE_BLOCK.sub("", content)


def _check_adr_state(target: Path, report: CheckReport) -> None:
    decisions = target / "docs" / "DECISIONS.md"
    if not decisions.is_file():
        return  # error già loggato in _check_structure

    content = _strip_code_blocks(decisions.read_text(encoding="utf-8"))
    n_accepted = len(_RE_ADR_ACCEPTED.findall(content))
    n_proposed = len(_RE_ADR_PROPOSED.findall(content))

    if n_accepted == 0:
        report.results.append(CheckResult(
            level="info",
            category="adr_state",
            message=f"nessuna ADR Accepted in docs/DECISIONS.md (proposed: {n_proposed})",
        ))
    if n_proposed > 0:
        report.results.append(CheckResult(
            level="info",
            category="adr_state",
            message=f"{n_proposed} ADR in stato Proposed da decidere",
        ))


# ---------------------------------------------------------------------------
# 4. PLACEHOLDERS — strutturali (WARN) vs BOOTSTRAP (INFO)
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
    """Tutti i .md kaora-managed: root + docs/ ricorsivo, escluso
    docs/archive/** e docs/PHILOSOPHY.md (contenuto narrativo non
    soggetto a sostituzione)."""
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
        content = path.read_text(encoding="utf-8")

        for ph in _STRUCTURAL_PLACEHOLDERS:
            token = "{{" + ph + "}}"
            if token in content:
                report.results.append(CheckResult(
                    level="warn",
                    category="placeholders",
                    message=f"placeholder strutturale {token} ancora aperto in {rel}",
                    hint="riesegui `kaora init` o sostituisci a mano",
                ))

        for ph in _BOOTSTRAP_PLACEHOLDERS:
            token = "{{" + ph + "}}"
            if token in content:
                report.results.append(CheckResult(
                    level="info",
                    category="placeholders",
                    message=f"BOOTSTRAP placeholder {token} da riempire in {rel}",
                ))

        for match in _RE_BOOTSTRAP_MARKER.finditer(content):
            report.results.append(CheckResult(
                level="info",
                category="placeholders",
                message=f"BOOTSTRAP marker da riempire in {rel}: {match.group()}",
            ))


# ---------------------------------------------------------------------------
# 5. HOOKS — .claude/hooks/*.sh devono essere eseguibili
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
                message=f"{rel} non eseguibile",
                hint=f"chmod +x {rel}",
            ))


# ---------------------------------------------------------------------------
# 6. SETTINGS — .claude/settings.json referenzia hook kaora
# ---------------------------------------------------------------------------

_KAORA_HOOK_NAMES = ("protect-credentials.sh", "log-api-calls.sh")


def _check_settings(target: Path, report: CheckReport) -> None:
    settings = target / ".claude" / "settings.json"
    if not settings.is_file():
        return
    try:
        data = json.loads(settings.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return  # già loggato da _check_structure

    if not _has_kaora_hook_command(data):
        report.results.append(CheckResult(
            level="info",
            category="settings",
            message=(
                ".claude/settings.json non referenzia hook kaora "
                f"({', '.join(_KAORA_HOOK_NAMES)})"
            ),
            hint="riesegui `kaora init` per aggiungere gli hook standard",
        ))


def _has_kaora_hook_command(settings_data: object) -> bool:
    """Naviga settings.json e cerca un command che termini con un hook kaora.

    Struttura attesa Claude Code:
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
        lines.append("✅ OK — tutti i check passano")
    return "\n".join(lines).lstrip("\n")


def format_json(report: CheckReport) -> str:
    payload = {
        "results": [asdict(r) for r in report.results],
        "exit_code": report.exit_code(),
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)
