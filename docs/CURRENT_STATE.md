# CURRENT_STATE.md — stato operativo

> Aggiornato a fine di ogni sessione. Risponde a "dove siamo, cosa funziona, cosa manca adesso".
>
> **Ultimo aggiornamento:** 2026-05-22 — Blocco 1 chiuso · scaffolding Python pubblicabile + memoria operativa dogfooding + dashboard premium anteprima.

---

## Snapshot oggi

**Blocco corrente:** Blocco 1 ✅ chiuso · Blocco 2 prossimo (da iniziare in nuova sessione)
**Commit ultimo:** `f45f4a3 chore: scaffolding iniziale kaora-memory v0.1`
**Branch:** `main`
**Repo remoto:** non ancora configurato (placeholder URL `alex-lamport/kaora-memory` in pyproject)

## Cosa esiste

```
kaora-memory/
├── .gitignore          (Python standard + macOS + IDE + venv)
├── BACKLOG.md          (idee v0.2+ già elencate)
├── LICENSE             (MIT, © 2026 alex.lamport)
├── README.md           (3 righe minime, da espandere in Blocco 5)
├── pyproject.toml      (hatchling, py>=3.10, entry point `kaora`)
├── kaora_memory/
│   └── __init__.py     (__version__ = "0.1.0")
├── CLAUDE.md           (master context — dogfooding di kaora-memory su se stesso)
└── docs/
    ├── CURRENT_STATE.md     (questo file)
    ├── SESSION_HANDOFF.md   (brief Blocco 2)
    └── DECISIONS.md         (ADR 000-004)
```

**Verifiche eseguite:**
- ✅ `pyproject.toml` valido (parse `tomllib` OK)
- ✅ `git init` + primo commit `f45f4a3`
- ✅ TOML expone name, version, entry point `kaora`

## Cosa manca (priorità ordinata)

1. **`template/` directory con i file generalizzati** — TUTTO Blocco 2
2. `kaora_memory/cli.py` — Blocco 3 (referenced da pyproject ma non esiste ancora, package non installabile finchÃ© manca)
3. `kaora_memory/check.py` — Blocco 4
4. README ricco con demo + screenshot — Blocco 5
5. Configurazione hatchling per includere `template/` come data file nel wheel — Blocco 3
6. Test minimali (`tests/test_init.py`, `tests/test_check.py`) — Blocco 3-4
7. Setup pubblicazione PyPI (`.pypirc`, token test.pypi) — Blocco 6

## Decisioni di design prese in sessione 22 maggio

Sintesi (dettaglio in `docs/DECISIONS.md`):

- **ADR-000** Dogfooding: kaora-memory usa se stessa. La memoria operativa di questo repo è generata applicando i propri pattern (questo file ne è la prova).
- **ADR-001** Rituale di apertura universale incondizionato + skip via riconoscimento intent naturale.
- **ADR-002** `kaora init` istantaneo (no wizard interattivo) + bootstrap agent-driven via `<BOOTSTRAP/>` markers.
- **ADR-003** Cross-agent garantito: `AGENTS.md` come gemello funzionale di `CLAUDE.md` per Codex/Cursor/Gemini CLI.
- **ADR-004** Layout package flat (`kaora_memory/` non `src/kaora_memory/`) + build backend hatchling.

## Asset di comunicazione collegati

- `/tmp/kaora-memory-preview.html` — dashboard premium anteprima (8 sezioni, double bezel, cyan glow, 3 mockup terminali su 3 CLI diversi). Generata 22/5 con skill `high-end-visual-design`. Asset showcase, NON parte del repo PyPI (per ora).
- `/tmp/kaora_builder_memory_architecture.md` — analisi tecnica memoria architetturale builder-side (11 sezioni). Asset di studio, NON parte del repo.

## Note operative

- **Repo NON ancora pushato** su GitHub. Username GitHub finale da decidere (placeholder `alex-lamport` in pyproject).
- **Test rapido salute:** `python3 -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))"`
- **Memoria persistente Claude Code:** non ancora popolata per questo progetto (file `~/.claude/projects/-Users-alexissilva-Desktop-kaora-memory/memory/` da generare alla prima sessione vera con `kaora init` self-applied dopo Blocco 3).
