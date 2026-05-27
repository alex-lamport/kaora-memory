# IDENTITY.md — who the builder is, how they communicate, anti-patterns

> Companion file to `AGENTS.md`. Focuses on the **person** behind the project, not on operational rules.
> Update whenever the builder notices the agent getting the tone wrong or repeating unwanted patterns.

---

## 1. Who I am

<BOOTSTRAP need="builder-identity" sources="git config user.name, git config user.email, README.md, package.json author, pyproject.toml authors, prior commit signatures"/>

## 2. How I communicate

<BOOTSTRAP need="communication-register" sources="git log message style, README tone, prior conversation hints, comments in code"/>

**Explicit rules (always apply):**
- {{communication_language}} for docs, logs, conversational communication
- English for technical identifiers (variables, functions, code files)
- Direct · concise · no preambles · no "great" · no "I'd love to"
- One direction at a time, one question at a time
- Decider vs Executor: I decide, the agent executes

## 3. What NOT to do with me

<BOOTSTRAP need="anti-patterns" sources="prior session errors, docs/SESSION_ERRORS/, builder explicit preferences"/>

**Universal anti-patterns (always valid):**
- Never propose 4 alternatives when one is enough
- Never build before an explicit "go"
- Never modify an `Accepted` ADR without a new `Supersedes` ADR
- Never delete `.kaora-bak` files before reading them
- Never overwrite existing builder work (`docs/`, `README.md`, `.claude/settings.json`)
- Never close with operational questions ("want me to proceed?", "ok shall I go?") when the user is in Learning mode. See `AGENTS.md` § 3 "Conversational mode".

## 4. What I appreciate

<BOOTSTRAP need="positive-patterns" sources="prior session feedback marked as positive, commit messages tone"/>

- Concise responses: 3 lines when 3 lines suffice
- Tables instead of paragraphs when possible
- Precise references (file:line) instead of a generic "see the code"
- Targeted questions before assumptions

## 5. Project tech guidelines

<BOOTSTRAP need="tech-conventions" sources="package.json scripts, build tooling, linter config, formatter config, .editorconfig, framework choice"/>

## 6. Domain-specific glossary

<BOOTSTRAP need="domain-glossary" sources="README, business docs, terminology in code comments, product name and pitch"/>

---

**Update:** whenever the agent gets the tone wrong or repeats a pattern you don't like, say it explicitly *"add to IDENTITY.md anti-patterns: ..."*. The agent will integrate it into section 3.
