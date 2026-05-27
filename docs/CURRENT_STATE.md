# CURRENT_STATE.md — operational state

> Updated at the end of every session. Answers "where are we, what works, what's missing right now".
>
> **Last update:** 2026-05-27 — **Mini-Block 4.5 closed**: full IT→EN i18n refactor of the entire codebase (template + root docs + Python code + tests + setup-dev.sh). English becomes the framework language; the user-agent runtime conversation language remains multilingual via the `{{communication_language}}` placeholder. Atomic regex+test fix: `_RE_ADR_*` now searches `**Status:**` (was `**Stato:**`). Suite 62/62 green throughout every wave. Sub-agent review GREEN on Wave A (10 template files), Wave B-1 (5 root files), Wave B-2 (6 docs), Wave C-1 (6 code modules), Wave C-2 (5 test files + bash script).

---

## Snapshot today

**Current block:** Block 4 ✅ closed (`kaora check`) · Block 4.5 ✅ closed (i18n EN-first refactor) · Block 5 next (rich README + launch assets — now to write in English)
**Last commit on main:** `607b5a9 refactor(check): _strip_code_blocks anche in _check_placeholders`. Working tree dirty: i18n refactor pending commit.
**Branch:** `main`
**Remote repo:** not configured yet (placeholder URL `alex-lamport/kaora-memory` in pyproject)
**Open ADRs:** none · all 000-009 Accepted

## What exists

```
kaora-memory/
├── .gitignore                        (.venv/, dist/, .pytest_cache/, ...)
├── BACKLOG.md                        (+"Known issues" section: UF_HIDDEN macOS)
├── LICENSE
├── README.md                         (minimal, will be rich in Block 5)
├── pyproject.toml                    (hatchling, py>=3.10, entry `kaora`, force-include `template/` → `kaora_memory/_template/`)
├── CLAUDE.md                         (4 lines `@AGENTS.md` — post-dogfooding 2026-05-26)
├── AGENTS.md                         ✨ NEW (post-dogfooding) — canonical master context, populated via guided merge of the .kaora-bak
├── AGENT_BRIEF.md                    ✨ NEW (post-dogfooding) — agent onboarding
├── bin/
│   └── setup-dev.sh                  ✨ UPDATED 2026-05-24 — venv + pip -e .[dev] + installs self-healing wrapper on .venv/bin/kaora (macOS UF_HIDDEN fix)
├── kaora_memory/                     ✨ EXPANDED (Block 3) + Block 4
│   ├── __init__.py                   (__version__ = "0.1.0")
│   ├── settings_merger.py            (Block 3) — JSON merge ADR-006 v2
│   ├── template_resolver.py          (Block 3) — get_template_root() with importlib.resources + dev fallback
│   ├── installer.py                  (Block 3) — install_template() + InstallReport, 3-category policy
│   ├── check.py                      ✨ NEW (Block 4) — check_project() + CheckResult/CheckReport, 6 categories, format_text/format_json
│   └── cli.py                        EXPANDED (Block 4) — added sub-command `kaora check [PATH] [--strict] [--quiet] [--json]`
├── tests/                            EXPANDED (Block 4) — 62 green tests (33 Block 3 + 29 Block 4)
│   ├── __init__.py
│   ├── test_settings_merger.py       (8 cases, Block 3)
│   ├── test_template_resolver.py     (3 cases, Block 3)
│   ├── test_init.py                  (18 cases, Block 3)
│   ├── test_cli.py                   (7 cases: 4 init + 3 check CLI smoke)
│   └── test_check.py                 ✨ NEW (Block 4) — 26 cases (6 categories + 3 format + 4 refactor regression)
├── docs/
│   ├── CURRENT_STATE.md              (this file)
│   ├── SESSION_HANDOFF.md            (Block 4 brief)
│   ├── DECISIONS.md                  (ADR 000-009 Accepted)
│   ├── PHILOSOPHY.md                 (the product's why, applied metacognition)
│   ├── IDENTITY.md                   ✨ NEW (post-dogfooding) — who the builder is, how they communicate, anti-patterns
│   ├── SESSION_ERRORS_TEMPLATE.md    ✨ NEW (post-dogfooding) — post-mortem template
│   ├── DOGFOODING_REPORT.md          ✨ NEW (post-dogfooding) — full case study of the self-dogfooding test 2026-05-26
│   └── archive/
│       └── CLAUDE.md.kaora-bak       ✨ NEW (post-dogfooding) — old master context, archived to avoid triggering the ritual scan
└── template/                         (Block 2, single source, force-included in the wheel)
    ├── AGENTS.md                     (cross-agent canonical)
    ├── CLAUDE.md                     (4 lines: @AGENTS.md)
    ├── AGENT_BRIEF.md                (agent onboarding)
    ├── README.md.tpl                 (→ renamed to README.md at init)
    ├── BACKLOG.md
    ├── docs/{IDENTITY,CURRENT_STATE,SESSION_HANDOFF,DECISIONS,SESSION_ERRORS_TEMPLATE}.md
    └── .claude/
        ├── settings.json
        └── hooks/{protect-credentials.sh, log-api-calls.sh}
```

**Verifications run in Block 3:**
- ✅ Pytest 33/33 green via `.venv/bin/python -m pytest`
- ✅ `python -m build` produces `dist/kaora_memory-0.1.0-py3-none-any.whl` with 13 `_template/` files inside (verified via `zipfile`)
- ✅ Smoke `kaora init /tmp/kaora-smoke --no-git-init`: 13 files created, `protect-credentials.sh` hook executable, `{{project_name}}` placeholder replaced with basename
- ✅ Smoke `kaora init --dry-run`: plan printed, zero files written
- ✅ Brownfield smoke pre-existing CLAUDE.md: `.kaora-bak` backup preserves user content, new CLAUDE.md contains `@AGENTS.md`

**Verifications run 2026-05-24 / 2026-05-26:**
- ✅ **macOS UF_HIDDEN bug RESOLVED** via self-healing wrapper in `bin/setup-dev.sh`. Stress test confirmed: forcing `chflags hidden` on the `.pth`, `kaora --version` keeps working and removes the flag on the fly. See BACKLOG → "Known issues" section marked RESOLVED 2026-05-24.
- ✅ **Self-dogfooding ADR-000 applied 2026-05-26** (option A): `kaora init .` run on the repo itself, guided AGENTS.md merge by a naive agent in a second Claude Code session (with this session as reviewer), `CLAUDE.md.kaora-bak` archived in `docs/archive/`. End-to-end validation of the product on its producer. Full report in `docs/DOGFOODING_REPORT.md`.
- ✅ **Session closing ritual (§ 6bis)** added to the template + repo AGENTS.md. Operational discovery from dogfooding (originally v0.2+, promoted to v0.1). Without an orderly closure, operating docs drifted from the real state. Now codified.

**Block 4.5 i18n EN-first refactor — 2026-05-27:**
- ✅ **Full IT→EN translation** of template/ (10 files), root .md (4 files), docs/ (6 files), kaora_memory/*.py (6 modules), tests/*.py (5 files), bin/setup-dev.sh. Voice preserved (direct, no preambles, "go" as imperative).
- ✅ **Atomic regex contract update**: `_RE_ADR_ACCEPTED` and `_RE_ADR_PROPOSED` in `kaora_memory/check.py` now search `**Status:**` (was `**Stato:**`). All ADR markers in template and root DECISIONS.md updated coherently. Test fixtures in `tests/test_check.py` synchronized.
- ✅ **Test-source sync**: `tests/test_cli.py:27` updated `"kaora init complete"`, `tests/test_check.py:190` updated `"lines"` to match translated production strings.
- ✅ **Multilingual runtime preserved**: `{{communication_language}}` placeholder kept intact in template. Repo root `AGENTS.md` § 3 + `docs/IDENTITY.md` § 2 explicit: "Italian for live conversation with the user. English for docs, logs, code, comments, and any written artifact on disk."
- ✅ **Sub-agent review GREEN on all 5 waves** (A, B-1, B-2, C-1, C-2). Zero critical issues. Minor polish applied inline (e.g. "where do we start?" instead of "starting point?", "intentional CI/automation use" instead of "conscious", "expected at least N" instead of "minimum expected N").
- ✅ **Pytest 62/62 green throughout every wave** (atomic incremental verification). Final `kaora check .` clean (3 known structural-placeholder WARN on BACKLOG/SESSION_HANDOFF unchanged from pre-refactor, 1 INFO on inline-backtick `Proposed` false positive in ADR-008 narrative — pre-existing pattern, not regression).

## Final placeholders (v0.1.1)

| Placeholder | Meaning | Example |
|---|---|---|
| `{{project_name}}` | User project name | `MyProject` |
| `{{project_oneliner}}` | One-line pitch | `SaaS app for Italian dentists` |
| `{{project_path}}` | Absolute project path | `/Users/alex/Desktop/myproject` |
| `{{owner_name}}` | Builder name | `Alex Rojas` |
| `{{owner_email}}` | Email | `alex@example.com` |
| `{{communication_register}}` | Preferred tone | `direct, concise, no preambles` |
| `{{communication_language}}` | Docs/log language | `english` |
| `{{year}}` | Current year | `2026` |

Change vs SESSION_HANDOFF Block 1: added `{{communication_language}}` for future i18n.

## What's missing (priority-ordered)

1. **Rich README + demo** — Block 5 (launch assets in BACKLOG already ready, see "Communication assets" section)
2. **PyPI publication setup** (`.pypirc`, test.pypi token) — Block 6
3. **Repo naming decision** (`kaora-memory` vs `kaora-mc` vs others) — before PyPI publication, see BACKLOG
4. **Possible ADR-010** "delegation depth selection: `/goal` vs normal kaora delegation" — emerged during Block 3 after a practical `/goal` test, to write when the usage pattern consolidates
5. **Structural placeholder cleanup in template `docs/SESSION_HANDOFF.md`** — `kaora check` post-fix4 no longer flags them (they're inside fenced blocks), but if they're not intentionally illustrative it's worth cleaning them at the source (`template/docs/SESSION_HANDOFF.md`). Low cost.

## Block 4 design decisions (pending formalization)

- **CheckResult / CheckReport** dataclass with `level: Literal["error", "warn", "info", "ok"]` + `category: str` + `message + hint`. Severity separate from the exit code: `CheckReport.exit_code(strict: bool = False)` promotes warn → 1 only if `--strict`. Separation of concerns: the check function doesn't change behavior in strict, only the exit code does.
- **AGENTS.md min 50-line threshold** (`_AGENTS_MIN_LINES`): empirical, post-`kaora init` the canonical AGENTS is ~150 lines. Below 50 = mutilated file.
- **`_strip_code_blocks` reused twice** (adr_state + placeholders): pattern that emerged during live re-dogfooding. Same root as the false positive "documentary content interpreted as real state". To formalize eventually as a "documentary-content-aware" function if a third case appears.
- **`_has_kaora_hook_command` with typed navigation** instead of `json.dumps + substring`: more robust choice after dogfooding-review, avoids false positives on arbitrary fields (`comment`, etc.) mentioning the hook name.
- **Dynamic `_placeholder_scan_paths`** (root .md + docs/**/*.md excluding archive/ and PHILOSOPHY.md): scales automatically when the builder adds `docs/NOTES.md`, `docs/CUSTOM.md`, etc. A hardcoded list didn't scale.
- **Skill `tdd-workflows-tdd-cycle` invoked and scaled down to the solo-builder context**: the skill prescribes orchestration with 8 sub-agents (architect-review, test-automator, backend-architect, code-reviewer), overkill for kaora. TDD red→green→refactor pattern applied directly by the agent with checkpoints to Alexis at the key transitions (Gate B). Consistent with § 3 "one direction at a time" + ADR-009 (skill skip if the spec is already closed).

## Block 3 design decisions (pending formalization)

- **`_template/` strategy (a):** `importlib.resources.files("kaora_memory") / "_template"` with fallback to `Path(__file__).parent.parent / "template"` for dev mode. Consistent with ADR-005 (no symlinks). Codified in `kaora_memory/template_resolver.py`. **Could become an ADR if we want to formalize it.**
- **Installer file categories ADR-006 v2:** `CANONICAL_MARKDOWN` (CLAUDE/AGENTS/AGENT_BRIEF backup+overwrite), `JSON_MERGE_FILES` (.claude/settings.json), everything else skip-if-exists, `RENAME` {README.md.tpl → README.md}. Codified as constants in `installer.py`.
- **Extra flag `--no-git-init`** not in the original HANDOFF: needed for testability (tests must not create a git repo in `tmp_path`). Reasonable compromise.
- **Skill `python-pro` skipped** for installer/cli: the ADR-006 v2 spec + written tests were enough. Consistent with ADR-009 (skill skip if the spec is closed). We'll note this in a possible ADR-010.

## Block 2 design decisions (Accepted)

- **ADR-005** Canonical `AGENTS.md` + import `@AGENTS.md` in `CLAUDE.md`. Supersedes ADR-003 on the *how*, not the *direction*. Eliminates drift by construction, validated in Claude Code 2.1.119 (Test 2).
- **ADR-006 v2** Brownfield install policy in 3 categories: markdown (backup + BOOTSTRAP-merge), JSON (intelligent merge for `.claude/settings.json`), everything-else (skip-conservative). Rewritten v2 before Accept because v1 (skip + warn for settings.json) would have left kaora hooks inactive on brownfield.
- **ADR-007** Conversational mode Operative vs Learning. Born from observing the builder in real time, applied immediately.
- **ADR-008** Zero friction for `Proposed` ADR decisions. Ritual step 7: show open ADRs directly in chat without making the user open `docs/DECISIONS.md`. Emerged while applying ADR-007.
- **ADR-009** Sub-agent vs direct Read: decision matrix on 3 variables (size, intent, post-action) for token + behavior optimization. Promoted from BACKLOG after in-session discussion. Completes the metacognitive triptych with ADR-001 (planning) and ADR-007 (Theory of Mind).

All 5 **Accepted** after Tests 1-5 and in-chat review.

## Annotations for Block 5 (README)

- Brownfield-friendly: no "greenfield-only" warnings, FAQ "I already have a CLAUDE.md?" → tell backup-first + BOOTSTRAP-merge as a feature
- Hero: "Operating memory for AI agents. Works on any project, fresh or existing."

## Linked communication assets

- `/tmp/kaora-memory-preview.html` — premium v0.1 preview landing page (dated May 22 00:55, to update in Block 5)
- `/tmp/kaora-memory-launch-essay-brief.md` — operational brief 16 sections for the launch essay (parallel session)
- `/Users/alexissilva/Desktop/kaora-memory-architecture-dashboard.html` — abstract vision document "LLM Wiki Extended" (dated May 20, reusable for academic audience)
- `docs/PHILOSOPHY.md` — the product's *why*: applied metacognition, ADR-001/007/009 triptych, humble-agent reverse positioning, cognitive accessibility, repo naming considerations

## Operational notes

- **Repo NOT yet pushed** to GitHub
- **Dev setup (one-liner):** `bash bin/setup-dev.sh` — creates venv, `pip install -e ".[dev]"`, installs self-healing wrapper on `.venv/bin/kaora` (auto-fix UF_HIDDEN macOS at every execution, ~5ms overhead), runs `kaora --version` and pytest. Re-run after `pip install -e .` to restore the wrapper.
- **Run tests:** `.venv/bin/python -m pytest` (or `source .venv/bin/activate && pytest`). For AI agents: prefer `.venv/bin/...` because `activate` doesn't survive between isolated shell calls.
- **Run CLI:** `.venv/bin/kaora init [PATH] [--force] [--dry-run] [--no-git-init]`
- **Quick health test:**
  ```bash
  python3 -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))" && echo "TOML OK"
  ls template/ template/docs template/.claude/hooks && echo "template complete"
  .venv/bin/python -m pytest -q && echo "TEST OK (62/62)"
  .venv/bin/kaora --version && echo "CLI OK"
  ```
- **Build wheel:** `.venv/bin/python -m build --wheel` → `dist/kaora_memory-0.1.0-py3-none-any.whl`
- **Claude Code persistent memory:** not yet populated for this project
