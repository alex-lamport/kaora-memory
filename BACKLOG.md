# Backlog

> Ideas and features for future versions. NOT part of v0.1.
> Anything that comes up during development and isn't strictly v0.1
> lands here, not in the code.

---

## Future CLI commands

- `kaora handoff` (v0.2+) — CLI automation of the session closing ritual (see § 6bis of AGENTS.md, already active via agent in v0.1). Investigates `git diff` autonomously, generates draft `SESSION_HANDOFF.md` + `CURRENT_STATE.md`, proposes a commit. The user just confirms.
- `kaora errors record` — wizard to write a structured post-mortem (immune memory)
- `kaora skill install` — automated skill registration into the various AI assistants (Claude Code skills dir, Cursor rules, etc.)

## Runtime automations

### Session closing ritual — IMPLEMENTED in v0.1 (2026-05-26)

Originally planned for v0.2+. Promoted to v0.1 after an operational discovery during dogfooding: the absence of a closing ritual symmetric to the opening ritual caused `docs/CURRENT_STATE.md` and `docs/SESSION_HANDOFF.md` to drift from the real state of the code (stale info inherited by the next session).

**Status:** § 6bis "Session closing ritual" added to `template/AGENTS.md` + `AGENTS.md` of the kaora-memory repo. The agent runs an orderly closure when the user signals end-of-session: summary → CURRENT_STATE update → SESSION_HANDOFF update → commit proposal. Gate C for each step.

See `docs/DOGFOODING_REPORT.md` § 4 for the discovery context.

### Context-threshold hook at 60% → auto-propose closure (v0.2+)

Automatic external trigger for the closing ritual (§ 6bis). When the host system reaches 60% context usage, it injects a message to the agent that runs the ritual before the session breaks from saturation.

- Claude Code only in the first release (mature hook system, Stop / context-threshold event available)
- In v0.2+ port to Codex / Cursor / Gemini CLI via an external wrapper (session file monitor + notification)

## Infrastructure

- MCP server (kaora-memory as a remote service)
- Cloud sync for memories across devices

### Premium dashboard — `kaora dashboard` (target v0.2)

Web UI to visualize the project's operating memory. Design reference:
`~/Desktop/kaora/kaora-dashboard.html` (existing asset, built for the Kaora Multi-Agent Platform project, needs adaptation).

**Planned tech stack:**
- Frontend: HTML/CSS/JS single-file, marked.js + highlight.js from CDN (or inline)
- Aesthetic: glassmorphism with `color-mix(in oklch)`, animated mesh gradient, anti-banding SVG noise, dark cyan/purple/orange palette
- Typography: Inter (UI) + Cinzel (decorative) + JetBrains Mono (code)
- Layout: 320px sidebar (brand + stage + search + file list) + content area (header meta + markdown rendering)

**Two possible strategies:**

**Strategy A — local server (default for dev):**
```
$ kaora dashboard
  Server started on http://localhost:7777 — browser opened. Ctrl+C to stop.
```
- `kaora_memory/dashboard.py` spawns `http.server` (stdlib, zero new dependencies)
- Auto-refresh every 30s, sees live changes during AI sessions
- Process dies on close

**Strategy B — static export (shareable snapshot):**
```
$ kaora dashboard --export
  Generated docs/dashboard.html — open from file://...
```
- Server-side markdown rendering (`markdown-it-py` or `mistletoe`), inline-everything in HTML
- Single portable file, zero runtime infrastructure, shareable via email/Slack
- Frozen snapshot, must be regenerated after changes

**Adaptations needed vs the design reference:**
1. Parametric branding: `{{project_name}}`, `{{project_oneliner}}` instead of `KAORA Multi-Agent Platform`
2. Abstract stage system: read `Current block` from `docs/CURRENT_STATE.md` via regex, NOT hardcoded "Stage 0/1/2"
3. Conventional file map by groups:
   - **Master context:** `CLAUDE.md`, `AGENTS.md`
   - **Onboarding:** `AGENT_BRIEF.md`
   - **Live state:** `docs/CURRENT_STATE.md`, `docs/SESSION_HANDOFF.md`
   - **Decisions:** `docs/DECISIONS.md` (ADR sub-view filterable by Status)
   - **Identity:** `docs/IDENTITY.md`
   - **Errors:** `docs/SESSION_ERRORS_TEMPLATE.md` + `docs/SESSION_ERRORS/*` if it exists
   - **Backlog:** `BACKLOG.md`
4. JSON index generated programmatically from the directory content
5. Dedicated ADR view with Accepted/Proposed/Rejected/Superseded filters (visual pattern of ADR-008)

**Roadmap timing:**
- v0.2.0 → Strategy A (`kaora dashboard`)
- v0.2.1 → Strategy B (`kaora dashboard --export`)

## Operational patterns

(open space — the sub-agent vs direct Read rule has been promoted to **ADR-009 Accepted** in `docs/DECISIONS.md` and codified in `template/AGENTS.md` § 10 on May 22, 2026, already active in v0.1)

## Template

- Full agent-driven bootstrap (the agent investigates and fills the `<BOOTSTRAP/>` markers by reading git config, README, package.json, etc.) — design defined, implementation in Block 2/3
- Alternative skins for the template (e.g. English register, terse-technical register, conversational register)

### `.kaora-bak` — third "archive" option in § 11 step 5 — IMPLEMENTED 2026-05-27 (v0.1)

Today `template/AGENTS.md` § 11 step 5 says:
> *"At the end, ask {{owner_name}} whether to keep `.kaora-bak` files or delete them"*

Operational discovery from the 2026-05-26 dogfooding: reality offers **three options**, not two:

1. **Delete** — loses the historical artifact
2. **Keep in root/docs/** — ritual § 6 step 4 finds it and signals it at every session opening (useless noise, the content has already been migrated)
3. **Archive** in `docs/archive/CLAUDE.md.kaora-bak` (or equivalent) — preserves the artifact, doesn't trigger the scan, demonstrability of the "kaora migrates pre-existing memory" pattern

The naive agent during the guided merge of the kaora-memory repo itself **spontaneously invented** option 3 — a signal that the convention is natural and only needs to be formalized in the template.

**Fix:** update `template/AGENTS.md` § 11 step 5 to:
> *"At the end, ask {{owner_name}} what to do with the `.kaora-bak`: (1) delete, (2) keep in current location, (3) archive in `docs/archive/` to avoid triggering the opening scan. Recommended default: (3)."*

Cost: 1 Edit to template/AGENTS.md, ~30 seconds. Zero impact on tests (no Python code involved). To close before the v0.1 launch.

### Multi-channel onboarding for `docs/IDENTITY.md` (target v0.2)

Today `kaora init` creates `docs/IDENTITY.md` with BOOTSTRAP markers and the agent fills them in the first session by investigating the repo (git config, README, package files). It works but assumes the builder's identity is deducible from the code — often it isn't.

Many users have **identity already written elsewhere**: a local personal dossier (e.g. `~/Desktop/linkedin/dossier-alexis.md`), an X / LinkedIn / Instagram profile, GitHub bio, a private manifesto. The agent should **ask the user which channel they prefer** to populate IDENTITY.md, instead of inferring only from the repo.

**Proposed behavior:**
At the first post-init session, the agent detects IDENTITY.md with open BOOTSTRAP markers and asks:
> *"To fill docs/IDENTITY.md (who you are as a builder), which source do you want to use?*
> *(1) Local dossier already written (tell me where)*
> *(2) X / LinkedIn / Instagram profile (I'll fetch and analyze public posts)*
> *(3) GitHub bio + recent commits (more technical)*
> *(4) I'll ask you 5 targeted questions (zero pre-existing asset)*
> *Which do you prefer?"*

The user chooses, the agent runs the channel and proposes the diff for IDENTITY.md.

**Likely implementation:**
- Convention in the template `AGENT_BRIEF.md` + `template/AGENTS.md` § 11 (or new § dedicated to onboarding)
- Pattern coherent with ADR-002 (zero friction) and ADR-008 (zero-friction in-chat decisions)
- No additional Python code needed if handled entirely at the agent layer
- Optional CLI helper `kaora identity --source dossier=PATH | x=@handle | ig=@handle | github=user | ask` to automate scraping (requires Apify/social API integration → cost)

**Why:** it's the leap from "project memory" to "memory of the builder behind the project". Strong differentiator for professional builders who already have an articulated personal brand and want to reuse it instead of re-explaining it for every new repo.

**How to apply:** when v0.1 is closed, the first thing in v0.2.

## v0.1 launch assets (target Block 5-6)

To finalize when we reach the rich README + PyPI publication:

- **Premium landing page:** `<private landing asset>` (1008 lines, dated May 22 00:55, v0.1 preview)
  - Update: ADR numbering (from "Stage 1 Phase 8 ADR-034" → "Block 2 closed · ADR 000-009"), add the metacognitive framing that emerged on May 22, realign the 6 layers to the real template files, cite ADR-005/006/007/008/009
- **Launch essay (operational brief):** `<private essay brief>` (16 sections, generated the evening of May 22) — handed off to the parallel session writing the essay
- **Abstract vision document:** `<private vision asset>` (dated May 20, "Memory Architecture LLM Wiki Extended") — reusable as an asset of philosophical depth for academic/intellectual audiences, otherwise to archive if not realigned

### Narrative strategy: where to show the philosophy (target Block 5-6)

The metacognitive philosophy (see [`docs/PHILOSOPHY.md`](docs/PHILOSOPHY.md)) is one of the main narrative pillars of the product and should be distributed across multiple channels with depth calibrated to audience:

| Channel | Depth | What to show of the philosophy |
|---|---|---|
| **Premium landing page** (updated `<private landing asset>`) | 🔴 Central | Dedicated "What it really is" section with metacognitive thesis + rules→acts mapping + humble-vs-arrogant agent narrative frame + 1-2 Flavell/Vygotsky citations in footnote |
| **Repo README.md** | 🟡 Synthetic | Practical hero + philosophical tagline + "Philosophy in 3 paragraphs" section + link to `docs/PHILOSOPHY.md` |
| **Launch essay** (Substack/Medium) | 🔴 Maximally expanded | Full argument ~3000 words. Brief in `<private essay brief>` already has the structure |
| **`kaora dashboard` v0.2 runtime** | 🟢 Light | "Why kaora" tab or link to PHILOSOPHY.md on GitHub. The user already using the product wants project state, not manifesto |
| **PyPI page** | 🟢 One line | Description: *"Operating memory for AI agents. Induced metacognition — the humble agent recognizes its limits."* + link to GitHub |
| **X/Twitter launch thread** | 🟡 Hook + demonstration | 10-15 tweets with concrete examples (code, ADR screenshots, `claude go` demo) |

**Landing page ordering strategy:** *solve first, tell the why after*. Practical hero → demo → "how it works" → "**what it really is**" (here goes the philosophy) → setup. Inverting loses the technical users looking for a solution.

**Narrative sub-plot to leverage:** ADR-007 was born from a real-time observation of a neurodivergent builder = a case of **documented human-agent co-evolution**. No other AI product has this story. Goes in the essay as a chapter, gets cited on the landing.

## Repo naming decision (target Block 5, before PyPI publication)

The metacognitive framing that emerged on May 22 makes `kaora-memory` an under-representative name for the product. See [`docs/PHILOSOPHY.md`](docs/PHILOSOPHY.md) § 7 for the candidate matrix (`kaora-metacognition`, `kaora-meta`, `kaora-mc`, `kaora-mind`, `kaora-self`, `kaora-thinks`, `kaora-core`, status quo). Decision needed **before** the PyPI publication (Block 6), because renaming a published package is painful.

## Known issues / Minor bugs

### macOS `UF_HIDDEN` on the `.pth` file generated by hatchling editable install — RESOLVED 2026-05-24

**Original symptom:** after `pip install -e .` on macOS with Python 3.13, the `kaora` command fails with `ModuleNotFoundError: No module named 'kaora_memory'`. Cause: hatchling creates `_editable_impl_kaora_memory.pth` with the macOS `UF_HIDDEN` flag. Python 3.13's `site.py` explicitly rejects `.pth` files with `UF_HIDDEN` ("Skipping hidden .pth file"), so the source path isn't added to `sys.path`. Aggravating factor: macOS spontaneously re-applies `UF_HIDDEN` even without `pip install` in between (likely APFS metadata or Spotlight indexing).

**Adopted solution (2026-05-24):** self-healing bash wrapper on `.venv/bin/kaora`. `bin/setup-dev.sh` overwrites the Python script generated by hatchling with a bash wrapper that runs `chflags nohidden` on the `.pth` at every invocation, then runs `exec python -m kaora_memory.cli "$@"`. Idempotent, costs ~5ms, doesn't block normal venv operations (e.g. `rm -rf .venv`, future `pip install -e .`). Stress test confirmed: forcing `chflags hidden` on the `.pth`, `kaora --version` keeps working and removes the flag on the fly.

**Behavior after fix:**
- The `UF_HIDDEN` flag can come back as often as it wants — irrelevant, it's removed on the fly at the next `kaora` invocation
- `pip install -e .` regenerates the original `.venv/bin/kaora` script (overwriting the wrapper) → just rerun `bash bin/setup-dev.sh` to restore it

**Scope:** affects only developers on macOS in editable install. End users (`pip install kaora-memory` from PyPI) don't have this problem (the wheel doesn't generate `.pth`, and `bin/` isn't distributed in the wheel).

**Remaining (non-blocking) actions:**
- Optional upstream issue to hatchling asking whether the `.pth` generator can avoid triggering `UF_HIDDEN`
- Monitor whether future hatchling versions change `.pth` naming (the wrapper uses glob `*kaora*.pth`, breaks silently if it changes)

## Pre-publish checklist (Block 6)

To run **immediately before** every `twine upload` to PyPI. Reason: the wheel in `dist/` doesn't regenerate itself when you modify code. Publishing a stale wheel = end user gets `ModuleNotFoundError` or missing features (bug discovered in test #3 of session 2026-05-24: wheel was dated May 23 before `cli.py` and `installer.py` existed).

```bash
# 1. Throw away old artifacts
rm -rf dist/ build/ *.egg-info/

# 2. Rebuild wheel + sdist from scratch
.venv/bin/python -m build

# 3. Test install in a completely clean venv
python3 -m venv /tmp/publish-test
/tmp/publish-test/bin/pip install dist/kaora_memory-*.whl
/tmp/publish-test/bin/kaora --version          # → kaora, version 0.1.0
/tmp/publish-test/bin/kaora init /tmp/publish-init-test --no-git-init
find /tmp/publish-init-test -type f | wc -l    # → 13
rm -rf /tmp/publish-test /tmp/publish-init-test

# 4. Test PyPI staging
.venv/bin/twine upload --repository testpypi dist/*

# 5. Test install from testpypi in another clean venv
python3 -m venv /tmp/testpypi-test
/tmp/testpypi-test/bin/pip install --index-url https://test.pypi.org/simple/ kaora-memory
/tmp/testpypi-test/bin/kaora --version
rm -rf /tmp/testpypi-test

# 6. Only after all green steps: PyPI production
.venv/bin/twine upload dist/*
```

**Future automation (v0.2+):** replace with GitHub Actions on release tag. See also UF_HIDDEN issue above (impacts only macOS dev, not end users).

## Ideas to evaluate

(open space — anything that emerges goes here before entering v0.x)
