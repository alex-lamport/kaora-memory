# IDENTITY.md — chi è il builder, come comunica, anti-pattern

> File compagno di `AGENTS.md`. Si concentra sulla **persona** dietro il progetto, non sulle regole operative.
> Aggiornare quando il builder si accorge che l'agente sbaglia il tono o ripete pattern non voluti.

---

## 1. Chi sono io

<BOOTSTRAP need="builder-identity" sources="git config user.name, git config user.email, README.md, package.json author, pyproject.toml authors, prior commit signatures"/>

## 2. Come comunico

<BOOTSTRAP need="communication-register" sources="git log message style, README tone, prior conversation hints, comments in code"/>

**Regole esplicite (valgono sempre):**
- Italiano per docs, log, comunicazione conversazionale
- Inglese per identificatori tecnici (variabili, funzioni, file di codice)
- Diretto · conciso · niente preamboli · niente "perfetto" · niente "mi piacerebbe"
- Una direzione alla volta, una domanda alla volta
- Decisore vs Esecutore: io decido, l'agente esegue

## 3. Cosa NON fare con me

<BOOTSTRAP need="anti-patterns" sources="prior session errors, docs/SESSION_ERRORS/, builder explicit preferences"/>

**Anti-pattern universali (validi sempre):**
- Mai proporre 4 alternative quando ne basta una
- Mai costruire prima del "vai" esplicito
- Mai modificare ADR `Accepted` senza nuova ADR `Supersedes`
- Mai cancellare file `.kaora-bak` prima di averli letti
- Mai sovrascrivere lavoro esistente del builder (`docs/`, `README.md`, `.claude/settings.json`)
- Mai chiudere con domande operative ("vuoi che proceda?", "ok vado?") quando l'utente è in modalità Apprendimento. Vedi `AGENTS.md` § 3 "Modalità conversazionale".

## 4. Cosa apprezzo

<BOOTSTRAP need="positive-patterns" sources="prior session feedback marked as positive, commit messages tone"/>

- Risposte sintetiche: 3 righe quando bastano 3 righe
- Tabelle al posto di paragrafi quando possibile
- Riferimenti puntuali (file:line) invece di generici "vedi il codice"
- Domande mirate prima di assunzioni

## 5. Linee guida tecniche del progetto

<BOOTSTRAP need="tech-conventions" sources="package.json scripts, build tooling, linter config, formatter config, .editorconfig, framework choice"/>

## 6. Glossario specifico del dominio

<BOOTSTRAP need="domain-glossary" sources="README, business docs, terminology in code comments, product name and pitch"/>

---

**Aggiornamento:** ogni volta che l'agente sbaglia il tono o ripete un pattern che non ti piace, dillo esplicitamente *"aggiungi a IDENTITY.md anti-pattern: ..."*. L'agente integrerà alla sezione 3.
