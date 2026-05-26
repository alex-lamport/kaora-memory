# CURRENT_STATE.md — stato operativo

> Aggiornato a fine di ogni sessione. Risponde a "dove siamo, cosa funziona, cosa manca adesso".
>
> **Ultimo aggiornamento:** 2026-05-26 — Self-dogfooding ADR-000 APPLICATO (opzione A): `kaora init .` eseguito sul repo stesso, merge AGENTS.md guidato dall'agente completato, `CLAUDE.md.kaora-bak` archiviato in `docs/archive/`. Bug UF_HIDDEN macOS RISOLTO via wrapper self-healing in `bin/setup-dev.sh` (2026-05-24).

---

## Snapshot oggi

**Blocco corrente:** Blocco 3 ✅ chiuso · Self-dogfooding ✅ applicato · Blocco 4 prossimo (`kaora check`)
**Commit ultimo in main:** `66e0c48 chore(backlog): pre-publish checklist Blocco 6 + nota wheel stale risk`. Blocco 2+3 già committati (`d212951 feat(cli): kaora init con policy brownfield ADR-006 v2`). Working tree con modifiche pending da consolidare in commit dogfooding.
**Branch:** `main`
**Repo remoto:** non ancora configurato (placeholder URL `alex-lamport/kaora-memory` in pyproject)
**ADR aperte:** nessuna · tutte 000-009 Accepted

## Cosa esiste

```
kaora-memory/
├── .gitignore                        (.venv/, dist/, .pytest_cache/, ...)
├── BACKLOG.md                        (+sezione "Issue noti": UF_HIDDEN macOS)
├── LICENSE
├── README.md                         (minimal, ricco in Blocco 5)
├── pyproject.toml                    (hatchling, py>=3.10, entry `kaora`, force-include `template/` → `kaora_memory/_template/`)
├── CLAUDE.md                         (4 righe `@AGENTS.md` — post-dogfooding 2026-05-26)
├── AGENTS.md                         ✨ NUOVO (post-dogfooding) — master context canonico, popolato via merge guidato del .kaora-bak
├── AGENT_BRIEF.md                    ✨ NUOVO (post-dogfooding) — onboarding agenti
├── bin/
│   └── setup-dev.sh                  ✨ AGGIORNATO 2026-05-24 — venv + pip -e .[dev] + installa wrapper self-healing su .venv/bin/kaora (fix UF_HIDDEN macOS)
├── kaora_memory/                     ✨ ESPANSO (Blocco 3)
│   ├── __init__.py                   (__version__ = "0.1.0")
│   ├── settings_merger.py            ✨ NUOVO — merge JSON ADR-006 v2 (permissions union, hooks dedup by matcher)
│   ├── template_resolver.py          ✨ NUOVO — get_template_root() con importlib.resources + fallback dev path
│   ├── installer.py                  ✨ NUOVO — install_template() + InstallReport, policy 3 categorie
│   └── cli.py                        ✨ NUOVO — Click app, comando `kaora init [PATH] [--force] [--dry-run] [--no-git-init]`
├── tests/                            ✨ NUOVO (Blocco 3) — 33 test green
│   ├── __init__.py
│   ├── test_settings_merger.py       (8 cases)
│   ├── test_template_resolver.py     (3 cases)
│   ├── test_init.py                  (18 cases: greenfield/brownfield/dry-run/force/placeholder)
│   └── test_cli.py                   (4 cases: --version, init greenfield, --dry-run, default cwd)
├── docs/
│   ├── CURRENT_STATE.md              (questo file)
│   ├── SESSION_HANDOFF.md            (brief Blocco 4)
│   ├── DECISIONS.md                  (ADR 000-009 Accepted)
│   ├── PHILOSOPHY.md                 (perché del prodotto, metacognizione applicata)
│   ├── IDENTITY.md                   ✨ NUOVO (post-dogfooding) — chi è il builder, come comunica, anti-pattern
│   ├── SESSION_ERRORS_TEMPLATE.md    ✨ NUOVO (post-dogfooding) — template post-mortem
│   ├── DOGFOODING_REPORT.md          ✨ NUOVO (post-dogfooding) — case study completo del test self-dogfooding 2026-05-26
│   └── archive/
│       └── CLAUDE.md.kaora-bak       ✨ NUOVO (post-dogfooding) — vecchio master context, archiviato per non far scattare lo scan rituale
└── template/                         (Blocco 2, sorgente unica, force-include nel wheel)
    ├── AGENTS.md                     (canonico cross-agent)
    ├── CLAUDE.md                     (4 righe: @AGENTS.md)
    ├── AGENT_BRIEF.md                (onboarding agenti)
    ├── README.md.tpl                 (→ rinomina a README.md in init)
    ├── BACKLOG.md
    ├── docs/{IDENTITY,CURRENT_STATE,SESSION_HANDOFF,DECISIONS,SESSION_ERRORS_TEMPLATE}.md
    └── .claude/
        ├── settings.json
        └── hooks/{protect-credentials.sh, log-api-calls.sh}
```

**Verifiche eseguite in Blocco 3:**
- ✅ Pytest 33/33 green via `.venv/bin/python -m pytest`
- ✅ `python -m build` produce `dist/kaora_memory-0.1.0-py3-none-any.whl` con 13 file `_template/` dentro (verificato via `zipfile`)
- ✅ Smoke `kaora init /tmp/kaora-smoke --no-git-init`: 13 file creati, hook `protect-credentials.sh` eseguibile, placeholder `{{project_name}}` sostituito con basename
- ✅ Smoke `kaora init --dry-run`: piano stampato, zero file scritti
- ✅ Smoke brownfield CLAUDE.md preesistente: backup `.kaora-bak` preserva contenuto utente, nuovo CLAUDE.md contiene `@AGENTS.md`

**Verifiche eseguite 2026-05-24 / 2026-05-26:**
- ✅ **Bug UF_HIDDEN macOS RISOLTO** via wrapper self-healing in `bin/setup-dev.sh`. Stress test confermato: forzando `chflags hidden` sul `.pth`, `kaora --version` continua a funzionare e rimuove il flag al volo. Vedi BACKLOG → "Issue noti" sezione marcata RISOLTO 2026-05-24.
- ✅ **Self-dogfooding ADR-000 applicato 2026-05-26** (opzione A): `kaora init .` eseguito sul repo stesso, merge AGENTS.md guidato da agente naive in seconda sessione Claude Code (con questa sessione come revisore), `CLAUDE.md.kaora-bak` archiviato in `docs/archive/`. Validazione end-to-end del prodotto sul produttore. Report completo in `docs/DOGFOODING_REPORT.md`.
- ✅ **Rituale di chiusura sessione (§ 6bis)** aggiunto al template + AGENTS.md del repo. Scoperta operativa dal dogfooding (originariamente v0.2+, promosso a v0.1). Senza chiusura ordinata, i docs operativi divergevano dallo stato reale. Ora codificato.

## Placeholder definitivi (v0.1.1)

| Placeholder | Significato | Esempio |
|---|---|---|
| `{{project_name}}` | Nome progetto utente | `MioProgetto` |
| `{{project_oneliner}}` | Pitch in una riga | `App SaaS per dentisti italiani` |
| `{{project_path}}` | Path assoluto progetto | `/Users/alex/Desktop/mioprogetto` |
| `{{owner_name}}` | Nome builder | `Alex Rojas` |
| `{{owner_email}}` | Email | `alex@example.com` |
| `{{communication_register}}` | Tono preferito | `diretto, conciso, no preamboli` |
| `{{communication_language}}` | Lingua docs/log | `italiano` |
| `{{year}}` | Anno corrente | `2026` |

Modifica vs SESSION_HANDOFF Blocco 1: aggiunto `{{communication_language}}` per i18n futura.

## Cosa manca (priorità ordinata)

1. **Commit dogfooding 2026-05-26** — working tree pending: AGENTS.md popolato + § 6bis rituale chiusura, BACKLOG aggiornato, CURRENT_STATE/SESSION_HANDOFF aggiornati, docs/archive/CLAUDE.md.kaora-bak, bin/setup-dev.sh con wrapper self-healing, docs/DOGFOODING_REPORT.md, template/AGENTS.md con § 6bis. Suggested message: `feat(dogfooding): kaora init sul repo + rituale chiusura + wrapper UF_HIDDEN + archive bak + report`
2. **Aggiornamento template § 11 step 5** — aggiungere terza opzione "archive" oltre a conserva/elimina. Scoperta operativa dal dogfooding (v0.1, basso costo). Vedi BACKLOG → Template.
3. **`kaora_memory/check.py`** + tests — TUTTO Blocco 4 (`kaora check`: linter integrità memoria operativa)
4. **README ricco + demo** — Blocco 5 (asset di lancio in BACKLOG già pronti)
5. **Setup pubblicazione PyPI** (`.pypirc`, token test.pypi) — Blocco 6
6. **Decisione naming repo** (`kaora-memory` vs `kaora-mc` vs altri) — prima di pubblicazione PyPI, vedi BACKLOG
7. **Possibile ADR-010** "delegation depth selection: `/goal` vs delega kaora normale" — emersa durante Blocco 3 dopo test pratico di `/goal`, da scrivere quando il pattern d'uso si consolida

## Decisioni di design Blocco 3 (in attesa formalizzazione)

- **Strategia `_template/` (a):** `importlib.resources.files("kaora_memory") / "_template"` con fallback a `Path(__file__).parent.parent / "template"` per dev mode. Coerente con ADR-005 (niente symlink). Codificata in `kaora_memory/template_resolver.py`. **Potrebbe diventare ADR se vogliamo formalizzarla.**
- **Categorie file installer ADR-006 v2:** `CANONICAL_MARKDOWN` (CLAUDE/AGENTS/AGENT_BRIEF backup+overwrite), `JSON_MERGE_FILES` (.claude/settings.json), tutto il resto skip-if-exists, `RENAME` {README.md.tpl → README.md}. Codificate come costanti in `installer.py`.
- **Flag aggiuntivo `--no-git-init`** non in HANDOFF originale: necessario per testabilità (tests non devono creare repo git in `tmp_path`). Compromesso ragionevole.
- **Skill `python-pro` skippata** per installer/cli: specifica ADR-006 v2 + test scritti erano sufficienti. Coerente con ADR-009 (skill skip se specifica chiusa). Lo annoteremo in eventuale ADR-010.

## Decisioni di design Blocco 2 (Accepted)

- **ADR-005** Canonico `AGENTS.md` + import `@AGENTS.md` in `CLAUDE.md`. Supersedes ADR-003 sul *modo*, non sulla *direzione*. Elimina drift per costruzione, validato in Claude Code 2.1.119 (Test 2).
- **ADR-006 v2** Policy install brownfield in 3 categorie: markdown (backup + BOOTSTRAP-merge), JSON (merge intelligente per `.claude/settings.json`), tutto-il-resto (skip-conservative). Riscritta v2 prima di Accept perché v1 (skip + warn per settings.json) avrebbe lasciato hook kaora inattivi su brownfield.
- **ADR-007** Modalità conversazionale Operativa vs Apprendimento. Nata dall'osservazione del builder in tempo reale, applicata immediatamente.
- **ADR-008** Zero attrito per decisioni ADR `Proposed`. Step 7 del rituale: mostra ADR aperte direttamente in chat senza far aprire `docs/DECISIONS.md`. Emersa applicando ADR-007.
- **ADR-009** Sub-agente vs Read diretto: matrice di decisione su 3 variabili (size, intent, post-action) per ottimizzazione token + comportamento. Promossa da BACKLOG dopo discussione in sessione. Completa il trittico metacognitivo con ADR-001 (planning) e ADR-007 (Theory of Mind).

Tutte e 5 **Accepted** dopo Test 1-5 e revisione in chat.

## Annotazioni per Blocco 5 (README)

- Brownfield-friendly: niente warning "solo greenfield", FAQ "ho già un CLAUDE.md?" → racconta backup-first + BOOTSTRAP-merge come feature
- Hero: "Memoria operativa per agenti AI. Funziona su qualsiasi progetto, fresco o esistente."

## Asset di comunicazione collegati

- `/tmp/kaora-memory-preview.html` — landing page premium anteprima v0.1 (datata 22 maggio 00:55, da aggiornare in Blocco 5)
- `/tmp/kaora-memory-launch-essay-brief.md` — brief operativo 16 sezioni per il saggio di lancio (sessione parallela)
- `/Users/alexissilva/Desktop/kaora-memory-architecture-dashboard.html` — documento di vision astratta "LLM Wiki Extended" (datato 20 maggio, riusabile per audience accademica)
- `docs/PHILOSOPHY.md` — il *perché* del prodotto: metacognizione applicata, trittico ADR-001/007/009, reverse positioning agente umile, accessibilità cognitiva, considerazioni naming repo

## Note operative

- **Repo NON ancora pushato** su GitHub
- **Setup dev (one-liner):** `bash bin/setup-dev.sh` — crea venv, `pip install -e ".[dev]"`, installa wrapper self-healing su `.venv/bin/kaora` (auto-fix UF_HIDDEN macOS ad ogni esecuzione, ~5ms overhead), esegue `kaora --version` e pytest. Da rieseguire dopo `pip install -e .` per ripristinare il wrapper.
- **Run test:** `.venv/bin/python -m pytest` (oppure `source .venv/bin/activate && pytest`). Per agenti AI: preferire `.venv/bin/...` perché `activate` non sopravvive tra chiamate shell isolate.
- **Run CLI:** `.venv/bin/kaora init [PATH] [--force] [--dry-run] [--no-git-init]`
- **Test rapido salute:**
  ```bash
  python3 -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))" && echo "TOML OK"
  ls template/ template/docs template/.claude/hooks && echo "template completo"
  .venv/bin/python -m pytest -q && echo "TEST OK (33/33)"
  .venv/bin/kaora --version && echo "CLI OK"
  ```
- **Build wheel:** `.venv/bin/python -m build --wheel` → `dist/kaora_memory-0.1.0-py3-none-any.whl`
- **Memoria persistente Claude Code:** non ancora popolata per questo progetto
