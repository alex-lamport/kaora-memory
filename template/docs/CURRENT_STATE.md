# CURRENT_STATE.md — stato operativo

> Aggiornato a **fine** di ogni sessione. Risponde a "dove siamo, cosa funziona, cosa manca adesso".
>
> **Ultimo aggiornamento:** {{year}}-MM-GG — scaffolding iniziale via `kaora init`.

---

## Snapshot oggi

**Stage corrente:** scaffolding iniziale — memoria operativa installata, BOOTSTRAP da compilare.
**Commit ultimo:** <BOOTSTRAP need="last-commit" sources="git log -1 --oneline"/>
**Branch:** <BOOTSTRAP need="current-branch" sources="git branch --show-current"/>
**Repo remoto:** <BOOTSTRAP need="remote-url" sources="git remote -v"/>

## Cosa esiste

```
{{project_name}}/
├── AGENTS.md                          (canonico cross-agent)
├── CLAUDE.md                          (entry point Claude Code, import @AGENTS.md)
├── AGENT_BRIEF.md                     (onboarding 3-min)
├── BACKLOG.md                         (idee fuori scope corrente)
├── docs/
│   ├── IDENTITY.md                    (chi sono io, come comunico)
│   ├── CURRENT_STATE.md               (questo file)
│   ├── SESSION_HANDOFF.md             (brief prima sessione)
│   ├── DECISIONS.md                   (ADR log, append-only)
│   └── SESSION_ERRORS_TEMPLATE.md     (template post-mortem)
└── .claude/
    ├── settings.json                  (hook config)
    └── hooks/
        ├── protect-credentials.sh
        └── log-api-calls.sh
```

<BOOTSTRAP need="existing-project-files" sources="ls -la, ls src/, ls lib/, package.json, README, prior .kaora-bak files content"/>

## Cosa funziona

- ✅ Memoria operativa kaora installata (`AGENTS.md`, `CLAUDE.md`, `docs/*`)
- ✅ Hook protezione credenziali attivi (`.claude/hooks/protect-credentials.sh`)
- ✅ Hook log API calls attivi (`.claude/hooks/log-api-calls.sh`)
<BOOTSTRAP need="working-features" sources="tests passing, build green, deploy status"/>

## Cosa manca (priorità ordinata)

1. **Compilazione marker `<BOOTSTRAP/>`** — la prima sessione AI deve scansionarli e compilarli (vedi `AGENT_BRIEF.md` § 3)
2. **Lettura file `.kaora-bak`** se presenti — estrarre setup tecnico esistente e integrarlo
3. **Prima ADR del progetto** in `docs/DECISIONS.md` — qualsiasi decisione iniziale di architettura
<BOOTSTRAP need="project-todo" sources="TODO comments in code, GitHub issues if remote configured, README roadmap section"/>

## Asset di comunicazione collegati

<BOOTSTRAP need="comms-assets" sources="docs/, .figma/, .canva/, marketing/, design/"/>

## Note operative

- **Memoria persistente:** non ancora popolata, si arricchirà sessione dopo sessione
- **File `.kaora-bak` da gestire:** <BOOTSTRAP need="kaora-bak-list" sources="ls *.kaora-bak, ls docs/*.kaora-bak"/>
