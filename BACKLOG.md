# Backlog

> Idee e funzionalità per versioni future. NON fanno parte della v0.1.
> Tutto ciò che viene fuori durante lo sviluppo e non è strettamente v0.1
> finisce qui, non nel codice.

---

## Comandi CLI futuri

- `kaora handoff` — chiusura sessione automatica (genera SESSION_HANDOFF.md + aggiorna CURRENT_STATE.md)
- `kaora errors record` — wizard per scrivere un post-mortem strutturato (immune memory)
- `kaora skill install` — registrazione automatica della skill nei vari AI assistant (Claude Code skills dir, Cursor rules, ecc.)

## Automazioni runtime

- **Hook context-threshold a 60% → proposta automatica SESSION_HANDOFF**
  · Claude Code only in prima release
  · In v0.2+ portare su Codex / Cursor / Gemini CLI tramite wrapper esterno (monitor file di sessione + notifica)

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

## Idee da valutare

(spazio aperto — ogni cosa che emerge va qui prima di entrare in v0.x)
