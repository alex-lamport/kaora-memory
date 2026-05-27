# SESSION_HANDOFF.md — brief for the next session

> Read right after `AGENTS.md` and `CURRENT_STATE.md`.
>
> **Last session:** {{year}}-MM-DD · kaora scaffolding installed.

---

## 🟢 NEXT SESSION — Project bootstrap

### Goal

Turn the installed template into operating memory specific to **{{project_name}}**. That is: fill all remaining `<BOOTSTRAP/>` markers in the files and — if present — read and integrate the `.kaora-bak` files.

### What you'll do (sequence)

1. **Open the project in an agent** (Claude Code, Codex CLI, Cursor, Aider, or Gemini CLI)
2. The agent will run the **opening ritual** (§ 6 of `AGENTS.md`)
3. After your "go", the agent:
   - Searches for `*.kaora-bak` files in root and `docs/` — if found, reads them and proposes integration
   - Scans the `<BOOTSTRAP/>` markers across all template files
   - Drafts content autonomously by reading `package.json`, `pyproject.toml`, `Cargo.toml`, `git config`, `README.md`, folder structure
   - Asks you **1-2 targeted questions** only for the gaps (e.g. preferred tone register, personal anti-patterns)
   - Shows a full diff
   - Applies only after an explicit "go"

### Files involved in BOOTSTRAP

| File | What it fills |
|---|---|
| `AGENTS.md` | Tech stack, current stage, scope, key files, skill mapping, health check |
| `docs/IDENTITY.md` | Builder identity, communication register, anti-patterns, conventions, domain glossary |
| `docs/CURRENT_STATE.md` | Current commit/branch, existing files, working features, todo |

### Estimated time

~30 seconds of user questions · ~2-3 minutes of autonomous agent work · ~1 minute of diff review.

### What NOT to open in this first session

- ❌ Product feature implementation (memory first, code after)
- ❌ Modify `.claude/settings.json` or `hooks/` (they're pre-configured)
- ❌ Delete `.kaora-bak` (never without explicit review)

### Opening session check

```bash
ls AGENTS.md CLAUDE.md AGENT_BRIEF.md BACKLOG.md docs/ .claude/ 2>/dev/null
ls *.kaora-bak docs/*.kaora-bak 2>/dev/null  # if it returns results: backup files to read
git log --oneline -3
```

### Expected output at the end of the first session

1. All `<BOOTSTRAP/>` markers replaced with project-specific content
2. Any `.kaora-bak` content integrated into the appropriate sections
3. `docs/CURRENT_STATE.md` updated with the real post-bootstrap state
4. `docs/SESSION_HANDOFF.md` updated with the second-session brief (e.g. "we start feature X")
5. Clean commit: `chore: bootstrap operating memory via kaora`

---

## Operational notes for the first session

- **Open the agent in the project root** ({{project_path}})
- **Register:** {{communication_register}}
- **Big decisions** → new ADR in `docs/DECISIONS.md`, never freeform notes
- **If the agent gets the tone wrong** → tell it *"add anti-pattern to IDENTITY.md: ..."*
