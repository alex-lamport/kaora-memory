# SESSION_HANDOFF.md — brief per la prossima sessione

> Leggi subito dopo `CLAUDE.md` e `CURRENT_STATE.md`.
>
> **Ultima sessione:** 2026-05-22 · Blocco 1 chiuso.

---

## 🔴 PROSSIMA SESSIONE — Blocco 2: template generalizzato

### Obiettivo

Creare la directory `template/` nel repo con tutti i file generalizzati che `kaora init` (Blocco 3) copierà in un nuovo progetto utente. I file usano placeholder Jinja-style `{{...}}` e markers `<BOOTSTRAP need="..." sources="..."/>` per le sezioni che l'agente compilerà alla prima sessione.

### File da creare in `template/`

```
template/
├── CLAUDE.md                          (rituale § universale + skip intent + 6 layer + gate)
├── AGENTS.md                          (gemello funzionale di CLAUDE.md per Codex/Cursor/Gemini)
├── AGENT_BRIEF.md                     (onboarding 3 minuti)
├── README.md.tpl                      (README minimo del progetto utente, NON di kaora-memory)
├── BACKLOG.md                         (vuoto con header)
├── docs/
│   ├── IDENTITY.md                    (chi sei, come comunichi, anti-pattern)
│   ├── CURRENT_STATE.md               (stato iniziale "scaffolding done, ADR-000 da scrivere")
│   ├── SESSION_HANDOFF.md             (brief per la prima sessione vera)
│   ├── DECISIONS.md                   (header + ADR-000 esempio compilato)
│   └── SESSION_ERRORS_TEMPLATE.md     (struttura post-mortem riusabile)
└── .claude/
    ├── settings.json                  (hook PreToolUse Edit/Write + PostToolUse Bash)
    └── hooks/
        ├── protect-credentials.sh     (blocca Edit su .env, credentials.*, .secret.*)
        └── log-api-calls.sh           (logga curl/API a logs/api-calls.jsonl)
```

### Placeholder Jinja-style da supportare (input minimi dell'`init`)

| Placeholder | Significato | Esempio |
|---|---|---|
| `{{project_name}}` | Nome del progetto utente | `MioProgetto` |
| `{{project_oneliner}}` | Pitch in una riga | `App SaaS per dentisti italiani` |
| `{{project_path}}` | Path assoluto del progetto | `/Users/alex/Desktop/mioprogetto` |
| `{{owner_name}}` | Nome del builder | `Alex Silva` |
| `{{owner_email}}` | Email | `alex@example.com` |
| `{{communication_register}}` | Tono preferito | `diretto, italiano, no preamboli` |
| `{{year}}` | Anno corrente | `2026` |

**Lista definitiva da concordare con Alexis prima di finalizzare.** Quella sopra è una proposta.

### Marker `<BOOTSTRAP/>` — sezioni che l'agente compila in autonomia

Esempio in `template/docs/IDENTITY.md`:

```markdown
## Chi sono io
<BOOTSTRAP need="user-identity" sources="git config user.name, git config user.email, README.md, alex_personality/"/>

## Come comunico
<BOOTSTRAP need="communication-register" sources="git log style, README tone, conversational hints"/>
```

L'agente alla prima `claude vai` (o equivalente):
1. Ispeziona git config, README, package files, commit log
2. Compila una bozza dei `<BOOTSTRAP/>`
3. Chiede 1-2 domande mirate solo per i buchi (es. registro preferito, anti-pattern specifici)
4. Applica diff con conferma utente

### Pyproject — aggiornamento necessario in Blocco 2 o 3

Per shippare `template/` dentro il wheel PyPI, aggiungere:

```toml
[tool.hatch.build.targets.wheel.force-include]
"template" = "kaora_memory/_template"
```

Così `kaora init` legge da `kaora_memory/_template/` via `importlib.resources`.

### Skill obbligatorie PRIMA di costruire (Gate A § 7.1.2)

- **`agents-md`** — per il template `AGENTS.md` (standard cross-AI proposto da Aider/Codex)
- **`architecture-decision-records`** — per l'ADR-000 esempio in `template/docs/DECISIONS.md`
- **`python-packaging`** — quando tocchiamo `pyproject.toml` per data files

### Cosa NON toccare (Blocco 1 chiuso)

- ❌ `pyproject.toml` SE NON per aggiungere `force-include` di `template/` (è il solo motivo legittimo)
- ❌ `LICENSE`, `.gitignore`, `README.md` (minimale ok per ora, polish in Blocco 5)
- ❌ `kaora_memory/__init__.py` (versione corretta)
- ❌ `CLAUDE.md`, `docs/CURRENT_STATE.md`, `docs/SESSION_HANDOFF.md`, `docs/DECISIONS.md` (memoria operativa di kaora-memory STESSO, non template)
- ❌ Riaprire ADR già chiuse (000-004)

### Check di apertura sessione

Prima di iniziare:

```bash
cd ~/Desktop/kaora-memory
python3 -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))" && echo "TOML OK"
git log --oneline -3   # deve mostrare almeno f45f4a3
ls -la template/ 2>/dev/null && echo "ATTENZIONE: template già esiste, valuta" || echo "template assente, parto da zero (atteso)"
```

### Output atteso a fine Blocco 2

1. Directory `template/` completa con tutti i file sopra elencati
2. Placeholder e `<BOOTSTRAP/>` markers presenti e coerenti
3. Lista definitiva dei placeholder confermata con Alexis
4. ADR-005 (o successiva) scritta per documentare le scelte di template (es. quale standard AGENTS.md, quali `<BOOTSTRAP/>` sources di default)
5. Commit pulito: `feat(template): generalizzazione v0.1 con BOOTSTRAP markers`
6. `CURRENT_STATE.md` e `SESSION_HANDOFF.md` aggiornati con il brief Blocco 3

### Cosa NON aprire in questa sessione

- ❌ Blocco 3 (`kaora init`) — solo dopo che il template è validato visivamente da Alexis
- ❌ Test (`pytest`) — Blocco 3
- ❌ Pubblicazione PyPI — Blocco 6
- ❌ Push su GitHub — solo quando username finale è confermato

---

## Note operative per la prossima sessione

- **Apri Claude Code in `~/Desktop/kaora-memory/`** (NON in `~/Desktop/kaora/`)
- **Registro:** italiano · diretto · no preamboli · una decisione alla volta
- **Decisioni grandi** → ADR in `docs/DECISIONS.md`, mai annotazioni libere
- **Memoria persistente** del progetto non ancora popolata — verrà generata applicando `kaora init` su se stesso dopo Blocco 3 (vedi ADR-000 dogfooding)
