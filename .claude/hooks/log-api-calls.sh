#!/usr/bin/env bash
# log-api-calls.sh — PostToolUse hook (matcher: Bash)
#
# Logga ogni Bash tool call che sembra fare una chiamata HTTP/API
# (curl, wget, http, https, gh api) in logs/api-calls.jsonl.
# Non-bloccante: exit 0 sempre.
#
# Riga di log JSONL formato:
#   {"ts":"YYYY-MM-DDTHH:MM:SSZ","command":"...","kind":"curl|wget|gh-api|http-other"}

set -uo pipefail

INPUT="$(cat || true)"

if command -v jq >/dev/null 2>&1; then
  COMMAND="$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null || true)"
else
  COMMAND="$(printf '%s' "$INPUT" | grep -oE '"command"[[:space:]]*:[[:space:]]*"[^"]+"' | head -n1 | sed -E 's/.*"command"[[:space:]]*:[[:space:]]*"([^"]+)".*/\1/')"
fi

if [ -z "${COMMAND:-}" ]; then
  exit 0
fi

# Match pattern di chiamate API (case-insensitive)
LOWER_CMD="$(printf '%s' "$COMMAND" | tr '[:upper:]' '[:lower:]')"

KIND=""
case "$LOWER_CMD" in
  *"curl "*|*"curl\\\""*) KIND="curl" ;;
  *"wget "*) KIND="wget" ;;
  *"gh api"*) KIND="gh-api" ;;
  *"http "*|*"https "*|*"httpie"*) KIND="http-other" ;;
esac

if [ -z "$KIND" ]; then
  exit 0
fi

# Determina root del progetto (prova git, fallback a cwd)
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
LOG_DIR="$PROJECT_ROOT/logs"
LOG_FILE="$LOG_DIR/api-calls.jsonl"

mkdir -p "$LOG_DIR" 2>/dev/null || exit 0

TS="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

# Escape comando per JSON: backslash + double quotes
ESCAPED_CMD="$(printf '%s' "$COMMAND" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))' 2>/dev/null || printf '"%s"' "$(printf '%s' "$COMMAND" | sed 's/\\/\\\\/g; s/"/\\"/g')")"

printf '{"ts":"%s","kind":"%s","command":%s}\n' "$TS" "$KIND" "$ESCAPED_CMD" >> "$LOG_FILE" 2>/dev/null || true

exit 0
