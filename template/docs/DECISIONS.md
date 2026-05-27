# DECISIONS.md — immutable ADR log

> Architectural Decision Records. **Append-only.** A closed decision is only reopened by a new ADR that explicitly supersedes it (`Supersedes: ADR-XXX`).
>
> Format: date · context · decision · rejected alternatives · consequences.

---

## ADR-000 — Adopting kaora-memory for the project's operating memory

**Date:** {{year}}-MM-DD
**Status:** Accepted

### Context

{{project_name}} is {{project_oneliner}}. The work involves multiple sessions with AI agents (Claude Code, Codex, Cursor, Aider, Gemini CLI). Without an explicit operating memory, every session starts from scratch: the agent doesn't know the current state, which decisions are already closed, or which communication register the builder prefers.

### Decision

We adopt **kaora-memory** as the operating-memory scaffolding for this project.

Concrete consequences:
- `AGENTS.md` (canonical) + `CLAUDE.md` (import) as master context
- `docs/CURRENT_STATE.md` updated at the end of every session
- `docs/SESSION_HANDOFF.md` as the brief for the next session
- `docs/DECISIONS.md` (this file) as the immutable log of architectural choices
- `docs/IDENTITY.md` with builder identity and anti-patterns
- `.claude/hooks/` for credential protection and API logging
- Mandatory session opening ritual (see `AGENTS.md` § 6)
- Three operational gates: pre-write, checkpoint, no-initiative (see `AGENTS.md` § 5)

### Rejected alternatives

- **Implicit memory** (no files, just conversation): doesn't scale beyond the first session. Every new agent starts from scratch.
- **A single rich README.md**: README serves humans discovering the project, not agents operating on it. Mixing the two ruins both.
- **Only `CLAUDE.md`**: cuts out Codex / Cursor / Aider / Gemini CLI, which look for `AGENTS.md`.
- **External Notion / Linear / Confluence docs**: agents don't read them automatically, access friction, outside the repo.

### Consequences

- At the end of every session I must update `CURRENT_STATE.md` and `SESSION_HANDOFF.md`. Without this, the value collapses.
- Architecture decisions → always a new ADR here, never freeform notes in code or README.
- The scaffolding adds ~10 files to the repo. Accepted trade-off: more files, less time wasted at every new AI session.

---

<BOOTSTRAP need="initial-project-adr" sources="prior major decisions visible from git log, README mentioned architectural choices, framework lock-in"/>

<!--
To add a new ADR:

## ADR-NNN — Decision title

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Deprecated | Superseded
**Supersedes:** ADR-XXX (only if applicable)

### Context
[Why this decision is needed, what has changed]

### Decision
[What was decided, clearly]

### Rejected alternatives
[At least 2 options considered and why not]

### Consequences
[What changes operationally, accepted trade-offs]
-->

---

## ADR versioning

- v0.1.0 — ADR-000 (scaffolding via kaora-memory · {{year}}-MM-DD)
