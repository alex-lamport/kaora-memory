# SESSION_ERRORS_TEMPLATE.md — post-mortem template for a failed session

> Copy this file into `docs/SESSION_ERRORS/YYYY-MM-DD-short-slug.md` when a session produces a significant error (wrong decision, code that broke things, time lost to a misunderstanding, agent anti-pattern not corrected in time).
>
> **Goal:** turn every error into codified learning. The file ends up in `docs/IDENTITY.md` § 3 (anti-patterns) or `docs/DECISIONS.md` (new ADR) depending on its nature.

---

## What happened

[Factual description, 2-4 lines. No accusatory tone.]

## When

- **Date:** YYYY-MM-DD
- **Agent involved:** [Claude Code / Codex / Cursor / Aider / Gemini CLI / other]
- **Model:** [e.g. claude-sonnet-4.6, gpt-5, gemini-2.5-pro]
- **Session duration:** ~X minutes
- **Estimated time lost:** ~Y minutes

## What you wanted to achieve

[Original session goal]

## What went wrong

[Error chronology. Indicate files, commands, decisions at the exact point where the session deviated.]

## Root cause

[One main cause. If there are several, pick the one without which the error wouldn't have happened.]

Probable category (circle one):
- Skipped opening ritual
- Gate A violation (skill not loaded before Write)
- Gate B violation (3-4 files modified without checkpoint)
- Gate C violation (initiative action without "go")
- Existing ADR ignored
- Anti-pattern in IDENTITY.md not respected
- Pre-existing memory (`.kaora-bak`) not read
- User spec ambiguous, agent didn't ask
- Genuine bug in code / tool / library

## What we repaired

[Commands/diffs/decisions that closed the incident]

## What to codify to prevent repetition

Pick **one** of the actions below (can be combined):

- [ ] **Anti-pattern in `docs/IDENTITY.md` § 3** — add a concrete line
- [ ] **New ADR in `docs/DECISIONS.md`** — if it's an architectural decision
- [ ] **Skill to add in `AGENTS.md` § 10** — if domain knowledge was missing
- [ ] **Hook in `.claude/hooks/`** — if automated prevention is feasible
- [ ] **Edit to `AGENTS.md` § 9 (What NOT to do)** — if it's a universal rule

Concretely:

```
[diff or added text]
```

## Lesson in one sentence

[A single, sharp sentence. This is what you'll remember 3 months from now.]

---

**Indexing:** at the end of this post-mortem, update `docs/CURRENT_STATE.md` with an optional note under "Operational notes" if active memory is needed in future sessions.
