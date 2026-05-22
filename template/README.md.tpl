# {{project_name}}

> {{project_oneliner}}

**Owner:** {{owner_name}} · **Anno:** {{year}}

---

## Stato

<BOOTSTRAP need="readme-status" sources="docs/CURRENT_STATE.md stage section"/>

## Stack

<BOOTSTRAP need="readme-stack" sources="package.json, pyproject.toml, Cargo.toml, go.mod, README in .kaora-bak"/>

## Setup

<BOOTSTRAP need="readme-setup" sources="package.json scripts, Makefile, installation docs, README in .kaora-bak"/>

## Comandi

<BOOTSTRAP need="readme-commands" sources="package.json scripts, Makefile targets, justfile, taskfile"/>

## Memoria operativa AI

Questo progetto usa [kaora-memory](https://pypi.org/project/kaora-memory/) per la memoria persistente di Claude Code / Codex CLI / Cursor / Aider / Gemini CLI.

- `AGENTS.md` — master context cross-agent
- `CLAUDE.md` — import per Claude Code
- `docs/CURRENT_STATE.md` · `docs/SESSION_HANDOFF.md` · `docs/DECISIONS.md` — stato vivo + brief + ADR log

Apri il progetto in un agente e dai il via: il rituale di apertura ti aggiornerà sullo stato in 3 righe.

## Licenza

<BOOTSTRAP need="readme-license" sources="LICENSE file, package.json license, pyproject.toml license"/>
