# DECISIONS.md — ADR log immutabile

> Architectural Decision Records. **Append-only.** Una decisione chiusa si riapre solo con una nuova ADR che la sostituisce esplicitamente (`Supersedes: ADR-XXX`).
>
> Formato: data · contesto · decisione · alternative scartate · conseguenze.

---

## ADR-000 — Adozione dogfooding

**Data:** 2026-05-22
**Stato:** accepted

### Contesto

Stiamo costruendo `kaora-memory`, un pacchetto Python che installa scaffolding di memoria operativa per agenti AI in qualsiasi progetto. Domanda emersa nella sessione del 22 maggio: il repo `kaora-memory` stesso deve usare la skill che pubblica?

### Decisione

**Sì.** Dopo che il Blocco 3 (`kaora init`) sarà chiuso e funzionante, eseguiremo `kaora init .` nel repo stesso. Nel frattempo (in Blocco 1) creiamo manualmente la memoria operativa minima per il repo (`CLAUDE.md`, `docs/CURRENT_STATE.md`, `docs/SESSION_HANDOFF.md`, `docs/DECISIONS.md`) replicando il pattern che la skill installerà.

### Alternative scartate

- **A — Repo di sviluppo senza memoria operativa.** Più semplice, ma:
  - Disonesto narrativamente (vendiamo memoria persistente senza usarla)
  - Le sessioni di sviluppo del repo stesso ripartirebbero da zero, perdendo coerenza
- **B — Memoria manuale ma divergente dal template.** Più libero, ma il repo non sarebbe un valid prima dimostrazione del prodotto

### Conseguenze

- Il repo `kaora-memory` è il **primo utente reale** della skill. Se non funziona qui, non funziona da nessuna parte.
- Quando i template Blocco 2 saranno pronti, i file `CLAUDE.md` / `docs/*` di questo repo andranno sostituiti con quelli generati da `kaora init` (forse rifiniti a mano dove diverge per specificità).
- Pattern di dogfooding va menzionato esplicitamente nel README come segnale di serietà del prodotto.

---

## ADR-001 — Rituale di apertura universale incondizionato + skip via intent naturale

**Data:** 2026-05-22
**Stato:** accepted

### Contesto

La skill kaora-memory promuove il "rituale di apertura sessione" come pratica operativa. Domanda: che cosa fa partire il rituale? Una frase specifica come `"claude vai"`? Un set di trigger phrases? Un'apertura automatica?

### Decisione

**Rituale incondizionato.** A prescindere da:
- chi è l'agente (Claude Code, Codex, Cursor, Gemini CLI, altro)
- come l'utente apre la sessione (qualsiasi input — "vai", "ciao", "?", richiesta tecnica, silenzio)
- se l'utente chiama l'agente per nome o no

Alla prima risposta della sessione, l'agente esegue il rituale (lettura file → sintesi 3 righe → attesa conferma). Una sola volta per conversazione.

**Skip via riconoscimento intent naturale.** L'agente riconosce semanticamente l'intento di skip (es. *"salta il rituale, so già cosa fare"*, *"bypass, vai dritto"*, *"veloce"*). Match semantico, non sintattico. In caso di dubbio chiede conferma in una riga.

### Alternative scartate

- **Trigger phrase fissa** (`"kaora go"` o `"claude vai"`): rigida, non funziona se l'utente apre con altro, e fa sembrare il prodotto Claude-only
- **Trigger via comando esplicito** (`/kaora-init-context`): troppa frizione cognitiva, dimentichi
- **Match sintattico** sulla skip phrase: fragile, fallisce con varianti non previste

### Conseguenze

- Il prodotto è agnostico rispetto all'agente — supporta Claude Code, Codex, Cursor, Gemini CLI con la stessa esperienza
- Il rituale va codificato in `CLAUDE.md` E in `AGENTS.md` (vedi ADR-003)
- Skip va documentato esplicitamente nel template con esempi multilingua

---

## ADR-002 — `kaora init` istantaneo + bootstrap agent-driven via `<BOOTSTRAP/>` markers

**Data:** 2026-05-22
**Stato:** accepted

### Contesto

Domanda di design: come si raccolgono le informazioni minime (identità progetto, registro comunicazione, ecc.) per popolare i template?

### Decisione

**`kaora init` è istantaneo. Zero prompt interattivi.** Copia il `template/` nella destinazione, sostituisce placeholder strutturali (path, anno, nome cartella), esegue `git init` se serve. Fine.

I file generati contengono `<BOOTSTRAP need="..." sources="..."/>` markers nelle sezioni che richiedono input umano. Alla **prima sessione AI** (qualsiasi agente), il modello:
1. Investiga il progetto (git config, README, package files, commit log)
2. Compila bozze dei `<BOOTSTRAP/>` autonomamente
3. Chiede 1-2 domande mirate solo per i buchi
4. Applica diff con conferma utente

Frizione cognitiva crollata da ~10 min di scrittura manuale a ~30 sec di 2 risposte.

### Alternative scartate

- **Wizard 4-prompt interattivo (`click.prompt`)** — proposta iniziale di Claude Desktop. Più semplice tecnicamente ma:
  - 10 min di scrittura manuale obbligatoria
  - Richiede all'utente di decidere TUTTO subito (pet peeve, anti-pattern, ecc.) — molti rispondono male e non tornano a sistemare
  - Il valore di "agente competente dal primo turno" non viene mostrato

- **File completamente pre-compilati** con valori default — fallisce perché ogni utente è diverso

### Conseguenze

- Implementazione `kaora init` (Blocco 3) è molto più semplice: copia + sostituisce path + git init
- Aggiunge un convention/protocollo `<BOOTSTRAP/>` che va documentato bene in `AGENT_BRIEF.md` (Blocco 2)
- Il vero "wow moment" della skill è la prima `claude vai` (o equivalente), non l'install

---

## ADR-003 — Cross-agent via AGENTS.md come gemello funzionale di CLAUDE.md

**Data:** 2026-05-22
**Stato:** accepted

### Contesto

Claude Code auto-carica `CLAUDE.md`. Codex CLI, Cursor, Aider, e altri agenti seguono il proposed standard `AGENTS.md`. Come supportare entrambi senza duplicare contenuto?

### Decisione

Il template include **entrambi**:
- `CLAUDE.md` — auto-caricato da Claude Code
- `AGENTS.md` — auto-caricato da Codex / Cursor / Aider / Gemini CLI / altri agenti compliant con lo standard

I due file sono **gemelli funzionali**: contengono lo stesso identico contenuto, generato dallo stesso template Jinja al momento di `kaora init`. Eventualmente nel futuro, se i due standard divergeranno, faremo due template separati.

### Alternative scartate

- **Solo `CLAUDE.md`** — taglia fuori 50%+ degli utenti potenziali (Codex/Cursor in espansione)
- **Solo `AGENTS.md`** — funziona ma Claude Code non lo legge (richiede istruzioni esplicite all'utente)
- **Symlink `AGENTS.md → CLAUDE.md`** — non funziona su Windows e in alcuni harness

### Conseguenze

- Il piano di Blocco 2 genera due file dallo stesso contenuto
- `kaora init` deve generare entrambi a partire dallo stesso template
- README evidenzia il supporto cross-agent come differenziatore

---

## ADR-004 — Layout package flat + build backend hatchling

**Data:** 2026-05-22
**Stato:** accepted

### Contesto

Scelta di layout per il pacchetto Python distribuito su PyPI. Opzioni: `src/kaora_memory/` (raccomandato come best practice per librerie) vs `kaora_memory/` flat (più semplice).

### Decisione

**Flat layout:** `kaora_memory/` accanto a `pyproject.toml`. **Build backend:** `hatchling`.

### Alternative scartate

- **`src/` layout** — best practice ufficiale Python. Più sicuro contro import accidentali da root, ma:
  - Aggiunge un livello di indirezione per un pacchetto piccolo (v0.1: 2-3 file Python)
  - Richiede config esplicita `packages.find` o equivalente in hatchling
  - Per un CLI tool con superficie minima, il costo cognitivo non è giustificato

- **setuptools / poetry / flit** — funzionano tutti ma:
  - `setuptools`: legacy, configurazione più verbosa
  - `poetry`: lock file ed ecosistema separato (overkill per un pacchetto senza dipendenze pesanti)
  - `flit`: ottimo per pure Python ma meno mainstream di hatchling oggi

### Conseguenze

- Pyproject minimale: `[tool.hatch.build.targets.wheel] packages = ["kaora_memory"]`
- Includere `template/` come data file richiede `force-include` (vedi `SESSION_HANDOFF.md` Blocco 2)
- Se in futuro v0.5+ il package crescerà a 15+ moduli, eventuale switch a `src/` layout richiederà nuova ADR

---

## Catena causale già emersa

- **ADR-000** (dogfooding) → spiega perché esistono `CLAUDE.md` e `docs/*` nel repo stesso prima del Blocco 3
- **ADR-001** (rituale universale) + **ADR-003** (cross-agent) si rafforzano: senza ADR-003 il rituale universale rimarrebbe Claude-only
- **ADR-002** (init istantaneo) dipende da **ADR-001** (rituale): l'agente sa cosa fare anche senza input perché il rituale è codificato

---

## Versionamento ADR

- v0.1.0 — ADR 000-004 (questa sessione 22 maggio 2026)
