# CURRENT_STATE.md — operational state

> Updated at the end of every session. Answers "where are we, what works, what's missing right now".
>
> **Last update:** 2026-05-29 (launch session) — **X launch thread published.** First public non-DeFi post is live: 10-tweet thread (EN · continuity build-in-public · 1 ND hint) + hero banner, init screenshot, and a 57s demo clip (init → opening-ritual recap → brownfield merge proposal). Repo polished for launch: README hero banner, metacognition-first tagline + "What it really is" section + KAORA footer, macOS install note, `AGENTS.md` drift fixed, ROADMAP translated EN. 6 commits pushed; product unchanged (`0.1.2` live). README now trilingual (EN/IT/ES, flag switcher, sub-agent reviewed); 2 backlog items added (anti-overload comm rule + robust/cross-agent config merge). Public-voice profile saved to persistent memory. **Prior close (2026-05-28):** **Block 4.6 + Block 5 partial + Block 6 closed in one session.** kaora-memory is now public on PyPI: `pip install kaora-memory` resolves to **0.1.2** globally. GitHub repo public on `alex-lamport/kaora-memory` with README, CHANGELOG, 2 GitHub Releases (v0.1.1 + v0.1.2). v0.1.1 was withdrawn from PyPI after publication for metadata-privacy hardening (Gmail leak in author field) — functionally identical to v0.1.2. 0 PII in tracked files. Suite 68/68 green, `kaora check .` clean (0 ERROR / 0 WARN).

---

## Snapshot today

**Current block:** Block 4/4.5/4.6 ✅ · Block 6 ✅ (PyPI 0.1.2) · **Block 5 in progress** — README rich ✅ · **X launch thread published ✅ (2026-05-29)**; still open: LinkedIn, launch essay, landing refresh
**Last commit on main:** `4426323 docs(readme): metacognition-first hero + "What it really is" + KAORA footer` — 4 launch-polish commits this session (`f9df0fc` AGENTS drift + ROADMAP EN · `79528c8` macOS note · `e02cdbf` hero banner · `4426323` metacognition README). Working tree clean.
**Branch:** `main` · pushed to `origin/main` since `473fb4c`
**Remote repo:** **live and public** at https://github.com/alex-lamport/kaora-memory · 2 GitHub Releases tagged (v0.1.1, v0.1.2) · description + topics configured
**PyPI:** **live** at https://pypi.org/project/kaora-memory/0.1.2/ · `pip install kaora-memory` works globally · 0.1.1 deleted from PyPI (metadata privacy)
**Open ADRs:** none · all 000-010 Accepted · naming decided 2026-05-28 = `kaora-memory` confirmed (PHILOSOPHY § 7 branch 3)

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
- ✅ **Pytest 62/62 green throughout every wave** (atomic incremental verification). Committed as `e351b95 refactor(i18n): translate framework + template to English` + `03f3f86 refactor(check): regex match Status + Python code/tests/script sync`.

**Block 4.6 documentary-content-aware stripping — 2026-05-28:**
- ✅ **Third recurrence of the documentary-content false-positive pattern** caught via dogfooding on the repo itself: 7 false-positive WARN (citations of structural placeholders inside inline backticks in tables and prose) + 1 false-positive INFO (`**Status:** Proposed` cited in ADR-008 narrative).
- ✅ **`_strip_code_blocks` extended** in `kaora_memory/check.py`: from fenced-only to fenced + inline-backtick stripping. Two sequential regex substitutions, fenced first (multiline DOTALL), inline second (`[^`\n]+` single-line). Function semantics broadened, name preserved.
- ✅ **2 new RED→GREEN tests** in `tests/test_check.py` (62→64): `test_adr_state_ignores_proposed_in_inline_backtick`, `test_placeholders_ignores_open_inside_inline_backtick`. TDD red verified before fix, green confirmed after.
- ✅ **ADR-010 Accepted** in `docs/DECISIONS.md`: formalizes "documentary citation ≠ live state" as the pattern. Edge case "double-backtick markdown spans" explicitly YAGNI'd, with a self-imposed convention not to use that syntax in operating-memory docs.
- ✅ **`kaora check .` post-fix**: 0 ERROR, 0 WARN, 7 INFO BOOTSTRAP (all genuine markers in BACKLOG.md + docs/IDENTITY.md awaiting fill — not false positives).
- ✅ Committed in `4651fe7`.

**Block 5 partial close — README + naming + Block 6 entanglement — 2026-05-28 afternoon:**
- ✅ **Rich README v0.1 published** (141 lines EN, Quickstart-before-Why pattern à la mise/uv/ripgrep). 10 sections: Hero · Quickstart · What you get · Why it exists · How it works · Brownfield FAQ · `kaora check` · Roadmap · Philosophy (1 paragraph) · License + dogfooding signal + iconic closing pull-quote. Committed in `2795f19`.
- ✅ **Naming decision recorded:** `kaora-memory` confirmed (PHILOSOPHY § 7 branch 3). Rationale: ecosystem consistency over framing-in-name; philosophical framing carried by tagline. Sealed by the first PyPI publication.
- 🟡 **Launch communication assets still open** (this is the half of Block 5 that's pending):
  - Landing refresh (off-repo `<private landing asset>`, 1008 lines HTML, May 22 — needs roadmap/date/framing update + metacognitive narrative incorporation)
  - X thread (10-15 tweets, concrete examples + brownfield + dogfooding hook)
  - LinkedIn post (single dense piece + invite)
  - Launch essay (~3000 words, brief exists at `<private essay brief>`)
  - asciicast / GIF demo of `kaora init && kaora check`

**Block 6 PyPI publication — 2026-05-28 afternoon:**
- ✅ **`pyproject.toml` polished:** description translated IT→EN, obsolete TODO removed (commit `60ab133`).
- ✅ **GitHub repo created public:** `alex-lamport/kaora-memory`, topics configured, README rendering verified. Push pre-launch in `473fb4c`.
- ✅ **Parallel sub-agent pre-publish review:** 1 code-reviewer + 1 security-auditor on the 5 core Python modules + the 2 shipped bash hooks + git history secret scan + supply chain (click, hatchling). Findings: 3 blocking brownfield-safety issues (F1+F2+F3) + 1 material security warning (no `template/.gitignore`). All fixed before broader distribution. No real secrets or unsafe shell patterns in the hooks. Commit `446d4bb`.
- ✅ **First PyPI publish (0.1.1):** twine check PASSED → testpypi upload + clean-venv install verify → PyPI prod upload + clean-venv install verify (`pip install kaora-memory` global). Tag `v0.1.1` + GitHub Release v0.1.1.
- ✅ **External review feedback round (0.1.2):** revealed Gmail PII in PyPI author email + local user paths (`/Users/alexissilva/...`) in public docs + "Block N" jargon opacity + PHILOSOPHY § 7 still "open" + IT/EN commit-language mix in DOGFOODING. All fixed via doc-only commit `1f61193` and a second publication 0.1.2. 0.1.1 deleted from PyPI (JSON 404). Tag `v0.1.2` + GitHub Release v0.1.2. Final cleanup of an overlooked Gmail in `AGENTS.md` Owner line committed in `4794ee4`. CHANGELOG.md created in `d70c7cc` to document the 0.1.1 withdrawal honestly.
- ✅ **Post-publication verification (anyone in the world):** `pip install kaora-memory` → 0.1.2 → `kaora --version` = 0.1.2 → `kaora init` writes 14 files (incl. F3-shipped `.gitignore` with `logs/`).
- 9 commits total on `main` since the morning session opened, all pushed.

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

1. **Launch communication assets** — second half of Block 5 (still open). In priority order: X thread (10-15 tweets) · LinkedIn post · landing refresh · launch essay · asciicast demo. To be handled in a separate Claude session dedicated to high-density writing, not in this technical-shipping session.
2. **Possible ADR-011** "delegation depth selection: `/goal` vs normal kaora delegation" — emerged during Block 3 after a practical `/goal` test, to write when the usage pattern consolidates (renumbered from ADR-010 after Block 4.6 took that slot).
3. **Documentation of known issues for 0.1.3** (from pre-publish sub-agent reviews, captured but not blocking): `template_resolver` zipped-wheel edge case · installer `rglob` symlink-follow · non-atomic write (Ctrl-C race) · log-api-calls.sh bearer-token redaction · chmod 0o755 location-blind for future `template/*.sh`.

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

- `<private landing asset>` — premium v0.1 preview landing page (dated May 22 00:55, to update in Block 5)
- `<private essay brief>` — operational brief 16 sections for the launch essay (parallel session)
- `<private vision asset>` — abstract vision document "LLM Wiki Extended" (dated May 20, reusable for academic audience)
- `docs/PHILOSOPHY.md` — the product's *why*: applied metacognition, ADR-001/007/009 triptych, humble-agent reverse positioning, cognitive accessibility, repo naming considerations

## Operational notes

- **Repo PUBLIC on GitHub:** https://github.com/alex-lamport/kaora-memory · `origin/main` tracks `main`
- **PyPI live:** https://pypi.org/project/kaora-memory/0.1.2/ · users install via `pip install kaora-memory` (no flag needed)
- **Dev setup (one-liner):** `bash bin/setup-dev.sh` — creates venv, `pip install -e ".[dev]"`, installs self-healing wrapper on `.venv/bin/kaora` (auto-fix UF_HIDDEN macOS at every execution, ~5ms overhead), runs `kaora --version` and pytest. Re-run after `pip install -e .` to restore the wrapper.
- **Run tests:** `.venv/bin/python -m pytest` (or `source .venv/bin/activate && pytest`). For AI agents: prefer `.venv/bin/...` because `activate` doesn't survive between isolated shell calls.
- **Run CLI:** `.venv/bin/kaora init [PATH] [--force] [--dry-run] [--no-git-init]`
- **Quick health test:**
  ```bash
  python3 -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))" && echo "TOML OK"
  ls template/ template/docs template/.claude/hooks && echo "template complete"
  .venv/bin/python -m pytest -q && echo "TEST OK (68/68)"
  .venv/bin/kaora --version && echo "CLI OK (0.1.2)"
  ```
- **Build wheel:** `.venv/bin/python -m build` → `dist/kaora_memory-0.1.2-{whl,tar.gz}`. Pre-publish checklist in BACKLOG.md.
- **PyPI credentials:** `~/.pypirc` configured with token-based auth for both `pypi` and `testpypi` (chmod 600, never committed). Re-publish flow: rebuild wheel → testpypi upload + verify install → prod upload + verify install → tag + GitHub Release.
- **Claude Code persistent memory:** populated for this project (`MEMORY.md` index, lives under user-memory area).
