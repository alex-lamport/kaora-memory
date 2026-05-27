# CURRENT_STATE.md — stato operativo

> Aggiornato a fine di ogni sessione. Risponde a "dove siamo, cosa funziona, cosa manca adesso".
>
> **Ultimo aggiornamento:** 2026-05-27 — **Blocco 4 chiuso**: `kaora check` linter integrità memoria operativa implementato TDD (green `29fa094` + refactor `a9e542a` + fix4 `607b5a9`). 6 categorie di check (structure/adr005/adr_state/placeholders/hooks/settings), CLI `kaora check [PATH] --strict --quiet --json`. Suite 62/62 verdi. Re-dogfooding live ha rivelato pattern coerente: `_strip_code_blocks` applicato sia in `_check_adr_state` sia in `_check_placeholders` per escludere contenuto documentario fenced in ```.

---

## Snapshot oggi

**Blocco corrente:** Blocco 4 ✅ chiuso (`kaora check`) · Blocco 5 prossimo (README ricco + asset di lancio)
**Commit ultimo in main:** `607b5a9 refactor(check): _strip_code_blocks anche in _check_placeholders`. Working tree pulito.
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
├── kaora_memory/                     ✨ ESPANSO (Blocco 3) + Blocco 4
│   ├── __init__.py                   (__version__ = "0.1.0")
│   ├── settings_merger.py            (Blocco 3) — merge JSON ADR-006 v2
│   ├── template_resolver.py          (Blocco 3) — get_template_root() con importlib.resources + fallback dev
│   ├── installer.py                  (Blocco 3) — install_template() + InstallReport, policy 3 categorie
│   ├── check.py                      ✨ NUOVO (Blocco 4) — check_project() + CheckResult/CheckReport, 6 categorie, format_text/format_json
│   └── cli.py                        ESPANSO (Blocco 4) — aggiunto sub-command `kaora check [PATH] [--strict] [--quiet] [--json]`
├── tests/                            ESPANSO (Blocco 4) — 62 test green (33 Blocco 3 + 29 Blocco 4)
│   ├── __init__.py
│   ├── test_settings_merger.py       (8 cases, Blocco 3)
│   ├── test_template_resolver.py     (3 cases, Blocco 3)
│   ├── test_init.py                  (18 cases, Blocco 3)
│   ├── test_cli.py                   (7 cases: 4 init + 3 check CLI smoke)
│   └── test_check.py                 ✨ NUOVO (Blocco 4) — 26 cases (6 categorie + 3 format + 4 refactor regression)
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

1. **README ricco + demo** — Blocco 5 (asset di lancio in BACKLOG già pronti, vedi sezione "Asset di comunicazione")
2. **Setup pubblicazione PyPI** (`.pypirc`, token test.pypi) — Blocco 6
3. **Decisione naming repo** (`kaora-memory` vs `kaora-mc` vs altri) — prima di pubblicazione PyPI, vedi BACKLOG
4. **Possibile ADR-010** "delegation depth selection: `/goal` vs delega kaora normale" — emersa durante Blocco 3 dopo test pratico di `/goal`, da scrivere quando il pattern d'uso si consolida
5. **Pulizia placeholder strutturali in `docs/SESSION_HANDOFF.md` template** — `kaora check` post-fix4 non li segnala più (sono in fenced block), ma se non sono volutamente esemplificativi conviene pulirli alla fonte (`template/docs/SESSION_HANDOFF.md`). Basso costo.

## Decisioni di design Blocco 4 (in attesa formalizzazione)

- **CheckResult / CheckReport** dataclass con `level: Literal["error", "warn", "info", "ok"]` + `category: str` + `message + hint`. Severity separata dall'exit code: `CheckReport.exit_code(strict: bool = False)` promuove warn → 1 solo se `--strict`. Separation of concerns: la funzione check non cambia comportamento in strict, solo l'exit code lo fa.
- **Soglia AGENTS.md min 50 righe** (`_AGENTS_MIN_LINES`): empirica, post-`kaora init` AGENTS canonico è ~150 righe. Sotto 50 = file mutilato.
- **`_strip_code_blocks` riusato 2 volte** (adr_state + placeholders): pattern emerso durante re-dogfooding live. Stessa radice del falso positivo "contenuto documentario interpretato come stato reale". Da formalizzare eventualmente come funzione "documentary-content-aware" se compare un terzo caso.
- **`_has_kaora_hook_command` con navigazione tipizzata** invece di `json.dumps + substring`: scelta più robusta dopo dogfooding-review, evita falsi positivi su campi arbitrari (`comment`, ecc.) che menzionano il nome dell'hook.
- **`_placeholder_scan_paths` dinamico** (root .md + docs/**/*.md escluso archive/ e PHILOSOPHY.md): scala automaticamente quando il builder aggiunge `docs/NOTES.md`, `docs/CUSTOM.md`, ecc. Hardcoded list non scalava.
- **Skill `tdd-workflows-tdd-cycle` invocata e scalata al contesto solo-builder**: la skill prescrive orchestrazione con 8 sub-agenti (architect-review, test-automator, backend-architect, code-reviewer), overkill per kaora. Pattern TDD red→green→refactor applicato direttamente dall'agente con checkpoint a Alexis ai passaggi chiave (Gate B). Coerente con § 3 "una direzione alla volta" + ADR-009 (skill skip se specifica già chiusa).

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
