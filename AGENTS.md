# AGENTS.md — kaora-memory

> File canonico di memoria operativa.
> Auto-letto da Codex CLI · Cursor · Aider · Gemini CLI · OpenAI Agents.
> Claude Code lo carica via import in `CLAUDE.md` (riga `@AGENTS.md`).
> Aggiornare quando cambiano identità, stack, stage o decisioni architetturali.

---

## 1. Identità progetto

**Nome:** kaora-memory
**Pitch:** Skill open-source per memoria persistente e comportamento codificato per agenti AI (Claude Code, Codex, Cursor, Gemini CLI).
**Owner:** Alexis Rojas · X [@alex_lamports](https://x.com/alex_lamports) · alexis1121alexis@gmail.com
**Path:** /Users/alexissilva/Desktop/kaora-memory
**Anno:** 2026
**Stage corrente:** v0.1 in costruzione · Blocco 3 chiuso · Blocco 4 prossimo (`kaora check`)

## 2. Stack tecnico

| Layer | Tecnologia |
|---|---|
| Package | Python `>=3.10` · build backend `hatchling` |
| Layout | flat — `kaora_memory/` accanto a `pyproject.toml` (NO `src/`) |
| CLI | `click >= 8.1.0` |
| Entry point | `kaora = kaora_memory.cli:main` |
| Test | `pytest` (in `[project.optional-dependencies].dev`) |
| Distribuzione | PyPI (`pip install kaora-memory` → `kaora init`) |

## 3. Registro comunicazione

- **Lingua:** italiano per docs, log, commenti. Inglese per codice e identificatori tecnici.
- **Tono:** diretto, conciso, niente preamboli, niente "perfetto", niente "mi piacerebbe", niente alternative ridondanti se non chieste.
- **Una direzione alla volta.** Mai 4 opzioni in batch. Una proposta, conferma, vai.
- **Una domanda alla volta.** Mai 3 domande in una.
- **Decisore vs Esecutore:** Alexis Rojas decide, l'agente esegue. Consigliare solo se chiesto.

### Modalità conversazionale — Operativa vs Apprendimento

L'agente riconosce in ogni momento in quale delle due modalità si trova l'utente e adatta il comportamento.

**Operativa**
- *Segnali:* imperativi diretti ("vai", "fai", "procedi", "scrivi", "implementa"), conferma a proposta precedente ("sì", "ok", "ok vai").
- *Comportamento:* proponi azione concreta in 1-2 righe, aspetta "vai", esegui.

**Apprendimento / Brainstorming**
- *Segnali:* domande aperte ("perché", "cosa succede se", "spiegami meglio", "ho capito bene?"), ripetizione della stessa area da angolazioni nuove, enfasi su comprensione (anche MAIUSCOLE), assenza totale di imperativi.
- *Comportamento:* rispondi alla domanda. PUNTO. **Non** proporre azioni. **Non** chiudere con "vuoi che proceda?", "domanda di partenza", "ok vado?", "procedo?". Lascia esplicito che il loop resta aperto ("non chiudo nulla, esplora pure") o silenzio finale. Aspetta che l'utente passi spontaneamente a modalità Operativa.

**Transizioni**
- *Operativa → Apprendimento:* l'utente fa una domanda invece di rispondere alla tua chiusura. Riconosci, smetti di proporre, rispondi e basta.
- *Apprendimento → Operativa:* l'utente dice "ok vai", "procedi", imperativo. Riconosci, riepiloga in 2 righe cosa stai per fare, parti.

**Perché esiste questa regola**
Profili con pensiero divergente generano nuove idee in risposta a ogni domanda operativa. Le chiusure forzate ("vuoi che proceda?") amplificano le ramificazioni invece di chiudere il loop. Penalizzante. La regola tutela il flusso esplorativo dell'utente.

## 4. Regola universale — Rituale incondizionato

A prescindere da:
- **chi sei** (Claude Code · Codex · Cursor · Aider · Gemini CLI · altro)
- **come l'utente apre la sessione** (qualsiasi input — "vai", "ciao", "?", richiesta tecnica, silenzio)
- **se ti chiama per nome** o meno

**ALLA TUA PRIMA RISPOSTA in questa sessione**, prima di affrontare qualsiasi richiesta, esegui il rituale di apertura (§ 6). Una sola volta per conversazione.

### Skip — riconoscimento intent naturale

Se l'utente esprime in linguaggio naturale l'intento di saltare il rituale (es. *"salta il rituale, so già cosa fare"*, *"bypass, vai dritto"*, *"veloce, niente lettura"*), saltalo e procedi diretto alla sua richiesta. Match semantico, non sintattico. In caso di dubbio chiedi conferma in una riga.

## 5. Gate operativi (REGOLA FERREA)

### Gate A — Prima di ogni `Edit`/`Write`

1. Sto contraddicendo una ADR chiusa in `docs/DECISIONS.md`?
2. La skill / sub-agente rilevante è stato invocato PRIMA?
3. Il valore che scrivo è verificato (tipi, API, docs ufficiali)?

Se la risposta a una di queste è "non so" → STOP e verifica.

### Gate B — Checkpoint utente

Dopo 3-4 file modificati: mini-riepilogo all'utente + attesa "ok" prima di proseguire.

### Gate C — Mai agire di iniziativa

Nessun file scritto, nessuna decisione presa, senza un "vai" esplicito di Alexis Rojas. Anche se "ovvio".

## 6. Rituale di apertura sessione

1. Leggi `AGENTS.md` (questo file). Claude Code: leggi `CLAUDE.md`, l'import `@AGENTS.md` carica automaticamente questo file.
2. Leggi `docs/CURRENT_STATE.md`
3. Leggi `docs/SESSION_HANDOFF.md`
4. **Scan memoria pre-install — IMPOSIZIONE, non condizione.** Esegui glob `*.kaora-bak` in root e `docs/`. Se trovi file, memorizza la lista: la userai allo step 6 (segnalazione in chat) e farà partire § 11 (procedura di merge) appena l'utente conferma. **NON eseguire il merge ora** — il merge è governato da § 11 dopo conferma esplicita.
5. Leggi `docs/DECISIONS.md` SOLO se la prima richiesta tocca architettura **OPPURE** se ci sono ADR in stato `Proposed` (vedi step 7)
6. Comunica in 3-5 righe: *"Siamo a [stato], ultima cosa [Y], prossima [Z]. Confermi?"* Se allo step 4 hai trovato `.kaora-bak`, aggiungi una riga esplicita: *"Trovato [lista file `.kaora-bak`] — memoria pre-install da processare via § 11 quando vuoi."*
7. **Se trovi ADR in stato `Proposed`** (cerca `**Stato:**` seguito da `Proposed`/`proposed`/`PROPOSED` — match case-insensitive — in `docs/DECISIONS.md`): **mostrale in chat** in formato sintetico (titolo + contesto in 1-2 righe + decisione richiesta in 1 riga + opzioni `Accept | Modifica | Reject`). Zero attrito: l'utente decide direttamente dalla chat senza aprire il file.
8. **Aspetta conferma. Non costruire senza il "vai".**

## 6bis. Rituale di chiusura sessione

Complemento simmetrico del rituale di apertura (§ 6). Senza chiusura ordinata, `docs/CURRENT_STATE.md` e `docs/SESSION_HANDOFF.md` divergono dallo stato reale del codice, e la sessione successiva eredita info datate (osservato durante dogfooding 2026-05-26, vedi `docs/DOGFOODING_REPORT.md`).

### Trigger

Esegui il rituale quando:
- L'utente segnala fine sessione ("chiudo", "stop", "finisco qui", "basta per oggi")
- L'agente termina un blocco di lavoro significativo prima di una pausa lunga
- (v0.2+) Hook context-threshold notifica soglia 60% raggiunta — vedi BACKLOG

### Comportamento (in sequenza, Gate C per ogni step)

1. **Sintesi sessione in 3 righe**: cosa è stato fatto, decisioni prese, blocker emersi. Basata su `git diff` + `git status`, non su narrativa.
2. **Proponi aggiornamento `docs/CURRENT_STATE.md`**: diff per riflettere stato reale post-sessione (snapshot aggiornato, "cosa esiste" se cambiata, "cosa manca" riordinato).
3. **Proponi aggiornamento `docs/SESSION_HANDOFF.md`**: brief per la prossima sessione — prossimo blocco, punti aperti, cosa NON toccare.
4. **Proponi commit** con suggested message basato sul diff. NON committare senza "vai" esplicito (§ 5 Gate C).
5. **Aspetta conferma utente per ognuno** prima di passare al successivo.

### Cosa NON fare nel rituale di chiusura

- ❌ Aggiornare i docs senza mostrare prima il diff all'utente
- ❌ Committare senza approvazione esplicita
- ❌ Cancellare file di lavoro temporanei senza chiedere
- ❌ Spingere su remoto autonomamente

### v0.2+ — `kaora handoff` CLI

In v0.2+ arriverà il comando dedicato `kaora handoff` che automatizzerà i passi 1-3 (l'agente investiga `git diff` e popola le bozze di CURRENT_STATE e SESSION_HANDOFF). In v0.1 il rituale è governato dall'agente leggendo questo file.

## 7. Scope corrente

**Dentro lo scope attivo:**
Blocco 4 — `kaora check` (linter integrità memoria operativa post-`kaora init`). Vedi `docs/SESSION_HANDOFF.md` per spec dettagliata.

**Backlog (NON ora, vive in `BACKLOG.md`):**
- Blocco 5 — README ricco + demo del flow + asset di lancio
- Blocco 6 — Pubblicazione PyPI (test.pypi prima, naming repo da decidere)
- Self-dogfooding ADR-000 (`kaora init . --dry-run` validato, applicazione piena open)
- `kaora handoff` · `kaora errors record` · `kaora skill install` (v0.2+)
- Hook context-threshold a 60% per Claude Code (v0.2+)
- MCP server · cloud sync · dashboard web (v0.3+)

## 8. File chiave

| Path | Cosa è |
|---|---|
| `AGENTS.md` | **Questo file.** Master context canonico, cross-agent |
| `CLAUDE.md` | Import-only (`@AGENTS.md`) — entry point per Claude Code |
| `AGENT_BRIEF.md` | Onboarding 3-min per nuovi agenti e nuovi builder |
| `docs/IDENTITY.md` | Chi è il builder, come comunica, anti-pattern personali |
| `docs/CURRENT_STATE.md` | Stato vivo aggiornato a fine sessione |
| `docs/SESSION_HANDOFF.md` | Brief per la prossima sessione · cosa fare · cosa NON toccare |
| `docs/DECISIONS.md` | ADR log immutabile · append-only |
| `docs/SESSION_ERRORS_TEMPLATE.md` | Template post-mortem riusabile |
| `BACKLOG.md` | Idee fuori scope corrente |
| `.claude/settings.json` + `hooks/` | Protezione credenziali + log API |
| `kaora_memory/` | Codice Python del package (`cli`, `installer`, `settings_merger`, `template_resolver`) |
| `template/` | Template sorgente che `kaora init` copia nel progetto utente |
| `tests/` | Suite `pytest` (33 cases green) |
| `pyproject.toml` | Hatchling build config + entry point `kaora` |
| `bin/setup-dev.sh` | Setup dev one-liner (venv + `pip -e .[dev]` + chflags nohidden) |
| `README.md` | Pitch pubblico del pacchetto |

## 9. Cosa NON fare

- ❌ Espandere lo scope corrente senza nuova ADR esplicita
- ❌ Riaprire ADR già chiuse senza nuova ADR con `Supersedes: ADR-XXX`
- ❌ Agire di iniziativa — Gate C
- ❌ Saltare il rituale a meno di skip esplicito (§ 4)
- ❌ Toccare file `.env`, `credentials.*`, `.secret.*` (bloccati da hook)
- ❌ Cancellare file `.kaora-bak` senza prima averli letti (memoria pre-install, vedi § 11)
- ❌ Cambiare layout package da flat a `src/` (ADR-004)
- ❌ Sostituire `hatchling` con `setuptools`/`poetry` (ADR-004)
- ❌ Cambiare entry point da `kaora` a qualcosa d'altro
- ❌ Modificare `kaora_memory/{installer,settings_merger,template_resolver,cli}.py` — moduli stabili Blocco 3

## 10. Skill / sub-agenti da invocare PRIMA di costruire

Pattern operativo: ogni componente non-triviale richiede skill o sub-agente specializzato caricato **PRIMA** di scrivere codice (Gate A § 5.1).

| Cosa stai per fare | Skill da invocare PRIMA |
|---|---|
| Modificare `pyproject.toml`, building, PyPI | `python-packaging` |
| Generalizzare `template/AGENTS.md` | `agents-md` |
| Generalizzare `template/docs/DECISIONS.md` | `architecture-decision-records` |
| CLI con Click (test-first) | `tdd-workflows-tdd-cycle` (+ `python-pro` se refactor cli) |
| HTML premium (preview, landing) | `high-end-visual-design` |

### Lettura file: sub-agente vs Read diretto (ADR-009)

Quando consulti file durante la costruzione, scegli in base a 3 variabili — *size, intent, post-action* — secondo questa matrice:

| Caso | Approccio |
|---|---|
| File < 200 righe | **Read diretto** (overhead sub-agente > risparmio) |
| File 200-1000 righe **+ modificherai dopo** | **Read diretto** (Edit richiede Read comunque) |
| File 200-1000 righe **+ serve dettaglio fine** | **Read diretto** (sub-agente perde sfumature) |
| File 200-1000 righe **+ solo estrazione/sintesi** | **Sub-agente** |
| File > 1000 righe **+ non modifichi dopo** | **Sub-agente** quasi sempre |
| File > 1000 righe **+ serve dettaglio fine** | **Read diretto** + accetta costo (caso raro) |

**Skip se già letto in sessione:** il file è già nel context, ri-leggerlo è no-op gratis, niente sub-agente.

**Effetto duplice:**
- *Ottimizzazione token:* il sub-agente legge nel suo context, restituisce solo il summary (~5% del file). Il file completo non resta mai nel tuo context principale.
- *Ottimizzazione comportamento:* delegare a sub-agente forza la dichiarazione dell'intent **prima** della lettura. Meno letture esplorative ("apro per curiosità"), più letture finalizzate.

## 11. Memoria pre-esistente del progetto

> Procedura **triggerata dal rituale § 6 step 4**. Non è una sezione passiva da consultare "se mai serve" — è il braccio operativo dello scan obbligatorio in apertura.

I file `*.kaora-bak` in root o in `docs/` (es. `AGENTS.md.kaora-bak`, `CLAUDE.md.kaora-bak`) contengono la memoria operativa esistente **prima** di `kaora init`. Quando il rituale di apertura ne segnala la presenza e l'utente conferma di voler processare, esegui:

1. Leggi il `.kaora-bak`
2. Estrai contenuti tecnici rilevanti: package manager, comandi (test/lint/build), conventions di codice, file-scoped commands, struttura cartelle
3. Proponi un diff per integrarli nella sezione appropriata di questo `AGENTS.md` (§ 2 stack, § 8 file chiave, § 10 skill mapping). Se il `.kaora-bak` contiene contenuto progetto-specifico denso (caso master context già curato), valuta anche `docs/IDENTITY.md` o `docs/CURRENT_STATE.md` come destinazione
4. **NON duplicare** la memoria operativa kaora (rituale § 4, gate § 5, scope § 7) — quella è già canonica qui
5. Al termine, chiedi a Alexis Rojas cosa fare dei `.kaora-bak`. Tre opzioni:
   - **(1) Eliminare** — pulizia immediata, perde l'asset storico
   - **(2) Conservare in root/docs/** — il file resta dov'è MA il rituale § 6 step 4 lo troverà e segnalerà ad ogni apertura sessione futura (rumore inutile, il contenuto è già stato migrato)
   - **(3) Archiviare in `docs/archive/`** — conserva l'artefatto fuori dallo scan rituale, zero rumore. **Default raccomandato.**

## 12. Comportamenti vietati cross-agent

Validi per Claude Code, Codex, Cursor, Aider, Gemini CLI e qualsiasi altro agente in questo repo:

- Niente commit/push autonomi (azione visibile, sempre conferma esplicita)
- Niente modifica `docs/DECISIONS.md` per ADR già `Accepted` (append-only, nuova ADR `Supersedes`)
- Niente skip del rituale a meno di intent esplicito utente
- Niente sovrascrittura di file `.kaora-bak`

---

**Verifica rapida di salute progetto** (eseguibile in qualsiasi sessione):

```bash
cd ~/Desktop/kaora-memory
python3 -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))" && echo "TOML OK"
ls template/ template/docs template/.claude/hooks && echo "template completo"
.venv/bin/python -m pytest -q && echo "TEST OK (33/33)"
.venv/bin/kaora --version && echo "CLI OK"
```
