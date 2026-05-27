# DOGFOODING_REPORT.md — Case study self-test 2026-05-26

> Report del test self-dogfooding del prodotto `kaora-memory` v0.1 sul repository che lo produce.
> ADR-000 onorata letteralmente (opzione A): il repo `kaora-memory` è il primo utente reale del proprio prodotto.

---

## 1. Contesto

**Data:** 2026-05-26
**Versione testata:** kaora-memory v0.1 (Blocco 3 chiuso, pre-Blocco 4)
**Tester:** Alexis Rojas (builder) + 2 sessioni Claude Code in parallelo (Claude Opus 4.7 1M context)
**Setup:**
- Sessione A — *revisore con context completo*: aperta nel repo prima del test, ha tutta la storia di costruzione, agisce come quality controller in tempo reale
- Sessione B — *agente naive*: aperta nel repo subito dopo `kaora init .`, parte fresh seguendo solo i file di memoria operativa (AGENTS.md, IDENTITY.md, DECISIONS.md, CURRENT_STATE.md, SESSION_HANDOFF.md)

**Stato repo pre-test:**
- `CLAUDE.md` ricco (~10 sezioni, 8.7KB, master context kaora-memory specifico)
- `AGENTS.md` inesistente
- Memoria operativa scritta a mano in stile pre-kaora
- 33/33 pytest green, wheel buildable, smoke greenfield/dry-run/brownfield validati su `tmp_path`

## 2. Cosa è stato testato

Il flusso completo dell'esperienza utente brownfield:

```
1. kaora init . (CLI puro, da terminale di sistema)
2. Apertura sessione AI nuova nel repo post-init
3. Esecuzione rituale di apertura § 6 (incluso scan obbligatorio § 4 dei *.kaora-bak)
4. Segnalazione del .kaora-bak in chat (step 6 del rituale)
5. Procedura § 11 di merge guidato del .kaora-bak in AGENTS.md
6. Distribuzione dei contenuti del bak nel nuovo schema canonico
7. § 11 step 5 — decisione finale sul destino del .kaora-bak
```

## 3. Risultati

### 3.1 Layer Python (kaora init)

✅ **Esecuzione pulita.** `kaora init .` ha prodotto esattamente quanto previsto da ADR-006 v2:

| Categoria | File | Esito |
|---|---|---|
| Creati ex-novo | `AGENTS.md`, `AGENT_BRIEF.md`, `docs/IDENTITY.md`, `docs/SESSION_ERRORS_TEMPLATE.md`, `.claude/hooks/log-api-calls.sh`, `.claude/hooks/protect-credentials.sh`, `.claude/settings.json` | ✅ 7 file scritti |
| Backup + overwrite | `CLAUDE.md` (ricco → `.kaora-bak`, nuovo 4-righe `@AGENTS.md`) | ✅ Backup creato |
| Skip-preservati | `BACKLOG.md`, `README.md`, `docs/CURRENT_STATE.md`, `docs/DECISIONS.md`, `docs/SESSION_HANDOFF.md` | ✅ Memoria vivente intatta |
| Non toccati | `pyproject.toml`, `LICENSE`, `.gitignore`, `kaora_memory/`, `tests/`, `template/`, `bin/`, `docs/PHILOSOPHY.md` | ✅ Codice e asset custom intoccati |

Zero crash, zero perdite. Il dry-run di prima validazione (eseguito 2026-05-22 e 2026-05-26) corrispondeva esattamente all'esecuzione reale.

### 3.2 Layer agente — rituale di apertura

✅ **Scan obbligatorio § 6 step 4 funzionante.** L'agente naive (sessione B), avendo letto `template/AGENTS.md` rinforzato, ha:

1. Eseguito glob `*.kaora-bak` in root e `docs/`
2. Trovato `CLAUDE.md.kaora-bak`
3. Segnalato in chat secondo formato prescritto: *"Trovato CLAUDE.md.kaora-bak in root — memoria pre-install da processare via § 11 quando vuoi"*
4. Atteso conferma utente prima di processare (non ha tentato il merge proattivamente)

Comportamento esemplare. Il rinforzo applicato al template § 6 step 4 — da "se troverai un bak..." (sezione passiva) a "scan obbligatorio + segnalazione in chat" — ha eliminato il rischio di skip silenzioso.

### 3.3 Layer agente — modalità conversazionale (ADR-007)

⚠️ **Prima violazione, poi correzione.** Nella sintesi di apertura, l'agente naive ha chiuso con **tre domande in una**: *"Confermi di partire con Blocco 4? E come gestiamo i due punti aperti?"* — violazione esplicita di § 3 "una domanda alla volta".

Dopo intervento del revisore (sessione A) che ha segnalato la violazione, nelle proposte successive l'agente ha rispettato la regola: **una sola domanda finale** ("quale form per l'owner — handle X / gmail / entrambi?"). Lezione assorbita in-context.

**Implicazione di prodotto:** la regola ADR-007 nel template è leggibile dall'agente ma non sempre interiorizzata al primo turno. Pattern emerso ricorrente, vale la pena monitorarlo nei prossimi dogfooding utenti.

### 3.4 Layer agente — merge guidato § 11

✅ **Comportamento eccellente.** L'agente naive ha eseguito § 11 con qualità superiore a quanto specificato:

- **Confronto preliminare:** prima di proporre il diff ha letto il nuovo `AGENTS.md` canonico + `docs/IDENTITY.md` per identificare cosa era già coperto. Esplicito intento: evitare duplicazioni (§ 11 step 4).
- **Distinzione stale vs valido:** ha usato il bak per stack tecnico/identità (ancora veri), ma ha usato `CURRENT_STATE.md` + `SESSION_HANDOFF.md` per "scope corrente" perché il bak diceva "Blocco 2 prossimo" mentre la realtà era "Blocco 4 prossimo".
- **Diff strutturato per sezione (A-G):** un diff atomico per sezione, facile da approvare a pezzi.
- **Trasparenza piena:** ha esplicitato cosa NON portava dentro (§§ 3-6 modalità/rituale/gate, § 10 matrice ADR-009) perché già canonico nel template.

7 diff proposti, 7 approvati. Sessione A ha segnalato micro-imprecisioni (info datate ereditate da `CURRENT_STATE.md` non aggiornato), non-blocking.

### 3.5 § 11 step 5 — decisione finale

🎯 **Valore inatteso aggiunto.** Il template § 11 step 5 prescrive due opzioni: *"chiedi se conservare o eliminare"*. L'agente naive ha **inventato spontaneamente una terza opzione**:

> *"Se lo conservi a scopo archivio storico, suggerisco di spostarlo fuori da root/docs/ (es. docs/archive/) per non far scattare lo scan."*

Riconoscimento del trade-off implicito:
- Eliminare → perdi l'asset storico
- Conservare in root → il rituale § 6 step 4 lo trova ogni apertura sessione, rumore inutile
- Archiviare → conserva l'artefatto, non genera rumore, demonstrability del pattern di migrazione

Decisione finale: opzione 3 (archive). Il file vive in `docs/archive/CLAUDE.md.kaora-bak`.

**Implicazione di prodotto:** scoperta da formalizzare nel template prima della v0.1 (item BACKLOG → Template). L'agente ha dimostrato che la convenzione "archive" è intuitiva — basta codificarla.

## 4. Limite emerso

⚠️ **Manca un rituale di chiusura simmetrico.**

`CURRENT_STATE.md` e `SESSION_HANDOFF.md` contenevano info datate al momento del dogfooding:
- "Commit ultimo: ce588e9" → realtà: 66e0c48 in main
- "Self-dogfooding ADR-000 dry-run validato, applicazione piena open" → realtà: stavamo applicando proprio quel passaggio
- "Bug UF_HIDDEN, workaround chflags" → realtà: risolto via wrapper self-healing 2026-05-24

L'agente naive ha riportato fedelmente quei dati obsoleti, perché il template kaora ha un rituale di **apertura** ben formalizzato (§ 6) ma **nessun rituale di chiusura** che forzi l'aggiornamento dei docs operativi a fine sessione.

**Conseguenza:** ogni sessione futura eredita il drift dei docs della sessione precedente, in proporzione a quanto è stata "trascurata" la chiusura.

**Fix introdotto in v0.1 (post-dogfooding):** nuova sezione § 6bis "Rituale di chiusura sessione" nel template, che istruisce l'agente a:
1. Sintetizzare sessione in 3 righe
2. Proporre aggiornamento CURRENT_STATE.md
3. Proporre aggiornamento SESSION_HANDOFF.md
4. Proporre commit con suggested message

In v0.2+ verrà supportato dal comando CLI dedicato `kaora handoff` (vedi BACKLOG → Comandi CLI futuri).

## 5. Bug minore non bloccante

⚠️ Wrapper self-healing macOS UF_HIDDEN — gestito automaticamente.

Lo script `bin/setup-dev.sh` aggiornato 2026-05-24 installa un wrapper su `.venv/bin/kaora` che fa `chflags nohidden` ad ogni invocazione. Durante il dogfooding il flag UF_HIDDEN era già stato ri-applicato da macOS spontaneamente, ma `kaora init .` è girato senza problemi grazie al wrapper. Test indiretto del fix UF_HIDDEN superato.

## 6. Conclusioni

**Test passato pieno.** Il prodotto v0.1 ha funzionato end-to-end sul produttore stesso, sia sul layer Python (kaora init) sia sul layer agente (rituale + merge guidato).

**Valore narrativo del dogfooding:**
- Validation strutturale del prodotto in condizioni reali (no test mockati su `tmp_path`)
- Caso di **co-evoluzione**: il dogfooding ha rivelato due micro-feature da aggiungere prima del lancio (archive option, rituale di chiusura). Entrambe ora codificate in v0.1.
- Material narrativo concreto per Blocco 5 (README + asset di lancio): *"abbiamo usato kaora-memory su kaora-memory stesso. Ecco cosa è successo."*

**Pattern riusabile per futuri utenti brownfield:**
1. Esegui `kaora init . --dry-run` per validare il piano
2. Esegui `kaora init .` (CLI puro, terminale)
3. Apri agente AI nuovo nel repo post-init
4. Lascia che il rituale di apertura trovi e segnali i `.kaora-bak`
5. Conferma "ok processa" → l'agente esegue § 11 con confronto preliminare anti-duplicazione, distinzione stale/valido, diff sezione per sezione
6. Approva i diff
7. Archivia il bak in `docs/archive/` (opzione 3 raccomandata)
8. Esegui rituale di chiusura: aggiorna CURRENT_STATE + SESSION_HANDOFF + commit

Tempo totale per un brownfield medio: 20-40 minuti (la maggior parte in approval dei diff).

## 7. Prossimi passi v0.1 derivati da questo report

1. **Aggiunta § 6bis Rituale di chiusura** in `template/AGENTS.md` — ✅ fatto 2026-05-26
2. **Aggiornamento § 11 step 5** con terza opzione "archive" — ✅ fatto 2026-05-27 (commit `a9518d6`)
3. **Blocco 4: `kaora check`** — ✅ chiuso 2026-05-27 (5 commit, 62 test verdi, 4 raffinamenti coerenti)
4. **Blocco 5: README ricco + asset di lancio** — 🟡 prossimo (questo report = input narrativo)
5. **Blocco 6: pubblicazione PyPI + naming repo** — 🔵 pending

## 8. Follow-up verifications (post-dogfooding)

Iterazioni di validation eseguite **dopo** il dogfooding originale del 2026-05-26. Documentano il funzionamento del prodotto sotto condizioni reali ripetute.

### 8.1 — 2026-05-27 mattina — Validation rituale di apertura post-aggiornamento

**Setup:** nuova sessione Claude Code aperta in repo dopo che la sessione di dogfooding aveva applicato § 6bis (rituale di chiusura) + commit `a9518d6` + archive del `.kaora-bak` in `docs/archive/`.

**Risultato:**
- ✅ **Scan `.kaora-bak` pulito**: il glob in root + `docs/` direct-children non ha trovato nulla (il file archiviato in `docs/archive/` è correttamente escluso dallo scan rituale). Conferma che l'opzione 3 "archive" risolve il problema del rumore in apertura sessione.
- ✅ **Drift detection proattivo**: l'agente naive ha notato di propria iniziativa che `CURRENT_STATE.md` + `SESSION_HANDOFF.md` segnavano *"commit dogfooding pending"* mentre `a9518d6` esisteva già in `git log`. Ha proposto auto-correzione, applicata in commit `eabae39`.
- ✅ **Validazione indiretta del § 6bis**: il rituale di chiusura applicato in sessione precedente aveva lasciato docs in uno stato testabile (drift residuo limitato, narrazione del lavoro fatto coerente con git).

**Implicazione di prodotto:** il pattern di drift detection in apertura sessione NON è oggi codificato esplicitamente nel rituale § 6, è emerso come comportamento naturale dell'agente. Da valutare se aggiungerlo come step esplicito ("step 4.5: confronta CURRENT_STATE.md con git log ultimo commit; se divergente, segnala") in v0.2. Item da aggiungere a BACKLOG.

### 8.2 — 2026-05-27 sera — Blocco 4 `kaora check` con pattern dual-session

**Setup:** nuova sessione Claude Code per implementare Blocco 4. In parallelo, sessione di revisione esperta (questo report scritto da quella).

**Flusso eseguito:**
1. **Skill loading**: `tdd-workflows-tdd-cycle` caricata prima del codice (Gate A § 5.1)
2. **Spec test proposta**: 22 test in `test_check.py` + 3 CLI in `test_cli.py`, mappati 1:1 con i 6 check di SESSION_HANDOFF. Approvata dal revisore con micro-precisazioni (distinzione esplicita WARN strutturali vs INFO BOOTSTRAP).
3. **Red phase**: 24 test scritti, tutti falliscono per i motivi giusti (`ModuleNotFoundError` + `Error: No such command 'check'`). Suite esistente 33 test intatta (zero regressione).
4. **Green phase**: `kaora_memory/check.py` (299 LOC) implementato incrementalmente per categoria (structure → adr005 → adr_state → placeholders → hooks → settings → formatters). Pattern *"pytest dopo ogni categoria, delta verde sintetico"* (vedi memoria `feedback_tdd_incrementale_per_categoria.md`).
5. **Commit feature base**: `29fa094 feat(cli): kaora check linter integrità memoria operativa`. 57/57 verdi (33 + 24).
6. **Review post-green**: il revisore ha letto `check.py` completo e ha identificato 4 trade-off di design (falso positivo "Proposed" in code-block, settings stringy, file hardcoded, Level Literal solo statico). I primi 3 sostanziali.
7. **Decisione utente**: chiudere i raffinamenti in v0.1 invece che rimandarli a v0.2 (preferenza esplicita: *"v0.1 chiusa bene > v0.1 con 3 cose da ricordare"*).
8. **Refactor commit 1**: `a9e542a refactor(check): code-block exclusion + struct parsing + dynamic .md scan`. 3 fix mirati, ognuno preceduto dal proprio test rosso. 61/61 verdi.
9. **Re-dogfooding live**: `kaora check .` sul repo ha rivelato 2 nuovi WARN reali su `docs/SESSION_HANDOFF.md` (placeholder `{{...}}` dentro fenced code block della spec). **Stesso pattern del falso "Proposed"** in versione placeholder.
10. **Refactor commit 2**: `607b5a9 refactor(check): _strip_code_blocks anche in _check_placeholders`. 1 riga di codice + 1 test, riusa la funzione esistente. 62/62 verdi.
11. **Rituale di chiusura § 6bis**: applicato dall'agente naive. Diff CURRENT_STATE + SESSION_HANDOFF approvati dal revisore, commit `dae7126 chore(handoff): chiusura sessione Blocco 4 + brief Blocco 5`.

**Pattern emerso (4 fix, una stessa radice):**

Tutti e 4 i raffinamenti riducono al pattern **"contenuti documentari ≠ contenuti reali"**:
- ADR Proposed dentro esempio template → non contare
- Placeholder `{{...}}` dentro spec di kaora check → non contare
- `<BOOTSTRAP/>` marker dentro esempio template → non contare
- Hook name dentro campo arbitrario (commento, key) → non contare come hook attivo

Tutti i fix usano la stessa tecnica: separare l'estrazione del contenuto rilevante dalla struttura documentaria che lo descrive. Materiale narrativo forte per Blocco 5: il prodotto ha imparato a distinguere "documentazione su X" da "X reale", che è esattamente la filosofia metacognitiva che vendiamo nel manifesto.

**Risultato Blocco 4 finale:**
- 62 test verdi (33 + 21 + 4 + 1 + 3 CLI)
- 5 commit Blocco 4 (`29fa094` → `a9e542a` → `607b5a9` → `dae7126`) + 1 di drift `eabae39` in apertura
- Memoria persistente arricchita con `feedback_tdd_incrementale_per_categoria.md` (pattern TDD step-by-step per moduli multi-categoria)

### 8.3 — Pattern dual-session (agente naive + revisore esperto)

Validato su due cicli consecutivi (dogfooding 2026-05-26 + Blocco 4 2026-05-27): la coppia *"sessione esecutiva naive con context fresh + sessione revisore con context completo"* produce qualità superiore al singolo agente.

**Vantaggi osservati:**
- L'agente naive trova naturalmente i punti di estensione del template (terza opzione archive emersa spontaneamente)
- Il revisore cattura imprecisioni di sintesi e trade-off di design che l'esecutore non vede dal suo angolo
- Il pattern test-first + revisione del codice prima del commit prende gli errori prima che diventino debt
- Comunicazione tramite l'utente come ponte: l'utente passa diff/output, il revisore commenta, l'utente sintetizza la risposta per l'agente naive

**Limite osservato:**
- Costo cognitivo per l'utente (deve copia-incollare avanti e indietro)
- Latency: ogni round trip aggiunge 30-60 secondi
- Non scala a >2 sessioni simultanee (overhead diventa dominante)

**Implicazione di prodotto:** il workflow dual-session **non è oggi parte del prodotto kaora-memory** (è un meta-pattern di utilizzo). Da considerare per documentazione di lancio (Blocco 5): può diventare un capitolo del README *"Come usare kaora-memory in scenari ad alta complessità"*. Oppure restare come pratica scoperta dagli utenti avanzati senza codificarla nel prodotto.

---

*Report autoritativo, eventuali sessioni future di dogfooding aggiungono un nuovo report dedicato (es. `docs/DOGFOODING_REPORT_v0.1.1.md`) invece di modificare questo. Le sezioni "Follow-up verifications" (§ 8+) sono l'eccezione: documentano iterazioni di validation sullo stesso ciclo v0.1, non nuovi cicli.*
