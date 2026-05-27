# SESSION_HANDOFF.md — brief per la prossima sessione

> Leggi subito dopo `CLAUDE.md` e `CURRENT_STATE.md`.
>
> **Ultima sessione:** 2026-05-27 · **Blocco 4 chiuso** — `kaora check` linter integrità memoria operativa implementato TDD red→green→refactor. Sei categorie (structure, adr005, adr_state, placeholders, hooks, settings). 4 commit nuovi (`eabae39` drift docs · `29fa094` green · `a9e542a` 3 fix mirati · `607b5a9` fix4 `_strip_code_blocks` in placeholders). Suite 62/62 verdi. Working tree pulito, no push.

---

## 🟢 PROSSIMA SESSIONE — Blocco 5: README ricco + asset di lancio

ADR 000-009 tutte `Accepted`. Blocchi 1-4 chiusi. `kaora init` + `kaora check` entrambi funzionanti, dogfooding validato sul repo stesso. Pronto per Blocco 5 senza punti aperti bloccanti.

---

## 🔵 PUNTI APERTI

### 1. Naming repo prima di PyPI (BACKLOG, Blocco 6)

Non bloccante per Blocco 5 ma se vogliamo evitare di pubblicare con nome "sbagliato", decidere entro fine Blocco 5. Vedi `BACKLOG.md` → naming.

### 2. Pulizia placeholder strutturali in `template/docs/SESSION_HANDOFF.md` (basso costo, opzionale)

`kaora check` post-fix4 NON li segnala più (sono dentro fenced code block, escluso da `_strip_code_blocks`). Ma se quei `{{project_path}}` e `{{year}}` nella spec stampata non sono volutamente esemplificativi, conviene pulirli alla fonte nel template. 30 secondi di edit.

### 3. Eventuale ADR-010 sul pattern `_strip_code_blocks` (formalizzazione)

Pattern emerso 2 volte nello stesso Blocco 4 come fix coerente: "contenuto documentario interpretato come stato reale". Se emerge una terza categoria che richiede lo stesso fix, vale la pena formalizzare con ADR.

---

## Obiettivo Blocco 5

Asset di lancio pubblico. Far capire in 30 secondi a un visitatore del repo cosa è kaora-memory e perché dovrebbe usarlo. Brownfield-friendly: niente warning "solo greenfield", FAQ "ho già un CLAUDE.md?" → racconta backup-first + BOOTSTRAP-merge come *feature*.

### Output atteso a fine Blocco 5

1. **`README.md` ricco** che sostituisce l'attuale minimal. Sezioni proposte (da validare in sessione):
   - Hero: "Memoria operativa per agenti AI. Funziona su qualsiasi progetto, fresco o esistente."
   - Problema: agenti AI senza memoria persistente, drift docs, sessioni isolate
   - Soluzione: `pip install kaora-memory` → `kaora init` → ogni agente nuovo legge `AGENTS.md` + `CLAUDE.md` e parte coerente
   - Quickstart: 3 comandi `pip install kaora-memory && cd mioprogetto && kaora init`
   - FAQ brownfield: "ho già un CLAUDE.md?" → backup + merge guidato
   - `kaora check` come strumento di validazione continua (output esempio)
   - Link a `docs/PHILOSOPHY.md` per il *perché*
2. **Demo del flow** (asciicast `asciinema` o GIF): `kaora init mioprogetto && kaora check mioprogetto`. Output reale visibile in poche righe.
3. **Refresh asset esistenti** (vedi `CURRENT_STATE.md` → "Asset di comunicazione collegati"):
   - `/tmp/kaora-memory-preview.html` — landing page premium, datata 22 maggio, da aggiornare con nuove feature (check, dogfooding)
   - `/tmp/kaora-memory-launch-essay-brief.md` — brief saggio (sessione parallela)
4. **Commit messaggio suggerito:** `feat(launch): README ricco + asciicast demo + landing refresh`
5. **CURRENT_STATE.md + SESSION_HANDOFF.md** aggiornati con brief Blocco 6 (pubblicazione PyPI)

### File da creare / modificare

- `README.md` (riscrittura completa)
- Eventuale `docs/quickstart.md` o `docs/faq.md` se README cresce troppo
- Eventuale `assets/demo.cast` (asciinema) o `assets/demo.gif` (terminalizer)
- Refresh `/tmp/kaora-memory-preview.html` (fuori repo)

### Cosa NON toccare (Blocchi 1-4 chiusi)

- ❌ `LICENSE`, `.gitignore`, `pyproject.toml` (salvo bump versione se servisse)
- ❌ `kaora_memory/{__init__, settings_merger, template_resolver, installer, check}.py` — moduli stabili
- ❌ `kaora_memory/cli.py` — salvo aggiunta di feature CLI legate al README (es. comando `kaora doctor` se emerge l'esigenza, ma è scope futuro)
- ❌ `template/` salvo l'item v0.1 di pulizia placeholder strutturali (vedi PUNTI APERTI 2)
- ❌ `bin/setup-dev.sh` — wrapper self-healing UF_HIDDEN stabile dal 2026-05-24
- ❌ Riaprire ADR `Accepted` (000-009)
- ❌ Push su GitHub — username finale ancora da decidere (vedi BACKLOG naming)

### Skill obbligatorie PRIMA di costruire (Gate A § 5.1)

- **Nessuna obbligatoria.** Blocco 5 è scrittura + asset visivi, non richiede skill tecniche specifiche di kaora.
- *Opzionali*, se Alexis vuole struttura validata: `copywriting`, `marketing-psychology`, `landing-page-generator`. Decisione caso per caso.

### Check di apertura sessione

```bash
cd ~/Desktop/kaora-memory
python3 -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))" && echo "TOML OK"
git log --oneline -5
.venv/bin/python -m pytest -q && echo "TEST OK (62/62)"
.venv/bin/kaora --version && echo "CLI OK"
.venv/bin/kaora check . 2>&1 | tail -20   # dogfooding rapido stato repo
```

Se `kaora --version` fallisce con `ModuleNotFoundError`: `bash bin/setup-dev.sh` (reinstalla wrapper self-healing su `.venv/bin/kaora`). Capita se hai rifatto `pip install -e .` bypassando lo script.

---

## Note operative per la prossima sessione

- **Apri Claude Code in `~/Desktop/kaora-memory/`**
- **Registro:** italiano · diretto · no preamboli · una decisione alla volta · modalità Operativa vs Apprendimento (ADR-007)
- **Decisioni grandi** → nuova ADR in `docs/DECISIONS.md` (ADR-008 step 6 del rituale)
- **Modalità Blocco 5** è **scrittura ad alta densità**, non implementazione. Aspettati molta più modalità *Apprendimento* (esplorazione narrativa, scelta hero, tone of voice) rispetto a Blocco 4.
