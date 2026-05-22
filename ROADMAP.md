# Roadmap — kaora-memory

> Visione di prodotto per versioni. Le voci `[x]` sono completate, `[ ]` sono pianificate.
> Il backlog dettagliato vive in [`BACKLOG.md`](BACKLOG.md).
> Le decisioni architetturali fondanti vivono in [`docs/DECISIONS.md`](docs/DECISIONS.md).

---

## v0.1 — *Foundations* · MVP installabile (in corso, target 2026-06)

Obiettivo: pacchetto Python pubblicato su PyPI con `kaora init` che installa scaffolding di memoria operativa in qualsiasi progetto, fresco o esistente.

### Blocchi

- [x] **Blocco 1** — Scaffolding repo: pyproject (hatchling, py>=3.10), layout flat, entry point `kaora`, LICENSE, README minimo, dogfooding memoria operativa
- [x] **Blocco 2** — Template generalizzato: 13 file in `template/` con 30 BOOTSTRAP markers + 8 placeholder Jinja, hook smoke-tested, ADR 005-009 Accepted (la 009 codifica la regola sub-agente vs Read per ottimizzazione context e comportamento)
- [ ] **Blocco 3** — `kaora init`: CLI Click + `installer.py` per copia template + `settings_merger.py` per merge JSON intelligente (ADR-006 v2), test brownfield/greenfield/dry-run/force
- [ ] **Blocco 4** — `kaora check`: verifica integrità memoria operativa (placeholder non risolti, BOOTSTRAP residui, ADR Proposed pendenti, drift CLAUDE.md ↔ AGENTS.md non più necessario via ADR-005)
- [ ] **Blocco 5** — README completo + demo (3 screenshot o GIF: `kaora init` → prima sessione `claude vai` → agente esegue rituale) + sezione "Filosofia del prodotto" con metacognizione applicata + brownfield FAQ
- [ ] **Blocco 6** — Pubblicazione: `.pypirc`, token test.pypi, build wheel, smoke test installazione, push GitHub, release v0.1.0 + saggio di lancio

### Cosa NON sarà in v0.1

- Dashboard premium → v0.2
- `kaora handoff`, `kaora errors record`, `kaora skill install` → v0.2+
- MCP server / cloud sync → v0.3+
- Hook context-threshold 60% → v0.2+

---

## v0.1.1 — *Quality of life* · CLI status (target +2 settimane post v0.1)

Obiettivo: aggiungere il comando rapido che mostra lo stato della memoria operativa direttamente in terminale, primo passo verso la dashboard.

- [ ] `kaora status` — output ~10 righe in terminale: stage corrente, ADR aperte, ultimo commit, file modificati 24h, anti-pattern count, post-mortem count
- [ ] Bugfix / refinement post-feedback prima settimana di adozione

---

## v0.2 — *Premium visibility* · Dashboard (target Q3 2026)

Obiettivo: trasformare il prodotto da *"file markdown + agente"* a *"file markdown + agente + console visuale premium"*. Wow moment per i nuovi utenti.

- [ ] `kaora dashboard` — server locale `http.server` con auto-refresh, glassmorphism premium (riferimento `~/Desktop/kaora/kaora-dashboard.html`), file map convenzionale a gruppi, vista ADR filtrabile
- [ ] `kaora dashboard --export` — snapshot statico singolo-file portabile, render server-side markdown
- [ ] `kaora handoff` — chiusura sessione automatica (genera `SESSION_HANDOFF.md` + aggiorna `CURRENT_STATE.md`)
- [ ] `kaora errors record` — wizard post-mortem strutturato (immune memory)
- [ ] Hook context-threshold 60% per Claude Code → proposta automatica `SESSION_HANDOFF.md`

---

## v0.3 — *Cross-machine* · Infrastruttura (target Q4 2026)

Obiettivo: portare kaora-memory oltre il singolo repo locale, verso team distribuiti e device multipli.

- [ ] MCP server (kaora-memory come servizio remoto interrogabile da agenti compatibili MCP)
- [ ] Cloud sync delle memorie cross-device
- [ ] `kaora skill install` — registrazione automatica della skill nei vari AI assistant (Claude Code skills dir, Cursor rules, ecc.)
- [ ] Hook context-threshold portato su Codex / Cursor / Gemini CLI (monitor file di sessione + notifica)

---

## v1.0 — *Maturity* (target 2027 o quando l'adozione lo giustifica)

Obiettivo: stabilità API, governance community, ecosistema esteso.

- [ ] API CLI stabile, breaking changes solo con major version
- [ ] Documentazione di contributo per community
- [ ] Skin alternative del template (registro inglese, tecnico-asciutto, conversazionale)
- [ ] Plugin ecosystem (estensioni che aggiungono regole/hook al template senza forkare)

---

## Filosofia del prodotto

kaora-memory è **metacognizione indotta** per agenti AI. Non scaffolding generico, non memory store, non rules engine. Forza l'agente a fare gli atti regolatori della metacognizione (planning, monitoring, evaluating, controlling) ogni volta che lavora.

**Reverse positioning** rispetto al mercato AI: dove tutti vendono *"agente potente, autonomo, super-intelligente"*, kaora vende *"agente umile che riconosce i limiti"*. L'agente potente è quello che sa di non sapere.

Riferimenti teorici nei docs di lancio: Flavell (1979), Schraw & Moshman (1995), Vygotsky (cognitive scaffolding).

**Cross-agent vero:** funziona su Claude Code, Codex CLI, Cursor, Aider, Gemini CLI con lo stesso set di file (ADR-005 — canonico `AGENTS.md` + import `@AGENTS.md` in `CLAUDE.md`).

**Brownfield-friendly:** mai distrugge lavoro utente esistente. Backup `.kaora-bak` per markdown + merge JSON intelligente per `.claude/settings.json` (ADR-006).

**Accessibilità cognitiva:** la regola di modalità conversazionale Operativa vs Apprendimento (ADR-007) è nata dall'osservazione di un builder neurodivergente in tempo reale. Il prodotto è anche un atto di accessibilità cognitiva per profili divergenti.
