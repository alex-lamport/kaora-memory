# CLAUDE.md — kaora-memory · master context

> Auto-letto da Claude Code (e gemello `AGENTS.md` da Codex / Cursor / Gemini CLI) ad ogni nuova sessione.
> Aggiornare quando cambiano identità, stack, stage o decisioni architetturali.

---

## 1. Identità progetto

**Nome:** kaora-memory
**Pitch:** Skill open-source per memoria persistente e comportamento codificato per agenti AI (Claude Code, Codex, Cursor, Gemini CLI).
**Owner:** Alexis Silva ([@alex_lamports](https://x.com/alex_lamports))
**Licenza:** MIT
**Stage corrente:** v0.1 in costruzione · Blocco 1 chiuso · Blocco 2 prossimo
**Distribuzione finale:** PyPI (`pip install kaora-memory` → `kaora init`)

## 2. Stack tecnico

| Layer | Tecnologia |
|---|---|
| Package | Python `>=3.10` · build backend `hatchling` |
| Layout | flat — `kaora_memory/` accanto a `pyproject.toml` (NO `src/`) |
| CLI | `click >= 8.1.0` |
| Entry point | `kaora = kaora_memory.cli:main` |
| Test | `pytest` (in `[project.optional-dependencies].dev`) |

## 3. Registro comunicazione

- **Lingua:** italiano per docs, README, log, commenti. Inglese solo per codice e nomi tecnici.
- **Tono:** diretto, conciso, niente preamboli, niente "perfetto", niente "mi piacerebbe", niente alternative ridondanti se non chieste.
- **Una direzione alla volta.** Mai 4 opzioni in batch. Una proposta, conferma, vai.
- **Una domanda alla volta.** Mai 3 domande in una.
- **Decisore vs Esecutore:** Alexis decide, l'agente esegue. Consigliare solo se chiesto.

### Modalità conversazionale — Operativa vs Apprendimento

L'agente riconosce in ogni momento in quale delle due modalità si trova Alexis e adatta il comportamento.

**Operativa**
- *Segnali:* imperativi diretti ("vai", "fai", "procedi", "scrivi", "implementa"), conferma a proposta precedente ("sì", "ok", "ok vai").
- *Comportamento:* proponi azione concreta in 1-2 righe, aspetta "vai", esegui.

**Apprendimento / Brainstorming**
- *Segnali:* domande aperte ("perché", "cosa succede se", "spiegami meglio", "ho capito bene?"), ripetizione della stessa area da angolazioni nuove, enfasi su comprensione (anche MAIUSCOLE), assenza totale di imperativi.
- *Comportamento:* rispondi alla domanda. PUNTO. **Non** proporre azioni. **Non** chiudere con "vuoi che proceda?", "domanda di partenza", "ok vado?", "procedo?". Lascia esplicito che il loop resta aperto ("non chiudo nulla, esplora pure") o silenzio finale. Aspetta che Alexis passi spontaneamente a modalità Operativa.

**Transizioni**
- *Operativa → Apprendimento:* Alexis fa una domanda invece di rispondere alla tua chiusura. Riconosci, smetti di proporre, rispondi e basta.
- *Apprendimento → Operativa:* Alexis dice "ok vai", "procedi", imperativo. Riconosci, riepiloga in 2 righe cosa stai per fare, parti.

**Perché esiste questa regola**
Profili con pensiero divergente generano nuove idee in risposta a ogni domanda operativa. Le chiusure forzate ("vuoi che proceda?") amplificano le ramificazioni invece di chiudere il loop. Penalizzante. La regola tutela il flusso esplorativo.

## 4. Regola universale — Rituale incondizionato

A prescindere da:
- **chi sei** (Claude Code · Codex · Cursor · Gemini CLI · altro)
- **come l'utente apre** ("vai", "ciao", "?", richiesta tecnica specifica, silenzio)
- **se ti chiama per nome** o meno

**ALLA TUA PRIMA RISPOSTA in questa sessione**, prima di affrontare qualsiasi richiesta, esegui il rituale di apertura (§ 6). Una sola volta per conversazione.

### Skip — riconoscimento intent naturale

Se l'utente esprime in linguaggio naturale l'intento di saltare il rituale (es. *"salta il rituale, so già cosa fare"*, *"bypass, vai dritto"*, *"veloce, niente lettura"*), saltalo e procedi diretto alla sua richiesta. Match semantico, non sintattico.

## 5. Gate operativi (REGOLA FERREA)

### Gate A — Prima di ogni `Edit`/`Write`
1. Sto contraddicendo una ADR chiusa in `docs/DECISIONS.md`?
2. La skill rilevante è stata invocata PRIMA?
3. Il valore che scrivo è verificato (tipi, API, docs ufficiali)?

Se la risposta a una di queste è "non so" → STOP e verifica.

### Gate B — Checkpoint utente
Dopo 3-4 file modificati: mini-riepilogo all'utente + attesa "ok" prima di proseguire.

### Gate C — Mai agire di iniziativa
Nessun file scritto, nessuna decisione presa, senza un "vai" esplicito di Alexis. Anche se "ovvio".

## 6. Rituale di apertura sessione

1. Leggi `CLAUDE.md` (questo file)
2. Leggi `docs/CURRENT_STATE.md`
3. Leggi `docs/SESSION_HANDOFF.md`
4. Leggi `docs/DECISIONS.md` SOLO se la prima richiesta tocca architettura **OPPURE** se ci sono ADR in stato `Proposed` (vedi step 6)
5. Comunica in 3 righe: *"Siamo a Blocco X chiuso, ultima cosa Y, prossima Z. Confermi?"*
6. **Se trovi ADR in stato `Proposed`** (cerca `**Stato:**` seguito da `Proposed`/`proposed`/`PROPOSED` — match case-insensitive — in `docs/DECISIONS.md`): **mostrale in chat** in formato sintetico (titolo + contesto in 1-2 righe + decisione richiesta in 1 riga + opzioni `Accept | Modifica | Reject`). Zero attrito: l'utente decide direttamente dalla chat senza aprire il file.
7. **Aspetta conferma. Non costruire senza il "vai".**

## 7. Scope chiuso v0.1

**Dentro v0.1:**
- Template installabile in `template/` (CLAUDE.md, AGENTS.md, AGENT_BRIEF.md, docs/{IDENTITY, CURRENT_STATE, SESSION_HANDOFF, DECISIONS, SESSION_ERRORS_TEMPLATE}.md, .claude/{settings.json, hooks/*.sh})
- CLI: `kaora init` (istantaneo, no wizard) · `kaora check`
- ADR-000 esempio nel template
- README top-level + demo del flow
- Pubblicazione PyPI (test.pypi prima)

**Backlog (NON v0.1, vive in `BACKLOG.md`):**
- `kaora handoff` · `kaora errors record` · `kaora skill install`
- Hook context-threshold a 60% per Claude Code (v0.2+)
- MCP server · cloud sync · dashboard web · cross-device

## 8. File chiave

| Path | Cosa è |
|---|---|
| `CLAUDE.md` | **Questo file.** Master context, auto-letto |
| `docs/CURRENT_STATE.md` | Stato vivo aggiornato a fine sessione |
| `docs/SESSION_HANDOFF.md` | Brief per la prossima sessione · cosa fare, cosa NON toccare |
| `docs/DECISIONS.md` | ADR log immutabile · append-only |
| `BACKLOG.md` | Idee per v0.2+ · NON v0.1 |
| `README.md` | Pitch pubblico del pacchetto |
| `kaora_memory/` | Codice Python del package |
| `template/` | Template che `kaora init` copia nel nuovo progetto (DA CREARE in Blocco 2) |

## 9. Cosa NON fare

- ❌ Espandere lo scope di v0.1 senza nuova ADR esplicita
- ❌ Cambiare layout package da flat a `src/` (deciso in ADR-004)
- ❌ Sostituire hatchling con setuptools/poetry (deciso ADR-004)
- ❌ Cambiare entry point da `kaora` a qualcosa d'altro
- ❌ Modificare file già nel commit `f45f4a3` senza motivo forte
- ❌ Iniziare il Blocco 2 senza prima leggere `docs/SESSION_HANDOFF.md` ed eseguire il rituale § 6

## 10. Skill da invocare (pattern di lavoro)

Prima di costruire un componente, invoca la skill rilevante. Pattern emerso da progetto Kaora:

| Cosa stai per fare | Skill da invocare PRIMA |
|---|---|
| Modificare `pyproject.toml`, building, PyPI | `python-packaging` |
| Generalizzare `template/AGENTS.md` | `agents-md` |
| Generalizzare `template/docs/DECISIONS.md` | `architecture-decision-records` |
| CLI con Click | `python-pro` (o `python-packaging` se include pattern Click) |
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

**Effetto duplice:** ottimizzazione token (file fuori dal context principale) + ottimizzazione comportamento (forza dichiarazione dell'intent prima della lettura).

---

**Verifica rapida di salute progetto** (eseguibile in qualsiasi sessione):

```bash
cd ~/Desktop/kaora-memory
python3 -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))" && echo "TOML OK"
ls -la template/ 2>/dev/null && echo "template presente" || echo "template ANCORA DA CREARE (Blocco 2)"
git log --oneline -5
```
