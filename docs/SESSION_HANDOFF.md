# SESSION_HANDOFF.md — brief for the next session

> Read right after `CLAUDE.md` and `CURRENT_STATE.md`.
>
> **Last session:** 2026-05-28 · **Mini-Block 4.6 closed** — `_strip_code_blocks` extended from fenced-only to fenced + inline-backtick stripping (third recurrence of the documentary-content false-positive pattern). 2 new tests (62→64). ADR-010 Accepted. `kaora check .` clean on the repo itself. Working tree dirty: Block 4.6 changes pending commit.

---

## 🟢 NEXT SESSION — Block 5: rich README + launch assets (in English)

ADR 000-010 all `Accepted`. Blocks 1-4 closed. Mini-Blocks 4.5 (i18n) + 4.6 (documentary-content-aware check) closed. `kaora init` + `kaora check` both working in EN, repo passes its own linter clean. **README to write in English** (audience now: global open-source community).

---

## 🔵 OPEN POINTS

### 1. Commit the Block 4.6 cleanup before starting Block 5

Working tree currently dirty with the documentary-content-aware fix. Suggested commit (single, scope-coherent):
- `feat(check): documentary-content-aware stripping + ADR-010` — `_strip_code_blocks` extended in `kaora_memory/check.py`, 2 new tests in `tests/test_check.py` (`test_*_ignores_*_inline_backtick`), ADR-010 Accepted in `docs/DECISIONS.md`, `docs/CURRENT_STATE.md` + `docs/SESSION_HANDOFF.md` updated.

### 2. Repo naming before PyPI (BACKLOG, Block 6)

Not blocking for Block 5 but if we want to avoid publishing under the "wrong" name, decide by the end of Block 5. See `BACKLOG.md` → naming.

---

## Block 5 goal

Public launch assets. Make a repo visitor understand in 30 seconds what kaora-memory is and why they should use it. Brownfield-friendly: no "greenfield-only" warning, FAQ "I already have a CLAUDE.md?" → tell backup-first + BOOTSTRAP-merge as a *feature*.

### Expected output at the end of Block 5

1. **Rich `README.md`** replacing the current minimal one. Proposed sections (to validate in session):
   - Hero: "Operating memory for AI agents. Works on any project, fresh or existing."
   - Problem: AI agents without persistent memory, doc drift, isolated sessions
   - Solution: `pip install kaora-memory` → `kaora init` → every new agent reads `AGENTS.md` + `CLAUDE.md` and starts coherent
   - Quickstart: 3 commands `pip install kaora-memory && cd myproject && kaora init`
   - Brownfield FAQ: "I already have a CLAUDE.md?" → backup + guided merge
   - `kaora check` as a continuous validation tool (example output)
   - Link to `docs/PHILOSOPHY.md` for the *why*
2. **Flow demo** (asciicast or GIF): `kaora init myproject && kaora check myproject`. Real output visible in a few lines.
3. **Refresh existing assets** (see `CURRENT_STATE.md` → "Linked communication assets"):
   - `/tmp/kaora-memory-preview.html` — premium landing page, dated May 22, to update with new features (check, dogfooding)
   - `/tmp/kaora-memory-launch-essay-brief.md` — essay brief (parallel session)
4. **Suggested commit message:** `feat(launch): rich README + asciicast demo + landing refresh`
5. **CURRENT_STATE.md + SESSION_HANDOFF.md** updated with the Block 6 brief (PyPI publication)

### Files to create / modify

- `README.md` (full rewrite)
- Optional `docs/quickstart.md` or `docs/faq.md` if the README grows too much
- Optional `assets/demo.cast` (asciinema) or `assets/demo.gif` (terminalizer)
- Refresh `/tmp/kaora-memory-preview.html` (outside repo)

### What NOT to touch (Blocks 1-4 closed)

- ❌ `LICENSE`, `.gitignore`, `pyproject.toml` (unless a version bump is needed)
- ❌ `kaora_memory/{__init__, settings_merger, template_resolver, installer, check}.py` — stable modules
- ❌ `kaora_memory/cli.py` — unless adding CLI features tied to the README (e.g. a `kaora doctor` command if the need arises, but that's future scope)
- ❌ `template/` except for the v0.1 cleanup of structural placeholders (see OPEN POINTS 2)
- ❌ `bin/setup-dev.sh` — UF_HIDDEN self-healing wrapper stable since 2026-05-24
- ❌ Reopen `Accepted` ADRs (000-009)
- ❌ Push to GitHub — final username still to decide (see BACKLOG naming)

### Mandatory skills BEFORE building (Gate A § 5.1)

- **None mandatory.** Block 5 is writing + visual assets, doesn't require kaora-specific technical skills.
- *Optional*, if Alexis wants validated structure: `copywriting`, `marketing-psychology`, `landing-page-generator`. Case-by-case decision.

### Opening session check

```bash
cd ~/Desktop/kaora-memory
python3 -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))" && echo "TOML OK"
git log --oneline -5
.venv/bin/python -m pytest -q && echo "TEST OK (64/64)"
.venv/bin/kaora --version && echo "CLI OK"
.venv/bin/kaora check . 2>&1 | tail -20   # quick dogfooding of repo state
```

If `kaora --version` fails with `ModuleNotFoundError`: `bash bin/setup-dev.sh` (reinstalls the self-healing wrapper on `.venv/bin/kaora`). Happens if you redid `pip install -e .` bypassing the script.

---

## Operational notes for the next session

- **Open Claude Code in `~/Desktop/kaora-memory/`**
- **Register:** Italian for live conversation · direct · no preambles · one decision at a time · Operative vs Learning mode (ADR-007)
- **Framework language:** English (post Block 4.5 i18n). All docs, code, tests, scripts on disk are EN. User-agent runtime conversation remains Italian (set via `{{communication_language}}` placeholder for user projects).
- **Big decisions** → new ADR in `docs/DECISIONS.md` (ADR-008 step 6 of the ritual)
- **Block 5 mode** is **high-density writing**, not implementation. Expect much more *Learning* mode (narrative exploration, hero choice, tone of voice) than Block 4.
- **First task of Block 5:** commit the Block 4.6 cleanup (see OPEN POINTS 1) before starting any new file edits.
