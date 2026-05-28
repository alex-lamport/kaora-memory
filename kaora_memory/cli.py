"""kaora-memory CLI entry point.

Command exposed as `kaora` (see pyproject.toml [project.scripts]).
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import click

from kaora_memory import __version__
from kaora_memory.check import check_project, format_json, format_text
from kaora_memory.installer import InstallReport, install_template


@click.group()
@click.version_option(__version__, prog_name="kaora")
def main() -> None:
    """kaora — persistent memory and codified behavior for AI agents."""


@main.command()
@click.argument(
    "path",
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    default=".",
    required=False,
)
@click.option(
    "--force",
    is_flag=True,
    help="Overwrite everything without backup, skip JSON merge. For intentional CI/automation use.",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show the full plan without touching any file.",
)
@click.option(
    "--no-git-init",
    is_flag=True,
    help="Do not run `git init` if the target is not inside a git repo.",
)
def init(path: Path, force: bool, dry_run: bool, no_git_init: bool) -> None:
    """Install the kaora-memory template into PATH (default: current directory)."""
    target = path.resolve()
    report = install_template(target, force=force, dry_run=dry_run)

    if not dry_run and not no_git_init:
        _maybe_git_init(target)

    _print_report(target, report, dry_run=dry_run)


@main.command()
@click.argument(
    "path",
    type=click.Path(file_okay=False, dir_okay=True, exists=False, path_type=Path),
    default=".",
    required=False,
)
@click.option("--strict", is_flag=True, help="Promote WARN to exit code 1.")
@click.option("--quiet", is_flag=True, help="Show only ERROR.")
@click.option(
    "--json", "json_output", is_flag=True, help="Machine-readable JSON output."
)
@click.pass_context
def check(
    ctx: click.Context, path: Path, strict: bool, quiet: bool, json_output: bool
) -> None:
    """Check kaora operating-memory integrity in PATH (default: cwd)."""
    target = path.resolve()
    report = check_project(target)

    if json_output:
        click.echo(format_json(report))
    else:
        click.echo(format_text(report, quiet=quiet))

    ctx.exit(report.exit_code(strict=strict))


def _maybe_git_init(target: Path) -> None:
    """Run `git init` in target if it's not already inside a git repo."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=target,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip() == "true":
            return
        subprocess.run(
            ["git", "init", "--quiet"], cwd=target, check=False, capture_output=True
        )
    except FileNotFoundError:
        # git not installed: silent, not a blocking error
        pass


def _print_report(target: Path, report: InstallReport, *, dry_run: bool) -> None:
    if dry_run:
        click.secho(f"\n[DRY-RUN] Plan for: {target}", fg="cyan", bold=True)
    else:
        click.secho(f"\nkaora init complete in: {target}", fg="green", bold=True)

    _section("created", report.created, "green")
    _section("backed up + overwritten (.kaora-bak)", report.backed_up, "yellow")
    _section("settings.json merged (.kaora-bak)", report.merged, "yellow")
    _section("skipped (preserved existing)", report.skipped, "blue")
    _section_warnings(report.warnings)

    click.echo("")
    click.secho("Next step: ", nl=False, bold=True)
    click.echo(
        "open the project in an AI agent (Claude Code / Codex / Cursor) "
        "and let it run the opening ritual (it reads AGENTS.md)."
    )


def _section(title: str, items: list[Path], color: str) -> None:
    if not items:
        return
    click.secho(f"\n  {title} ({len(items)}):", fg=color, bold=True)
    for p in items:
        click.echo(f"    • {p.as_posix()}")


def _section_warnings(items: list[tuple[Path, str]]) -> None:
    if not items:
        return
    click.secho(f"\n  warnings ({len(items)}):", fg="red", bold=True)
    for path, msg in items:
        click.echo(f"    • {path.as_posix()}: {msg}")


if __name__ == "__main__":
    main()
