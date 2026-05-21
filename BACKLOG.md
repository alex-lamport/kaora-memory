# Backlog

> Idee e funzionalità per versioni future. NON fanno parte della v0.1.
> Tutto ciò che viene fuori durante lo sviluppo e non è strettamente v0.1
> finisce qui, non nel codice.

---

## Comandi CLI futuri

- `kaora handoff` — chiusura sessione automatica (genera SESSION_HANDOFF.md + aggiorna CURRENT_STATE.md)
- `kaora errors record` — wizard per scrivere un post-mortem strutturato (immune memory)
- `kaora skill install` — registrazione automatica della skill nei vari AI assistant (Claude Code skills dir, Cursor rules, ecc.)

## Automazioni runtime

- **Hook context-threshold a 60% → proposta automatica SESSION_HANDOFF**
  · Claude Code only in prima release
  · In v0.2+ portare su Codex / Cursor / Gemini CLI tramite wrapper esterno (monitor file di sessione + notifica)

## Infrastruttura

- MCP server (kaora-memory come servizio remoto)
- Cloud sync delle memorie cross-device
- Dashboard / web UI per visualizzare lo stato del progetto

## Template

- Bootstrap agent-driven completo (l'agente investiga e compila i `<BOOTSTRAP/>` markers leggendo git config, README, package.json, ecc.) — design definito, implementazione in Blocco 2/3
- Skin alternative per il template (es. registro inglese, registro tecnico-asciutto, registro conversazionale)

## Idee da valutare

(spazio aperto — ogni cosa che emerge va qui prima di entrare in v0.x)
