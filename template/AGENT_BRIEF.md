# AGENT_BRIEF.md — 3-minute onboarding

> For AI agents (Claude Code, Codex, Cursor, Aider, Gemini CLI) and for new builders joining this project.
> If you already read `AGENTS.md`, here you'll only find the *why* behind the conventions.

---

## 1. What this project is at the memory layer

This repo uses **kaora-memory** — an operating-memory scaffolding for AI agents. That means:

- `AGENTS.md` (or `CLAUDE.md` via import) tells you who you are, how you work, what not to do
- `docs/CURRENT_STATE.md` tells you where you are right now
- `docs/SESSION_HANDOFF.md` tells you what to do next
- `docs/DECISIONS.md` tells you why certain choices are closed
- `docs/IDENTITY.md` tells you who the builder is and how they communicate
- `.claude/hooks/` protect credentials and log API calls

Every AI session starts with the **opening ritual** (§ 6 of `AGENTS.md`). Don't skip it unless skip is explicit.

## 2. Philosophy in 3 sentences

1. **The agent is the executor, the builder is the decider.** Never act on your own initiative.
2. **One direction at a time.** Never propose 4 options in a batch, never bundle 3 questions into one.
3. **Memory is the product.** If you don't update `docs/CURRENT_STATE.md` and `docs/SESSION_HANDOFF.md` at the end of the session, the next session starts from scratch.

## 3. What you'll do in the first session (BOOTSTRAP)

`kaora init` just copied this template into the project. Several files contain markers like:

```markdown
<BOOTSTRAP need="tech-stack" sources="package.json, pyproject.toml, ..."/>
```

In the **first AI session** of the project, after the ritual:

1. Scan `<BOOTSTRAP/>` markers across the template files
2. For each, inspect the indicated `sources` (e.g. `package.json`, `pyproject.toml`, `git log`, `README.md`)
3. Draft substitutions **autonomously** wherever possible (e.g. tech stack, build/test commands)
4. Ask **1-2 targeted questions** only for the gaps you cannot infer (e.g. preferred tone register, personal anti-patterns)
5. Show a full diff before applying
6. Apply only after an explicit "go" (Gate C)

The goal is to move the builder from manual writing (~10 min) to 2 targeted answers (~30 sec).

## 4. What the gates mean (§ 5 of `AGENTS.md`)

- **Gate A** — Before writing/editing a file: ADR respected? Skill loaded? Value verified?
- **Gate B** — After 3-4 files: summarize and wait for "ok".
- **Gate C** — Nothing is "obvious". No action without an explicit "go".

These are not suggestions. They are iron rules. If you're not sure, stop and ask.

## 5. `.kaora-bak` files — pre-existing memory

`kaora init` never destroys existing files. If the project already had:

- `CLAUDE.md` → backup in `CLAUDE.md.kaora-bak`
- `AGENTS.md` → backup in `AGENTS.md.kaora-bak`
- other existing operating-documentation files → possibly backed up with `.kaora-bak` suffix

`.kaora-bak` files are an **authoritative source** for the first BOOTSTRAP: they contain tech setup, commands, project-specific conventions the builder had already curated. Extract the technical value, integrate it into the new `AGENTS.md` or `docs/IDENTITY.md`, then ask the builder whether they can be deleted.

**Never delete a `.kaora-bak` without reading it and showing the merge to the builder.**

## 6. Quick glossary

| Term | Meaning |
|---|---|
| **Ritual** | Session opening sequence (§ 6 `AGENTS.md`). Unconditional unless natural skip. |
| **Gate A/B/C** | Three operational constraints: pre-write, checkpoint, no-initiative. |
| **ADR** | Architecture Decision Record. Lives in `docs/DECISIONS.md`, append-only, never modified after `Accepted`. |
| **`<BOOTSTRAP/>`** | Marker for sections the agent fills by inspecting the project. |
| **`.kaora-bak`** | Backup of existing files before `kaora init`. Source of value, not garbage. |
| **Natural skip** | Semantic (not syntactic) recognition of intent to skip the ritual. |
| **Decider vs Executor** | The builder decides, the agent executes. Advice only if asked. |
| **Conversational mode** | Operative (go/do) vs Learning (why/how). The agent recognizes and adapts. Never close with operational questions in Learning mode. See `AGENTS.md` § 3. |

## 7. What to do if you're confused

- Direct question in chat. One only, targeted.
- No "obvious" assumptions, no "preventive" actions.
- If your action contradicts a section of `AGENTS.md` or an `Accepted` ADR → STOP.

---

**Estimated reading time: 3 minutes. You're done. Now go back to `AGENTS.md` and follow the ritual.**
