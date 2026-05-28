# DOGFOODING_REPORT.md — Self-test case study 2026-05-26

> Report of the self-dogfooding test of the `kaora-memory` v0.1 product on the repository that produces it.
> ADR-000 honored literally (option A): the `kaora-memory` repo is the first real user of its own product.

> **Reading note 1 — "Block N" terminology**
> "Block N" is internal builder shorthand for a v0.1 development milestone (Block 1 = scaffolding, Block 2 = template, Block 3 = `kaora init` CLI, Block 4 = `kaora check` CLI, Block 4.5 = English i18n refactor, Block 4.6 = documentary-content-aware linter, Block 5 = launch assets, Block 6 = PyPI publication). Full glossary in [PHILOSOPHY.md](PHILOSOPHY.md).

> **Reading note 2 — commit-message language**
> Commit messages quoted verbatim from `git log` in this report reflect the builder's working language at the time of the commit. Commits up to Block 4.4 (early May 2026) are in Italian; from the i18n refactor of 2026-05-27 (Block 4.5) onwards, all commits, docs, and code are in English. The IT/EN mix in citations is therefore historical, not stylistic drift.

---

## 1. Context

**Date:** 2026-05-26
**Version tested:** kaora-memory v0.1 (Block 3 closed, pre-Block 4)
**Tester:** Alexis Rojas (builder) + 2 parallel Claude Code sessions (Claude Opus 4.7 1M context)
**Setup:**
- Session A — *reviewer with full context*: opened in the repo before the test, has the entire construction history, acts as a real-time quality controller
- Session B — *naive agent*: opened in the repo right after `kaora init .`, starts fresh following only the operating-memory files (AGENTS.md, IDENTITY.md, DECISIONS.md, CURRENT_STATE.md, SESSION_HANDOFF.md)

**Pre-test repo state:**
- Rich `CLAUDE.md` (~10 sections, 8.7KB, kaora-memory-specific master context)
- `AGENTS.md` non-existent
- Operating memory hand-written in pre-kaora style
- 33/33 pytest green, buildable wheel, greenfield/dry-run/brownfield smoke tests validated on `tmp_path`

## 2. What was tested

The full brownfield user experience flow:

```
1. kaora init . (pure CLI, from system terminal)
2. Open a new AI session in the post-init repo
3. Run opening ritual § 6 (including the mandatory § 4 scan of *.kaora-bak files)
4. Signal the .kaora-bak in chat (step 6 of the ritual)
5. § 11 procedure for guided merge of the .kaora-bak into AGENTS.md
6. Distribute the bak content into the new canonical schema
7. § 11 step 5 — final decision on the fate of the .kaora-bak
```

## 3. Results

### 3.1 Python layer (kaora init)

✅ **Clean execution.** `kaora init .` produced exactly what was foreseen by ADR-006 v2:

| Category | Files | Outcome |
|---|---|---|
| Created from scratch | `AGENTS.md`, `AGENT_BRIEF.md`, `docs/IDENTITY.md`, `docs/SESSION_ERRORS_TEMPLATE.md`, `.claude/hooks/log-api-calls.sh`, `.claude/hooks/protect-credentials.sh`, `.claude/settings.json` | ✅ 7 files written |
| Backup + overwrite | `CLAUDE.md` (rich → `.kaora-bak`, new 4-line `@AGENTS.md`) | ✅ Backup created |
| Skip-preserved | `BACKLOG.md`, `README.md`, `docs/CURRENT_STATE.md`, `docs/DECISIONS.md`, `docs/SESSION_HANDOFF.md` | ✅ Living memory intact |
| Untouched | `pyproject.toml`, `LICENSE`, `.gitignore`, `kaora_memory/`, `tests/`, `template/`, `bin/`, `docs/PHILOSOPHY.md` | ✅ Code and custom assets untouched |

Zero crashes, zero losses. The first-validation dry-run (run 2026-05-22 and 2026-05-26) matched exactly the real execution.

### 3.2 Agent layer — opening ritual

✅ **Mandatory § 6 step 4 scan working.** The naive agent (session B), having read the reinforced `template/AGENTS.md`, did:

1. Ran glob `*.kaora-bak` in root and `docs/`
2. Found `CLAUDE.md.kaora-bak`
3. Signaled in chat according to the prescribed format: *"Found CLAUDE.md.kaora-bak in root — pre-install memory to process via § 11 whenever you want"*
4. Waited for user confirmation before processing (didn't try the merge proactively)

Exemplary behavior. The reinforcement applied to template § 6 step 4 — from "if you find a bak..." (passive section) to "mandatory scan + in-chat signal" — eliminated the risk of silent skip.

### 3.3 Agent layer — conversational mode (ADR-007)

⚠️ **First violation, then correction.** In the opening summary, the naive agent closed with **three questions in one**: *"Confirm starting with Block 4? And how do we handle the two open points?"* — explicit violation of § 3 "one question at a time".

After the reviewer (session A) intervention flagging the violation, in subsequent proposals the agent respected the rule: **one final question only** ("which form for the owner — X handle / gmail / both?"). Lesson absorbed in-context.

**Product implication:** the ADR-007 rule in the template is readable by the agent but not always internalized at the first turn. Recurring pattern observed, worth monitoring in future user dogfooding.

### 3.4 Agent layer — guided merge § 11

✅ **Excellent behavior.** The naive agent ran § 11 with higher quality than what was specified:

- **Preliminary comparison:** before proposing the diff, it read the new canonical `AGENTS.md` + `docs/IDENTITY.md` to identify what was already covered. Explicit intent: avoid duplications (§ 11 step 4).
- **Stale vs valid distinction:** it used the bak for tech stack/identity (still true), but used `CURRENT_STATE.md` + `SESSION_HANDOFF.md` for "current scope" because the bak said "Block 2 next" while reality was "Block 4 next".
- **Diff structured by section (A-G):** one atomic diff per section, easy to approve piece by piece.
- **Full transparency:** it explicitly stated what it was NOT bringing in (§§ 3-6 mode/ritual/gate, § 10 ADR-009 matrix) because already canonical in the template.

7 diffs proposed, 7 approved. Session A flagged micro-imprecisions (stale info inherited from a non-updated `CURRENT_STATE.md`), non-blocking.

### 3.5 § 11 step 5 — final decision

🎯 **Unexpected added value.** The template § 11 step 5 prescribes two options: *"ask whether to keep or delete"*. The naive agent **spontaneously invented a third option**:

> *"If you keep it for historical archival, I suggest moving it outside root/docs/ (e.g. docs/archive/) so it doesn't trigger the scan."*

Recognition of the implicit trade-off:
- Delete → lose the historical asset
- Keep in root → ritual § 6 step 4 finds it at every session opening, useless noise
- Archive → preserve the artifact, no noise, demonstrability of the migration pattern

Final decision: option 3 (archive). The file lives in `docs/archive/CLAUDE.md.kaora-bak`.

**Product implication:** discovery to formalize in the template before v0.1 (BACKLOG → Template item). The agent demonstrated that the "archive" convention is intuitive — it just needs to be codified.

## 4. Limit that emerged

⚠️ **A symmetric closing ritual is missing.**

`CURRENT_STATE.md` and `SESSION_HANDOFF.md` contained stale info at the time of the dogfooding:
- "Last commit: ce588e9" → reality: 66e0c48 on main
- "Self-dogfooding ADR-000 dry-run validated, full application open" → reality: we were applying that very step
- "UF_HIDDEN bug, chflags workaround" → reality: resolved via self-healing wrapper 2026-05-24

The naive agent faithfully reported that obsolete data, because the kaora template has a well-formalized **opening** ritual (§ 6) but **no closing ritual** that forces the operating docs to update at session end.

**Consequence:** every future session inherits the doc drift of the previous session, in proportion to how much closure was "neglected".

**Fix introduced in v0.1 (post-dogfooding):** new § 6bis "Session closing ritual" section in the template, which instructs the agent to:
1. Synthesize the session in 3 lines
2. Propose CURRENT_STATE.md update
3. Propose SESSION_HANDOFF.md update
4. Propose commit with suggested message

In v0.2+ it will be supported by the dedicated `kaora handoff` CLI command (see BACKLOG → Future CLI commands).

## 5. Minor non-blocking bug

⚠️ macOS UF_HIDDEN self-healing wrapper — handled automatically.

The `bin/setup-dev.sh` script updated 2026-05-24 installs a wrapper on `.venv/bin/kaora` that runs `chflags nohidden` at every invocation. During dogfooding the UF_HIDDEN flag had already been spontaneously re-applied by macOS, but `kaora init .` ran without issues thanks to the wrapper. Indirect test of the UF_HIDDEN fix passed.

## 6. Conclusions

**Full test passed.** The v0.1 product worked end-to-end on its own producer, both at the Python layer (kaora init) and at the agent layer (ritual + guided merge).

**Narrative value of dogfooding:**
- Structural validation of the product in real conditions (no mocked tests on `tmp_path`)
- Case of **co-evolution**: dogfooding revealed two micro-features to add before launch (archive option, closing ritual). Both now codified in v0.1.
- Concrete narrative material for Block 5 (README + launch assets): *"we used kaora-memory on kaora-memory itself. Here's what happened."*

**Reusable pattern for future brownfield users:**
1. Run `kaora init . --dry-run` to validate the plan
2. Run `kaora init .` (pure CLI, terminal)
3. Open a new AI agent in the post-init repo
4. Let the opening ritual find and signal the `.kaora-bak`
5. Confirm "ok process" → the agent runs § 11 with preliminary anti-duplication comparison, stale/valid distinction, section-by-section diff
6. Approve the diffs
7. Archive the bak in `docs/archive/` (option 3 recommended)
8. Run the closing ritual: update CURRENT_STATE + SESSION_HANDOFF + commit

Total time for an average brownfield: 20-40 minutes (most of it spent approving diffs).

## 7. Next v0.1 steps derived from this report

1. **Added § 6bis Closing ritual** in `template/AGENTS.md` — ✅ done 2026-05-26
2. **Updated § 11 step 5** with the third "archive" option — ✅ done 2026-05-27 (commit `a9518d6`)
3. **Block 4: `kaora check`** — ✅ closed 2026-05-27 (5 commits, 62 green tests, 4 consistent refinements)
4. **Block 5: rich README + launch assets** — 🟡 next (this report = narrative input)
5. **Block 6: PyPI publication + repo naming** — 🔵 pending

## 8. Follow-up verifications (post-dogfooding)

Validation iterations run **after** the original 2026-05-26 dogfooding. They document product behavior under repeated real conditions.

### 8.1 — 2026-05-27 morning — Opening-ritual validation post-update

**Setup:** new Claude Code session opened in the repo after the dogfooding session had applied § 6bis (closing ritual) + commit `a9518d6` + archive of the `.kaora-bak` to `docs/archive/`.

**Result:**
- ✅ **Clean `.kaora-bak` scan**: the glob in root + `docs/` direct-children found nothing (the file archived in `docs/archive/` is correctly excluded from the ritual scan). Confirms that option 3 "archive" solves the opening-session noise problem.
- ✅ **Proactive drift detection**: the naive agent noticed on its own initiative that `CURRENT_STATE.md` + `SESSION_HANDOFF.md` marked *"dogfooding commit pending"* while `a9518d6` already existed in `git log`. It proposed an auto-correction, applied in commit `eabae39`.
- ✅ **Indirect validation of § 6bis**: the closing ritual applied in the previous session had left the docs in a testable state (limited residual drift, narrative of work done consistent with git).

**Product implication:** the opening-session drift detection pattern is NOT explicitly codified today in ritual § 6, it emerged as natural agent behavior. To evaluate whether to add it as an explicit step ("step 4.5: compare CURRENT_STATE.md with git log latest commit; if divergent, flag") in v0.2. Item to add to BACKLOG.

### 8.2 — 2026-05-27 evening — Block 4 `kaora check` with dual-session pattern

**Setup:** new Claude Code session to implement Block 4. In parallel, an expert review session (this report written by that one).

**Flow executed:**
1. **Skill loading**: `tdd-workflows-tdd-cycle` loaded before code (Gate A § 5.1)
2. **Proposed test spec**: 22 tests in `test_check.py` + 3 CLI in `test_cli.py`, mapped 1:1 to the 6 checks in SESSION_HANDOFF. Approved by the reviewer with micro-precisions (explicit distinction WARN structural vs INFO BOOTSTRAP).
3. **Red phase**: 24 tests written, all fail for the right reasons (`ModuleNotFoundError` + `Error: No such command 'check'`). Existing 33-test suite intact (zero regression).
4. **Green phase**: `kaora_memory/check.py` (299 LOC) implemented incrementally by category (structure → adr005 → adr_state → placeholders → hooks → settings → formatters). Pattern *"pytest after every category, synthetic green delta"* (see memory `feedback_tdd_incrementale_per_categoria.md`).
5. **Base feature commit**: `29fa094 feat(cli): kaora check operating-memory integrity linter`. 57/57 green (33 + 24).
6. **Post-green review**: the reviewer read the full `check.py` and identified 4 design trade-offs (false positive "Proposed" in code-block, stringy settings, hardcoded files, statically-only Literal Level). The first 3 substantial.
7. **User decision**: close the refinements in v0.1 rather than postpone to v0.2 (explicit preference: *"v0.1 closed well > v0.1 with 3 things to remember"*).
8. **Refactor commit 1**: `a9e542a refactor(check): code-block exclusion + struct parsing + dynamic .md scan`. 3 targeted fixes, each preceded by its own red test. 61/61 green.
9. **Live re-dogfooding**: `kaora check .` on the repo revealed 2 new real WARNs on `docs/SESSION_HANDOFF.md` (placeholders `{{...}}` inside fenced code block of the spec). **Same pattern as the false "Proposed"** in placeholder version.
10. **Refactor commit 2**: `607b5a9 refactor(check): _strip_code_blocks anche in _check_placeholders`. 1 line of code + 1 test, reuses the existing function. 62/62 green.
11. **Closing ritual § 6bis**: applied by the naive agent. CURRENT_STATE + SESSION_HANDOFF diffs approved by the reviewer, commit `dae7126 chore(handoff): chiusura sessione Blocco 4 + brief Blocco 5`.

**Pattern that emerged (4 fixes, one same root):**

All 4 refinements reduce to the pattern **"documentary content ≠ real content"**:
- ADR Proposed inside a template example → don't count
- Placeholder `{{...}}` inside the kaora check spec → don't count
- `<BOOTSTRAP/>` marker inside template example → don't count
- Hook name inside an arbitrary field (comment, key) → don't count as an active hook

All fixes use the same technique: separate the extraction of relevant content from the documentary structure that describes it. Strong narrative material for Block 5: the product learned to distinguish "documentation about X" from "real X", which is exactly the metacognitive philosophy we sell in the manifesto.

**Final Block 4 result:**
- 62 green tests (33 + 21 + 4 + 1 + 3 CLI)
- 5 Block 4 commits (`29fa094` → `a9e542a` → `607b5a9` → `dae7126`) + 1 drift `eabae39` at opening
- Persistent memory enriched with `feedback_tdd_incrementale_per_categoria.md` (step-by-step TDD pattern for multi-category modules)

### 8.3 — Dual-session pattern (naive agent + expert reviewer)

Validated over two consecutive cycles (dogfooding 2026-05-26 + Block 4 2026-05-27): the pair *"naive executive session with fresh context + reviewer session with full context"* produces higher quality than a single agent.

**Observed advantages:**
- The naive agent naturally finds template extension points (the third archive option emerged spontaneously)
- The reviewer catches synthesis imprecisions and design trade-offs the executor doesn't see from its angle
- The test-first + code-review-before-commit pattern catches errors before they become debt
- Communication via the user as a bridge: the user passes diff/output, the reviewer comments, the user synthesizes the answer for the naive agent

**Observed limitations:**
- Cognitive cost for the user (must copy-paste back and forth)
- Latency: every round trip adds 30-60 seconds
- Doesn't scale to >2 simultaneous sessions (overhead becomes dominant)

**Product implication:** the dual-session workflow **is not part of the kaora-memory product today** (it's a meta usage pattern). Worth considering for launch documentation (Block 5): could become a README chapter *"How to use kaora-memory in high-complexity scenarios"*. Or stay as a practice discovered by advanced users without being codified in the product.

---

*Authoritative report, any future dogfooding sessions add a new dedicated report (e.g. `docs/DOGFOODING_REPORT_v0.1.1.md`) rather than modifying this one. The "Follow-up verifications" sections (§ 8+) are the exception: they document validation iterations on the same v0.1 cycle, not new cycles.*
