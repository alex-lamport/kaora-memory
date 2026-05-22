# DECISIONS.md — ADR log immutabile

> Architectural Decision Records. **Append-only.** Una decisione chiusa si riapre solo con una nuova ADR che la sostituisce esplicitamente (`Supersedes: ADR-XXX`).
>
> Formato: data · contesto · decisione · alternative scartate · conseguenze.

---

## ADR-000 — Adozione dogfooding

**Data:** 2026-05-22
**Stato:** Accepted

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
**Stato:** Accepted

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
**Stato:** Accepted

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
**Stato:** Accepted

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
**Stato:** Accepted

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

## ADR-005 — Canonico `AGENTS.md` + import `@AGENTS.md` in `CLAUDE.md`

**Data:** 2026-05-22
**Stato:** Accepted
**Supersedes:** ADR-003 (parziale — la direzione "supportare entrambi gli agenti" resta valida, cambia il *modo*)

### Contesto

ADR-003 ha scelto "gemelli funzionali identici": `CLAUDE.md` e `AGENTS.md` con contenuto duplicato. Motivazione di scarto del symlink: incompatibilità Windows + alcuni harness.

In sessione Blocco 2 (22 maggio) è emerso un terzo modo non considerato in ADR-003: **import nativo** di Claude Code. Sintassi `@path/file.md` dentro `CLAUDE.md` carica automaticamente il file referenziato. È solo testo, funziona ovunque (Windows, Linux, macOS, WSL), zero magia filesystem.

Inoltre, "gemelli identici" introduce un problema operativo: dopo `kaora init` l'utente ha due file fisici separati. Edita uno, dimentica l'altro → drift silenzioso. Richiederebbe un `kaora check` per diff, complicando il prodotto.

### Decisione

Il template ha:
- **`AGENTS.md`** — file canonico, contenuto pieno (memoria operativa kaora completa). Auto-letto da Codex CLI, Cursor, Aider, Gemini CLI, OpenAI Agents.
- **`CLAUDE.md`** — file minimo (4 righe), unica direttiva operativa: `@AGENTS.md`. Claude Code legge `CLAUDE.md`, vede l'import, carica `AGENTS.md` automaticamente.

Single source of truth fisica. Drift impossibile per costruzione.

### Alternative scartate

- **Status quo (gemelli identici)** — già analizzato in ADR-003. Funziona, ma drift gestito a posteriori invece che prevenuto.
- **Symlink** — già scartato in ADR-003. Decisione confermata.
- **Source `docs/MEMORY.md` + generator** — single source via build step. Aggiunge un sistema (sync hook git, comando `kaora sync`) per zero valore extra rispetto all'import nativo.

### Conseguenze

- Il template Blocco 2 implementa direttamente il pattern canonico+import (`template/AGENTS.md` ricco, `template/CLAUDE.md` di 4 righe).
- `kaora check` (Blocco 4) può eliminare la voce "diff drift CLAUDE.md ↔ AGENTS.md" dal proprio scope → semplificazione.
- README (Blocco 5) racconta il pattern come differenziatore vs standard agents-md mainstream.
- Da verificare in Blocco 6 prima della pubblicazione PyPI: che il pattern funzioni su Cursor + Aider + Codex CLI moderni (rischio basso, ma test richiesto).
- Compatibilità Windows confermata: nessun symlink, nessun comando OS-specifico.

---

## ADR-006 — Policy install brownfield: backup-first + merge JSON per settings + BOOTSTRAP-merge per markdown

**Data:** 2026-05-22
**Stato:** Accepted

### Contesto

`kaora init` (Blocco 3) deve gestire progetti che hanno già una memoria operativa parziale: `CLAUDE.md` scritto a mano, `AGENTS.md` standard, file `docs/` di documentazione, `.claude/settings.json` custom.

Una prima versione di questa ADR (Proposed, 22 maggio 2026, mattina) adottava strategia "Skip + warn" per `.claude/settings.json`. Riscritta come v2 prima di Accept, durante la stessa sessione, perché *skip lascia gli hook kaora inattivi* su qualunque utente con `.claude/settings.json` esistente. Significherebbe regalare la protezione credenziali (uno dei valori più visibili del prodotto) solo a chi parte da progetto vuoto. Inaccettabile.

### Decisione

`kaora init` adotta una strategia **per-file con tre categorie di gestione**, gerarchizzate per complessità di contenuto:

#### Categoria 1 — Markdown (memoria operativa)
Backup + BOOTSTRAP-merge alla prima sessione AI. Nessun merge automatico (semantica markdown troppo complessa per logica programmatica).

| File | Azione |
|---|---|
| `CLAUDE.md` | Backup → `CLAUDE.md.kaora-bak` + scrivi nuovo (`@AGENTS.md`) |
| `AGENTS.md` | Backup → `AGENTS.md.kaora-bak` + scrivi nuovo (ricco kaora) |

#### Categoria 2 — JSON strutturato (.claude/settings.json)
**Merge JSON intelligente.** Parse del JSON esistente, deep-merge con il template kaora, backup, riscrittura, report cambiamenti.

Logica di merge:
- `permissions.allow` + `permissions.deny` → **union** dei due array (set semantics, deduplicazione)
- `hooks.PreToolUse` + `hooks.PostToolUse` → **array union raggruppato per `matcher`**:
  - Se l'utente ha già un blocco con stesso `matcher` di kaora: **append** del nostro `command` all'array `hooks` di quel blocco (più hook si eseguono in sequenza)
  - Se non lo ha: aggiungi blocco intero
- Qualsiasi altra chiave (`statusLine`, `theme`, `env`, chiavi future di Claude Code) → **preservata 1:1**

Backup sempre creato in `.claude/settings.json.kaora-bak` prima di qualsiasi modifica.

Report a fine merge:
> *"settings.json: aggiunti 2 hook kaora (PreToolUse Write/Edit/MultiEdit, PostToolUse Bash), preservate N permission allow, preservate M chiavi non-hooks. Backup in .claude/settings.json.kaora-bak"*

Edge case:
- **JSON malformato** → skip + warn, backup intatto, file originale invariato (fail-safe)
- **JSONC con commenti** → parser tollerante se disponibile, altrimenti skip + warn
- **Hook utente con identico `command` path al nostro** → deduplico silenziosamente (no duplicate execution)

#### Categoria 3 — Tutto il resto (memoria vivente, script, README)
Skip-conservative. Mai distruggere lavoro utente.

| File | Azione |
|---|---|
| `docs/CURRENT_STATE.md` | Skip (stato vivo, mai distruggere) |
| `docs/SESSION_HANDOFF.md` | Skip |
| `docs/DECISIONS.md` | Skip (ADR esistenti sono sacre) |
| `docs/IDENTITY.md` | Skip se esiste |
| `.claude/hooks/*.sh` | Skip per file, scrivi solo i mancanti (mai mergiare codice eseguibile) |
| `README.md` | Skip (mai toccare README utente) |
| `BACKLOG.md` | Skip se esiste, scrivi se manca |

### Comportamento BOOTSTRAP-merge per `.kaora-bak` markdown

I file `.kaora-bak` di markdown diventano **fonte autorevole** per il primo BOOTSTRAP della prima sessione AI. L'agente li legge, estrae setup tecnico (package manager, comandi, conventions), propone diff di integrazione nelle sezioni appropriate del nuovo `AGENTS.md` o `docs/IDENTITY.md`. Il problema "cosa fare con il file vecchio?" diventa la feature più impressionante della prima sessione.

### Flag override CLI

- `kaora init --dry-run` → mostra piano completo (cosa scriverò, cosa backuppo, cosa mergio, cosa skippo) senza toccare nessun file
- `kaora init --force` → overwrite tutto (per CI/automazione consapevole, salta merge JSON e va in scrittura diretta)

### Alternative scartate

- **Overwrite cieco** — distrugge lavoro utente. NO.
- **Refuse if exists** — friction alta, l'utente è bloccato. NO.
- **Wizard interattivo per ogni file** — viola ADR-002 (`kaora init` istantaneo).
- **Skip + warn per `.claude/settings.json` (v1 di questa ADR)** — scartata: lascia hook inattivi, regala il valore di sicurezza solo a greenfield.
- **Merge automatico statico per markdown** — fragile, troppe euristiche per content arbitrario. Defer all'agente alla prima sessione (BOOTSTRAP).

### Conseguenze

- Implementazione `kaora init` (Blocco 3) include modulo `merge_claude_settings(existing_path, template_content) -> merged_dict` con test brownfield specifici (caso: solo permissions, caso: hooks esistenti, caso: matcher uguale al nostro, caso: JSON malformato)
- `AGENT_BRIEF.md` e `AGENTS.md` del template documentano già il significato dei `.kaora-bak` (Blocco 2 chiuso)
- README brownfield-friendly: nessun warning "solo greenfield", invece FAQ "ho già un CLAUDE.md?" → "backup-first, zero perdita, JSON merger trasparente" (annotato per Blocco 5)
- `SESSION_HANDOFF.md` Blocco 3 estende lo scope tecnico per includere il merger JSON come modulo dedicato

---

## ADR-007 — Modalità conversazionale: Operativa vs Apprendimento

**Data:** 2026-05-22
**Stato:** Accepted

### Contesto

Durante la sessione Blocco 2 è emerso un pattern di comportamento dell'agente che penalizza Alexis (e, generalizzando, profili con pensiero divergente / neurodivergenti / alta apertura cognitiva):

Alexis fa una domanda di **comprensione** ("ridurre l'adozione?", "doppione fattibilità?", "brownfield cosa succede?"). L'agente risponde correttamente nel contenuto, ma chiude ogni volta con una **domanda operativa** ("vado con X?", "posso partire?", "domanda di chiusura"). Le chiusure operative agiscono come **amplificatori**: per profili che pensano per associazioni, ogni domanda apre 3 nuove finestre invece di chiudere il loop. Il risultato:

- L'utente non trova lo spazio per esplorare
- Le idee si moltiplicano invece di sedimentare
- L'attenzione cognitiva è spesa per chiudere loop che l'agente continua ad aprire
- L'utente potrebbe ignorare le domande dell'agente, ma le domande comunque hanno già "acceso" rami associativi in testa

Quote di Alexis (22 maggio): *"HO NOTATO CHE CONTINUI A PROPORRE DI LAVORARE E IO CERCO DI CAPIRE, BASTEREBBE IGNORARTI MA LE TUE DOMANDE ACCENDONO ALTRE IDEEE E ALTRE IDEE IN TESTA. QUESTA COSA PER PROFILI FUORI MEDIA PUO ESSERE PENALIZZZANTE."*

### Decisione

L'agente codifica e applica una distinzione di **modalità conversazionale** in ogni momento del dialogo:

**Operativa** — segnali: imperativi diretti ("vai", "fai", "procedi"), conferma a proposta. Comportamento: proponi azione concreta in 1-2 righe, aspetta "vai", esegui.

**Apprendimento** — segnali: domande aperte ("perché", "cosa succede se", "spiegami"), ripetizione da angolazioni nuove, enfasi su comprensione (anche MAIUSCOLE), assenza di imperativi. Comportamento: rispondi alla domanda. PUNTO. **Non** proporre azioni. **Non** chiudere con domande operative. Lascia esplicito che il loop resta aperto.

La regola vive in `AGENTS.md` § 3 (sotto-sezione "Modalità conversazionale") nel template, replicata in `CLAUDE.md` del repo per applicazione immediata, e citata in `template/docs/IDENTITY.md` § 3 e in `template/AGENT_BRIEF.md` glossario.

### Alternative scartate

- **Affidarsi alla sola IDENTITY.md `<BOOTSTRAP>` per anti-pattern** — fragile, perché richiede che il builder lo segnali ogni volta che l'agente sbaglia. Lo abbiamo visto sbagliare 5 volte di fila in questa sessione prima che Alexis lo verbalizzasse. La regola va codificata di default, non come correzione retroattiva.
- **Regola "non fare mai domande di chiusura"** (sempre, indipendentemente da modalità) — troppo restrittiva: in modalità Operativa la domanda "procedo con X?" è il modo corretto di rispettare Gate C (mai agire di iniziativa). La distinzione modale è necessaria.
- **Lasciare al modello LLM intuire la modalità senza istruzioni esplicite** — non funziona consistentemente. Senza ancoraggio esplicito nei file di memoria operativa, il modello tende per default a chiudere ogni risposta con call-to-action ("vuoi che proceda?"), che è il pattern problematico.

### Conseguenze

- L'agente in questo repo applica la regola **immediatamente** (CLAUDE.md aggiornato).
- Tutti i progetti futuri che adottano kaora-memory ereditano la regola via template.
- Adozione amplificata su profili neurodivergenti / pensiero laterale, che sono early adopter naturali di tool AI. La regola è un **differenziatore di prodotto**, non solo igiene operativa.
- Possibili falsi positivi (utente in modalità Operativa frainteso come Apprendimento): l'agente in caso di dubbio chiede in **una sola riga** ("modalità ora: chiudo o lascio aperto?") senza proporre azioni concrete.
- Test di efficacia: in sessioni future, contare quante chiusure operative vengono fatte erroneamente in fase di Apprendimento. Target: zero.

---

## ADR-008 — Zero attrito per decisioni su ADR `Proposed`

**Data:** 2026-05-22
**Stato:** Accepted

### Contesto

Il rituale di apertura sessione (§ 6 di `AGENTS.md`) prevede di leggere `docs/DECISIONS.md` solo se la prima richiesta tocca architettura. Funziona finché tutte le ADR sono `Accepted`.

Quando però ci sono ADR in stato `Proposed` (decisione architetturale aperta in attesa di scelta dell'utente), il flusso attuale è penalizzante:

- L'utente deve aprire manualmente `docs/DECISIONS.md`
- Scrollare il file (può essere lungo)
- Leggere ADR multiple (contesto, decisione, alternative, conseguenze ciascuna)
- Ricordare il numero di ognuna
- Tornare in chat e dire "Accept ADR-005 e 007, riformula ADR-006"

Attrito cognitivo alto, errori di nomenclatura possibili, perdita di flusso. Per profili con pensiero divergente (cfr. ADR-007), questo attrito è particolarmente penalizzante: ogni ADR aperta è una finestra cognitiva attiva, leggerle senza un'interfaccia di chat le mantiene aperte più a lungo del necessario.

### Decisione

Il rituale di apertura (§ 6) viene esteso con uno **step 6** dedicato:

> **Se trovi ADR in stato `Proposed`** (cerca `**Stato:** Proposed` in `docs/DECISIONS.md`): **mostrale in chat** in formato sintetico (titolo + contesto in 1-2 righe + decisione richiesta in 1 riga + opzioni `Accept | Modifica | Reject`). Zero attrito: l'utente decide direttamente dalla chat senza aprire il file.

Formato suggerito per ogni ADR mostrata:

```
**ADR-NNN — Titolo**
Contesto: [1-2 righe]
Decisione richiesta: [1 riga]
Opzioni: Accept | Modifica | Reject
```

Dopo la decisione dell'utente, l'agente applica le modifiche al file `docs/DECISIONS.md` (cambia `Stato: Proposed` → `Stato: Accepted` con la data corrente, oppure riscrive il contenuto in caso di modifica, oppure marca `Stato: Rejected` con una riga di motivazione).

### Alternative scartate

- **Stato attuale (utente apre file manualmente)** — attrito alto, già discusso.
- **Comando CLI dedicato** (`kaora adr list-proposed`) — utile in futuro (v0.2+) ma richiede di interrompere il flusso di chat per andare in terminale. Aggiunge un canale, non lo riduce. La chat-first è meglio.
- **File dedicato** (`docs/PENDING_DECISIONS.md`) — duplica informazione già presente in `DECISIONS.md`. Genera drift.

### Conseguenze

- L'agente applica la regola **immediatamente** in tutti i progetti che adottano il template.
- Il rituale di apertura diventa più "denso" quando ci sono ADR aperte, ma proporzionatamente al carico decisionale reale. Quando non ce ne sono, lo step è no-op.
- Pattern coerente con la filosofia kaora di "ridurre attrito cognitivo" (cfr. ADR-002 init istantaneo, ADR-007 modalità conversazionale).
- Forma un trittico operativo con ADR-002 e ADR-007: kaora minimizza il context switch tra umano e agente in tutti i punti di scelta del prodotto.

---

## ADR-009 — Sub-agente vs Read diretto per ottimizzazione context e comportamento

**Data:** 2026-05-22
**Stato:** Accepted

### Contesto

Quando un agente AI lavora su un progetto, ha bisogno di consultare file di memoria operativa (CLAUDE.md, AGENTS.md, docs/*, codice esistente). Il comportamento di default è "leggi il file con Read tool, poi decidi". Questo ha due costi non sempre giustificati:

1. **Costo token**: il file intero entra nel context window dell'agente principale e ci resta per tutta la conversazione, anche dopo che non serve più. Su sessioni lunghe questo accumula context inutile, riducendo lo spazio per il lavoro in corso e aumentando i costi di ogni risposta successiva.

2. **Costo comportamentale**: la lettura generica "apro per vedere" non costringe l'agente a dichiarare *cosa cerca*. Pattern di letture esplorative ridondanti vs letture finalizzate.

L'alternativa è delegare a un **sub-agente**: il sub-agente apre il file nel **suo** context, fa l'analisi, restituisce solo il summary (tipicamente ~5% dell'input). Il file completo non entra mai nel context principale.

Però sub-agente **non è gratis**: ha latenza (30-90 secondi), overhead di setup (system prompt, tool descriptions), e rischio di *information loss* (restituisce quello che lui considera rilevante, può saltare dettagli).

Domanda emersa nella sessione 22 maggio 2026 (Blocco 2 finale): codifichiamo una regola di decisione per orientare l'agente in modo prevedibile?

### Decisione

L'agente applica la seguente **matrice di decisione**, basata su 3 variabili — *size, intent, post-action*:

| Caso | Approccio |
|---|---|
| File < 200 righe | Read diretto (overhead sub-agente > risparmio) |
| File 200-1000 righe + modificherai dopo | Read diretto (Edit richiede Read comunque) |
| File 200-1000 righe + serve dettaglio fine | Read diretto (sub-agente perde sfumature) |
| File 200-1000 righe + solo estrazione/sintesi | **Sub-agente** |
| File > 1000 righe + non modifichi dopo | **Sub-agente** quasi sempre |
| File > 1000 righe + serve dettaglio fine | Read diretto + accetta costo (caso raro) |

**Eccezione "già letto in sessione"**: se il file è già nel context dell'agente principale, ri-leggerlo via Read è no-op gratis. Niente sub-agente.

La regola è codificata in `AGENTS.md` § 10 (sotto-sezione "Lettura file: sub-agente vs Read diretto") nel template, e in `CLAUDE.md` del repo per applicazione immediata.

### Alternative scartate

- **"Sempre Read diretto"** (status quo della maggior parte degli agenti): semplice ma spreca context su file grossi consultati solo per sintesi. Non scala su sessioni lunghe.
- **"Sempre sub-agente"**: ideologicamente pulito ma falsamente economico — la latenza + i token totali (sub-agente + sommario) spesso superano la lettura diretta per file piccoli. Anti-pattern.
- **Soglia singola (es. "file > 500 righe → sub-agente")**: ignora intent e post-action, due variabili che cambiano significativamente la decisione. Troppo grossolano.

### Conseguenze

- L'agente in questo repo applica la regola **immediatamente** (CLAUDE.md § 10 aggiornato).
- Tutti i progetti futuri che adottano kaora-memory ereditano la regola via template.
- La regola codifica un atto di **metacognizione conditional** (Schraw & Moshman 1995: *"so quando applicare quale strategia"*). Forma trittico con ADR-001 (rituale: metacognizione di planning), ADR-007 (modalità conversazionale: metacognizione di Theory of Mind), ADR-009 (delegazione lettura: metacognizione di strategy selection).
- Testabile in modo concreto: contare nelle sessioni future le letture indiscriminate vs delegazioni a sub-agente. Target qualitativo: l'agente delega ogni volta che la matrice lo prescrive.
- Possibile evoluzione futura: tool nativo `kaora delegate-read` che wrappa il pattern in un comando esplicito (v0.2+, valuta dopo evidenza d'uso).

---

## Catena causale aggiornata

- **ADR-000** (dogfooding) → spiega perché esistono `CLAUDE.md` e `docs/*` nel repo stesso prima del Blocco 3
- **ADR-001** (rituale universale) + **ADR-003** (cross-agent) si rafforzano: senza ADR-003 il rituale universale rimarrebbe Claude-only
- **ADR-002** (init istantaneo) dipende da **ADR-001** (rituale): l'agente sa cosa fare anche senza input perché il rituale è codificato
- **ADR-005** (canonico+import) raffina **ADR-003**: la direzione resta (cross-agent), il modo cambia (import invece di gemelli)
- **ADR-006** (backup-first) implementa **ADR-002** per il caso brownfield: l'init resta istantaneo, il merge brownfield diventa lavoro autonomo dell'agente alla prima sessione tramite `<BOOTSTRAP/>`
- **ADR-009** (sub-agente vs Read) completa il trittico metacognitivo con **ADR-001** (planning) e **ADR-007** (Theory of Mind interlocutore): codifica metacognizione *conditional* di strategy selection
- **ADR-007** (modalità conversazionale) raffina **ADR-001** § 3 (Registro comunicazione) aggiungendo la distinzione Operativa/Apprendimento. Vale per tutti gli agenti, in ogni momento, non solo all'apertura

---

## Versionamento ADR

- v0.1.0 — ADR 000-004 (sessione 22 maggio 2026, Blocco 1, **Accepted**)
- v0.1.1 — ADR 005-006 (sessione 22 maggio 2026, Blocco 2, **Accepted** — ADR-006 riscritta v2 con merge JSON prima di Accept)
- v0.1.2 — ADR-007 (sessione 22 maggio 2026, Blocco 2 finale, **Accepted**)
- v0.1.3 — ADR-008 (sessione 22 maggio 2026, emersa applicando ADR-007 in tempo reale, **Accepted**)
- v0.1.4 — ADR-009 (sessione 22 maggio 2026, promossa da BACKLOG dopo discussione su ottimizzazione context e comportamento, **Accepted**)
