"""Tests for kaora_memory.template_resolver.

In the test environment (pip install -e .) the resolver must find the template
via the dev-mode fallback (top-level repo `template/`).
"""
from pathlib import Path

import pytest

from kaora_memory.template_resolver import (
    TemplateNotFoundError,
    get_template_root,
)


def test_get_template_root_returns_existing_dir_with_agents_md():
    root = get_template_root()
    assert root.is_dir()
    assert (root / "AGENTS.md").is_file()


def test_get_template_root_contains_expected_subtree():
    root = get_template_root()
    assert (root / "CLAUDE.md").is_file()
    assert (root / "docs").is_dir()
    assert (root / ".claude" / "settings.json").is_file()
    assert (root / ".claude" / "hooks" / "protect-credentials.sh").is_file()


def test_template_not_found_error_is_a_runtime_error():
    assert issubclass(TemplateNotFoundError, RuntimeError)
