# DECISIONS.md — ADR log immutabile

> Architectural Decision Records. **Append-only.** Una decisione chiusa si riapre solo con una nuova ADR che la sostituisce esplicitamente (`Supersedes: ADR-XXX`).
>
> Formato: data · contesto · decisione · alternative scartate · conseguenze.

---

## ADR-000 — Adozione kaora-memory per la memoria operativa del progetto

**Data:** {{year}}-MM-GG
**Stato:** Accepted

### Contesto

{{project_name}} è {{project_oneliner}}. Il lavoro coinvolge sessioni multiple con agenti AI (Claude Code, Codex, Cursor, Aider, Gemini CLI). Senza una memoria operativa esplicita, ogni sessione riparte da zero: l'agente non sa lo stato corrente, quali decisioni sono già chiuse, quale registro di comunicazione preferisce il builder.

### Decisione

Adottiamo **kaora-memory** come scaffolding di memoria operativa per questo progetto.

Conseguenze concrete:
- `AGENTS.md` (canonico) + `CLAUDE.md` (import) come master context
- `docs/CURRENT_STATE.md` aggiornato a fine di ogni sessione
- `docs/SESSION_HANDOFF.md` come brief per la prossima sessione
- `docs/DECISIONS.md` (questo file) come log immutabile delle scelte architetturali
- `docs/IDENTITY.md` con identità builder e anti-pattern
- Hook `.claude/hooks/` per protezione credenziali e log API
- Rituale di apertura sessione obbligatorio (vedi `AGENTS.md` § 6)
- Tre gate operativi: pre-write, checkpoint, no-initiative (vedi `AGENTS.md` § 5)

### Alternative scartate

- **Memoria implicita** (nessun file, solo conversazione): non scala oltre la prima sessione. Ogni nuovo agente riparte da zero.
- **README.md unico ricco**: README serve agli umani che scoprono il progetto, non agli agenti che operano. Mescolare i due rovina entrambi.
- **Solo `CLAUDE.md`**: taglia fuori Codex / Cursor / Aider / Gemini CLI che cercano `AGENTS.md`.
- **Documenti Notion / Linear / Confluence esterni**: agenti non li leggono automaticamente, friction di accesso, fuori dal repo.

### Conseguenze

- A fine di ogni sessione devo aggiornare `CURRENT_STATE.md` e `SESSION_HANDOFF.md`. Senza questo, il valore crolla.
- Decisioni di architettura → sempre una nuova ADR qui, mai annotazioni nel codice o nel README.
- Lo scaffolding aggiunge ~10 file al repo. Trade-off accettato: più file, meno tempo perso per ogni nuova sessione AI.

---

<BOOTSTRAP need="initial-project-adr" sources="prior major decisions visible from git log, README mentioned architectural choices, framework lock-in"/>

<!--
Per aggiungere una nuova ADR:

## ADR-NNN — Titolo della decisione

**Data:** YYYY-MM-DD
**Stato:** Proposed | Accepted | Deprecated | Superseded
**Supersedes:** ADR-XXX (solo se applicabile)

### Contesto
[Perché serve questa decisione, cosa è cambiato]

### Decisione
[Cosa abbiamo deciso, in modo chiaro]

### Alternative scartate
[Almeno 2 opzioni considerate e perché no]

### Conseguenze
[Cosa cambia operativamente, trade-off accettati]
-->

---

## Versionamento ADR

- v0.1.0 — ADR-000 (scaffolding via kaora-memory · {{year}}-MM-GG)
