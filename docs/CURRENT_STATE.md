# CURRENT_STATE.md — stato operativo

> Aggiornato a fine di ogni sessione. Risponde a "dove siamo, cosa funziona, cosa manca adesso".
>
> **Ultimo aggiornamento:** 2026-05-22 — Blocco 2 chiuso definitivo · template/ installabile + ADR 005-008 Accepted (incluso ADR-006 v2 con merge JSON).

---

## Snapshot oggi

**Blocco corrente:** Blocco 2 ✅ chiuso definitivo · Blocco 3 prossimo (`kaora init` implementazione)
**Commit ultimo:** `f45f4a3 chore: scaffolding iniziale kaora-memory v0.1` (pre-Blocco 2, commit Blocco 2 in attesa di approvazione)
**Branch:** `main`
**Repo remoto:** non ancora configurato (placeholder URL `alex-lamport/kaora-memory` in pyproject)
**ADR aperte:** nessuna · tutte 000-008 Accepted

## Cosa esiste

```
kaora-memory/
├── .gitignore
├── BACKLOG.md
├── LICENSE
├── README.md
├── pyproject.toml                    (hatchling, py>=3.10, entry point `kaora`)
├── kaora_memory/
│   └── __init__.py                   (__version__ = "0.1.0")
├── CLAUDE.md                         (master context kaora-memory stesso, dogfooding)
├── docs/
│   ├── CURRENT_STATE.md              (questo file)
│   ├── SESSION_HANDOFF.md            (brief Blocco 3)
│   └── DECISIONS.md                  (ADR 000-006 — 005/006 Proposed)
└── template/                         ✨ NUOVO (Blocco 2)
    ├── AGENTS.md                     (canonico cross-agent, ~130 righe, placeholder + BOOTSTRAP)
    ├── CLAUDE.md                     (4 righe: @AGENTS.md import, opzione C / ADR-005)
    ├── AGENT_BRIEF.md                (onboarding 3-min: rituale, gate, BOOTSTRAP, .kaora-bak)
    ├── README.md.tpl                 (template README progetto utente)
    ├── BACKLOG.md                    (header + BOOTSTRAP per idee iniziali)
    ├── docs/
    │   ├── IDENTITY.md               (6 sezioni con BOOTSTRAP)
    │   ├── CURRENT_STATE.md          (stato iniziale post-init)
    │   ├── SESSION_HANDOFF.md        (brief prima sessione vera)
    │   ├── DECISIONS.md              (header + ADR-000 esempio compilato)
    │   └── SESSION_ERRORS_TEMPLATE.md (template post-mortem strutturato)
    └── .claude/
        ├── settings.json             (hook PreToolUse Write/Edit + PostToolUse Bash)
        └── hooks/
            ├── protect-credentials.sh (smoke-tested OK)
            └── log-api-calls.sh       (smoke-tested OK)
```

**Verifiche eseguite in Blocco 2:**
- ✅ `template/` tree completo con 13 file
- ✅ Hook `protect-credentials.sh` testato: blocca `.env`, `id_rsa`, allow file innocui
- ✅ Hook `log-api-calls.sh` testato: logga `curl`, ignora `ls`
- ✅ Placeholder Jinja `{{...}}` uniformi (7 placeholder definitivi)
- ✅ Marker `<BOOTSTRAP need="..." sources="..."/>` su tutti i punti che richiedono conoscenza progetto

## Placeholder definitivi (v0.1.1)

| Placeholder | Significato | Esempio |
|---|---|---|
| `{{project_name}}` | Nome progetto utente | `MioProgetto` |
| `{{project_oneliner}}` | Pitch in una riga | `App SaaS per dentisti italiani` |
| `{{project_path}}` | Path assoluto progetto | `/Users/alex/Desktop/mioprogetto` |
| `{{owner_name}}` | Nome builder | `Alex Silva` |
| `{{owner_email}}` | Email | `alex@example.com` |
| `{{communication_register}}` | Tono preferito | `diretto, conciso, no preamboli` |
| `{{communication_language}}` | Lingua docs/log | `italiano` |
| `{{year}}` | Anno corrente | `2026` |

Modifica vs SESSION_HANDOFF Blocco 1: aggiunto `{{communication_language}}` per i18n futura.

## Cosa manca (priorità ordinata)

1. **Conferma ADR-005 e ADR-006** da Alexis — Accepted dopo review
2. **`kaora_memory/cli.py`** con comando `init` — TUTTO Blocco 3
3. **`pyproject.toml`** — aggiungere `[tool.hatch.build.targets.wheel.force-include] "template" = "kaora_memory/_template"` (Blocco 3)
4. **`kaora_memory/_template/`** generato/sincronizzato da `template/` (Blocco 3 — strategia: symlink in dev, copy in wheel build)
5. **`kaora_memory/check.py`** — Blocco 4
6. **Test minimali** in `tests/` — Blocco 3-4
7. **README ricco + demo** — Blocco 5
8. **Setup pubblicazione PyPI** (`.pypirc`, token test.pypi) — Blocco 6

## Decisioni di design Blocco 2 (Accepted)

- **ADR-005** Canonico `AGENTS.md` + import `@AGENTS.md` in `CLAUDE.md`. Supersedes ADR-003 sul *modo*, non sulla *direzione*. Elimina drift per costruzione, validato in Claude Code 2.1.119 (Test 2).
- **ADR-006 v2** Policy install brownfield in 3 categorie: markdown (backup + BOOTSTRAP-merge), JSON (merge intelligente per `.claude/settings.json`), tutto-il-resto (skip-conservative). Riscritta v2 prima di Accept perché v1 (skip + warn per settings.json) avrebbe lasciato hook kaora inattivi su brownfield.
- **ADR-007** Modalità conversazionale Operativa vs Apprendimento. Nata dall'osservazione del builder in tempo reale, applicata immediatamente.
- **ADR-008** Zero attrito per decisioni ADR `Proposed`. Step 7 del rituale: mostra ADR aperte direttamente in chat senza far aprire `docs/DECISIONS.md`. Emersa applicando ADR-007.

Tutte e 4 **Accepted** dopo Test 1-4 e revisione in chat.

## Annotazioni per Blocco 5 (README)

- Brownfield-friendly: niente warning "solo greenfield", FAQ "ho già un CLAUDE.md?" → racconta backup-first + BOOTSTRAP-merge come feature
- Hero: "Memoria operativa per agenti AI. Funziona su qualsiasi progetto, fresco o esistente."

## Asset di comunicazione collegati

- `/tmp/kaora-memory-preview.html` — dashboard premium anteprima (Blocco 1, asset NON nel repo)
- `/tmp/kaora_builder_memory_architecture.md` — analisi tecnica (Blocco 1, asset NON nel repo)

## Note operative

- **Repo NON ancora pushato** su GitHub
- **Test rapido salute:**
  ```bash
  python3 -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))" && echo "TOML OK"
  ls template/ template/docs template/.claude/hooks && echo "template completo"
  ```
- **Memoria persistente Claude Code:** non ancora popolata per questo progetto
