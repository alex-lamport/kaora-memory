# SESSION_HANDOFF.md — brief per la prossima sessione

> Leggi subito dopo `CLAUDE.md` e `CURRENT_STATE.md`.
>
> **Ultima sessione:** 2026-05-23 · Blocco 3 chiuso (kaora init implementato, 33/33 test green, wheel buildable, smoke OK end-to-end).

---

## 🟢 PROSSIMA SESSIONE — Blocco 4: `kaora check`

ADR 000-009 tutte `Accepted`. Blocco 3 chiuso, commit pending approvazione Alexis. Blocco 4 può partire dopo il commit (o anche prima se si vuole proseguire e committare in batch a fine sessione successiva).

---

## 🔵 PUNTI APERTI DA DECIDERE PRIMA DI PARTIRE

### 1. Self-dogfooding `kaora init .` (ADR-000)

ADR-000 promette dogfooding del repo dopo Blocco 3 chiuso. Ora è chiuso, quindi tecnicamente è il momento. **Ma:** il `CLAUDE.md` attuale del repo è ricco (~10 sezioni, master context kaora-memory stesso), mentre il template ha il 4-righe `@AGENTS.md`. Eseguire `kaora init .` produrrebbe:

- `CLAUDE.md.kaora-bak` con l'attuale denso
- `CLAUDE.md` nuovo (4 righe)
- `AGENTS.md.kaora-bak` con i 166 righe vecchi (se mai ricreato) o niente
- `AGENTS.md` nuovo (template canonico)

**Tre opzioni:**

| Opzione | Effetto |
|---|---|
| **A — Esegui `kaora init .` per davvero** | ADR-000 onorata letteralmente. Però perdiamo il `CLAUDE.md` ricco (resta in `.kaora-bak`). Significa adottare il template canonico anche per il repo che lo produce → coerenza massima ma sostituzione di un asset narrativo importante. |
| **B — `kaora init . --dry-run` per validare il piano, poi NON applicare** | Verifica end-to-end della logica sul repo stesso, senza mutare lo stato. ADR-000 onorata in spirito ma non in pratica. |
| **C — Trattare kaora-memory come caso speciale, scrivere ADR-010** | Documentare che il repo che produce kaora ha legittimamente un master context più ricco, e che il dogfooding pratico avviene tramite test e smoke su tmp_path. ADR-000 va aggiornata/superseded. |

**Raccomandazione:** B per ora (dry-run safe), poi decidere se C vale come ADR. A è troppo invasiva sul lavoro narrativo accumulato.

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
- ❌ `template/` salvo bug critici scoperti durante implementazione `check`
- ❌ Riaprire ADR `Accepted` (000-009)
- ❌ `bin/setup-dev.sh` salvo workaround UF_HIDDEN da migliorare

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

Se `kaora --version` fallisce con `ModuleNotFoundError`: `bash bin/setup-dev.sh` (rifa setup + chflags).

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
- **Self-dogfooding:** vedi punto 1 sopra. Probabilmente B (dry-run validation), C (nuova ADR) se vogliamo formalizzare l'eccezione del repo che produce kaora.
