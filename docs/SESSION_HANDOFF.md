# SESSION_HANDOFF.md — brief for the next session

> Read right after `CLAUDE.md` and `CURRENT_STATE.md`.
>
> **Last session:** 2026-05-28 afternoon · **Technical launch fully closed.** `kaora-memory` is publicly installable: `pip install kaora-memory` resolves to **0.1.2** worldwide. Public repo on `alex-lamport/kaora-memory`, 2 GitHub Releases tagged (v0.1.1 + v0.1.2), CHANGELOG.md created, 0 PII in tracked files. Block 4.6 (ADR-010) + Block 6 (PyPI publication) both closed in this session. README v0.1 published (Block 5 first half). What's still open: launch communication assets.

---

## 🟢 NEXT SESSION — Block 5 (second half): launch communication

Open Claude Code in `~/Desktop/kaora-memory/`. The product is **live and shippable**; this session is purely about **narrative and reach**. Expect heavy *Learning* mode (audience choice, hook selection, voice calibration), much less *Operative* mode than the technical sessions.

**Three voice-of-builder decisions are pending from chat 2026-05-28 (please surface them at the opening ritual):**

1. **Language of the X thread** — EN (global OSS audience), IT (existing X audience that knows you from DeFi), or bilingual (one thread per language, more work). Open.
2. **Framing of the pivot** — this is the first non-DeFi public post from the builder. Three concrete framings were floated in chat:
   - *(a)* normalize as a side project: *"not DeFi today, side project I just shipped, take or leave"* — low commitment, preserves existing-audience contract.
   - *(b)* explicit strategic pivot: *"from today I'll talk about AI tooling too, here's the first piece"* — redefines the contract.
   - *(c)* topical post, no transition meta-talk — neutral, lets the topic carry itself.
3. **Neurodivergent subplot** (PHILOSOPHY § 6: ADR-007 was born from real-time co-evolution between the neurodivergent builder and the agent — no other AI product has that documented origin) — include as 2 closing tweets, hint at 1, or keep out of the first release.

These three decisions condition everything downstream. The agent must NOT draft tweets before they're chosen.

---

## 🔵 OPEN POINTS (priority order)

### 1. X thread — primary launch asset

Target: 10-15 tweets. Concrete examples > claims (one tweet with terminal output of `kaora init` beats five tweets of marketing prose). Brownfield is a differentiator vs Mem0 / Letta / claude-memory-mcp — surface it. Dogfooding (the repo passes its own linter) is unique narrative material. Iconic closing pull-quote already EN-translated: *"kaora-memory doesn't add intelligence to the agent. It adds preparation."*

### 2. LinkedIn post — single dense piece

~200-300 words. More structured tone. Audience: technical decision-makers, AI/devtools recruiters, OSS observers. Lower frequency than X — one shot, well-aimed.

### 3. Landing refresh (off-repo `<private landing asset>`)

1008-line HTML, currently dated May 22 with stale framing. Issues already audited (see CURRENT_STATE → Block 6 section): dates, roadmap shows "Block 1 done / Block 2 next" (reality is everything closed), dogfooding presented as future (it's done), "Repo · in arrivo" (it's live), invented `ADR-034` / `SESSION_ERRORS_2026_05_21` examples, six-layer architecture includes one host-Claude layer that isn't kaora's, "tre micro-feature" hero promise never delivered in the page, pre-metacognitive framing throughout. Refresh integrates the metacognitive philosophy + ADR-010 + real current state.

### 4. Launch essay (~3000 words, off-repo `<private essay brief>`)

16-section brief already written. Audience: Substack/Medium readers. Most expanded form of the message. Can be drafted in parallel — does NOT block the X thread + LinkedIn.

### 5. asciicast / GIF demo

Concrete: terminal session of `kaora init myproject && kaora check myproject`. Real output in a few lines, paste into the README and the landing. Asciinema or terminalizer.

---

## What you can NOT touch in this session

- ❌ Anything in `kaora_memory/` (stable code, 68/68 tests must remain green)
- ❌ `template/` (immutable per published wheel — changes here require a 0.1.3 cut with PyPI re-publish)
- ❌ `pyproject.toml` (no version bump unless the next CLI/template change is shipped)
- ❌ ADRs 000-010 (all Accepted, append-only policy)
- ❌ `README.md` substantial rewrite (it's the public hero now; small polish is OK, full rewrite is not)
- ❌ `CHANGELOG.md` history entries (append-only)
- ❌ Force push (the 2 tags v0.1.1, v0.1.2 must remain on their commits)

## Skills suggested BEFORE drafting (Gate A § 5.1)

- `copywriting` — for the X thread voice
- `marketing-psychology` — to calibrate hook + closure
- `brand-storytelling` — for the narrative arc across thread + LinkedIn + essay
- `launch-strategy` — if a sequencing decision needs to be made (thread first then LinkedIn next day, or simultaneous, etc.)
- *Optional:* `linkedin-cli` if direct posting from terminal is wanted later

None are mandatory — Block 5 communication is judgment-heavy work. Skills are recommended but the builder's voice matters more.

## Opening session check

```bash
cd ~/Desktop/kaora-memory
git log --oneline -10
git tag --list "v*"
.venv/bin/python -m pytest -q && echo "TEST OK (68/68)"
.venv/bin/kaora --version && echo "CLI OK (0.1.2)"
.venv/bin/kaora check . 2>&1 | head -3
curl -sf https://pypi.org/pypi/kaora-memory/json | python3 -c "import sys, json; print('PyPI latest:', json.load(sys.stdin)['info']['version'])"
```

If anything fails: nothing to fix on disk — diagnose only. The product is shipped; this session must NOT regress the technical state.

---

## Operational notes for the next session

- **Open Claude Code in `~/Desktop/kaora-memory/`**
- **Register:** Italian for live conversation · direct · no preambles · one decision at a time · Operative vs Learning mode (ADR-007)
- **Framework language:** English on disk (post Block 4.5 i18n). User-agent conversation remains Italian.
- **Mode:** **high-density writing**, not implementation. Most of the session will be *Learning*. Forced operative closures ("want me to draft now?") are penalizing for the builder's exploratory flow — see PHILOSOPHY § 6 + ADR-007.
- **First task of the next session:** at the opening ritual, surface the 3 pending voice decisions (language / framing / neurodivergent subplot) and wait. Do NOT draft tweets, posts, or essay paragraphs before they're resolved.
- **What to commit:** if drafts of thread / LinkedIn / essay are written, they can live as off-repo working files (the repo doesn't need them as tracked content). If they're committed, suggest a `docs/launch/` subfolder kept out of the wheel.
- **Reference assets:** README.md (locked v0.1), PHILOSOPHY.md (full thesis), DOGFOODING_REPORT.md (concrete narrative material), DECISIONS.md (ADRs that can be cited), CHANGELOG.md (factual storia delle release).
