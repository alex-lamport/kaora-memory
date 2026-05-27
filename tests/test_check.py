"""Test per kaora_memory.check.check_project (Blocco 4).

Linter integrità memoria operativa post-`kaora init`. Sei categorie di check:
- structure: file/cartelle minime presenti
- adr005: CLAUDE.md importa @AGENTS.md, AGENTS.md ricco a sufficienza
- adr_state: presenza ADR Accepted, segnalazione Proposed
- placeholders: distingue strutturali (WARN) da BOOTSTRAP (INFO)
- hooks: .claude/hooks/*.sh eseguibili
- settings: .claude/settings.json contiene hook kaora attesi

Severity: error / warn / info / ok.
Exit code: 0 di default; --strict promuove warn a error.

Fixture: scriviamo lo scheletro minimo direttamente, NON dipendiamo da template/ reale
(così cambi al template non rompono questi test).
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from kaora_memory.check import (
    CheckResult,
    CheckReport,
    check_project,
    format_text,
    format_json,
)


# ---------------------------------------------------------------------------
# Fixture builder
# ---------------------------------------------------------------------------

def _valid_project(target: Path) -> None:
    """Scrive uno scheletro kaora che passa tutti i check (tutto OK / INFO).

    Tutti i test partono da qui e rompono UN aspetto per volta.
    """
    target.mkdir(parents=True, exist_ok=True)

    # AGENTS.md: ricco (>=50 righe), senza placeholder strutturali aperti.
    # Lascia un BOOTSTRAP marker per simulare progetto fresco post-init (INFO atteso).
    agents_lines = [
        "# AGENTS.md — fixture project",
        "",
        "## 1. Identità",
        "",
        "Project fixture per test di check.",
        "",
        "## 2. Stack",
        "",
        '<BOOTSTRAP need="tech-stack" sources="pyproject.toml"/>',
        "",
    ]
    # Pad a >50 righe con sezioni placeholder valide.
    for i in range(3, 20):
        agents_lines += [f"## {i}. Sezione", "", f"Contenuto sezione {i}.", ""]
    (target / "AGENTS.md").write_text("\n".join(agents_lines), encoding="utf-8")

    # CLAUDE.md con direttiva @AGENTS.md
    (target / "CLAUDE.md").write_text(
        "# CLAUDE.md\n\n> Entry point per Claude Code.\n\n@AGENTS.md\n",
        encoding="utf-8",
    )

    # docs/
    docs = target / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "IDENTITY.md").write_text("# IDENTITY\n", encoding="utf-8")
    (docs / "DECISIONS.md").write_text(
        "# DECISIONS\n\n## ADR-001 Esempio\n\n**Stato:** Accepted\n\nDecisione presa.\n",
        encoding="utf-8",
    )

    # .claude/settings.json con hook kaora attesi
    claude = target / ".claude"
    hooks = claude / "hooks"
    hooks.mkdir(parents=True, exist_ok=True)
    (claude / "settings.json").write_text(
        json.dumps(
            {
                "hooks": {
                    "PreToolUse": [
                        {
                            "matcher": "Write|Edit",
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
        ),
        encoding="utf-8",
    )
    hook = hooks / "protect-credentials.sh"
    hook.write_text("#!/bin/sh\necho protect\n", encoding="utf-8")
    hook.chmod(0o755)


def _levels(report: CheckReport, category: str) -> list[str]:
    return [r.level for r in report.results if r.category == category]


# ---------------------------------------------------------------------------
# 1. STRUCTURE (5)
# ---------------------------------------------------------------------------

def test_structure_missing_agents_md_is_error(tmp_path: Path):
    _valid_project(tmp_path)
    (tmp_path / "AGENTS.md").unlink()

    report = check_project(tmp_path)

    assert "error" in _levels(report, "structure")
    assert any("AGENTS.md" in r.message for r in report.errors)


def test_structure_missing_claude_md_is_error(tmp_path: Path):
    _valid_project(tmp_path)
    (tmp_path / "CLAUDE.md").unlink()

    report = check_project(tmp_path)

    assert "error" in _levels(report, "structure")
    assert any("CLAUDE.md" in r.message for r in report.errors)


def test_structure_missing_docs_decisions_is_error(tmp_path: Path):
    _valid_project(tmp_path)
    (tmp_path / "docs" / "DECISIONS.md").unlink()

    report = check_project(tmp_path)

    assert "error" in _levels(report, "structure")
    assert any("DECISIONS.md" in r.message for r in report.errors)


def test_structure_invalid_settings_json_is_error(tmp_path: Path):
    _valid_project(tmp_path)
    (tmp_path / ".claude" / "settings.json").write_text(
        "{ not valid json", encoding="utf-8"
    )

    report = check_project(tmp_path)

    assert "error" in _levels(report, "structure")
    assert any("settings.json" in r.message for r in report.errors)


def test_structure_all_present_is_ok(tmp_path: Path):
    _valid_project(tmp_path)

    report = check_project(tmp_path)

    assert "error" not in _levels(report, "structure")


# ---------------------------------------------------------------------------
# 2. ADR-005 — canonico + import (3)
# ---------------------------------------------------------------------------

def test_adr005_claude_without_import_directive_is_warn(tmp_path: Path):
    _valid_project(tmp_path)
    (tmp_path / "CLAUDE.md").write_text(
        "# CLAUDE.md\n\nNessuna direttiva di import qui.\n", encoding="utf-8"
    )

    report = check_project(tmp_path)

    assert "warn" in _levels(report, "adr005")
    assert any("@AGENTS.md" in r.message for r in report.warnings)


def test_adr005_agents_too_short_is_warn(tmp_path: Path):
    _valid_project(tmp_path)
    (tmp_path / "AGENTS.md").write_text(
        "# AGENTS.md\n\nTroppo corto.\n", encoding="utf-8"
    )

    report = check_project(tmp_path)

    assert "warn" in _levels(report, "adr005")
    assert any("AGENTS.md" in r.message and "righe" in r.message
               for r in report.warnings)


def test_adr005_canonical_setup_is_ok(tmp_path: Path):
    _valid_project(tmp_path)

    report = check_project(tmp_path)

    assert "warn" not in _levels(report, "adr005")
    assert "error" not in _levels(report, "adr005")


# ---------------------------------------------------------------------------
# 3. ADR STATE (3)
# ---------------------------------------------------------------------------

def test_adr_state_zero_adr_is_info(tmp_path: Path):
    _valid_project(tmp_path)
    (tmp_path / "docs" / "DECISIONS.md").write_text(
        "# DECISIONS\n\nNessuna ADR registrata.\n", encoding="utf-8"
    )

    report = check_project(tmp_path)

    assert "info" in _levels(report, "adr_state")
    assert "error" not in _levels(report, "adr_state")


def test_adr_state_only_proposed_is_info(tmp_path: Path):
    _valid_project(tmp_path)
    (tmp_path / "docs" / "DECISIONS.md").write_text(
        "# DECISIONS\n\n## ADR-001 Bozza\n\n**Stato:** Proposed\n",
        encoding="utf-8",
    )

    report = check_project(tmp_path)

    info_msgs = [r.message for r in report.results
                 if r.category == "adr_state" and r.level == "info"]
    assert any("Proposed" in m for m in info_msgs)


def test_adr_state_has_accepted_is_ok(tmp_path: Path):
    _valid_project(tmp_path)

    report = check_project(tmp_path)

    levels = _levels(report, "adr_state")
    # Almeno una Accepted → niente warn, niente error
    assert "warn" not in levels
    assert "error" not in levels


# ---------------------------------------------------------------------------
# 4. PLACEHOLDERS (3)
# ---------------------------------------------------------------------------

def test_placeholders_structural_open_is_warn(tmp_path: Path):
    _valid_project(tmp_path)
    # Iniettiamo un placeholder strutturale aperto in AGENTS.md
    current = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    (tmp_path / "AGENTS.md").write_text(
        current + "\n\nProject path: {{project_path}}\n", encoding="utf-8"
    )

    report = check_project(tmp_path)

    assert "warn" in _levels(report, "placeholders")
    assert any("project_path" in r.message for r in report.warnings)


def test_placeholders_bootstrap_marker_open_is_info(tmp_path: Path):
    # _valid_project lascia già <BOOTSTRAP need="tech-stack"/> aperto
    _valid_project(tmp_path)

    report = check_project(tmp_path)

    placeholder_results = [r for r in report.results if r.category == "placeholders"]
    info_present = any(r.level == "info" for r in placeholder_results)
    assert info_present, "BOOTSTRAP marker aperto deve generare almeno un INFO"
    # NON deve essere un WARN
    assert "warn" not in [r.level for r in placeholder_results]


def test_placeholders_clean_is_ok(tmp_path: Path):
    _valid_project(tmp_path)
    # Rimuoviamo anche il BOOTSTRAP marker per avere un AGENTS completamente pulito
    agents = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    cleaned = agents.replace(
        '<BOOTSTRAP need="tech-stack" sources="pyproject.toml"/>',
        "Python 3.10+, pytest, click",
    )
    (tmp_path / "AGENTS.md").write_text(cleaned, encoding="utf-8")

    report = check_project(tmp_path)

    levels = _levels(report, "placeholders")
    assert "warn" not in levels
    assert "error" not in levels


# ---------------------------------------------------------------------------
# 5. HOOKS (2)
# ---------------------------------------------------------------------------

def test_hooks_not_executable_is_warn(tmp_path: Path):
    _valid_project(tmp_path)
    (tmp_path / ".claude" / "hooks" / "protect-credentials.sh").chmod(0o644)

    report = check_project(tmp_path)

    assert "warn" in _levels(report, "hooks")
    assert any("protect-credentials.sh" in r.message for r in report.warnings)


def test_hooks_executable_is_ok(tmp_path: Path):
    _valid_project(tmp_path)

    report = check_project(tmp_path)

    levels = _levels(report, "hooks")
    assert "warn" not in levels
    assert "error" not in levels


# ---------------------------------------------------------------------------
# 6. SETTINGS — hook kaora attesi (2)
# ---------------------------------------------------------------------------

def test_settings_without_kaora_hooks_is_info(tmp_path: Path):
    _valid_project(tmp_path)
    (tmp_path / ".claude" / "settings.json").write_text(
        json.dumps({"theme": "dark"}), encoding="utf-8"
    )

    report = check_project(tmp_path)

    assert "info" in _levels(report, "settings")


def test_settings_with_kaora_hooks_is_ok(tmp_path: Path):
    _valid_project(tmp_path)

    report = check_project(tmp_path)

    levels = _levels(report, "settings")
    assert "warn" not in levels
    assert "error" not in levels


# ---------------------------------------------------------------------------
# REPORT / FORMAT (3)
# ---------------------------------------------------------------------------

def test_report_exit_code_strict_promotes_warn(tmp_path: Path):
    _valid_project(tmp_path)
    # induciamo un warn (placeholder strutturale aperto)
    current = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    (tmp_path / "AGENTS.md").write_text(
        current + "\n\nName: {{project_name}}\n", encoding="utf-8"
    )

    report = check_project(tmp_path)

    assert report.exit_code(strict=False) == 0
    assert report.exit_code(strict=True) == 1


def test_report_format_text_contains_section_markers(tmp_path: Path):
    _valid_project(tmp_path)
    (tmp_path / "AGENTS.md").unlink()  # forza un error

    report = check_project(tmp_path)
    text = format_text(report)

    # markers visivi per livello
    assert any(token in text for token in ("ERROR", "❌"))
    assert "AGENTS.md" in text


def test_report_format_json_is_valid_json(tmp_path: Path):
    _valid_project(tmp_path)

    report = check_project(tmp_path)
    payload = format_json(report)

    data = json.loads(payload)
    assert "results" in data
    assert isinstance(data["results"], list)
    assert "exit_code" in data
