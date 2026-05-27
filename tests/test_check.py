"""Tests for kaora_memory.check.check_project (Block 4).

Operating-memory integrity linter post-`kaora init`. Six check categories:
- structure: minimal required files/folders present
- adr005: CLAUDE.md imports @AGENTS.md, AGENTS.md rich enough
- adr_state: presence of Accepted ADRs, flag Proposed
- placeholders: distinguish structural (WARN) from BOOTSTRAP (INFO)
- hooks: .claude/hooks/*.sh executable
- settings: .claude/settings.json contains the expected kaora hooks

Severity: error / warn / info / ok.
Exit code: 0 by default; --strict promotes warn to error.

Fixtures: we write the minimal skeleton directly, NOT depending on the real template/
(so changes to the template don't break these tests).
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
    """Write a kaora skeleton that passes all checks (everything OK / INFO).

    All tests start from here and break ONE aspect at a time.
    """
    target.mkdir(parents=True, exist_ok=True)

    # AGENTS.md: rich (>=50 lines), no open structural placeholders.
    # Leaves a BOOTSTRAP marker to simulate a fresh post-init project (INFO expected).
    agents_lines = [
        "# AGENTS.md — fixture project",
        "",
        "## 1. Identity",
        "",
        "Fixture project for check tests.",
        "",
        "## 2. Stack",
        "",
        '<BOOTSTRAP need="tech-stack" sources="pyproject.toml"/>',
        "",
    ]
    # Pad to >50 lines with valid placeholder sections.
    for i in range(3, 20):
        agents_lines += [f"## {i}. Section", "", f"Section {i} content.", ""]
    (target / "AGENTS.md").write_text("\n".join(agents_lines), encoding="utf-8")

    # CLAUDE.md with @AGENTS.md directive
    (target / "CLAUDE.md").write_text(
        "# CLAUDE.md\n\n> Entry point for Claude Code.\n\n@AGENTS.md\n",
        encoding="utf-8",
    )

    # docs/
    docs = target / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "IDENTITY.md").write_text("# IDENTITY\n", encoding="utf-8")
    (docs / "DECISIONS.md").write_text(
        "# DECISIONS\n\n## ADR-001 Example\n\n**Status:** Accepted\n\nDecision taken.\n",
        encoding="utf-8",
    )

    # .claude/settings.json with expected kaora hooks
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
# 2. ADR-005 — canonical + import (3)
# ---------------------------------------------------------------------------

def test_adr005_claude_without_import_directive_is_warn(tmp_path: Path):
    _valid_project(tmp_path)
    (tmp_path / "CLAUDE.md").write_text(
        "# CLAUDE.md\n\nNo import directive here.\n", encoding="utf-8"
    )

    report = check_project(tmp_path)

    assert "warn" in _levels(report, "adr005")
    assert any("@AGENTS.md" in r.message for r in report.warnings)


def test_adr005_agents_too_short_is_warn(tmp_path: Path):
    _valid_project(tmp_path)
    (tmp_path / "AGENTS.md").write_text(
        "# AGENTS.md\n\nToo short.\n", encoding="utf-8"
    )

    report = check_project(tmp_path)

    assert "warn" in _levels(report, "adr005")
    assert any("AGENTS.md" in r.message and "lines" in r.message
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
        "# DECISIONS\n\nNo ADR registered.\n", encoding="utf-8"
    )

    report = check_project(tmp_path)

    assert "info" in _levels(report, "adr_state")
    assert "error" not in _levels(report, "adr_state")


def test_adr_state_only_proposed_is_info(tmp_path: Path):
    _valid_project(tmp_path)
    (tmp_path / "docs" / "DECISIONS.md").write_text(
        "# DECISIONS\n\n## ADR-001 Draft\n\n**Status:** Proposed\n",
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
    # At least one Accepted → no warn, no error
    assert "warn" not in levels
    assert "error" not in levels


def test_adr_state_ignores_proposed_in_code_block(tmp_path: Path):
    """A **Status:** Proposed inside a fenced code block is a template example,
    not a real ADR. It must NOT generate INFO."""
    _valid_project(tmp_path)
    (tmp_path / "docs" / "DECISIONS.md").write_text(
        "# DECISIONS\n\n"
        "## ADR-001 Real\n\n"
        "**Status:** Accepted\n\n"
        "Decision taken.\n\n"
        "---\n\n"
        "Template for new ADRs (example, not a real ADR):\n\n"
        "```\n"
        "## ADR-XXX Title\n\n"
        "**Status:** Proposed\n"
        "```\n",
        encoding="utf-8",
    )

    report = check_project(tmp_path)

    proposed_infos = [
        r for r in report.results
        if r.category == "adr_state" and "Proposed" in r.message
    ]
    assert proposed_infos == [], (
        f"Expected 0 'Proposed' INFOs (they're inside a code-block), "
        f"found {len(proposed_infos)}: {[r.message for r in proposed_infos]}"
    )


# ---------------------------------------------------------------------------
# 4. PLACEHOLDERS (3)
# ---------------------------------------------------------------------------

def test_placeholders_structural_open_is_warn(tmp_path: Path):
    _valid_project(tmp_path)
    # Inject an open structural placeholder in AGENTS.md
    current = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    (tmp_path / "AGENTS.md").write_text(
        current + "\n\nProject path: {{project_path}}\n", encoding="utf-8"
    )

    report = check_project(tmp_path)

    assert "warn" in _levels(report, "placeholders")
    assert any("project_path" in r.message for r in report.warnings)


def test_placeholders_bootstrap_marker_open_is_info(tmp_path: Path):
    # _valid_project already leaves <BOOTSTRAP need="tech-stack"/> open
    _valid_project(tmp_path)

    report = check_project(tmp_path)

    placeholder_results = [r for r in report.results if r.category == "placeholders"]
    info_present = any(r.level == "info" for r in placeholder_results)
    assert info_present, "Open BOOTSTRAP marker must generate at least one INFO"
    # Must NOT be a WARN
    assert "warn" not in [r.level for r in placeholder_results]


def test_placeholders_clean_is_ok(tmp_path: Path):
    _valid_project(tmp_path)
    # Remove the BOOTSTRAP marker too so we have a fully clean AGENTS
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


def test_placeholders_scans_all_md_in_docs(tmp_path: Path):
    """Extra .md files in docs/ (e.g. CUSTOM.md, NOTES.md) must be
    scanned. A hardcoded list does not scale."""
    _valid_project(tmp_path)
    (tmp_path / "docs" / "CUSTOM.md").write_text(
        "# Custom\n\nProject: {{project_name}}\n", encoding="utf-8"
    )

    report = check_project(tmp_path)

    placeholder_warns = [r for r in report.warnings if r.category == "placeholders"]
    assert any("CUSTOM.md" in r.message for r in placeholder_warns), (
        f"Expected warn on docs/CUSTOM.md, warnings found: "
        f"{[r.message for r in placeholder_warns]}"
    )


def test_placeholders_ignores_open_inside_code_block(tmp_path: Path):
    """Placeholder and BOOTSTRAP markers inside a fenced code block are
    documentary examples (e.g. spec of the check itself), not real
    placeholders to substitute. Same pattern as the adr_state fix."""
    _valid_project(tmp_path)
    (tmp_path / "docs" / "SPEC.md").write_text(
        "# Spec check\n\n"
        "Example of expected output:\n\n"
        "```\n"
        "PATH = {{project_path}}\n"
        "YEAR = {{year}}\n"
        '<BOOTSTRAP need="..." sources="..."/>\n'
        "```\n\n"
        "End of spec.\n",
        encoding="utf-8",
    )

    report = check_project(tmp_path)

    spec_results = [
        r for r in report.results
        if r.category == "placeholders" and "SPEC.md" in r.message
    ]
    assert spec_results == [], (
        f"Expected 0 placeholder signals for SPEC.md (they're inside a code-block), "
        f"found {len(spec_results)}: {[r.message for r in spec_results]}"
    )


def test_placeholders_skips_archive_and_philosophy(tmp_path: Path):
    """docs/archive/** and docs/PHILOSOPHY.md are not kaora-managed and must
    be excluded (they contain narrative text, false positives)."""
    _valid_project(tmp_path)
    archive = tmp_path / "docs" / "archive"
    archive.mkdir()
    (archive / "OLD.md").write_text(
        "Pre-install memory: {{project_name}}\n", encoding="utf-8"
    )
    (tmp_path / "docs" / "PHILOSOPHY.md").write_text(
        "Narrative example: {{project_name}} is a conceptual placeholder.\n",
        encoding="utf-8",
    )

    report = check_project(tmp_path)

    placeholder_warns = [r for r in report.warnings if r.category == "placeholders"]
    paths_with_warn = " ".join(r.message for r in placeholder_warns)
    assert "archive" not in paths_with_warn
    assert "PHILOSOPHY" not in paths_with_warn


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
# 6. SETTINGS — expected kaora hooks (2)
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


def test_settings_string_match_outside_hooks_struct_is_not_enough(tmp_path: Path):
    """Stringy match is too permissive: an arbitrary field can mention the
    hook name without the hook being actually configured. The check must
    walk hooks.<Event>[*].hooks[*].command, not run substring on the blob."""
    _valid_project(tmp_path)
    (tmp_path / ".claude" / "settings.json").write_text(
        json.dumps({
            "theme": "dark",
            "comment": "see protect-credentials.sh for details",
            "hooks": {},  # no real hook configured
        }),
        encoding="utf-8",
    )

    report = check_project(tmp_path)

    assert "info" in _levels(report, "settings"), (
        "permissive string-match is not enough: the check must verify the "
        "hooks.<Event>[*].hooks[*].command structure"
    )


# ---------------------------------------------------------------------------
# REPORT / FORMAT (3)
# ---------------------------------------------------------------------------

def test_report_exit_code_strict_promotes_warn(tmp_path: Path):
    _valid_project(tmp_path)
    # induce a warn (open structural placeholder)
    current = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    (tmp_path / "AGENTS.md").write_text(
        current + "\n\nName: {{project_name}}\n", encoding="utf-8"
    )

    report = check_project(tmp_path)

    assert report.exit_code(strict=False) == 0
    assert report.exit_code(strict=True) == 1


def test_report_format_text_contains_section_markers(tmp_path: Path):
    _valid_project(tmp_path)
    (tmp_path / "AGENTS.md").unlink()  # force an error

    report = check_project(tmp_path)
    text = format_text(report)

    # visual markers per level
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
