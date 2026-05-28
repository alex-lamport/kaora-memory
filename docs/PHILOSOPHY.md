# PHILOSOPHY.md — the why of the product

> Conceptual document. Answers *"why kaora-memory exists, what it really is, where it sits relative to the AI market"*.
> Companion to [DECISIONS.md](DECISIONS.md) (the *how*) and [CURRENT_STATE.md](CURRENT_STATE.md) (the *what now*).
> Home for reflections emerged in development sessions that need to be preserved beyond individual ADRs.

> **Reading note — "Block N" terminology**
> Throughout this document and [DOGFOODING_REPORT.md](DOGFOODING_REPORT.md), *Block N* refers to a development milestone of the v0.1 roadmap:
> Block 1 = repo scaffolding · Block 2 = template generalization · Block 3 = `kaora init` CLI · Block 4 = `kaora check` CLI · Block 4.5 = English i18n refactor · Block 4.6 = documentary-content-aware linter (ADR-010) · Block 5 = README + launch assets · Block 6 = PyPI publication. It is internal builder shorthand, not product terminology.

---

## 1. Central thesis

**kaora-memory is induced metacognition for AI agents.**

Not generic scaffolding, not a memory store, not a rules engine. It is the first tool that **forces the agent to perform the regulatory acts of metacognition** every time it works: plan before acting, monitor during action, evaluate retrospectively, control its initiative impulses, recognize the interlocutor's cognitive state.

Without kaora: the agent executes.
With kaora: the agent **thinks about its own thinking** while executing.

## 2. Theoretical references

The metaphor holds academically, it is not cosmetic. Three sources:

- **Flavell (1979)** — foundational distinction between *metacognitive knowledge* (knowing what you know and what you do NOT know) and *metacognitive experiences* (active regulation of the process)
- **Schraw & Moshman (1995)** — articulate *metacognitive regulation* into 4 acts (*planning · monitoring · evaluating · controlling*) and *metacognitive knowledge* into 3 types (*declarative · procedural · conditional*)
- **Vygotsky** — *cognitive scaffolding* / zone of proximal development: external structure that supports a cognitive process until it is internalized

kaora-memory implements **all 4 regulatory acts + two of the three knowledge types** (declarative + conditional). It misses no canonical piece of operational metacognition.

## 3. Mapping: kaora rule → metacognitive act

| kaora rule | Induced metacognitive act |
|---|---|
| **Opening ritual** (ADR-001) | *Planning* — "what do I have to do, where am I, what do I know about the context" |
| **Gate A** (skill loaded BEFORE Edit/Write) | *Monitoring* — "do I have the right tool?" + *Conditional knowledge* — "I know when to apply which strategy" |
| **Gate B** (checkpoint after 3-4 files) | *Monitoring + evaluating* — "am I going well? confirm?" |
| **Gate C** (never act on initiative) | *Controlling* — inhibition of the default "do it anyway" impulse |
| **`<BOOTSTRAP/>` markers** (ADR-002) | *Declarative knowledge* — "I explicitly know what I do NOT know and where to fetch it" |
| **CURRENT_STATE + SESSION_HANDOFF** | Retrospective *evaluating* + prospective *planning* |
| **SESSION_ERRORS_TEMPLATE** | *Evaluating* after failure → codified anti-pattern |
| **Operative/Learning conversational mode** (ADR-007) | *Monitoring* of the **interlocutor's** cognitive state (Theory of Mind, one level up) |
| **Sub-agent vs Read** (ADR-009) | *Conditional knowledge* — "I know when to delegate reading and when to read directly" |

## 4. Metacognitive triptych

Three ADRs form the product's **metacognitive nucleus**:

- **ADR-001** — Unconditional session opening ritual → forces *planning* before every action
- **ADR-007** — Operative vs Learning conversational mode → forces *Theory of Mind* of the interlocutor in every response
- **ADR-009** — Sub-agent vs direct Read → forces *conditional strategy selection* in every act of file reading

Together they form a complete system of metacognitive regulation: before acting, during interaction, and in execution decisions.

## 5. Product reverse positioning

The AI market sells: *"powerful, autonomous, super-intelligent agents, agentic super-coders"*.

kaora-memory sells **the opposite**:

> *"The powerful agent is the one who knows it does not know."*

It is pure **reverse positioning**. Instead of competing in the race to "the most autonomous", it exits the race by saying that **autonomy without metacognition is algorithmic arrogance**. No other mainstream AI product sells this way. Empty market space.

### Narrative frame: arrogant agent vs humble agent

- **Arrogant agent** (default today): doesn't know it doesn't know, doesn't ask for tools, acts on initiative, repeats already-made mistakes, ignores user context, closes every response with a call-to-action.
- **Humble agent** (with kaora): recognizes limits, loads tools before, stops for confirmation, remembers past errors, recognizes the interlocutor's mode, leaves loops open when the user explores.

### Image-rich domains for copy

- *Beginner's mind* (Shoshin, Shunryū Suzuki)
- *Socratic wisdom* — "I know that I do not know"
- *Reverse Dunning-Kruger* — those who know, know what they don't know
- *Strong opinions, loosely held* (engineering culture)
- *Epistemic humility* (philosophy of science)

## 6. Cognitive accessibility for neurodivergent profiles

ADR-007 (Operative vs Learning conversational mode) is not an abstract rule. It was written **during** the May 22 2026 development session, after the builder observed in real time a default LLM behavior:

> *"You keep proposing work and I'm trying to understand. I could just ignore you but your questions ignite other ideas in my head. For profiles outside the average this can be penalizing."*

The agent codified the builder's observation as a universal operational rule. It is **documented co-evolution between a neurodivergent human and an AI agent**.

The product evolves because the builder is gifted/divergent. The product makes it possible for future neurodivergent builders to work with AI without being penalized by defaults that amplify divergent cognition in unwanted ways.

**This is also an act of cognitive accessibility**, not just a product rule.

## 7. Repo naming considerations — decision closed 2026-05-28

> **Decision:** `kaora-memory`. Confirmed at the start of Block 5, before the first PyPI publication.
> Rationale: consistency with the author's "Kaora" ecosystem prioritized over framing-in-name. The metacognitive framing lives in the README tagline, the landing page, and the launch essay — not in the package name. Renaming a published package is painful; the name became immutable on 2026-05-28 when 0.1.1 went to PyPI.

The section below is preserved as the historical rationale that led to the decision.

The current name `kaora-memory` was chosen in Block 1, before the metacognitive framing emerged. It reflects the *what* (operating memory) but not the *why* (applied metacognition + humble agent).

**Tension of the current name:**
- "memory" is accurate as a mechanism (persistent files across sessions)
- "memory" is incomplete as a framing (doesn't tell about gates, ritual, conversational mode, sub-agent)
- Everything that emerged today (metacognition, reverse positioning, cognitive accessibility) is not covered by "memory"

**Renaming candidates that were evaluated:**

| Name | Pro | Con |
|---|---|---|
| `kaora-memory` (status quo) ✅ chosen | Already chosen, zero brand recognition but consistent with "kaora multi-agent" | Under-represents the framing |
| `kaora-metacognition` | Explicit, academic, original, no similar name on the market | Long (15 chars), hard word to pronounce/remember for non-Italian speakers |
| `kaora-meta` | Short, evocative | Too generic, "meta" is overused (Meta company, meta-programming) |
| `kaora-mc` | Acronym, very short | Cryptic, loses the framing |
| `kaora-mind` | Suggestive, short | Vague, "mind" is a beloved metaphor but can slip into new-age |
| `kaora-self` | Reference to self-awareness layer | Confused with consciousness concepts |
| `kaora-thinks` | Active verb, suggestive | Sounds childish in English, slips into marketing |
| `kaora-core` | Clean, professional, neutral | Generic, doesn't tell the framing |
| `kaora` (no suffix) | Very short, brandable | Conflicts with the author's Kaora multi-agent project |

The decision followed the third branch of the matrix above: ecosystem consistency over framing density, with the framing carried by the tagline.

---

**Document version:** 0.2 — first revised 2026-05-28 at the start of Block 5: naming decision closed, internal references to private dev assets removed for public consumption.
**To update:** when new philosophical reflections emerge from the launch.
