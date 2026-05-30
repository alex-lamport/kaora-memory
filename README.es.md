![kaora-memory — metacognición inducida para agentes de IA](https://raw.githubusercontent.com/alex-lamport/kaora-memory/main/docs/assets/kaora-hero.png)

[🇬🇧 English](README.md) · [🇮🇹 Italiano](README.it.md) · **🇪🇸 Español**

# kaora-memory

> **Metacognición inducida para agentes de IA.**
> Una memoria operativa a nivel de proyecto que hace que los agentes de coding arranquen preparados, respeten las decisiones y se detengan antes de actuar a ciegas.

`pip install kaora-memory` → `kaora init` → cada agente que abre el proyecto (Claude Code, Codex, Cursor, Gemini CLI) lee el mismo contexto canónico y arranca coherente.

---

## Inicio rápido

```bash
pip install kaora-memory
cd myproject
kaora init
```

Eso es todo. Abre Claude Code (o cualquier otro agente) en `myproject`, escribe `go`, y el agente lee la memoria operativa antes de hacer cualquier otra cosa.

Proyecto nuevo: `kaora init` escribe 13 archivos (ver abajo).
Proyecto existente con un `CLAUDE.md` o `AGENTS.md` ya presente: `kaora init` les hace una copia de seguridad como `.kaora-bak` y el agente fusiona tu contenido existente en la estructura canónica durante la primera sesión. Mira las [Brownfield FAQ](#brownfield-faq).

### Instalación en macOS

En macOS un simple `pip install` suele estar bloqueado (el "entorno gestionado externamente" de Python). Instala `kaora` como una CLI aislada con **pipx**:

```bash
brew install pipx        # si aún no lo tienes
pipx ensurepath
pipx install kaora-memory
```

¿Prefieres un virtualenv? También funciona:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install kaora-memory
```

Si justo después de instalar sigues viendo `kaora: command not found`, abre una nueva ventana de terminal para que la shell actualice el `PATH`.

---

## Qué obtienes

Después de `kaora init` tu proyecto tiene:

```
myproject/
├── AGENTS.md              # contexto maestro canónico, cross-agent
├── CLAUDE.md              # punto de entrada de 4 líneas, importa @AGENTS.md
├── AGENT_BRIEF.md         # onboarding de 3 minutos para cualquier agente nuevo
├── BACKLOG.md             # ideas fuera del alcance actual
├── docs/
│   ├── IDENTITY.md              # quién es el builder, cómo colaborar
│   ├── CURRENT_STATE.md         # estado vivo, actualizado al cierre de sesión
│   ├── SESSION_HANDOFF.md       # brief para la siguiente sesión
│   ├── DECISIONS.md             # registro ADR, append-only
│   └── SESSION_ERRORS_TEMPLATE.md
└── .claude/
    ├── settings.json      # configuración de hooks de Claude Code
    └── hooks/             # protect-credentials.sh, log-api-calls.sh
```

Todos los templates llevan marcadores `<BOOTSTRAP/>` que el agente rellena durante la primera sesión inspeccionando el repo — sin configuración manual.

---

## Qué es en realidad

kaora-memory no es una base de datos de memoria, un vector store, ni otro framework de agentes.

Es un **protocolo operativo** para agentes de coding con IA: un pequeño conjunto de archivos, rituales, gates y reglas de handoff que obligan al agente a realizar los actos regulatorios de la metacognición antes y durante el trabajo.

Sin kaora, el agente ejecuta.

Con kaora, el agente arranca preguntándose: *¿qué sé, qué no sé, qué ya se ha decidido y cuándo debo detenerme?*

---

## Por qué existe

Los agentes de IA tienen un problema de amnesia. Cada nueva sesión arranca desde cero: sin memoria de las decisiones pasadas, sin conciencia de las preferencias del builder, sin reglas codificadas sobre qué hacer ante la incertidumbre.

Tres síntomas concretos:

1. **Drift de los docs** — README, ADRs y documentos del proyecto pierden la sincronía con el código porque nada obliga al agente a actualizarlos al cierre de la sesión.
2. **Acción improvisada** — sin reglas explícitas, el agente se salta las herramientas correctas, escribe archivos sin confirmación y resuelve la incertidumbre adivinando.
3. **Pérdida de contexto entre agentes** — un proyecto que pasa de Claude Code a Codex arranca desde nada dos veces.

kaora-memory aborda los tres dando al proyecto una **memoria operativa canónica** que cualquier agente de IA lee al inicio de la sesión, y un conjunto de **comportamientos codificados** que el agente ejecuta tanto si el builder se acuerda de pedirlo como si no.

---

## Cómo funciona

Después de `kaora init`, el proyecto lleva consigo dos lados independientes.

**Lado memoria** — archivos persistentes en la raíz del proyecto y en `docs/`:
- `AGENTS.md` es el contexto maestro canónico. `CLAUDE.md` es un archivo de 4 líneas que importa `AGENTS.md` (ver [ADR-005](https://github.com/alex-lamport/kaora-memory/blob/main/docs/DECISIONS.md)).
- `CURRENT_STATE.md` registra "dónde estamos ahora"; `SESSION_HANDOFF.md` lleva el brief para la siguiente sesión.
- `DECISIONS.md` es el registro ADR append-only: cada decisión arquitectónica vive aquí con su fecha, estado y justificación.

**Lado comportamiento** — reglas codificadas dentro de `AGENTS.md`, respetadas por cada agente:
- **Ritual de apertura** — en la primera respuesta de cada sesión el agente lee la memoria operativa, resume el estado en 3-5 líneas y espera confirmación.
- **Gate A** — antes de cualquier `Edit` o `Write` el agente verifica que no se esté contradiciendo un ADR cerrado, que se haya invocado la skill correcta y que el valor esté verificado.
- **Gate B** — después de 3-4 archivos modificados el agente hace un checkpoint con el builder.
- **Gate C** — ningún archivo escrito, ninguna decisión tomada, sin un `go` explícito.
- **Modo Operativo vs Aprendizaje** — el agente detecta si el builder está ejecutando o explorando y se adapta (ver [ADR-007](https://github.com/alex-lamport/kaora-memory/blob/main/docs/DECISIONS.md)).

La memoria persiste entre sesiones y agentes. El comportamiento se lee al inicio de la sesión y se respeta durante toda la conversación.

---

## Brownfield FAQ

> **Ya tengo un `CLAUDE.md` (o `AGENTS.md`) en mi proyecto. ¿Qué pasa?**

`kaora init` le hace una copia de seguridad como `CLAUDE.md.kaora-bak` (preservando cada byte) y escribe el `CLAUDE.md` canónico de 4 líneas que importa `AGENTS.md`. En tu primera sesión después de `kaora init`, el agente encuentra el `.kaora-bak`, lo lee y propone una **fusión guiada** en el `AGENTS.md` canónico. Tú confirmas, la fusión ocurre, el `.kaora-bak` se archiva en `docs/archive/` para que no dispare el escaneo de apertura en cada sesión futura.

Tu memoria preexistente se **preserva como una feature**, no se marca como una advertencia. Mira [ADR-006](https://github.com/alex-lamport/kaora-memory/blob/main/docs/DECISIONS.md) para la política de instalación brownfield.

> **Mi `.claude/settings.json` ya tiene hooks. ¿`kaora init` los sobrescribe?**

No. `settings.json` se fusiona de forma inteligente: los hooks de kaora se añaden junto a los tuyos, los conflictos se señalan. Las otras claves JSON quedan intactas.

---

## kaora check

Ejecuta `kaora check` en cualquier momento para verificar que tu memoria operativa no haya driftado de la estructura canónica.

```
$ kaora check .

ℹ️  INFO:
  [placeholders] BOOTSTRAP marker to fill in docs/IDENTITY.md: <BOOTSTRAP need="builder-identity" sources="..."/>
```

Seis categorías de control: estructura (archivos requeridos), ADR-005 (canónico + directiva de import), estado ADR (Accepted/Proposed), placeholders (estructurales vs BOOTSTRAP), hooks (`.claude/hooks/*.sh` ejecutables), settings (`.claude/settings.json` referencia los hooks de kaora).

El exit code es 0 por defecto; `--strict` promueve los warnings a errores (útil en CI). `--json` para salida legible por máquina.

---

## Roadmap

v0.1 (actual) — `kaora init`, `kaora check`, template canónico de 13 archivos, política de instalación brownfield, ritual de apertura + cierre.

v0.2+ — `kaora handoff` (automatización CLI del cierre de sesión), `kaora dashboard` (UI web para visualizar la memoria operativa), hook de umbral de contexto para Claude Code, onboarding multicanal para `IDENTITY.md`.

v0.3+ — servidor MCP, sync en la nube entre dispositivos.

Backlog completo en [`BACKLOG.md`](https://github.com/alex-lamport/kaora-memory/blob/main/BACKLOG.md).

---

## Filosofía

kaora-memory es **metacognición inducida para agentes de IA**: los lados memoria + comportamiento obligan al agente a planificar antes de actuar, monitorear durante la acción, evaluar al cierre de la sesión y reconocer el estado cognitivo del builder. La tesis completa vive en [`docs/PHILOSOPHY.md`](https://github.com/alex-lamport/kaora-memory/blob/main/docs/PHILOSOPHY.md).

---

> *kaora-memory no añade inteligencia al agente. Añade preparación.*

---

## Licencia

MIT — mira [LICENSE](https://github.com/alex-lamport/kaora-memory/blob/main/LICENSE).

Construido con kaora-memory misma. El repo pasa su propio `kaora check`, y cada ADR en [`docs/DECISIONS.md`](https://github.com/alex-lamport/kaora-memory/blob/main/docs/DECISIONS.md) se decidió a través de los mismos gates que kaora codifica para otros proyectos. Mira [`docs/DOGFOODING_REPORT.md`](https://github.com/alex-lamport/kaora-memory/blob/main/docs/DOGFOODING_REPORT.md) para la historia de la auto-aplicación.

---

Construido por [Alexis Rojas](https://x.com/alex_lamports) — parte del workspace/investigación KAORA sobre agentes de IA, memoria y colaboración humano-agente.
