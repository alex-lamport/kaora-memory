#!/bin/bash
# Setup dev environment per kaora-memory.
# Esegui dopo aver clonato il repo: `bash bin/setup-dev.sh`
#
# Workaround macOS UF_HIDDEN: hatchling editable install crea un file `.pth`
# che macOS marca con UF_HIDDEN (e ri-applica spontaneamente nel tempo).
# Python 3.13 skippa silenziosamente i .pth nascosti, rompendo `kaora`.
# Soluzione self-healing: sovrascriviamo `.venv/bin/kaora` (script Python
# generato da hatchling) con un wrapper bash che rimuove UF_HIDDEN ad
# ogni esecuzione prima di lanciare il CLI. Costo runtime: ~5ms.
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
    echo "→ macOS: installing self-healing wrapper at .venv/bin/kaora"
    chflags nohidden .venv/lib/python*/site-packages/*kaora*.pth 2>/dev/null || true
    cat > .venv/bin/kaora <<'WRAPPER_EOF'
#!/bin/bash
# Self-healing wrapper — rimuove UF_HIDDEN dal .pth prima di ogni run.
# Generato da bin/setup-dev.sh. Sovrascritto ad ogni `pip install -e .`,
# basta rieseguire `bash bin/setup-dev.sh` per ripristinarlo.
VENV_BIN="$(cd "$(dirname "$0")" && pwd)"
VENV_ROOT="$(dirname "$VENV_BIN")"
chflags nohidden "$VENV_ROOT"/lib/python*/site-packages/*kaora*.pth 2>/dev/null || true
exec "$VENV_BIN/python" -m kaora_memory.cli "$@"
WRAPPER_EOF
    chmod +x .venv/bin/kaora
fi

echo "→ Verifying installation"
.venv/bin/kaora --version
.venv/bin/python -m pytest -q

echo ""
echo "✓ Setup complete. Activate venv: source .venv/bin/activate"
echo "  Or use binaries directly: .venv/bin/kaora ... / .venv/bin/python -m pytest"
