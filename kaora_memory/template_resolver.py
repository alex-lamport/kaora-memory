"""Resolve the path to the kaora-memory template.

Two modes (Block 3 architectural decision, consistent with ADR-005):

1. **Wheel installed from PyPI:** the `kaora_memory/_template/` folder exists
   physically (hatch force-include in pyproject.toml). Read via
   `importlib.resources.files("kaora_memory") / "_template"`.

2. **Dev mode (`pip install -e .`):** the `_template/` folder does NOT exist
   inside `kaora_memory/`. Fallback to the top-level repo `template/`
   (`Path(__file__).parent.parent / "template"`).

The caller (`installer.py`) calls `get_template_root()` and gets a `Path`
to a folder that contains `AGENTS.md`, `CLAUDE.md`, `docs/`, `.claude/`.
"""
from __future__ import annotations

from importlib.resources import files
from pathlib import Path


__all__ = ["get_template_root", "TemplateNotFoundError"]


# Marker file used to validate that a candidate is a valid kaora template.
# If it exists, this is (almost certainly) the right template.
_TEMPLATE_MARKER = "AGENTS.md"


class TemplateNotFoundError(RuntimeError):
    """Raised if none of the lookup strategies finds a valid template."""


def get_template_root() -> Path:
    """Return the `Path` to the root of the kaora-memory template.

    Strategy:
    1. Try `importlib.resources.files("kaora_memory") / "_template"`
       (works if the wheel force-included the folder).
    2. Fallback to `Path(__file__).parent.parent / "template"`
       (works in dev mode editable install).

    Raises `TemplateNotFoundError` if neither works.
    """
    wheel_candidate = _try_wheel_template()
    if wheel_candidate is not None:
        return wheel_candidate

    dev_candidate = _try_dev_template()
    if dev_candidate is not None:
        return dev_candidate

    raise TemplateNotFoundError(
        "kaora-memory template not found. "
        "Searched in kaora_memory/_template/ (wheel) and in template/ (top-level dev mode). "
        "Reinstall with `pip install -e .` or `pip install kaora-memory`."
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
