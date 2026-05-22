# SESSION_HANDOFF.md — brief per la prossima sessione

> Leggi subito dopo `CLAUDE.md` e `CURRENT_STATE.md`.
>
> **Ultima sessione:** 2026-05-22 · Blocco 2 chiuso.

---

## 🟢 PROSSIMA SESSIONE — Blocco 3: `kaora init`

ADR 005-008 tutte `Accepted` in sessione 22 maggio (Blocco 2 finale). Blocco 3 può partire senza preliminari.

### Obiettivo

Implementare il comando `kaora init` che copia `template/` nel cwd (o path specificato), sostituendo placeholder strutturali e gestendo file pre-esistenti secondo ADR-006.

### File da creare

```
kaora_memory/
├── __init__.py            (già esiste, __version__ = "0.1.0")
├── cli.py                 ✨ NUOVO (Click app, comando `init`)
├── installer.py           ✨ NUOVO (logica copy + placeholder + backup per markdown/script)
├── settings_merger.py     ✨ NUOVO (merge JSON intelligente per .claude/settings.json, ADR-006 v2)
└── _template/             ✨ NUOVO (data files dal template/, gestiti da hatch)
tests/
├── __init__.py            ✨ NUOVO
├── test_init.py           ✨ NUOVO (greenfield, brownfield, dry-run, force)
└── test_settings_merger.py ✨ NUOVO (4+ casi: solo permissions, hooks esistenti, matcher conflict, JSON malformato)
```

### Modifiche a file esistenti

- **`pyproject.toml`**: aggiungere sezione data files
  ```toml
  [tool.hatch.build.targets.wheel.force-include]
  "template" = "kaora_memory/_template"
  ```
  Verifica con `python -m build` che `template/*` finisca in `kaora_memory/_template/` nel wheel.

### Comando `kaora init` — comportamento atteso

```
$ kaora init [PATH] [--force] [--dry-run]

Default PATH = directory corrente.

1. Verifica che PATH sia una directory (creala se non esiste)
2. Per ogni file in template/, applica policy ADR-006 v2:
   - **Markdown** (CLAUDE.md, AGENTS.md): backup → NOME.kaora-bak prima di scrivere il nuovo
   - **JSON** (.claude/settings.json): merge intelligente via `settings_merger.merge_claude_settings()` — preserva permissions + chiavi non-hooks, append degli hooks kaora per matcher, backup `.kaora-bak`
   - **Skip-conservative** (docs/* esistenti, README, BACKLOG): lascia stare + log
   - **Hook scripts** (.claude/hooks/*.sh): skip se file esiste, scrivi solo i mancanti
   - File mancante in tutte le categorie → scrivi sempre
3. Sostituisci placeholder strutturali inferibili automaticamente:
   - {{project_name}} ← basename(PATH)
   - {{project_path}} ← absolute(PATH)
   - {{year}} ← anno corrente
4. Lascia tutti gli altri placeholder ({{owner_name}}, {{owner_email}}, ...) intatti
   per il BOOTSTRAP della prima sessione AI
5. Esegui `git init` se PATH non è dentro un repo git
6. Stampa report finale: creati / backup / skippati + prossimo step
```

### Skill obbligatorie PRIMA di costruire (Gate A § 5.1)

- **`python-packaging`** — per la modifica `pyproject.toml` con `force-include` e per verifica wheel
- **`python-pro`** — per il CLI Click con sotto-comandi futuri (init ora, check/handoff/errors poi)
- **`tdd-workflows-tdd-cycle`** — opzionale, ma test brownfield/greenfield sono il cuore: red-green-refactor consigliato

### `template/` vs `kaora_memory/_template/` — strategia

Durante sviluppo, mantenere **una sola fonte**: `template/` (al top-level del repo). Hatch lo include nel wheel con `force-include`, mappandolo a `kaora_memory/_template/`. Cli legge da `importlib.resources.files("kaora_memory") / "_template"`.

In dev mode (`pip install -e .`), `_template` può non esistere fisicamente. Strategia: `importlib.resources` con fallback a path relativo dal codice (`Path(__file__).parent.parent / "template"`). Da decidere in implementazione.

### Cosa NON toccare (Blocco 1+2 chiusi)

- ❌ `LICENSE`, `.gitignore`, `README.md` minimale (polish in Blocco 5)
- ❌ `kaora_memory/__init__.py` versione corretta
- ❌ `CLAUDE.md`, `docs/*` del repo (memoria operativa di kaora-memory stesso, NON template)
- ❌ `template/` salvo bug critici scoperti durante implementazione `init`
- ❌ Riaprire ADR `Accepted` (000-004)
- ❌ Modificare ADR-005/006 dopo che Alexis le marca Accepted

### Check di apertura sessione

```bash
cd ~/Desktop/kaora-memory
python3 -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))" && echo "TOML OK"
ls template/ template/docs template/.claude/hooks
git log --oneline -5
grep -c "Proposed" docs/DECISIONS.md   # deve essere 0 dopo l'accept
```

### Output atteso a fine Blocco 3

1. `kaora init` funzionante su:
   - Cartella vuota (greenfield)
   - Cartella con `CLAUDE.md` esistente (brownfield → backup `.kaora-bak`)
   - Cartella con `docs/DECISIONS.md` esistente (skip, mai distruggere ADR)
2. `pyproject.toml` aggiornato con `force-include`, wheel buildabile via `python -m build`
3. Test green: `pytest tests/test_init.py`
4. Self-dogfooding: `kaora init .` nel repo stesso → genera `.kaora-bak` per CLAUDE.md/docs (ADR-000 finalmente concretizzato)
5. Commit: `feat(cli): kaora init con policy brownfield`
6. `CURRENT_STATE.md` e `SESSION_HANDOFF.md` aggiornati con brief Blocco 4

### Cosa NON aprire in questa sessione

- ❌ Blocco 4 (`kaora check`) — solo dopo `init` validato
- ❌ Pubblicazione PyPI — Blocco 6
- ❌ Push su GitHub — username finale ancora da decidere

---

## Note operative per la prossima sessione

- **Apri Claude Code in `~/Desktop/kaora-memory/`**
- **Registro:** italiano · diretto · no preamboli · una decisione alla volta
- **Decisioni grandi** → nuova ADR in `docs/DECISIONS.md`
- **Self-dogfooding:** alla fine di Blocco 3, eseguire `kaora init .` sul repo stesso è il momento più importante del progetto (ADR-000)
