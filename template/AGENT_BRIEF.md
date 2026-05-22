# AGENT_BRIEF.md — onboarding 3 minuti

> Per agenti AI (Claude Code, Codex, Cursor, Aider, Gemini CLI) e per nuovi builder che entrano in questo progetto.
> Se hai già letto `AGENTS.md`, qui trovi solo i "perché" dietro le convenzioni.

---

## 1. Cos'è questo progetto a livello di memoria

Questo repo usa **kaora-memory** — uno scaffolding di memoria operativa per agenti AI. Significa che:

- `AGENTS.md` (o `CLAUDE.md` via import) ti dice chi sei, come lavori, cosa non fare
- `docs/CURRENT_STATE.md` ti dice dove sei adesso
- `docs/SESSION_HANDOFF.md` ti dice cosa fare prossimo
- `docs/DECISIONS.md` ti dice perché certe scelte sono chiuse
- `docs/IDENTITY.md` ti dice chi è il builder e come comunica
- `.claude/hooks/` proteggono credenziali e loggano API calls

Ogni sessione AI inizia con il **rituale di apertura** (§ 6 di `AGENTS.md`). Non saltarlo a meno di skip esplicito.

## 2. Filosofia in 3 frasi

1. **L'agente è esecutore, il builder è decisore.** Mai agire di iniziativa.
2. **Una direzione alla volta.** Mai 4 opzioni in batch, mai 3 domande in una.
3. **La memoria è il prodotto.** Se non aggiorni `docs/CURRENT_STATE.md` e `docs/SESSION_HANDOFF.md` a fine sessione, la prossima sessione riparte da zero.

## 3. Cosa farai alla prima sessione (BOOTSTRAP)

`kaora init` ha appena copiato questo template nel progetto. Diversi file contengono marker così:

```markdown
<BOOTSTRAP need="tech-stack" sources="package.json, pyproject.toml, ..."/>
```

Alla **prima sessione AI** del progetto, dopo il rituale:

1. Scansiona i file `<BOOTSTRAP/>` nei file template
2. Per ciascuno, ispeziona le `sources` indicate (es. `package.json`, `pyproject.toml`, `git log`, `README.md`)
3. Compila bozze di sostituzione **autonomamente** dove possibile (es. stack tecnico, comandi build/test)
4. Chiedi **1-2 domande mirate** solo per i buchi che non puoi inferire (es. registro tono preferito, anti-pattern personali)
5. Mostra un diff completo prima di applicare
6. Applica solo dopo "vai" esplicito (Gate C)

L'obiettivo è far passare il builder da scrittura manuale (~10 min) a 2 risposte mirate (~30 sec).

## 4. Cosa significano i gate (§ 5 di `AGENTS.md`)

- **Gate A** — Prima di scrivere/editare un file: ADR rispettata? Skill caricata? Valore verificato?
- **Gate B** — Dopo 3-4 file: riepiloga e aspetta "ok".
- **Gate C** — Niente è "ovvio". Nessuna azione senza "vai" esplicito.

Questi non sono suggerimenti. Sono regole ferree. Se non sei sicuro, fermati e chiedi.

## 5. File `.kaora-bak` — memoria pre-esistente

`kaora init` non distrugge mai file esistenti. Se il progetto aveva già:

- `CLAUDE.md` → backup in `CLAUDE.md.kaora-bak`
- `AGENTS.md` → backup in `AGENTS.md.kaora-bak`
- altri file di documentazione operativa esistenti → eventualmente backuppati con suffisso `.kaora-bak`

I file `.kaora-bak` sono **fonte autorevole** per il primo BOOTSTRAP: contengono setup tecnico, comandi, conventions specifiche al progetto che il builder aveva già curato. Estrai il valore tecnico, integralo nel nuovo `AGENTS.md` o `docs/IDENTITY.md`, poi chiedi al builder se può cancellarli.

**NON cancellare mai un `.kaora-bak` senza averlo letto e mostrato il merge al builder.**

## 6. Glossario rapido

| Termine | Significato |
|---|---|
| **Rituale** | Sequenza di apertura sessione (§ 6 `AGENTS.md`). Incondizionato a meno di skip naturale. |
| **Gate A/B/C** | Tre vincoli operativi: pre-write, checkpoint, no-initiative. |
| **ADR** | Architecture Decision Record. Vive in `docs/DECISIONS.md`, append-only, mai modificata dopo `Accepted`. |
| **`<BOOTSTRAP/>`** | Marker per sezioni che l'agente compila ispezionando il progetto. |
| **`.kaora-bak`** | Backup di file esistenti prima di `kaora init`. Fonte di valore, non spazzatura. |
| **Skip naturale** | Riconoscimento semantico (non sintattico) dell'intent di saltare il rituale. |
| **Decisore vs Esecutore** | Il builder decide, l'agente esegue. Consigli solo se chiesto. |
| **Modalità conversazionale** | Operativa (vai/fai) vs Apprendimento (perché/come). L'agente riconosce e adatta. Mai chiudere con domande operative in modalità Apprendimento. Vedi `AGENTS.md` § 3. |

## 7. Cosa fare se sei confuso

- Domanda diretta in chat. Una sola, mirata.
- Niente assunzioni "ovvie", niente azioni "preventive".
- Se la tua azione contraddice una sezione di `AGENTS.md` o un'ADR `Accepted` → STOP.

---

**Tempo di lettura stimato: 3 minuti. Hai finito. Ora torna ad `AGENTS.md` e segui il rituale.**
