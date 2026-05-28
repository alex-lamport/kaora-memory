# Changelog

All notable changes to `kaora-memory` are documented here.
Format inspired by [Keep a Changelog](https://keepachangelog.com/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [0.1.2] — 2026-05-28 (current)

Privacy hardening over 0.1.1. **Zero code or template changes.** Same `kaora init` and `kaora check` behaviour. Suite 68/68 green.

### Removed
- Personal email from PyPI `[project].authors` metadata — replaced with the GitHub no-reply address (`192558850+alex-lamport@users.noreply.github.com`).
- Personal email from `AGENTS.md` Owner line (shipped in commit `4794ee4` right after the v0.1.2 cut).
- Section §8 of `docs/PHILOSOPHY.md` (references to private dev assets in `/tmp/` and `~/Desktop/`).
- Absolute local paths (`/Users/<owner>/...`) from `AGENTS.md`, `BACKLOG.md`, `docs/CURRENT_STATE.md`, `docs/SESSION_HANDOFF.md`, `docs/DOGFOODING_REPORT.md` — replaced with `~/` or anonymous placeholders.

### Added
- "Block N" terminology glossary at the top of `docs/PHILOSOPHY.md` and `docs/DOGFOODING_REPORT.md`. Explains internal builder shorthand for external readers.
- Italian/English commit-message reading note in `docs/DOGFOODING_REPORT.md`. Clarifies that pre-Block 4.5 commits quoted in the report are in Italian (the builder's working language at the time), not stylistic drift.
- Closure marker on `docs/PHILOSOPHY.md` §7 — naming decision recorded as `kaora-memory` confirmed on 2026-05-28.

### Note on v0.1.1
**v0.1.1 was withdrawn from PyPI on 2026-05-28** as part of this privacy hardening cycle. It was functionally identical to v0.1.2 — the only difference was the leaked Gmail in the package metadata. The withdrawal targeted PyPI metadata cleanup, not the code. Anyone who installed v0.1.1 in the few hours it was live got the same code and template; `pip install kaora-memory` resolves to v0.1.2 automatically.

---

## [0.1.1] — 2026-05-28 — withdrawn

Brownfield safety hardening. Pre-publish review by parallel code-review + security-audit sub-agents surfaced three issues against the *"Works on any project, fresh or existing"* promise. All three fixed in this release. Suite 64 → 68 green (+4 regression tests).

### Added
- **`.kaora-bak` rotation** (F1) — re-running `kaora init` no longer silently overwrites the original `.kaora-bak`. Subsequent backups rotate to `.kaora-bak.1`, `.kaora-bak.2`, etc. The original pre-kaora content is preserved indefinitely.
- **Surfaced merge warnings** (F2) — when `.claude/settings.json` cannot be merged (invalid JSON or unexpected structure), the install report now prints an explicit `warnings (N):` block instead of a silent `skipped`. Users know when kaora hooks were *not* installed.
- **`template/.gitignore` shipped** (F3) — greenfield projects now get a `.gitignore` that excludes `logs/`, `.env*`, `*.pem`, `*.pypirc`, plus standard Python/IDE defaults. Protects against accidental commits of bearer tokens captured by `log-api-calls.sh`.

### Withdrawn on 2026-05-28
See v0.1.2 note above. Functionally identical to v0.1.2. Install v0.1.2 instead.

---

## [0.1.0] — internal pre-release

Internal version used for the first `twine upload --repository testpypi` cycle on 2026-05-28. Never published to PyPI prod. Carried the same `kaora init` + `kaora check` baseline that ships in v0.1.1+.

---

For the full pre-release development trail (Blocks 1 through 4.6, the metacognitive framing, ADRs 000-010), see [`docs/DECISIONS.md`](docs/DECISIONS.md) and [`docs/DOGFOODING_REPORT.md`](docs/DOGFOODING_REPORT.md).
