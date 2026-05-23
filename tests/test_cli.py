"""Smoke test del CLI kaora (Click)."""
from __future__ import annotations

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
