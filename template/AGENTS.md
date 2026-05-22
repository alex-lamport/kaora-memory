# AGENTS.md — {{project_name}}

> File canonico di memoria operativa.
> Auto-letto da Codex CLI · Cursor · Aider · Gemini CLI · OpenAI Agents.
> Claude Code lo carica via import in `CLAUDE.md` (riga `@AGENTS.md`).
> Aggiornare quando cambiano identità, stack, stage o decisioni architetturali.

---

## 1. Identità progetto

**Nome:** {{project_name}}
**Pitch:** {{project_oneliner}}
**Owner:** {{owner_name}} ({{owner_email}})
**Path:** {{project_path}}
**Anno:** {{year}}
**Stage corrente:** <BOOTSTRAP need="stage" sources="docs/CURRENT_STATE.md, git log, README"/>

## 2. Stack tecnico

<BOOTSTRAP need="tech-stack" sources="package.json, pyproject.toml, Cargo.toml, go.mod, Gemfile, composer.json, lock files, build config, README"/>

## 3. Registro comunicazione

- **Lingua:** {{communication_language}} per docs, log, commenti. Inglese per codice e identificatori tecnici.
- **Tono:** {{communication_register}}
- **Una direzione alla volta.** Mai 4 opzioni in batch. Una proposta, conferma, vai.
- **Una domanda alla volta.** Mai 3 domande in una.
- **Decisore vs Esecutore:** {{owner_name}} decide, l'agente esegue. Consigliare solo se chiesto.

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

Nessun file scritto, nessuna decisione presa, senza un "vai" esplicito di {{owner_name}}. Anche se "ovvio".

## 6. Rituale di apertura sessione

1. Leggi `AGENTS.md` (questo file). Claude Code: leggi `CLAUDE.md`, l'import `@AGENTS.md` carica automaticamente questo file.
2. Leggi `docs/CURRENT_STATE.md`
3. Leggi `docs/SESSION_HANDOFF.md`
4. Leggi `docs/DECISIONS.md` SOLO se la prima richiesta tocca architettura **OPPURE** se ci sono ADR in stato `Proposed` (vedi step 6)
5. Comunica in 3 righe: *"Siamo a [stato], ultima cosa [Y], prossima [Z]. Confermi?"*
6. **Se trovi ADR in stato `Proposed`** (cerca `**Stato:**` seguito da `Proposed`/`proposed`/`PROPOSED` — match case-insensitive — in `docs/DECISIONS.md`): **mostrale in chat** in formato sintetico (titolo + contesto in 1-2 righe + decisione richiesta in 1 riga + opzioni `Accept | Modifica | Reject`). Zero attrito: l'utente decide direttamente dalla chat senza aprire il file.
7. **Aspetta conferma. Non costruire senza il "vai".**

## 7. Scope corrente

**Dentro lo scope attivo:**
<BOOTSTRAP need="current-scope" sources="docs/CURRENT_STATE.md, docs/SESSION_HANDOFF.md, recent ADR in docs/DECISIONS.md"/>

**Backlog (NON ora, vive in `BACKLOG.md`):**
<BOOTSTRAP need="backlog-summary" sources="BACKLOG.md"/>

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
<BOOTSTRAP need="project-specific-key-files" sources="src/, lib/, packages/, README, build entry points"/>

## 9. Cosa NON fare

- ❌ Espandere lo scope corrente senza nuova ADR esplicita
- ❌ Riaprire ADR già chiuse senza nuova ADR con `Supersedes: ADR-XXX`
- ❌ Agire di iniziativa — Gate C
- ❌ Saltare il rituale a meno di skip esplicito (§ 4)
- ❌ Toccare file `.env`, `credentials.*`, `.secret.*` (bloccati da hook)
- ❌ Cancellare file `.kaora-bak` senza prima averli letti (memoria pre-install, vedi § 11)
<BOOTSTRAP need="project-specific-do-not" sources="docs/IDENTITY.md anti-pattern, prior session errors, recent commit messages"/>

## 10. Skill / sub-agenti da invocare PRIMA di costruire

Pattern operativo: ogni componente non-triviale richiede skill o sub-agente specializzato caricato **PRIMA** di scrivere codice (Gate A § 5.1).

<BOOTSTRAP need="skill-mapping" sources="package.json scripts, build config, tech stack inferred from § 2, framework conventions"/>

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

Se trovi file `*.kaora-bak` nella root o in `docs/` (es. `AGENTS.md.kaora-bak`, `CLAUDE.md.kaora-bak`), contengono la memoria operativa esistente **prima** di `kaora init`. Procedi così:

1. Leggi il `.kaora-bak`
2. Estrai contenuti tecnici rilevanti: package manager, comandi (test/lint/build), conventions di codice, file-scoped commands, struttura cartelle
3. Proponi un diff per integrarli nella sezione appropriata di questo `AGENTS.md` (§ 2 stack, § 8 file chiave, § 10 skill mapping)
4. **NON duplicare** la memoria operativa kaora (rituale § 4, gate § 5, scope § 7) — quella è già canonica qui
5. Al termine, chiedi a {{owner_name}} se vuole conservare i `.kaora-bak` o eliminarli

## 12. Comportamenti vietati cross-agent

Validi per Claude Code, Codex, Cursor, Aider, Gemini CLI e qualsiasi altro agente in questo repo:

- Niente commit/push autonomi (azione visibile, sempre conferma esplicita)
- Niente modifica `docs/DECISIONS.md` per ADR già `Accepted` (append-only, nuova ADR `Supersedes`)
- Niente skip del rituale a meno di intent esplicito utente
- Niente sovrascrittura di file `.kaora-bak`

---

**Verifica rapida di salute progetto** (eseguibile in qualsiasi sessione):

<BOOTSTRAP need="health-check" sources="primary build/test command, lint command, package manager check, lock file integrity"/>
