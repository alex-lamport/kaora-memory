# {{project_name}}

> {{project_oneliner}}

**Owner:** {{owner_name}} · **Year:** {{year}}

---

## Status

<BOOTSTRAP need="readme-status" sources="docs/CURRENT_STATE.md stage section"/>

## Stack

<BOOTSTRAP need="readme-stack" sources="package.json, pyproject.toml, Cargo.toml, go.mod, README in .kaora-bak"/>

## Setup

<BOOTSTRAP need="readme-setup" sources="package.json scripts, Makefile, installation docs, README in .kaora-bak"/>

## Commands

<BOOTSTRAP need="readme-commands" sources="package.json scripts, Makefile targets, justfile, taskfile"/>

## AI operating memory

This project uses [kaora-memory](https://pypi.org/project/kaora-memory/) for persistent memory across Claude Code / Codex CLI / Cursor / Aider / Gemini CLI.

- `AGENTS.md` — cross-agent master context
- `CLAUDE.md` — import for Claude Code
- `docs/CURRENT_STATE.md` · `docs/SESSION_HANDOFF.md` · `docs/DECISIONS.md` — live state + brief + ADR log

Open the project in an agent and give it the go: the opening ritual will catch you up on the state in 3 lines.

## License

<BOOTSTRAP need="readme-license" sources="LICENSE file, package.json license, pyproject.toml license"/>
