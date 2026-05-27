"""Smoke test del CLI kaora (Click)."""
from __future__ import annotations

import json
from pathlib import Path

from click.testing import CliRunner

from kaora_memory.cli import main


def test_cli_version_flag():
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "kaora" in result.output.lower()


def test_cli_init_greenfield(tmp_path: Path):
    runner = CliRunner()
    target = tmp_path / "newproject"
    result = runner.invoke(main, ["init", str(target), "--no-git-init"])

    assert result.exit_code == 0, result.output
    assert (target / "CLAUDE.md").is_file()
    assert (target / "AGENTS.md").is_file()
    assert "kaora init completato" in result.output


def test_cli_init_dry_run_writes_nothing(tmp_path: Path):
    runner = CliRunner()
    target = tmp_path / "preview"
    result = runner.invoke(
        main, ["init", str(target), "--dry-run", "--no-git-init"]
    )

    assert result.exit_code == 0, result.output
    assert "DRY-RUN" in result.output
    # In dry-run la cartella non viene creata
    assert not target.exists() or list(target.rglob("*")) == []


def test_cli_init_default_to_cwd(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, ["init", "--no-git-init"])
    assert result.exit_code == 0, result.output
    assert (tmp_path / "CLAUDE.md").is_file()


# ---------------------------------------------------------------------------
# kaora check — Blocco 4
# ---------------------------------------------------------------------------

def test_cli_check_on_greenfield_post_init_exit_zero(tmp_path: Path):
    runner = CliRunner()
    target = tmp_path / "freshproject"
    init_result = runner.invoke(main, ["init", str(target), "--no-git-init"])
    assert init_result.exit_code == 0, init_result.output

    check_result = runner.invoke(main, ["check", str(target)])
    assert check_result.exit_code == 0, check_result.output


def test_cli_check_strict_promotes_warn_to_exit_one(tmp_path: Path):
    runner = CliRunner()
    target = tmp_path / "proj"
    runner.invoke(main, ["init", str(target), "--no-git-init"])
    # induciamo un WARN aprendo un placeholder strutturale in AGENTS.md
    agents = target / "AGENTS.md"
    agents.write_text(
        agents.read_text(encoding="utf-8") + "\n\nPath: {{project_path}}\n",
        encoding="utf-8",
    )

    soft = runner.invoke(main, ["check", str(target)])
    strict = runner.invoke(main, ["check", str(target), "--strict"])

    assert soft.exit_code == 0, soft.output
    assert strict.exit_code == 1, strict.output


def test_cli_check_json_flag_outputs_valid_json(tmp_path: Path):
    runner = CliRunner()
    target = tmp_path / "proj"
    runner.invoke(main, ["init", str(target), "--no-git-init"])

    result = runner.invoke(main, ["check", str(target), "--json"])
    assert result.exit_code == 0, result.output
    data = json.loads(result.output)
    assert "results" in data
    assert "exit_code" in data
