"""Tests for kaora_memory.installer.install_template (ADR-006 v2).

File categories handled:
- **canonical** (CLAUDE.md, AGENTS.md, AGENT_BRIEF.md): backup .kaora-bak + overwrite,
  with placeholder substitution
- **json-merge** (.claude/settings.json): merge via settings_merger, backup .kaora-bak
- **skip-if-exists** (everything else: docs/*, BACKLOG.md, README.md, hook scripts):
  write only if missing
- **rename**: README.md.tpl → README.md

Flags:
- dry_run=True → compute report but write nothing
- force=True → overwrite everything without backup, skip JSON merge
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from kaora_memory.installer import install_template, InstallReport


YEAR = 2026


# ---------------------------------------------------------------------------
# Greenfield — empty folder
# ---------------------------------------------------------------------------

def test_greenfield_creates_canonical_markdown(tmp_path: Path):
    install_template(tmp_path, year=YEAR)
    assert (tmp_path / "CLAUDE.md").is_file()
    assert (tmp_path / "AGENTS.md").is_file()
    assert (tmp_path / "AGENT_BRIEF.md").is_file()


def test_greenfield_creates_docs_subtree(tmp_path: Path):
    install_template(tmp_path, year=YEAR)
    assert (tmp_path / "docs" / "IDENTITY.md").is_file()
    assert (tmp_path / "docs" / "CURRENT_STATE.md").is_file()
    assert (tmp_path / "docs" / "SESSION_HANDOFF.md").is_file()
    assert (tmp_path / "docs" / "DECISIONS.md").is_file()


def test_greenfield_creates_claude_settings_and_hooks(tmp_path: Path):
    install_template(tmp_path, year=YEAR)
    assert (tmp_path / ".claude" / "settings.json").is_file()
    assert (tmp_path / ".claude" / "hooks" / "protect-credentials.sh").is_file()
    assert (tmp_path / ".claude" / "hooks" / "log-api-calls.sh").is_file()


def test_greenfield_renames_readme_tpl_to_readme(tmp_path: Path):
    install_template(tmp_path, year=YEAR)
    assert (tmp_path / "README.md").is_file()
    assert not (tmp_path / "README.md.tpl").exists()


def test_greenfield_creates_backlog(tmp_path: Path):
    install_template(tmp_path, year=YEAR)
    assert (tmp_path / "BACKLOG.md").is_file()


# ---------------------------------------------------------------------------
# Placeholder substitution
# ---------------------------------------------------------------------------

def test_structural_placeholders_substituted_in_canonical(tmp_path: Path):
    target = tmp_path / "myproject"
    target.mkdir()
    install_template(target, year=YEAR)

    agents = (target / "AGENTS.md").read_text(encoding="utf-8")
    assert "{{project_name}}" not in agents
    assert "{{project_path}}" not in agents
    assert "{{year}}" not in agents
    assert "myproject" in agents
    assert str(target.resolve()) in agents
    assert "2026" in agents


def test_bootstrap_placeholders_left_untouched(tmp_path: Path):
    install_template(tmp_path, year=YEAR)
    agents = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    # At least one user placeholder must remain intact for BOOTSTRAP
    bootstrap_placeholders = (
        "{{owner_name}}",
        "{{owner_email}}",
        "{{project_oneliner}}",
        "{{communication_register}}",
        "{{communication_language}}",
    )
    assert any(p in agents for p in bootstrap_placeholders), (
        f"Expected at least one BOOTSTRAP placeholder in AGENTS.md, "
        f"found 0 of {bootstrap_placeholders}"
    )


# ---------------------------------------------------------------------------
# Brownfield — canonical backup
# ---------------------------------------------------------------------------

def test_brownfield_claude_md_backed_up_and_rewritten(tmp_path: Path):
    existing = tmp_path / "CLAUDE.md"
    existing.write_text("MY OLD CLAUDE", encoding="utf-8")

    report = install_template(tmp_path, year=YEAR)

    bak = tmp_path / "CLAUDE.md.kaora-bak"
    assert bak.is_file()
    assert bak.read_text(encoding="utf-8") == "MY OLD CLAUDE"
    new = (tmp_path / "CLAUDE.md").read_text(encoding="utf-8")
    assert new != "MY OLD CLAUDE"
    assert any(p.name == "CLAUDE.md" for p in report.backed_up)


def test_brownfield_agents_md_backed_up_and_rewritten(tmp_path: Path):
    existing = tmp_path / "AGENTS.md"
    existing.write_text("MY OLD AGENTS", encoding="utf-8")

    install_template(tmp_path, year=YEAR)

    bak = tmp_path / "AGENTS.md.kaora-bak"
    assert bak.is_file()
    assert bak.read_text(encoding="utf-8") == "MY OLD AGENTS"
    new = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    assert new != "MY OLD AGENTS"


# ---------------------------------------------------------------------------
# Brownfield — skip-if-exists
# ---------------------------------------------------------------------------

def test_brownfield_docs_decisions_md_skipped(tmp_path: Path):
    (tmp_path / "docs").mkdir()
    existing = tmp_path / "docs" / "DECISIONS.md"
    existing.write_text("# My existing ADR log", encoding="utf-8")

    report = install_template(tmp_path, year=YEAR)

    assert existing.read_text(encoding="utf-8") == "# My existing ADR log"
    assert not (tmp_path / "docs" / "DECISIONS.md.kaora-bak").exists()
    assert any(p.name == "DECISIONS.md" for p in report.skipped)


def test_brownfield_readme_md_skipped(tmp_path: Path):
    existing = tmp_path / "README.md"
    existing.write_text("# My project", encoding="utf-8")

    install_template(tmp_path, year=YEAR)

    assert existing.read_text(encoding="utf-8") == "# My project"
    assert not (tmp_path / "README.md.kaora-bak").exists()


def test_brownfield_hook_script_skipped(tmp_path: Path):
    hooks = tmp_path / ".claude" / "hooks"
    hooks.mkdir(parents=True)
    user_hook = hooks / "protect-credentials.sh"
    user_hook.write_text("#!/bin/sh\necho user-custom", encoding="utf-8")

    install_template(tmp_path, year=YEAR)

    assert user_hook.read_text(encoding="utf-8") == "#!/bin/sh\necho user-custom"
    # the other hook (log-api-calls.sh) doesn't exist → must be written
    assert (hooks / "log-api-calls.sh").is_file()


# ---------------------------------------------------------------------------
# Brownfield — JSON merge
# ---------------------------------------------------------------------------

def test_brownfield_claude_settings_merged(tmp_path: Path):
    claude = tmp_path / ".claude"
    claude.mkdir()
    settings = claude / "settings.json"
    settings.write_text(
        json.dumps(
            {"permissions": {"allow": ["Bash(ls:*)"], "deny": []}, "theme": "dark"}
        ),
        encoding="utf-8",
    )

    report = install_template(tmp_path, year=YEAR)

    data = json.loads(settings.read_text(encoding="utf-8"))
    allow = data["permissions"]["allow"]
    assert "Bash(ls:*)" in allow, "user permission must be preserved"
    assert data.get("theme") == "dark", "non-hooks keys must be preserved"
    assert "hooks" in data, "kaora hooks must be added by the merge"

    bak = claude / "settings.json.kaora-bak"
    assert bak.is_file()
    assert any(p.name == "settings.json" for p in report.merged)


# ---------------------------------------------------------------------------
# Flags dry-run and force
# ---------------------------------------------------------------------------

def test_dry_run_writes_nothing(tmp_path: Path):
    report = install_template(tmp_path, dry_run=True, year=YEAR)

    written = list(tmp_path.rglob("*"))
    assert written == [], f"dry-run must write nothing, found: {written}"
    # report populated even in dry-run (shows what would have been done)
    assert len(report.created) > 0


def test_force_overwrites_without_backup(tmp_path: Path):
    existing = tmp_path / "CLAUDE.md"
    existing.write_text("OLD CLAUDE", encoding="utf-8")

    install_template(tmp_path, force=True, year=YEAR)

    assert (tmp_path / "CLAUDE.md").read_text(encoding="utf-8") != "OLD CLAUDE"
    assert not (tmp_path / "CLAUDE.md.kaora-bak").exists()


def test_force_overwrites_settings_json_without_merge(tmp_path: Path):
    claude = tmp_path / ".claude"
    claude.mkdir()
    settings = claude / "settings.json"
    settings.write_text(
        json.dumps({"permissions": {"allow": ["Bash(ls:*)"], "deny": []}}),
        encoding="utf-8",
    )

    install_template(tmp_path, force=True, year=YEAR)

    data = json.loads(settings.read_text(encoding="utf-8"))
    # in force mode the merger is bypassed → user permissions lost
    assert "Bash(ls:*)" not in data.get("permissions", {}).get("allow", [])
    assert not (claude / "settings.json.kaora-bak").exists()


# ---------------------------------------------------------------------------
# InstallReport structure
# ---------------------------------------------------------------------------

def test_report_has_all_categories(tmp_path: Path):
    report = install_template(tmp_path, year=YEAR)
    assert isinstance(report, InstallReport)
    assert isinstance(report.created, list)
    assert isinstance(report.backed_up, list)
    assert isinstance(report.merged, list)
    assert isinstance(report.skipped, list)
    # greenfield: everything in created, nothing in the other lists
    assert len(report.created) > 0
    assert report.backed_up == []
    assert report.merged == []


def test_target_created_if_missing(tmp_path: Path):
    target = tmp_path / "nonexistent_dir"
    assert not target.exists()
    install_template(target, year=YEAR)
    assert target.is_dir()
    assert (target / "CLAUDE.md").is_file()
