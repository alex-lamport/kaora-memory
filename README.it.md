![kaora-memory — metacognizione indotta per agenti AI](https://raw.githubusercontent.com/alex-lamport/kaora-memory/main/docs/assets/kaora-hero.png)

[🇬🇧 English](README.md) · **🇮🇹 Italiano** · [🇪🇸 Español](README.es.md)

# kaora-memory

> **Metacognizione indotta per agenti AI.**
> Una memoria operativa a livello di progetto che fa partire gli agenti di coding già preparati, rispettare le decisioni e fermarsi prima di agire alla cieca.

`pip install kaora-memory` → `kaora init` → ogni agente che apre il progetto (Claude Code, Codex, Cursor, Gemini CLI) legge lo stesso contesto canonico e parte coerente.

---

## Avvio rapido

```bash
pip install kaora-memory
cd myproject
kaora init
```

Tutto qui. Apri Claude Code (o qualsiasi altro agente) in `myproject`, scrivi `go`, e l'agente legge la memoria operativa prima di fare qualsiasi altra cosa.

Progetto nuovo: `kaora init` scrive 13 file (vedi sotto).
Progetto esistente con un `CLAUDE.md` o `AGENTS.md` già presente: `kaora init` ne fa il backup come `.kaora-bak` e l'agente fonde i tuoi contenuti esistenti nella struttura canonica durante la prima sessione. Vedi le [Brownfield FAQ](#brownfield-faq).

### Installazione su macOS

Su macOS un semplice `pip install` è spesso bloccato (l'"ambiente gestito esternamente" di Python). Installa `kaora` come CLI isolata con **pipx**:

```bash
brew install pipx        # se non ce l'hai ancora
pipx ensurepath
pipx install kaora-memory
```

Preferisci un virtualenv? Va bene anche quello:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install kaora-memory
```

Se subito dopo l'installazione ottieni ancora `kaora: command not found`, apri una nuova finestra del terminale così la shell aggiorna il `PATH`.

---

## Cosa ottieni

Dopo `kaora init` il tuo progetto ha:

```
myproject/
├── AGENTS.md              # contesto master canonico, cross-agent
├── CLAUDE.md              # entry point di 4 righe, importa @AGENTS.md
├── AGENT_BRIEF.md         # onboarding di 3 minuti per ogni nuovo agente
├── BACKLOG.md             # idee fuori dallo scope attuale
├── docs/
│   ├── IDENTITY.md              # chi è il builder, come collaborare
│   ├── CURRENT_STATE.md         # stato vivo, aggiornato a fine sessione
│   ├── SESSION_HANDOFF.md       # brief per la sessione successiva
│   ├── DECISIONS.md             # registro ADR, append-only
│   └── SESSION_ERRORS_TEMPLATE.md
└── .claude/
    ├── settings.json      # configurazione hook di Claude Code
    └── hooks/             # protect-credentials.sh, log-api-calls.sh
```

Tutti i template contengono marcatori `<BOOTSTRAP/>` che l'agente riempie durante la prima sessione ispezionando il repo — nessuna configurazione manuale.

---

## Cos'è davvero

kaora-memory non è un database di memoria, un vector store, né un altro framework per agenti.

È un **protocollo operativo** per agenti di coding AI: un piccolo insieme di file, rituali, gate e regole di handoff che costringono l'agente a compiere gli atti regolatori della metacognizione prima e durante il lavoro.

Senza kaora, l'agente esegue.

Con kaora, l'agente parte chiedendosi: *cosa so, cosa non so, cosa è già stato deciso, e quando devo fermarmi?*

---

## Perché esiste

Gli agenti AI hanno un problema di amnesia. Ogni nuova sessione parte da zero: nessuna memoria delle decisioni passate, nessuna consapevolezza delle preferenze del builder, nessuna regola codificata su cosa fare quando si è incerti.

Tre sintomi concreti:

1. **Drift dei doc** — README, ADR e documenti di progetto perdono sincronia con il codice perché niente costringe l'agente ad aggiornarli alla chiusura della sessione.
2. **Azione improvvisata** — senza regole esplicite, l'agente salta gli strumenti giusti, scrive file senza conferma e risolve l'incertezza tirando a indovinare.
3. **Perdita di contesto tra agenti** — un progetto passato da Claude Code a Codex riparte da zero due volte.

kaora-memory affronta tutti e tre dando al progetto una **memoria operativa canonica** che ogni agente AI legge all'inizio della sessione, e un insieme di **comportamenti codificati** che l'agente esegue, che il builder si ricordi di chiederlo o no.

---

## Come funziona

Dopo `kaora init`, il progetto porta con sé due lati indipendenti.

**Lato memoria** — file persistenti nella root del progetto e in `docs/`:
- `AGENTS.md` è il contesto master canonico. `CLAUDE.md` è un file di 4 righe che importa `AGENTS.md` (vedi [ADR-005](https://github.com/alex-lamport/kaora-memory/blob/main/docs/DECISIONS.md)).
- `CURRENT_STATE.md` registra "dove siamo adesso"; `SESSION_HANDOFF.md` porta il brief per la sessione successiva.
- `DECISIONS.md` è il registro ADR append-only: ogni decisione architetturale vive qui con la sua data, lo stato e la motivazione.

**Lato comportamento** — regole codificate dentro `AGENTS.md`, rispettate da ogni agente:
- **Rituale di apertura** — alla prima risposta di ogni sessione l'agente legge la memoria operativa, riassume lo stato in 3-5 righe e attende conferma.
- **Gate A** — prima di ogni `Edit` o `Write` l'agente verifica che non si stia contraddicendo un ADR chiuso, che sia stata invocata la skill giusta e che il valore sia verificato.
- **Gate B** — dopo 3-4 file modificati l'agente fa un checkpoint con il builder.
- **Gate C** — nessun file scritto, nessuna decisione presa, senza un `go` esplicito.
- **Modalità Operativa vs Apprendimento** — l'agente rileva se il builder sta eseguendo o esplorando e si adatta (vedi [ADR-007](https://github.com/alex-lamport/kaora-memory/blob/main/docs/DECISIONS.md)).

La memoria persiste tra sessioni e agenti. Il comportamento viene letto all'inizio della sessione e rispettato per tutta la conversazione.

---

## Brownfield FAQ

> **Ho già un `CLAUDE.md` (o `AGENTS.md`) nel mio progetto. Cosa succede?**

`kaora init` ne fa il backup come `CLAUDE.md.kaora-bak` (preservando ogni byte) e scrive il `CLAUDE.md` canonico di 4 righe che importa `AGENTS.md`. Alla tua prima sessione dopo `kaora init`, l'agente trova il `.kaora-bak`, lo legge e propone una **fusione guidata** nel `AGENTS.md` canonico. Tu confermi, la fusione avviene, il `.kaora-bak` viene archiviato in `docs/archive/` così non innesca la scansione di apertura a ogni sessione futura.

La tua memoria pre-esistente è **preservata come una feature**, non segnalata come un avviso. Vedi [ADR-006](https://github.com/alex-lamport/kaora-memory/blob/main/docs/DECISIONS.md) per la policy di installazione brownfield.

> **Il mio `.claude/settings.json` ha già degli hook. `kaora init` li sovrascrive?**

No. `settings.json` viene fuso in modo intelligente: gli hook di kaora vengono aggiunti accanto ai tuoi, i conflitti vengono segnalati. Le altre chiavi JSON restano intatte.

---

## kaora check

Esegui `kaora check` in qualsiasi momento per verificare che la tua memoria operativa non sia driftata dalla struttura canonica.

```
$ kaora check .

ℹ️  INFO:
  [placeholders] BOOTSTRAP marker to fill in docs/IDENTITY.md: <BOOTSTRAP need="builder-identity" sources="..."/>
```

Sei categorie di controllo: struttura (file richiesti), ADR-005 (canonico + direttiva di import), stato ADR (Accepted/Proposed), placeholder (strutturali vs BOOTSTRAP), hook (`.claude/hooks/*.sh` eseguibili), settings (`.claude/settings.json` referenzia gli hook di kaora).

L'exit code è 0 di default; `--strict` promuove i warning a errori (utile in CI). `--json` per output leggibile da una macchina.

---

## Roadmap

v0.1 (attuale) — `kaora init`, `kaora check`, template canonico di 13 file, policy di installazione brownfield, rituale di apertura + chiusura.

v0.2+ — `kaora handoff` (automazione CLI della chiusura di sessione), `kaora dashboard` (UI web per visualizzare la memoria operativa), hook a soglia di contesto per Claude Code, onboarding multi-canale per `IDENTITY.md`.

v0.3+ — server MCP, sync cloud tra dispositivi.

Backlog completo in [`BACKLOG.md`](https://github.com/alex-lamport/kaora-memory/blob/main/BACKLOG.md).

---

## Filosofia

kaora-memory è **metacognizione indotta per agenti AI**: i lati memoria + comportamento costringono l'agente a pianificare prima di agire, monitorare durante l'azione, valutare alla chiusura della sessione e riconoscere lo stato cognitivo del builder. La tesi completa vive in [`docs/PHILOSOPHY.md`](https://github.com/alex-lamport/kaora-memory/blob/main/docs/PHILOSOPHY.md).

---

> *kaora-memory non aggiunge intelligenza all'agente. Aggiunge preparazione.*

---

## Licenza

MIT — vedi [LICENSE](https://github.com/alex-lamport/kaora-memory/blob/main/LICENSE).

Costruito con kaora-memory stessa. Il repo passa il proprio `kaora check`, e ogni ADR in [`docs/DECISIONS.md`](https://github.com/alex-lamport/kaora-memory/blob/main/docs/DECISIONS.md) è stato deciso attraverso gli stessi gate che kaora codifica per gli altri progetti. Vedi [`docs/DOGFOODING_REPORT.md`](https://github.com/alex-lamport/kaora-memory/blob/main/docs/DOGFOODING_REPORT.md) per la storia dell'auto-applicazione.

---

Costruito da [Alexis Rojas](https://x.com/alex_lamports) — parte del workspace/ricerca KAORA su agenti AI, memoria e collaborazione uomo-agente.
