"""Kaora-memory CLI entry point.

Comando esposto come `kaora` (vedi pyproject.toml [project.scripts]).
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
    """kaora — memoria persistente e comportamento codificato per agenti AI."""


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
    help="Sovrascrivi tutto senza backup, salta merge JSON. Per CI/automazione consapevole.",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Mostra il piano completo senza toccare alcun file.",
)
@click.option(
    "--no-git-init",
    is_flag=True,
    help="Non eseguire `git init` se il target non è dentro un repo git.",
)
def init(path: Path, force: bool, dry_run: bool, no_git_init: bool) -> None:
    """Installa il template kaora-memory in PATH (default: directory corrente)."""
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
@click.option("--strict", is_flag=True, help="Promuovi WARN a exit code 1.")
@click.option("--quiet", is_flag=True, help="Mostra solo ERROR.")
@click.option(
    "--json", "json_output", is_flag=True, help="Output JSON machine-readable."
)
@click.pass_context
def check(
    ctx: click.Context, path: Path, strict: bool, quiet: bool, json_output: bool
) -> None:
    """Verifica integrità memoria operativa kaora in PATH (default: cwd)."""
    target = path.resolve()
    report = check_project(target)

    if json_output:
        click.echo(format_json(report))
    else:
        click.echo(format_text(report, quiet=quiet))

    ctx.exit(report.exit_code(strict=strict))


def _maybe_git_init(target: Path) -> None:
    """Esegue `git init` in target se non è già dentro un repo git."""
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
        # git non installato: silenzioso, non è un errore bloccante
        pass


def _print_report(target: Path, report: InstallReport, *, dry_run: bool) -> None:
    if dry_run:
        click.secho(f"\n[DRY-RUN] Piano per: {target}", fg="cyan", bold=True)
    else:
        click.secho(f"\nkaora init completato in: {target}", fg="green", bold=True)

    _section("creati", report.created, "green")
    _section("backup + sovrascritti (.kaora-bak)", report.backed_up, "yellow")
    _section("settings.json mergiati (.kaora-bak)", report.merged, "yellow")
    _section("skippati (preservati esistenti)", report.skipped, "blue")

    click.echo("")
    click.secho("Prossimo passo: ", nl=False, bold=True)
    click.echo(
        "apri il progetto in un agente AI (Claude Code / Codex / Cursor) "
        "e lascia che esegua il rituale di apertura (legge AGENTS.md)."
    )


def _section(title: str, items: list[Path], color: str) -> None:
    if not items:
        return
    click.secho(f"\n  {title} ({len(items)}):", fg=color, bold=True)
    for p in items:
        click.echo(f"    • {p.as_posix()}")


if __name__ == "__main__":
    main()
