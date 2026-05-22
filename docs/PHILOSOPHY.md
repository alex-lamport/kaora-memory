# PHILOSOPHY.md — il perché del prodotto

> Documento concettuale. Risponde a *"perché kaora-memory esiste, cosa è davvero, dove si posiziona rispetto al mercato AI"*.
> Compagno di [DECISIONS.md](DECISIONS.md) (il *come*) e [CURRENT_STATE.md](CURRENT_STATE.md) (il *cosa adesso*).
> Sede delle riflessioni emerse nelle sessioni di sviluppo che vanno preservate al di là delle singole ADR.

---

## 1. Tesi centrale

**kaora-memory è metacognizione indotta per agenti AI.**

Non scaffolding generico, non memory store, non rules engine. È il primo strumento che **costringe l'agente a fare gli atti regolatori della metacognizione** ogni volta che lavora: pianificare prima di agire, monitorare durante l'azione, valutare retrospettivamente, controllare gli impulsi di iniziativa, riconoscere lo stato cognitivo dell'interlocutore.

Senza kaora: l'agente esegue.
Con kaora: l'agente **pensa al proprio pensare** mentre esegue.

## 2. Riferimenti teorici

La metafora regge accademicamente, non è cosmetica. Tre fonti:

- **Flavell (1979)** — distinzione fondante tra *metacognitive knowledge* (sapere cosa sai e cosa NON sai) e *metacognitive experiences* (regolazione attiva del processo)
- **Schraw & Moshman (1995)** — articolano la *metacognitive regulation* in 4 atti (*planning · monitoring · evaluating · controlling*) e la *metacognitive knowledge* in 3 tipi (*declarative · procedural · conditional*)
- **Vygotsky** — *cognitive scaffolding* / zona di sviluppo prossimale: struttura esterna che supporta un processo cognitivo finché non viene internalizzato

kaora-memory implementa **tutti e 4 gli atti regolatori + due dei tre tipi di knowledge** (declarative + conditional). Non manca nessun tassello canonico della metacognizione operativa.

## 3. Mapping regola kaora → atto metacognitivo

| Regola kaora | Atto metacognitivo indotto |
|---|---|
| **Rituale di apertura** (ADR-001) | *Planning* — "cosa devo fare, dove sono, cosa so del contesto" |
| **Gate A** (skill caricata PRIMA di Edit/Write) | *Monitoring* — "ho lo strumento giusto?" + *Knowledge conditional* — "so quando applicare quale strategia" |
| **Gate B** (checkpoint dopo 3-4 file) | *Monitoring + evaluating* — "sto andando bene? confermo?" |
| **Gate C** (mai agire di iniziativa) | *Controlling* — inibizione dell'impulso default di "fare comunque" |
| **`<BOOTSTRAP/>` markers** (ADR-002) | *Knowledge declarative* — "so esplicitamente cosa NON so e dove andarlo a prendere" |
| **CURRENT_STATE + SESSION_HANDOFF** | *Evaluating* retrospettivo + *planning* prospettivo |
| **SESSION_ERRORS_TEMPLATE** | *Evaluating* dopo fallimento → anti-pattern codificato |
| **Modalità conversazionale Op/Ap** (ADR-007) | *Monitoring* dello stato cognitivo dell'**interlocutore** (Theory of Mind, livello sopra) |
| **Sub-agente vs Read** (ADR-009) | *Knowledge conditional* — "so quando delegare lettura e quando leggere direttamente" |

## 4. Trittico metacognitivo

Tre ADR formano il **nucleo metacognitivo** del prodotto:

- **ADR-001** — Rituale incondizionato di apertura sessione → forza *planning* prima di ogni azione
- **ADR-007** — Modalità conversazionale Operativa vs Apprendimento → forza *Theory of Mind* dell'interlocutore in ogni risposta
- **ADR-009** — Sub-agente vs Read diretto → forza *strategy selection conditional* in ogni atto di lettura file

Insieme costituiscono un sistema completo di regolazione metacognitiva: prima di agire, durante l'interazione, e nelle decisioni di esecuzione.

## 5. Reverse positioning del prodotto

Il mercato AI vende: *"agenti potenti, autonomi, super-intelligenti, agentic super-coders"*.

kaora-memory vende **l'opposto**:

> *"L'agente potente è quello che sa di non sapere."*

È **reverse positioning** puro. Invece di gareggiare nella corsa al "più autonomo", esce dalla gara dicendo che **autonomia senza metacognizione è arroganza algoritmica**. Nessun altro prodotto AI mainstream vende così. Spazio di mercato vuoto.

### Frame narrativo: agente arrogante vs agente umile

- **Agente arrogante** (default oggi): non sa di non sapere, non chiede strumenti, agisce di iniziativa, ripete errori già fatti, ignora il contesto utente, chiude ogni risposta con call-to-action.
- **Agente umile** (con kaora): riconosce i limiti, carica strumenti prima, si ferma per conferma, ricorda errori passati, riconosce in che modalità è l'interlocutore, lascia loop aperti quando l'utente esplora.

### Domini ricchi di immagini per copy

- *Mentalità del principiante* (Shoshin, Shunryū Suzuki)
- *Sapienza socratica* — "so di non sapere"
- *Dunning-Kruger inverso* — chi sa, sa cosa non sa
- *Strong opinions, loosely held* (engineering culture)
- *Epistemic humility* (filosofia della scienza)

## 6. Accessibilità cognitiva per profili neurodivergenti

ADR-007 (modalità conversazionale Operativa vs Apprendimento) non è una regola astratta. È stata scritta **durante** la sessione di sviluppo del 22 maggio 2026, dopo che il builder ha osservato in tempo reale un comportamento default degli LLM:

> *"Continui a proporre di lavorare e io cerco di capire. Basterebbe ignorarti ma le tue domande accendono altre idee in testa. Per profili fuori media può essere penalizzante."*

L'agente ha codificato l'osservazione del builder come regola operativa universale. È **co-evoluzione documentata tra umano neurodivergente e agente AI**.

Il prodotto evolve perché il builder è plusdotato/divergente. Il prodotto rende possibile a futuri builder neurodivergenti di lavorare con AI senza essere penalizzati dai default che amplificano la cognizione divergente in modi indesiderati.

**Questo è anche un atto di accessibilità cognitiva**, non solo una regola di prodotto.

## 7. Considerazioni sul naming del repo

Il nome attuale `kaora-memory` è stato scelto in Blocco 1, prima che il framing metacognitivo emergesse. Riflette il *cosa* (memoria operativa) ma non il *perché* (metacognizione applicata + agente umile).

**Tensione del nome attuale:**
- "memory" è esatto come meccanismo (file persistenti tra sessioni)
- "memory" è incompleto come framing (non racconta gate, rituale, modalità conversazionale, sub-agente)
- Tutto quello che è emerso oggi (metacognizione, reverse positioning, accessibilità cognitiva) non è coperto da "memory"

**Candidati per rinaming (da valutare prima del rilascio v0.1, non oggi):**

| Nome | Pro | Contro |
|---|---|---|
| `kaora-memory` (status quo) | Già scelto, brand recognition zero ma coerente con "kaora multi-agent" | Sotto-rappresenta il framing |
| `kaora-metacognition` | Esplicito, accademico, originale, nessun altro nome simile sul mercato | Lungo (15 caratteri), parola difficile da pronunciare/ricordare per non-italiani |
| `kaora-meta` | Breve, evocativo | Troppo generico, "meta" è abusato (Meta company, meta-programming) |
| `kaora-mc` | Acronimo, brevissimo | Cripto, perde il framing |
| `kaora-mind` | Suggestivo, breve | Vago, "mind" è una metafora cara ma può scivolare in new-age |
| `kaora-self` | Riferimento a self-awareness layer | Confonde con concetti di consciousness |
| `kaora-thinks` | Verbo attivo, suggestivo | Suona infantile in inglese, scivola in marketing |
| `kaora-core` | Pulito, professionale, neutro | Generico, non racconta il framing |
| `kaora` (senza suffisso) | Brevissimo, brandable | Va a confliggere con il progetto Kaora multi-agent dell'autore |

**Mia raccomandazione (in attesa di decisione finale):** rinviare la decisione al **Blocco 5** (README + comunicazione), quando il framing sarà stabilizzato dal saggio di lancio. A quel punto:
- Se il framing metacognitivo è il filo conduttore narrativo principale → considerare `kaora-metacognition`
- Se il nome breve è priorità marketing → considerare `kaora-mc` o `kaora-meta`
- Se la coerenza con l'ecosistema "Kaora" dell'autore è priorità → mantenere `kaora-memory` e usare il framing metacognitivo solo come tagline

Da decidere prima della pubblicazione PyPI (Blocco 6), perché rinominare un pacchetto pubblicato è doloroso.

## 8. Riferimenti per il saggio di lancio

Brief operativo per il saggio: `/tmp/kaora-memory-launch-essay-brief.md` (generato 22 maggio 2026, 16 sezioni, da passare alla sessione parallela che sta scrivendo il saggio).

Landing page candidate: `/tmp/kaora-memory-preview.html` (datato 22 maggio 00:55, da aggiornare in Blocco 5 con framing metacognitivo + ADR 005-009 + Blocco 2 chiuso).

Documento di vision astratta: `/Users/alexissilva/Desktop/kaora-memory-architecture-dashboard.html` (datato 20 maggio, asset di vision più filosofico, riusabile come "wiki extended" per audience accademica).

---

**Versione documento:** 0.1 — 22 maggio 2026, emerso al chiudere di Blocco 2.
**Da aggiornare:** quando la decisione sul naming sarà presa (Blocco 5), e quando emergeranno nuove riflessioni filosofiche dal lancio.
