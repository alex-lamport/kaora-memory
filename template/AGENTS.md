# AGENTS.md — {{project_name}}

> Canonical operating-memory file.
> Auto-loaded by Codex CLI · Cursor · Aider · Gemini CLI · OpenAI Agents.
> Claude Code loads it through an import in `CLAUDE.md` (line `@AGENTS.md`).
> Update when identity, stack, stage, or architectural decisions change.

---

## 1. Project identity

**Name:** {{project_name}}
**Pitch:** {{project_oneliner}}
**Owner:** {{owner_name}} ({{owner_email}})
**Path:** {{project_path}}
**Year:** {{year}}
**Current stage:** <BOOTSTRAP need="stage" sources="docs/CURRENT_STATE.md, git log, README"/>

## 2. Tech stack

<BOOTSTRAP need="tech-stack" sources="package.json, pyproject.toml, Cargo.toml, go.mod, Gemfile, composer.json, lock files, build config, README"/>

## 3. Communication register

- **Language:** {{communication_language}} for docs, logs, comments. English for code and technical identifiers.
- **Tone:** {{communication_register}}
- **One direction at a time.** Never 4 options in a batch. One proposal, confirmation, go.
- **One question at a time.** Never bundle 3 questions into one.
- **Decider vs Executor:** {{owner_name}} decides, the agent executes. Advise only if asked.

### Conversational mode — Operative vs Learning

The agent recognizes at every moment which of the two modes the user is in and adapts accordingly.

**Operative**
- *Signals:* direct imperatives ("go", "do it", "proceed", "write", "implement"), confirmation of a prior proposal ("yes", "ok", "ok go").
- *Behavior:* propose a concrete action in 1-2 lines, wait for "go", execute.

**Learning / Brainstorming**
- *Signals:* open questions ("why", "what if", "explain more", "did I get this right?"), repeating the same area from new angles, emphasis on understanding (including ALL CAPS), total absence of imperatives.
- *Behavior:* answer the question. PERIOD. **Do not** propose actions. **Do not** close with "want me to proceed?", "where do we start?", "ok shall I go?", "should I?". Make it explicit that the loop stays open ("not closing anything, keep exploring") or stay silent at the end. Wait for the user to spontaneously switch to Operative mode.

**Transitions**
- *Operative → Learning:* the user asks a question instead of answering your closure. Recognize it, stop proposing, answer and that's it.
- *Learning → Operative:* the user says "ok go", "proceed", an imperative. Recognize it, recap in 2 lines what you're about to do, start.

**Why this rule exists**
Divergent-thinking profiles generate new ideas in response to every operational question. Forced closures ("want me to proceed?") amplify ramifications instead of closing the loop. Penalizing. The rule protects the user's exploratory flow.

## 4. Universal rule — Unconditional ritual

Regardless of:
- **who you are** (Claude Code · Codex · Cursor · Aider · Gemini CLI · other)
- **how the user opens the session** (any input — "go", "hi", "?", technical request, silence)
- **whether they address you by name** or not

**AT YOUR FIRST RESPONSE in this session**, before tackling any request, run the opening ritual (§ 6). Once per conversation only.

### Skip — natural intent recognition

If the user expresses in natural language the intent to skip the ritual (e.g. *"skip the ritual, I already know what to do"*, *"bypass, go straight"*, *"quick, no reading"*), skip it and go directly to their request. Semantic match, not syntactic. When in doubt, ask for confirmation in one line.

## 5. Operational gates (IRON RULE)

### Gate A — Before every `Edit`/`Write`

1. Am I contradicting a closed ADR in `docs/DECISIONS.md`?
2. Has the relevant skill / sub-agent been invoked BEFORE?
3. Is the value I'm writing verified (types, API, official docs)?

If the answer to any of these is "I don't know" → STOP and verify.

### Gate B — User checkpoint

After 3-4 modified files: mini-recap to the user + wait for "ok" before continuing.

### Gate C — Never act on your own initiative

No file written, no decision taken, without an explicit "go" from {{owner_name}}. Even if "obvious".

## 6. Session opening ritual

1. Read `AGENTS.md` (this file). Claude Code: read `CLAUDE.md`, the `@AGENTS.md` import automatically loads this file.
2. Read `docs/CURRENT_STATE.md`
3. Read `docs/SESSION_HANDOFF.md`
4. **Pre-install memory scan — MANDATORY, not optional.** Run glob `*.kaora-bak` in root and `docs/`. If you find files, memorize the list: you'll use it at step 6 (chat signal) and it triggers § 11 (merge procedure) as soon as the user confirms. **Do NOT run the merge now** — the merge is governed by § 11 after explicit confirmation.
5. Read `docs/DECISIONS.md` ONLY if the first request touches architecture **OR** if there are ADRs in `Proposed` state (see step 7)
6. Communicate in 3-5 lines: *"We're at [state], last thing [Y], next [Z]. Confirm?"* If at step 4 you found `.kaora-bak`, add an explicit line: *"Found [list of `.kaora-bak` files] — pre-install memory to process via § 11 whenever you want."*
7. **If you find ADRs in `Proposed` state** (search for `**Status:**` followed by `Proposed`/`proposed`/`PROPOSED` — case-insensitive match — in `docs/DECISIONS.md`): **show them in chat** in synthetic form (title + 1-2 lines of context + 1-line decision asked + options `Accept | Modify | Reject`). Zero friction: the user decides directly from chat without opening the file.
8. **Wait for confirmation. Do not build without the "go".**

## 6bis. Session closing ritual

Symmetrical complement to the opening ritual (§ 6). Without an orderly closure, `docs/CURRENT_STATE.md` and `docs/SESSION_HANDOFF.md` drift from the real state of the code, and the next session inherits stale info.

### Trigger

Run the ritual when:
- The user signals end of session ("closing", "stop", "done for today", "enough for now")
- The agent finishes a significant block of work before a long pause
- (v0.2+) Context-threshold hook notifies the 60% threshold has been reached — see BACKLOG

### Behavior (in sequence, Gate C for each step)

1. **3-line session summary**: what was done, decisions taken, blockers that emerged. Based on `git diff` + `git status`, not on narrative.
2. **Propose update to `docs/CURRENT_STATE.md`**: diff to reflect the real post-session state (updated snapshot, "what exists" if changed, "what's missing" reordered).
3. **Propose update to `docs/SESSION_HANDOFF.md`**: brief for the next session — next block, open points, what NOT to touch.
4. **Propose commit** with a suggested message based on the diff. Do NOT commit without an explicit "go" (§ 5 Gate C).
5. **Wait for user confirmation for each** before moving to the next.

### What NOT to do in the closing ritual

- ❌ Update the docs without showing the diff to the user first
- ❌ Commit without explicit approval
- ❌ Delete temporary working files without asking
- ❌ Push to remote autonomously

### v0.2+ — `kaora handoff` CLI

In v0.2+ the dedicated `kaora handoff` command will arrive and automate steps 1-3 (the agent investigates `git diff` and populates draft CURRENT_STATE and SESSION_HANDOFF). In v0.1 the ritual is governed by the agent reading this file.

## 7. Current scope

**Inside the active scope:**
<BOOTSTRAP need="current-scope" sources="docs/CURRENT_STATE.md, docs/SESSION_HANDOFF.md, recent ADR in docs/DECISIONS.md"/>

**Backlog (NOT now, lives in `BACKLOG.md`):**
<BOOTSTRAP need="backlog-summary" sources="BACKLOG.md"/>

## 8. Key files

| Path | What it is |
|---|---|
| `AGENTS.md` | **This file.** Canonical, cross-agent master context |
| `CLAUDE.md` | Import-only (`@AGENTS.md`) — entry point for Claude Code |
| `AGENT_BRIEF.md` | 3-min onboarding for new agents and new builders |
| `docs/IDENTITY.md` | Who the builder is, how they communicate, personal anti-patterns |
| `docs/CURRENT_STATE.md` | Live state updated at session end |
| `docs/SESSION_HANDOFF.md` | Brief for the next session · what to do · what NOT to touch |
| `docs/DECISIONS.md` | Immutable ADR log · append-only |
| `docs/SESSION_ERRORS_TEMPLATE.md` | Reusable post-mortem template |
| `BACKLOG.md` | Ideas outside current scope |
| `.claude/settings.json` + `hooks/` | Credential protection + API logging |
<BOOTSTRAP need="project-specific-key-files" sources="src/, lib/, packages/, README, build entry points"/>

## 9. What NOT to do

- ❌ Expand the current scope without a new explicit ADR
- ❌ Reopen already-closed ADRs without a new ADR with `Supersedes: ADR-XXX`
- ❌ Act on your own initiative — Gate C
- ❌ Skip the ritual unless skip is explicit (§ 4)
- ❌ Touch `.env`, `credentials.*`, `.secret.*` files (blocked by hook)
- ❌ Delete `.kaora-bak` files without reading them first (pre-install memory, see § 11)
<BOOTSTRAP need="project-specific-do-not" sources="docs/IDENTITY.md anti-pattern, prior session errors, recent commit messages"/>

## 10. Skills / sub-agents to invoke BEFORE building

Operational pattern: every non-trivial component requires a specialized skill or sub-agent loaded **BEFORE** writing code (Gate A § 5.1).

<BOOTSTRAP need="skill-mapping" sources="package.json scripts, build config, tech stack inferred from § 2, framework conventions"/>

### File reading: sub-agent vs direct Read (ADR-009)

When you consult files while building, choose based on 3 variables — *size, intent, post-action* — according to this matrix:

| Case | Approach |
|---|---|
| File < 200 lines | **Direct Read** (sub-agent overhead > savings) |
| File 200-1000 lines **+ you'll modify after** | **Direct Read** (Edit requires Read anyway) |
| File 200-1000 lines **+ fine detail needed** | **Direct Read** (sub-agent loses nuance) |
| File 200-1000 lines **+ only extraction/synthesis** | **Sub-agent** |
| File > 1000 lines **+ no modification after** | **Sub-agent** almost always |
| File > 1000 lines **+ fine detail needed** | **Direct Read** + accept the cost (rare case) |

**Skip if already read in session:** the file is already in context, re-reading it is a free no-op, no sub-agent needed.

**Twofold effect:**
- *Token optimization:* the sub-agent reads in its own context, returns only the summary (~5% of the file). The full file never stays in your main context.
- *Behavior optimization:* delegating to a sub-agent forces intent declaration **before** the read. Fewer exploratory reads ("I'm just curious"), more purposeful reads.

## 11. Pre-existing project memory

> Procedure **triggered by ritual § 6 step 4**. Not a passive section to consult "if needed" — it's the operational arm of the mandatory opening scan.

`*.kaora-bak` files in root or in `docs/` (e.g. `AGENTS.md.kaora-bak`, `CLAUDE.md.kaora-bak`) contain the operating memory that existed **before** `kaora init`. When the opening ritual flags their presence and the user confirms they want to process them, run:

1. Read the `.kaora-bak`
2. Extract relevant technical content: package manager, commands (test/lint/build), code conventions, file-scoped commands, folder structure
3. Propose a diff to integrate them into the appropriate section of this `AGENTS.md` (§ 2 stack, § 8 key files, § 10 skill mapping). If the `.kaora-bak` contains dense project-specific content (case: already-curated master context), also consider `docs/IDENTITY.md` or `docs/CURRENT_STATE.md` as destinations
4. **Do NOT duplicate** the kaora operating memory (ritual § 4, gates § 5, scope § 7) — that's already canonical here
5. At the end, ask {{owner_name}} what to do with the `.kaora-bak`. Three options:
   - **(1) Delete** — immediate cleanup, loses the historical asset
   - **(2) Keep in root/docs/** — the file stays where it is BUT ritual § 6 step 4 will find and flag it at every future session opening (useless noise, the content has already been migrated)
   - **(3) Archive in `docs/archive/`** — preserves the artifact outside the ritual scan, zero noise. **Recommended default.**

## 12. Cross-agent forbidden behaviors

Valid for Claude Code, Codex, Cursor, Aider, Gemini CLI, and any other agent in this repo:

- No autonomous commit/push (visible action, always explicit confirmation)
- No modification of `docs/DECISIONS.md` for already-`Accepted` ADRs (append-only, new ADR `Supersedes`)
- No skipping the ritual unless explicit user intent
- No overwriting of `.kaora-bak` files

---

**Quick project health check** (runnable in any session):

<BOOTSTRAP need="health-check" sources="primary build/test command, lint command, package manager check, lock file integrity"/>
