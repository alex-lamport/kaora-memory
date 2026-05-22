# SESSION_ERRORS_TEMPLATE.md — template post-mortem per sessione fallita

> Copia questo file in `docs/SESSION_ERRORS/YYYY-MM-DD-slug-breve.md` quando una sessione produce un errore significativo (decisione sbagliata, codice che ha rotto, tempo perso per malinteso, anti-pattern dell'agente non corretto in tempo).
>
> **Obiettivo:** trasformare ogni errore in apprendimento codificato. Il file finisce in `docs/IDENTITY.md` § 3 (anti-pattern) o `docs/DECISIONS.md` (nuova ADR) a seconda della natura.

---

## Cosa è successo

[Descrizione fattuale, 2-4 righe. Nessun tono accusatorio.]

## Quando

- **Data:** YYYY-MM-DD
- **Agente coinvolto:** [Claude Code / Codex / Cursor / Aider / Gemini CLI / altro]
- **Modello:** [es. claude-sonnet-4.6, gpt-5, gemini-2.5-pro]
- **Durata sessione:** ~X minuti
- **Tempo perso stimato:** ~Y minuti

## Cosa si voleva ottenere

[Obiettivo originale della sessione]

## Cosa è andato storto

[Cronologia dell'errore. Indica file, comandi, decisioni nel punto preciso in cui la sessione ha deviato.]

## Causa radice

[Una sola causa principale. Se ce ne sono più, scegli quella senza la quale l'errore non sarebbe successo.]

Categoria probabile (cerchia una):
- Skip del rituale di apertura
- Violazione Gate A (skill non caricata prima di Write)
- Violazione Gate B (3-4 file modificati senza checkpoint)
- Violazione Gate C (azione di iniziativa senza "vai")
- ADR esistente ignorata
- Anti-pattern in IDENTITY.md non rispettato
- Memoria pre-esistente (`.kaora-bak`) non letta
- Specifica utente ambigua, agente non ha chiesto
- Bug genuino nel codice / tool / libreria

## Cosa abbiamo riparato

[Comandi/diff/decisioni che hanno chiuso l'incidente]

## Cosa codificare per evitare ripetizione

Scegli **una** delle azioni seguenti (può essere combinata):

- [ ] **Anti-pattern in `docs/IDENTITY.md` § 3** — aggiungi una riga concreta
- [ ] **Nuova ADR in `docs/DECISIONS.md`** — se è una decisione architetturale
- [ ] **Skill da aggiungere a `AGENTS.md` § 10** — se mancava il sapere di dominio
- [ ] **Hook in `.claude/hooks/`** — se la prevenzione automatica è fattibile
- [ ] **Modifica `AGENTS.md` § 9 (Cosa NON fare)** — se è una regola universale

Concretamente:

```
[diff o testo aggiunto]
```

## Lezione in una frase

[Una sola frase, secca. Sarà quella che ricorderai tra 3 mesi.]

---

**Indicizzazione:** alla fine di questo post-mortem, aggiorna `docs/CURRENT_STATE.md` con un'eventuale nota sotto "Note operative" se serve memoria attiva nelle sessioni future.
