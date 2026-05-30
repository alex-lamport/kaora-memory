![kaora-memory — induced metacognition for AI agents](https://raw.githubusercontent.com/alex-lamport/kaora-memory/main/docs/assets/kaora-hero.png)

**🇬🇧 English** · [🇮🇹 Italiano](README.it.md) · [🇪🇸 Español](README.es.md)

# kaora-memory

> **Induced metacognition for AI agents.**
> A project-level operating memory that makes coding agents start prepared, respect decisions, and stop before acting blindly.

`pip install kaora-memory` → `kaora init` → every agent that opens the project (Claude Code, Codex, Cursor, Gemini CLI) reads the same canonical context and starts coherent.

---

## Quickstart

```bash
pip install kaora-memory
cd myproject
kaora init
```

That's it. Open Claude Code (or any other agent) in `myproject`, type `go`, and the agent reads the operating memory before doing anything else.

Fresh project: `kaora init` writes 13 files (see below).
Existing project with a `CLAUDE.md` or `AGENTS.md` already present: `kaora init` backs them up as `.kaora-bak` and the agent merges your existing content into the canonical structure during the first session. See [Brownfield FAQ](#brownfield-faq).

### Installing on macOS

On macOS a plain `pip install` is often blocked (Python's "externally-managed environment"). Install `kaora` as an isolated CLI with **pipx**:

```bash
brew install pipx        # if you don't have it yet
pipx ensurepath
pipx install kaora-memory
```

Prefer a virtualenv? That works too:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install kaora-memory
```

If you still get `kaora: command not found` right after installing, open a new terminal window so your shell picks up the updated `PATH`.

---

## What you get

After `kaora init` your project has:

```
myproject/
├── AGENTS.md              # canonical master context, cross-agent
├── CLAUDE.md              # 4-line entry point, imports @AGENTS.md
├── AGENT_BRIEF.md         # 3-minute onboarding for any new agent
├── BACKLOG.md             # ideas outside current scope
├── docs/
│   ├── IDENTITY.md              # who the builder is, how to collaborate
│   ├── CURRENT_STATE.md         # live state, updated at session end
│   ├── SESSION_HANDOFF.md       # brief for the next session
│   ├── DECISIONS.md             # ADR log, append-only
│   └── SESSION_ERRORS_TEMPLATE.md
└── .claude/
    ├── settings.json      # Claude Code hook config
    └── hooks/             # protect-credentials.sh, log-api-calls.sh
```

All templates carry `<BOOTSTRAP/>` markers that the agent fills during the first session by inspecting the repo — no manual setup.

---

## What it really is

kaora-memory is not a memory database, a vector store, or another agent framework.

It is an **operating protocol** for AI coding agents: a small set of files, rituals, gates, and handoff rules that force the agent to perform the regulatory acts of metacognition before and during work.

Without kaora, the agent executes.

With kaora, the agent starts by asking: *what do I know, what don't I know, what has already been decided, and when should I stop?*

---

## Why it exists

AI agents have an amnesia problem. Every new session starts from zero: no memory of past decisions, no awareness of the builder's preferences, no codified rules about what to do when uncertain.

Three concrete symptoms:

1. **Doc drift** — README, ADRs, and project docs lose sync with the code because nothing forces the agent to update them at session close.
2. **Improvised action** — without explicit rules, the agent skips the right tools, writes files without confirmation, and resolves uncertainty by guessing.
3. **Context loss across agents** — a project handed off from Claude Code to Codex starts from nothing twice.

kaora-memory addresses all three by giving the project a **canonical operating memory** that any AI agent reads at session start, and a set of **codified behaviours** that the agent executes whether or not the builder remembers to ask.

---

## How it works

After `kaora init`, the project carries two independent sides.

**Memory side** — persistent files at the project root and `docs/`:
- `AGENTS.md` is the canonical master context. `CLAUDE.md` is a 4-line file that imports `AGENTS.md` (see [ADR-005](https://github.com/alex-lamport/kaora-memory/blob/main/docs/DECISIONS.md)).
- `CURRENT_STATE.md` records "where we are right now"; `SESSION_HANDOFF.md` carries the brief for the next session.
- `DECISIONS.md` is the append-only ADR log: every architectural decision lives here with its date, status, and rationale.

**Behaviour side** — rules codified inside `AGENTS.md`, enforced by every agent:
- **Opening ritual** — at the first response of every session the agent reads the operating memory, summarizes the state in 3-5 lines, and waits for confirmation.
- **Gate A** — before any `Edit` or `Write` the agent checks that a closed ADR isn't being contradicted, the right skill has been invoked, and the value is verified.
- **Gate B** — after 3-4 modified files the agent checkpoints with the builder.
- **Gate C** — no file written, no decision taken, without an explicit `go`.
- **Operative vs Learning mode** — the agent detects whether the builder is executing or exploring and adapts (see [ADR-007](https://github.com/alex-lamport/kaora-memory/blob/main/docs/DECISIONS.md)).

Memory persists across sessions and agents. Behaviour is read at session start and enforced throughout the conversation.

---

## Brownfield FAQ

> **I already have a `CLAUDE.md` (or `AGENTS.md`) in my project. What happens?**

`kaora init` backs it up as `CLAUDE.md.kaora-bak` (preserving every byte) and writes the canonical 4-line `CLAUDE.md` that imports `AGENTS.md`. At your first session after `kaora init`, the agent finds the `.kaora-bak`, reads it, and proposes a **guided merge** into the canonical `AGENTS.md`. You confirm, the merge happens, the `.kaora-bak` archives to `docs/archive/` so it doesn't trigger the opening scan at every future session.

Your pre-existing memory is **preserved as a feature**, not flagged as a warning. See [ADR-006](https://github.com/alex-lamport/kaora-memory/blob/main/docs/DECISIONS.md) for the brownfield install policy.

> **My `.claude/settings.json` already has hooks. Will `kaora init` overwrite them?**

No. `settings.json` is merged intelligently: kaora's hooks are added next to yours, conflicts are flagged. Other JSON keys remain untouched.

---

## kaora check

Run `kaora check` at any time to verify your operating memory hasn't drifted from the canonical structure.

```
$ kaora check .

ℹ️  INFO:
  [placeholders] BOOTSTRAP marker to fill in docs/IDENTITY.md: <BOOTSTRAP need="builder-identity" sources="..."/>
```

Six check categories: structure (required files), ADR-005 (canonical + import directive), ADR state (Accepted/Proposed), placeholders (structural vs BOOTSTRAP), hooks (`.claude/hooks/*.sh` executable), settings (`.claude/settings.json` references kaora hooks).

Exit code is 0 by default; `--strict` promotes warnings to errors (useful for CI). `--json` for machine output.

---

## Roadmap

v0.1 (current) — `kaora init`, `kaora check`, 13-file canonical template, brownfield install policy, opening + closing ritual.

v0.2+ — `kaora handoff` (CLI automation of session closing), `kaora dashboard` (web UI to visualize operating memory), context-threshold hook for Claude Code, multi-channel onboarding for `IDENTITY.md`.

v0.3+ — MCP server, cloud sync across devices.

Full backlog in [`BACKLOG.md`](https://github.com/alex-lamport/kaora-memory/blob/main/BACKLOG.md).

---

## Philosophy

kaora-memory is **induced metacognition for AI agents**: the memory + behaviour sides force the agent to plan before acting, monitor during action, evaluate at session close, and recognize the builder's cognitive state. The full thesis lives in [`docs/PHILOSOPHY.md`](https://github.com/alex-lamport/kaora-memory/blob/main/docs/PHILOSOPHY.md).

---

> *kaora-memory doesn't add intelligence to the agent. It adds preparation.*

---

## License

MIT — see [LICENSE](https://github.com/alex-lamport/kaora-memory/blob/main/LICENSE).

Built with kaora-memory itself. The repo passes its own `kaora check`, and every ADR in [`docs/DECISIONS.md`](https://github.com/alex-lamport/kaora-memory/blob/main/docs/DECISIONS.md) was decided through the same gates that kaora codifies for other projects. See [`docs/DOGFOODING_REPORT.md`](https://github.com/alex-lamport/kaora-memory/blob/main/docs/DOGFOODING_REPORT.md) for the self-application story.

---

Built by [Alexis Rojas](https://x.com/alex_lamports) — part of the KAORA research/workspace around AI agents, memory, and human-agent collaboration.
