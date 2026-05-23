#!/bin/bash
# Setup dev environment per kaora-memory.
# Esegui dopo aver clonato il repo: `bash bin/setup-dev.sh`
#
# Workaround incluso: rimuove il flag macOS UF_HIDDEN dai file .pth generati
# da hatchling in editable install. Senza, Python 3.13 skippa il .pth
# ("Skipping hidden .pth file") e `kaora` fallisce con ModuleNotFoundError.
# Vedi BACKLOG "Issue noti".
set -e

cd "$(dirname "$0")/.."

if [ ! -d ".venv" ]; then
    echo "→ Creating .venv/"
    python3 -m venv .venv
fi

echo "→ Installing kaora-memory editable + dev deps"
.venv/bin/pip install --upgrade pip --quiet
.venv/bin/pip install -e ".[dev]" --quiet

if [ "$(uname)" = "Darwin" ]; then
    echo "→ macOS: removing UF_HIDDEN flag from .pth files"
    chflags nohidden .venv/lib/python*/site-packages/*kaora*.pth 2>/dev/null || true
fi

echo "→ Verifying installation"
.venv/bin/kaora --version
.venv/bin/python -m pytest -q

echo ""
echo "✓ Setup complete. Activate venv: source .venv/bin/activate"
echo "  Or use binaries directly: .venv/bin/kaora ... / .venv/bin/python -m pytest"
