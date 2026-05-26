# Backlog

> Idee e funzionalità per versioni future. NON fanno parte della v0.1.
> Tutto ciò che viene fuori durante lo sviluppo e non è strettamente v0.1
> finisce qui, non nel codice.

---

## Comandi CLI futuri

- `kaora handoff` (v0.2+) — automazione CLI del rituale di chiusura sessione (vedi § 6bis di AGENTS.md, già attivo via agente in v0.1). Investiga `git diff` autonomamente, genera bozze di `SESSION_HANDOFF.md` + `CURRENT_STATE.md`, propone commit. L'utente conferma e basta.
- `kaora errors record` — wizard per scrivere un post-mortem strutturato (immune memory)
- `kaora skill install` — registrazione automatica della skill nei vari AI assistant (Claude Code skills dir, Cursor rules, ecc.)

## Automazioni runtime

### Rituale di chiusura sessione — IMPLEMENTATO in v0.1 (2026-05-26)

Originariamente pensato per v0.2+. Promosso a v0.1 dopo scoperta operativa durante dogfooding: la mancanza di un rituale di chiusura simmetrico al rituale di apertura ha portato `docs/CURRENT_STATE.md` e `docs/SESSION_HANDOFF.md` a divergere dallo stato reale del codice (info datate ereditate dalla sessione successiva).

**Stato:** § 6bis "Rituale di chiusura sessione" aggiunta a `template/AGENTS.md` + `AGENTS.md` del repo kaora-memory. L'agente esegue chiusura ordinata quando l'utente segnala fine sessione: sintesi → aggiornamento CURRENT_STATE → aggiornamento SESSION_HANDOFF → proposta commit. Gate C per ogni step.

Vedi `docs/DOGFOODING_REPORT.md` § 4 per il contesto della scoperta.

### Hook context-threshold a 60% → proposta automatica chiusura (v0.2+)

Trigger automatico esterno per il rituale di chiusura (§ 6bis). Quando il sistema host raggiunge 60% di context usage, inietta un messaggio all'agente che esegue il rituale prima che la sessione si rompa per saturazione.

- Claude Code only in prima release (hook system maturo, evento Stop / context-threshold disponibile)
- In v0.2+ portare su Codex / Cursor / Gemini CLI tramite wrapper esterno (monitor file di sessione + notifica)

## Infrastruttura

- MCP server (kaora-memory come servizio remoto)
- Cloud sync delle memorie cross-device

### Dashboard premium — `kaora dashboard` (target v0.2)

Web UI per visualizzare la memoria operativa del progetto. Riferimento di design:
`~/Desktop/kaora/kaora-dashboard.html` (asset esistente, costruito per progetto Kaora Multi-Agent Platform, va adattato).

**Stack tecnico previsto:**
- Frontend: HTML/CSS/JS single-file, marked.js + highlight.js da CDN (o inline)
- Estetica: glassmorphism con `color-mix(in oklch)`, mesh gradient animato, noise SVG anti-banding, palette dark cyan/purple/orange
- Tipografia: Inter (UI) + Cinzel (decorativo) + JetBrains Mono (code)
- Layout: sidebar 320px (brand + stage + search + file list) + content area (header meta + markdown rendering)

**Due strategie possibili:**

**Strategia A — server locale (default per dev):**
```
$ kaora dashboard
  Server avviato su http://localhost:7777 — browser aperto. Ctrl+C per fermare.
```
- `kaora_memory/dashboard.py` spawn `http.server` (stdlib, zero dipendenze nuove)
- Auto-refresh ogni 30s, vede modifiche live durante le sessioni AI
- Process muore alla chiusura

**Strategia B — static export (snapshot condivisibile):**
```
$ kaora dashboard --export
  Generato docs/dashboard.html — apri da file://...
```
- Render server-side dei markdown (`markdown-it-py` o `mistletoe`), inline-everything nell'HTML
- File singolo portatile, zero infrastruttura runtime, condivisibile via email/Slack
- Snapshot fissa, va rigenerato dopo modifiche

**Adattamenti necessari rispetto al riferimento di design:**
1. Branding parametrico: `{{project_name}}`, `{{project_oneliner}}` invece di `KAORA Multi-Agent Platform`
2. Stage system astratto: leggere `Blocco corrente` da `docs/CURRENT_STATE.md` via regex, NON hardcoded "Stage 0/1/2"
3. File map convenzionale a gruppi:
   - **Master context:** `CLAUDE.md`, `AGENTS.md`
   - **Onboarding:** `AGENT_BRIEF.md`
   - **Stato vivo:** `docs/CURRENT_STATE.md`, `docs/SESSION_HANDOFF.md`
   - **Decisioni:** `docs/DECISIONS.md` (sub-vista ADR filtrabile per Stato)
   - **Identità:** `docs/IDENTITY.md`
   - **Errori:** `docs/SESSION_ERRORS_TEMPLATE.md` + `docs/SESSION_ERRORS/*` se esiste
   - **Backlog:** `BACKLOG.md`
4. JSON index generato programmaticamente dal contenuto della directory
5. Vista ADR dedicata con filtri Accepted/Proposed/Rejected/Superseded (pattern visuale di ADR-008)

**Roadmap timing:**
- v0.2.0 → Strategia A (`kaora dashboard`)
- v0.2.1 → Strategia B (`kaora dashboard --export`)

## Pattern operativi

(spazio aperto — la regola sub-agente vs Read diretto è stata promossa a **ADR-009 Accepted** in `docs/DECISIONS.md` e codificata in `template/AGENTS.md` § 10 il 22 maggio 2026, già attiva in v0.1)

## Template

- Bootstrap agent-driven completo (l'agente investiga e compila i `<BOOTSTRAP/>` markers leggendo git config, README, package.json, ecc.) — design definito, implementazione in Blocco 2/3
- Skin alternative per il template (es. registro inglese, registro tecnico-asciutto, registro conversazionale)

### `.kaora-bak` — terza opzione "archive" in § 11 step 5 — IMPLEMENTATA 2026-05-27 (v0.1)

Oggi `template/AGENTS.md` § 11 step 5 dice:
> *"Al termine, chiedi a {{owner_name}} se vuole conservare i `.kaora-bak` o eliminarli"*

Scoperta operativa dal dogfooding 2026-05-26: la realtà offre **tre opzioni**, non due:

1. **Eliminare** — perde l'artefatto storico
2. **Conservare in root/docs/** — il rituale § 6 step 4 lo trova e lo segnala ad ogni apertura sessione (rumore inutile, il contenuto è già stato migrato)
3. **Archiviare** in `docs/archive/CLAUDE.md.kaora-bak` (o equivalente) — conserva l'artefatto, non fa scattare lo scan, demonstrability del pattern "kaora migra memoria pre-esistente"

L'agente naive durante il merge guidato del repo kaora-memory stesso ha **inventato spontaneamente** l'opzione 3 — segnale che la convenzione è naturale, va solo formalizzata nel template.

**Fix:** aggiornare `template/AGENTS.md` § 11 step 5 a:
> *"Al termine, chiedi a {{owner_name}} cosa fare dei `.kaora-bak`: (1) eliminare, (2) conservare in posizione attuale, (3) archiviare in `docs/archive/` per non far scattare lo scan rituale di apertura. Default suggerito: (3)."*

Costo: 1 Edit a template/AGENTS.md, ~30 secondi. Zero impatto su test (non c'è codice Python coinvolto). Da chiudere prima del lancio v0.1.

### Onboarding multi-canale per `docs/IDENTITY.md` (target v0.2)

Oggi `kaora init` crea `docs/IDENTITY.md` con BOOTSTRAP markers e l'agente alla prima sessione li riempie investigando il repo (git config, README, package files). Funziona ma assume che l'identità builder sia deducibile dal codice — spesso non lo è.

Molti utenti hanno **identità già scritta altrove**: dossier personale locale (es. `~/Desktop/linkedin/dossier-alexis.md`), profilo X / LinkedIn / Instagram, bio GitHub, manifesto privato. L'agente dovrebbe **chiedere all'utente quale canale preferisce** per compilare IDENTITY.md, invece di dedurre solo dal repo.

**Comportamento proposto:**
Alla prima sessione post-init, l'agente rileva IDENTITY.md con BOOTSTRAP aperti e chiede:
> *"Per riempire docs/IDENTITY.md (chi sei come builder), quale fonte vuoi usare?*
> *(1) Dossier locale già scritto (mi dici dove sta)*
> *(2) Profilo X / LinkedIn / Instagram (scarico e analizzo i post pubblici)*
> *(3) Bio GitHub + recent commits (più tecnica)*
> *(4) Ti faccio 5 domande mirate (zero asset pre-esistente)*
> *Quale preferisci?"*

L'utente sceglie, l'agente esegue il canale e propone il diff per IDENTITY.md.

**Implementazione probabile:**
- Convenzione nel template `AGENT_BRIEF.md` + `template/AGENTS.md` § 11 (o nuova § dedicata all'onboarding)
- Pattern coerente con ADR-002 (zero attrito) e ADR-008 (zero attrito decisioni in chat)
- Non richiede codice Python aggiuntivo se gestito interamente dal layer agente
- Eventualmente CLI helper `kaora identity --source dossier=PATH | x=@handle | ig=@handle | github=user | ask` per automatizzare lo scraping (richiede integrazione Apify/social API → costo)

**Why:** è il salto da "memoria del progetto" a "memoria del builder dietro il progetto". Differenziatore forte per professional builder che hanno già un personal brand articolato e vogliono riusarlo invece di rispiegarlo ad ogni nuovo repo.

**How to apply:** quando v0.1 è chiusa, prima cosa di v0.2.

## Asset di lancio v0.1 (target Blocco 5-6)

Da finalizzare quando arriviamo al README ricco + pubblicazione PyPI:

- **Landing page premium:** `/tmp/kaora-memory-preview.html` (1008 righe, datato 22 maggio 00:55, anteprima v0.1)
  - Aggiornare: numerazione ADR (da "Stage 1 Fase 8 ADR-034" → "Blocco 2 chiuso · ADR 000-009"), aggiungere framing metacognitivo emerso il 22 maggio, riallineare 6 layer ai file template reali, citare ADR-005/006/007/008/009
- **Saggio di lancio (brief operativo):** `/tmp/kaora-memory-launch-essay-brief.md` (16 sezioni, generato 22 maggio sera) — passato alla sessione parallela che sta scrivendo il saggio
- **Documento vision astratta:** `/Users/alexissilva/Desktop/kaora-memory-architecture-dashboard.html` (datato 20 maggio, "Memory Architecture LLM Wiki Extended") — riusabile come asset di profondità filosofica per audience accademica/intellettuale, oppure da archiviare se non riallineato

### Strategia narrativa: dove mostrare la filosofia (target Blocco 5-6)

La filosofia metacognitiva (vedi [`docs/PHILOSOPHY.md`](docs/PHILOSOPHY.md)) è uno dei pilastri narrativi principali del prodotto e va distribuita su più canali con profondità calibrata per audience:

| Canale | Profondità | Cosa mostrare della filosofia |
|---|---|---|
| **Landing page premium** (`/tmp/kaora-memory-preview.html` aggiornata) | 🔴 Centrale | Sezione dedicata "Cos'è davvero" con tesi metacognitiva + mapping regole→atti + frame narrativo agente umile vs arrogante + 1-2 citazioni Flavell/Vygotsky in nota |
| **README.md del repo** | 🟡 Sintetica | Hero pratico + tagline filosofica + sezione "Filosofia in 3 paragrafi" + link a `docs/PHILOSOPHY.md` |
| **Saggio di lancio** (Substack/Medium) | 🔴 Espansa al massimo | Argomentazione completa ~3000 parole. Brief in `/tmp/kaora-memory-launch-essay-brief.md` ha già la struttura |
| **`kaora dashboard` v0.2 runtime** | 🟢 Light | Tab "Why kaora" o link a PHILOSOPHY.md su GitHub. L'utente che usa già il prodotto vuole stato del progetto, non manifesto |
| **Pagina PyPI** | 🟢 Una riga | Description: *"Memoria operativa per agenti AI. Metacognizione indotta — l'agente umile riconosce i limiti."* + link a GitHub |
| **X/Twitter thread di lancio** | 🟡 Hook + dimostrazione | 10-15 tweet con esempi concreti (codice, screenshot ADR, demo `claude vai`) |

**Strategia ordine landing page:** *risolvere prima, raccontare il perché dopo*. Hero pratico → demo → "come funziona" → "**cos'è davvero**" (qui filosofia) → setup. Invertire perde i tecnici che cercano soluzione.

**Sotto-trama narrativa da sfruttare:** ADR-007 nata da osservazione builder neurodivergente in tempo reale = caso di **co-evoluzione umano-agente documentato**. Nessun altro prodotto AI ha questa storia. Va nel saggio come capitolo, va citata nella landing.

## Decisione naming repo (target Blocco 5, prima della pubblicazione PyPI)

Il framing metacognitivo emerso il 22 maggio rende `kaora-memory` un nome sotto-rappresentativo del prodotto. Vedi [`docs/PHILOSOPHY.md`](docs/PHILOSOPHY.md) § 7 per la matrice di candidati (`kaora-metacognition`, `kaora-meta`, `kaora-mc`, `kaora-mind`, `kaora-self`, `kaora-thinks`, `kaora-core`, status quo). Decisione necessaria **prima** della pubblicazione PyPI (Blocco 6), perché rinominare un pacchetto pubblicato è doloroso.

## Issue noti / Bug minori

### macOS `UF_HIDDEN` su file `.pth` generato da hatchling editable install — RISOLTO 2026-05-24

**Sintomo originale:** dopo `pip install -e .` su macOS con Python 3.13, il comando `kaora` fallisce con `ModuleNotFoundError: No module named 'kaora_memory'`. Causa: hatchling crea `_editable_impl_kaora_memory.pth` con il flag macOS `UF_HIDDEN`. Python 3.13's `site.py` rifiuta esplicitamente i `.pth` con `UF_HIDDEN` ("Skipping hidden .pth file"), quindi il path al sorgente non viene aggiunto a `sys.path`. Aggravante: macOS ri-applica spontaneamente `UF_HIDDEN` anche senza `pip install` nel mezzo (probabile APFS metadata o Spotlight indexing).

**Soluzione adottata (2026-05-24):** wrapper bash self-healing su `.venv/bin/kaora`. `bin/setup-dev.sh` sovrascrive lo script Python generato da hatchling con un wrapper bash che esegue `chflags nohidden` sul `.pth` ad ogni invocazione, poi fa `exec python -m kaora_memory.cli "$@"`. Idempotente, costa ~5ms, non blocca operazioni normali del venv (es. `rm -rf .venv`, futuri `pip install -e .`). Stress test confermato: forzando `chflags hidden` sul `.pth`, `kaora --version` continua a funzionare e rimuove il flag al volo.

**Comportamento dopo fix:**
- Il flag `UF_HIDDEN` può tornare spontaneamente quanto vuole — irrilevante, viene rimosso al volo all'esecuzione successiva di `kaora`
- `pip install -e .` rigenera lo script `.venv/bin/kaora` originale (sovrascrivendo il wrapper) → basta rieseguire `bash bin/setup-dev.sh` per ripristinarlo

**Scope:** colpisce solo developer su macOS in editable install. Utente finale (`pip install kaora-memory` da PyPI) non ha questo problema (il wheel non genera `.pth`, e `bin/` non è distribuito nel wheel).

**Azioni residue (non bloccanti):**
- Eventuale issue upstream a hatchling chiedendo se il `.pth` generator può evitare di triggerare `UF_HIDDEN`
- Monitorare se future versioni di hatchling cambiano naming del `.pth` (il wrapper usa glob `*kaora*.pth`, rompe silenziosamente se cambia)

## Pre-publish checklist (Blocco 6)

Da eseguire **immediatamente prima** di ogni `twine upload` su PyPI. Motivo: il wheel in `dist/` non si rigenera da solo quando modifichi codice. Pubblicare un wheel stale = utente finale riceve `ModuleNotFoundError` o feature mancanti (bug scoperto in test #3 sessione 2026-05-24: wheel era datato 23 maggio prima che `cli.py` e `installer.py` esistessero).

```bash
# 1. Butta artefatti vecchi
rm -rf dist/ build/ *.egg-info/

# 2. Rebuild wheel + sdist da zero
.venv/bin/python -m build

# 3. Test installazione in venv totalmente pulito
python3 -m venv /tmp/publish-test
/tmp/publish-test/bin/pip install dist/kaora_memory-*.whl
/tmp/publish-test/bin/kaora --version          # → kaora, version 0.1.0
/tmp/publish-test/bin/kaora init /tmp/publish-init-test --no-git-init
find /tmp/publish-init-test -type f | wc -l    # → 13
rm -rf /tmp/publish-test /tmp/publish-init-test

# 4. Test PyPI staging
.venv/bin/twine upload --repository testpypi dist/*

# 5. Test install da testpypi in altro venv pulito
python3 -m venv /tmp/testpypi-test
/tmp/testpypi-test/bin/pip install --index-url https://test.pypi.org/simple/ kaora-memory
/tmp/testpypi-test/bin/kaora --version
rm -rf /tmp/testpypi-test

# 6. Solo dopo tutti gli step verdi: PyPI production
.venv/bin/twine upload dist/*
```

**Automazione futura (v0.2+):** sostituire con GitHub Actions su tag di release. Vedi anche issue UF_HIDDEN sopra (impatta solo dev macOS, non utente finale).

## Idee da valutare

(spazio aperto — ogni cosa che emerge va qui prima di entrare in v0.x)
