# CURRENT_STATE.md — operational state

> Updated at the **end** of every session. Answers "where are we, what works, what's missing right now".
>
> **Last update:** {{year}}-MM-DD — initial scaffolding via `kaora init`.

---

## Snapshot today

**Current stage:** initial scaffolding — operating memory installed, BOOTSTRAP to fill.
**Last commit:** <BOOTSTRAP need="last-commit" sources="git log -1 --oneline"/>
**Branch:** <BOOTSTRAP need="current-branch" sources="git branch --show-current"/>
**Remote repo:** <BOOTSTRAP need="remote-url" sources="git remote -v"/>

## What exists

```
{{project_name}}/
├── AGENTS.md                          (cross-agent canonical)
├── CLAUDE.md                          (Claude Code entry point, imports @AGENTS.md)
├── AGENT_BRIEF.md                     (3-min onboarding)
├── BACKLOG.md                         (ideas outside current scope)
├── docs/
│   ├── IDENTITY.md                    (who I am, how I communicate)
│   ├── CURRENT_STATE.md               (this file)
│   ├── SESSION_HANDOFF.md             (first-session brief)
│   ├── DECISIONS.md                   (ADR log, append-only)
│   └── SESSION_ERRORS_TEMPLATE.md     (post-mortem template)
└── .claude/
    ├── settings.json                  (hook config)
    └── hooks/
        ├── protect-credentials.sh
        └── log-api-calls.sh
```

<BOOTSTRAP need="existing-project-files" sources="ls -la, ls src/, ls lib/, package.json, README, prior .kaora-bak files content"/>

## What works

- ✅ kaora operating memory installed (`AGENTS.md`, `CLAUDE.md`, `docs/*`)
- ✅ Credential-protection hook active (`.claude/hooks/protect-credentials.sh`)
- ✅ API-call logging hook active (`.claude/hooks/log-api-calls.sh`)
<BOOTSTRAP need="working-features" sources="tests passing, build green, deploy status"/>

## What's missing (priority-ordered)

1. **Fill `<BOOTSTRAP/>` markers** — the first AI session must scan and fill them (see `AGENT_BRIEF.md` § 3)
2. **Read `.kaora-bak` files** if present — extract existing tech setup and integrate it
3. **First project ADR** in `docs/DECISIONS.md` — any initial architectural decision
<BOOTSTRAP need="project-todo" sources="TODO comments in code, GitHub issues if remote configured, README roadmap section"/>

## Linked communication assets

<BOOTSTRAP need="comms-assets" sources="docs/, .figma/, .canva/, marketing/, design/"/>

## Operational notes

- **Persistent memory:** not yet populated, it will grow session by session
- **`.kaora-bak` files to handle:** <BOOTSTRAP need="kaora-bak-list" sources="ls *.kaora-bak, ls docs/*.kaora-bak"/>
