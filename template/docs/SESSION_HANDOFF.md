# SESSION_HANDOFF.md — brief per la prossima sessione

> Leggi subito dopo `AGENTS.md` e `CURRENT_STATE.md`.
>
> **Ultima sessione:** {{year}}-MM-GG · scaffolding kaora installato.

---

## 🟢 PROSSIMA SESSIONE — Bootstrap del progetto

### Obiettivo

Trasformare il template installato in una memoria operativa specifica per **{{project_name}}**. Cioè: compilare tutti i marker `<BOOTSTRAP/>` rimasti nei file e — se esistono — leggere e integrare i file `.kaora-bak`.

### Cosa farai (sequenza)

1. **Apri il progetto in un agente** (Claude Code, Codex CLI, Cursor, Aider o Gemini CLI)
2. L'agente eseguirà il **rituale di apertura** (§ 6 di `AGENTS.md`)
3. Dopo il "vai" tuo, l'agente:
   - Cerca file `*.kaora-bak` in root e `docs/` — se trova, li legge e propone integrazione
   - Scansiona i marker `<BOOTSTRAP/>` in tutti i file template
   - Compila bozze autonomamente leggendo `package.json`, `pyproject.toml`, `Cargo.toml`, `git config`, `README.md`, struttura cartelle
   - Ti chiede **1-2 domande mirate** solo per i buchi (es. registro tono preferito, anti-pattern personali)
   - Mostra un diff completo
   - Applica solo dopo "vai" esplicito

### File coinvolti dal BOOTSTRAP

| File | Cosa compila |
|---|---|
| `AGENTS.md` | Stack tecnico, stage corrente, scope, file chiave, skill mapping, health check |
| `docs/IDENTITY.md` | Identità builder, registro comunicazione, anti-pattern, conventions, glossario dominio |
| `docs/CURRENT_STATE.md` | Commit/branch correnti, file esistenti, feature funzionanti, todo |

### Tempo stimato

~30 secondi di domande utente · ~2-3 minuti di lavoro autonomo dell'agente · ~1 minuto di review del diff.

### Cosa NON aprire in questa prima sessione

- ❌ Implementazione di feature di prodotto (prima la memoria, poi il codice)
- ❌ Modifica `.claude/settings.json` o `hooks/` (sono pre-configurati)
- ❌ Cancellazione `.kaora-bak` (mai senza review esplicita)

### Check di apertura sessione

```bash
ls AGENTS.md CLAUDE.md AGENT_BRIEF.md BACKLOG.md docs/ .claude/ 2>/dev/null
ls *.kaora-bak docs/*.kaora-bak 2>/dev/null  # se torna risultati: file backup da leggere
git log --oneline -3
```

### Output atteso a fine prima sessione

1. Tutti i marker `<BOOTSTRAP/>` sostituiti con contenuti specifici al progetto
2. Eventuale contenuto dei `.kaora-bak` integrato nelle sezioni appropriate
3. `docs/CURRENT_STATE.md` aggiornato con stato reale post-bootstrap
4. `docs/SESSION_HANDOFF.md` aggiornato con brief della seconda sessione (es. "iniziamo prima feature X")
5. Commit pulito: `chore: bootstrap memoria operativa via kaora`

---

## Note operative per la prima sessione

- **Apri l'agente nella root del progetto** ({{project_path}})
- **Registro:** {{communication_register}}
- **Decisioni grandi** → nuova ADR in `docs/DECISIONS.md`, mai annotazioni libere
- **Se l'agente sbaglia tono** → digli *"aggiungi anti-pattern a IDENTITY.md: ..."*
