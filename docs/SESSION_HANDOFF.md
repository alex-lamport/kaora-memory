# SESSION_HANDOFF.md — brief per la prossima sessione

> Leggi subito dopo `CLAUDE.md` e `CURRENT_STATE.md`.
>
> **Ultima sessione:** 2026-05-26 · Self-dogfooding ADR-000 APPLICATO + committato (`a9518d6`). Merge AGENTS.md guidato da agente naive in seconda sessione (con revisore in parallelo), `CLAUDE.md.kaora-bak` archiviato in `docs/archive/`. Bug UF_HIDDEN RISOLTO (2026-05-24). Working tree pulito. Drift docs allineato 2026-05-27 in apertura sessione Blocco 4.

---

## 🟢 PROSSIMA SESSIONE — Blocco 4: `kaora check`

ADR 000-009 tutte `Accepted`. Blocco 3 chiuso. Self-dogfooding ADR-000 applicato e committato (`a9518d6`). Template § 11 step 5 già aggiornato con terza opzione "archive" (template/AGENTS.md:194). Pronto per Blocco 4 senza punti aperti bloccanti.

---

## 🔵 PUNTI APERTI DA DECIDERE PRIMA DI PARTIRE

### 1. Rituale di chiusura sessione — IMPLEMENTATO 2026-05-26 (era v0.2+, promosso a v0.1)

Scoperta operativa dal dogfooding: senza rituale di chiusura simmetrico, i docs operativi divergono dallo stato reale. § 6bis aggiunta a `template/AGENTS.md` + `AGENTS.md` del repo. Comportamento: sintesi sessione → diff CURRENT_STATE → diff SESSION_HANDOFF → proposta commit, ognuno con Gate C. Vedi `docs/DOGFOODING_REPORT.md` § 4 per il contesto.

`kaora handoff` CLI per automazione completa resta in v0.2+.

### 2. Naming repo prima di PyPI (BACKLOG, Blocco 6)

Non bloccante per Blocco 4, ma se vogliamo evitare di pubblicare con nome "sbagliato", decidere entro Blocco 5.

---

### Obiettivo Blocco 4

Implementare `kaora check`: **linter per memoria operativa kaora installata**. Diagnostica integrità di un progetto post-`kaora init`. Pensato per:
- Sviluppatori che vogliono validare il loro setup
- Agenti AI che possono chiamarlo nel rituale di apertura per dare un report
- CI in progetti che usano kaora

### Comportamento atteso

```
$ kaora check [PATH]

Default PATH = directory corrente.

CHECKS (in ordine):
1. Struttura minima:
   - AGENTS.md presente (required)
   - CLAUDE.md presente (required)
   - docs/ presente con almeno DECISIONS.md + IDENTITY.md
   - .claude/settings.json valido come JSON
2. Coerenza ADR-005 (canonico + import):
   - CLAUDE.md contiene direttiva `@AGENTS.md` (warn altrimenti)
   - AGENTS.md ha contenuto ricco (>= N righe, soglia da definire)
3. Stato ADR:
   - docs/DECISIONS.md ha almeno una ADR `Accepted` (info se zero)
   - ADR in stato `Proposed` segnalate (info, non error)
4. Placeholder:
   - {{project_name}}, {{project_path}}, {{year}} sostituiti (warn se ancora aperti)
   - BOOTSTRAP markers ancora aperti (info, normale post-init)
5. Hook eseguibili:
   - .claude/hooks/*.sh hanno chmod +x (warn altrimenti)
6. Settings:
   - .claude/settings.json contiene hook kaora attesi (info se non match)

OUTPUT:
- Sezioni colorate: ❌ ERROR / ⚠️ WARN / ℹ️ INFO / ✅ OK
- Exit code: 0 se OK o solo warn/info, 1 se errors

FLAG:
- --strict: warn diventano error (exit 1 anche su warn)
- --quiet: mostra solo errors
- --json: output machine-readable
```

### File da creare

```
kaora_memory/
└── check.py                ✨ NUOVO — funzione check_project(target) -> CheckReport, plus CLI integration

tests/
└── test_check.py           ✨ NUOVO — coverage per ogni check definito sopra
```

### Modifiche a file esistenti

- **`kaora_memory/cli.py`**: aggiungere `@main.command()` `check` (specchio di `init`)
- **`docs/DECISIONS.md`**: eventuale ADR-010 (delegation depth: `/goal` vs delega normale kaora) o ADR su strategia `_template/`. Solo se decidi di formalizzare.

### Skill obbligatorie PRIMA di costruire (Gate A § 5.1)

- **`tdd-workflows-tdd-cycle`** — pattern test-first applicato in Blocco 3, funziona bene per check.py (specifica come tests)
- **`python-pro`** se serve refactor cli.py per sub-comandi multipli (non strettamente necessario, Click lo gestisce out-of-box)

### Cosa NON toccare (Blocco 1+2+3 chiusi)

- ❌ `LICENSE`, `.gitignore` finalizzati
- ❌ `kaora_memory/{__init__, settings_merger, template_resolver, installer}.py` — moduli stabili Blocco 3
- ❌ `template/` salvo: (a) bug critici scoperti durante implementazione `check`, (b) aggiornamento § 11 step 5 con terza opzione "archive" (item v0.1 in BACKLOG)
- ❌ Riaprire ADR `Accepted` (000-009)
- ❌ `bin/setup-dev.sh` — wrapper self-healing UF_HIDDEN già applicato 2026-05-24, non rivederlo

### Check di apertura sessione

```bash
cd ~/Desktop/kaora-memory
python3 -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))" && echo "TOML OK"
ls template/ template/docs template/.claude/hooks
git log --oneline -5
grep -c "Proposed" docs/DECISIONS.md   # deve essere 0
.venv/bin/python -m pytest -q && echo "TEST OK (33/33)"
.venv/bin/kaora --version && echo "CLI OK"
```

Se `kaora --version` fallisce con `ModuleNotFoundError`: `bash bin/setup-dev.sh` (reinstalla wrapper self-healing su `.venv/bin/kaora`). Capita se hai rifatto `pip install -e .` manualmente bypassando lo script.

### Output atteso a fine Blocco 4

1. `kaora check` funzionante su:
   - Progetto greenfield appena fatto `kaora init` → tutti i check OK
   - Progetto con CLAUDE.md mancante → ERROR
   - Progetto con BOOTSTRAP marker ancora aperti → INFO non bloccante
   - Progetto con placeholder strutturali ancora aperti → WARN
2. Test green: `pytest tests/test_check.py` + suite totale invariata
3. Commit: `feat(cli): kaora check linter integrità memoria operativa`
4. `CURRENT_STATE.md` e `SESSION_HANDOFF.md` aggiornati con brief Blocco 5

### Cosa NON aprire in questa sessione

- ❌ Blocco 5 (README ricco + asset di lancio) — solo dopo check validato
- ❌ Pubblicazione PyPI — Blocco 6
- ❌ Push su GitHub — username finale ancora da decidere (vedi BACKLOG naming repo)

---

## Note operative per la prossima sessione

- **Apri Claude Code in `~/Desktop/kaora-memory/`**
- **Registro:** italiano · diretto · no preamboli · una decisione alla volta · modalità Operativa vs Apprendimento (ADR-007)
- **Decisioni grandi** → nuova ADR in `docs/DECISIONS.md` (ADR-008 step 6 del rituale)
- **Self-dogfooding:** APPLICATO 2026-05-26 con opzione A (esecuzione reale). Commit pending nel working tree.
