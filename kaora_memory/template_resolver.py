"""Risolve il path al template kaora-memory.

Due modalità (decisione architetturale Blocco 3, ADR-005 coerente):

1. **Wheel installato da PyPI:** la cartella `kaora_memory/_template/` esiste
   fisicamente (force-include di hatch in pyproject.toml). Lettura via
   `importlib.resources.files("kaora_memory") / "_template"`.

2. **Dev mode (`pip install -e .`):** la cartella `_template/` NON esiste
   dentro `kaora_memory/`. Fallback al `template/` top-level del repo
   (`Path(__file__).parent.parent / "template"`).

Il caller (`installer.py`) chiama `get_template_root()` e ottiene un `Path`
verso una cartella che contiene `AGENTS.md`, `CLAUDE.md`, `docs/`, `.claude/`.
"""
from __future__ import annotations

from importlib.resources import files
from pathlib import Path


__all__ = ["get_template_root", "TemplateNotFoundError"]


# Marker file che usiamo per validare che una candidate sia un template kaora valido.
# Se esiste, è (quasi certamente) il template giusto.
_TEMPLATE_MARKER = "AGENTS.md"


class TemplateNotFoundError(RuntimeError):
    """Sollevata se nessuna delle strategie di lookup trova un template valido."""


def get_template_root() -> Path:
    """Ritorna il `Path` della radice del template kaora-memory.

    Strategia:
    1. Prova `importlib.resources.files("kaora_memory") / "_template"`
       (funziona se il wheel ha incluso force-include la cartella).
    2. Fallback a `Path(__file__).parent.parent / "template"`
       (funziona in dev mode editable install).

    Solleva `TemplateNotFoundError` se nessuna funziona.
    """
    wheel_candidate = _try_wheel_template()
    if wheel_candidate is not None:
        return wheel_candidate

    dev_candidate = _try_dev_template()
    if dev_candidate is not None:
        return dev_candidate

    raise TemplateNotFoundError(
        "Template kaora-memory non trovato. "
        "Cercato in kaora_memory/_template/ (wheel) e in template/ (dev mode top-level). "
        "Reinstalla con `pip install -e .` o `pip install kaora-memory`."
    )


def _try_wheel_template() -> Path | None:
    try:
        root = files("kaora_memory").joinpath("_template")
    except (ModuleNotFoundError, FileNotFoundError):
        return None

    path = Path(str(root))
    if path.is_dir() and (path / _TEMPLATE_MARKER).is_file():
        return path
    return None


def _try_dev_template() -> Path | None:
    here = Path(__file__).resolve().parent  # .../kaora_memory/
    candidate = here.parent / "template"     # .../template/
    if candidate.is_dir() and (candidate / _TEMPLATE_MARKER).is_file():
        return candidate
    return None
