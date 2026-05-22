#!/usr/bin/env bash
# protect-credentials.sh — PreToolUse hook
#
# Blocca Write/Edit/MultiEdit su file che probabilmente contengono credenziali.
# Riceve in stdin un JSON con i dettagli del tool call (tool_input.file_path).
# Exit 2 = blocca (stderr mostrato all'utente). Exit 0 = consenti.
#
# Pattern bloccati (case-insensitive, match su basename o path completo):
#   .env  .env.local  .env.production  ...
#   credentials.json  credentials.yaml  credentials.yml  credentials.toml
#   secrets.json  secrets.yaml  secrets.yml  .secret.*
#   *.pem  *.key  *.p12  *.pfx  id_rsa  id_ed25519
#   service-account*.json  gcp-key*.json  aws-credentials*

set -euo pipefail

INPUT="$(cat)"

# Estrai file_path con jq se disponibile, altrimenti grep robusto
if command -v jq >/dev/null 2>&1; then
  FILE_PATH="$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty')"
else
  FILE_PATH="$(printf '%s' "$INPUT" | grep -oE '"file_path"[[:space:]]*:[[:space:]]*"[^"]+"' | head -n1 | sed -E 's/.*"file_path"[[:space:]]*:[[:space:]]*"([^"]+)".*/\1/')"
fi

if [ -z "${FILE_PATH:-}" ]; then
  exit 0
fi

BASENAME="$(basename "$FILE_PATH")"
LOWER_BASE="$(printf '%s' "$BASENAME" | tr '[:upper:]' '[:lower:]')"
LOWER_PATH="$(printf '%s' "$FILE_PATH" | tr '[:upper:]' '[:lower:]')"

is_blocked() {
  local name="$1"
  case "$name" in
    .env|.env.*) return 0 ;;
    credentials.json|credentials.yaml|credentials.yml|credentials.toml) return 0 ;;
    secrets.json|secrets.yaml|secrets.yml|secrets.toml) return 0 ;;
    .secret|.secret.*|.secrets|.secrets.*) return 0 ;;
    *.pem|*.key|*.p12|*.pfx) return 0 ;;
    id_rsa|id_rsa.*|id_ed25519|id_ed25519.*|id_ecdsa|id_ecdsa.*) return 0 ;;
    service-account*.json|gcp-key*.json|aws-credentials*) return 0 ;;
    .aws|.aws/*|.ssh|.ssh/*) return 0 ;;
  esac
  return 1
}

if is_blocked "$LOWER_BASE" || [[ "$LOWER_PATH" == *"/.ssh/"* ]] || [[ "$LOWER_PATH" == *"/.aws/"* ]]; then
  cat >&2 <<EOF
[kaora-memory] BLOCCATO: $FILE_PATH

Questo file corrisponde a un pattern di credenziali/segreti.
Modifica manuale richiesta — l'agente non scrive su file sensibili.

Se sei sicuro e vuoi procedere comunque:
  1. Apri il file a mano nell'editor
  2. Oppure rimuovi temporaneamente il pattern da .claude/hooks/protect-credentials.sh
EOF
  exit 2
fi

exit 0
