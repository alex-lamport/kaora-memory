# Roadmap — kaora-memory

> Product vision by version. `[x]` items are done, `[ ]` are planned.
> Detailed backlog lives in [`BACKLOG.md`](BACKLOG.md).
> Founding architectural decisions live in [`docs/DECISIONS.md`](docs/DECISIONS.md).

---

## v0.1 — *Foundations* · installable MVP · **shipped** (2026-05 · `0.1.2` live on PyPI)

Goal: a Python package on PyPI whose `kaora init` installs operating-memory scaffolding into any project, fresh or existing.

- [x] Repo scaffolding — `pyproject` (hatchling, py>=3.10), flat layout, entry point `kaora`, LICENSE, README, operating-memory dogfooding
- [x] Generalized template — 13 files in `template/` with BOOTSTRAP markers + placeholders, smoke-tested hooks, ADR 005-009 Accepted
- [x] `kaora init` — Click CLI + `installer.py` (template copy) + `settings_merger.py` (intelligent JSON merge, ADR-006 v2); brownfield / greenfield / dry-run / force tests
- [x] `kaora check` — operating-memory integrity linter (unfilled placeholders, leftover BOOTSTRAP markers, pending Proposed ADRs); documentary-content-aware (ADR-010)
- [x] English i18n refactor — framework + template moved to English-first (multilingual runtime preserved via `{{communication_language}}`)
- [x] Rich README + "Product philosophy" section (applied metacognition) + brownfield FAQ
- [x] PyPI publication — `pip install kaora-memory` → `0.1.2` (0.1.1 withdrawn for metadata privacy; see [`CHANGELOG.md`](CHANGELOG.md))

### Not in v0.1
- Premium dashboard → v0.2
- `kaora handoff`, `kaora errors record`, `kaora skill install` → v0.2+
- MCP server / cloud sync → v0.3+
- Context-threshold hook (60%) → v0.2+

---

## v0.1.x — *Quality of life* · CLI status (next)

Goal: a quick command that shows operating-memory status right in the terminal — first step toward the dashboard.

- [ ] `kaora status` — ~10-line terminal output: current stage, open ADRs, last commit, files changed in 24h, anti-pattern count, post-mortem count
- [ ] Bugfix / refinement from first-week adoption feedback

---

## v0.2 — *Premium visibility* · Dashboard (target Q3 2026)

Goal: move the product from *"markdown files + agent"* to *"markdown files + agent + premium visual console"*. Wow moment for new users.

- [ ] `kaora dashboard` — local `http.server` with auto-refresh, premium glassmorphism, conventional grouped file map, filterable ADR view
- [ ] `kaora dashboard --export` — portable single-file static snapshot, server-side markdown render
- [ ] `kaora handoff` — automatic session close (generates `SESSION_HANDOFF.md` + updates `CURRENT_STATE.md`)
- [ ] `kaora errors record` — structured post-mortem wizard (immune memory)
- [ ] Context-threshold hook (60%) for Claude Code → automatic `SESSION_HANDOFF.md` proposal

---

## v0.3 — *Cross-machine* · Infrastructure (target Q4 2026)

Goal: take kaora-memory beyond the single local repo, toward distributed teams and multiple devices.

- [ ] MCP server (kaora-memory as a remote service queryable by MCP-compatible agents)
- [ ] Cloud sync of memories across devices
- [ ] `kaora skill install` — auto-registration of the skill across AI assistants (Claude Code skills dir, Cursor rules, etc.)
- [ ] Context-threshold hook ported to Codex / Cursor / Gemini CLI (session-file monitor + notification)

---

## v1.0 — *Maturity* (target 2027, or when adoption justifies it)

Goal: API stability, community governance, extended ecosystem.

- [ ] Stable CLI API, breaking changes only on major version
- [ ] Community contribution docs
- [ ] Alternative template skins (English register, terse-technical, conversational)
- [ ] Plugin ecosystem (extensions that add rules/hooks to the template without forking)

---

## Product philosophy

kaora-memory is **induced metacognition** for AI agents. Not generic scaffolding, not a memory store, not a rules engine. It forces the agent to perform the regulatory acts of metacognition (planning, monitoring, evaluating, controlling) every time it works.

**Reverse positioning** vs the AI market: where everyone sells *"powerful, autonomous, super-intelligent agent"*, kaora sells *"humble agent that recognizes its limits"*. The powerful agent is the one that knows what it doesn't know.

Theoretical references in the launch docs: Flavell (1979), Schraw & Moshman (1995), Vygotsky (cognitive scaffolding).

**True cross-agent:** works on Claude Code, Codex CLI, Cursor, Aider, Gemini CLI with the same file set (ADR-005 — canonical `AGENTS.md` + `@AGENTS.md` import in `CLAUDE.md`).

**Brownfield-friendly:** never destroys existing user work. `.kaora-bak` backup for markdown + intelligent JSON merge for `.claude/settings.json` (ADR-006).

**Cognitive accessibility:** the Operative vs Learning conversational-mode rule (ADR-007) was born from observing a neurodivergent builder in real time. The product is also an act of cognitive accessibility for divergent profiles.
