#!/usr/bin/env bash
# Paperclip "Process"-Adapter -> Claude Code gegen ein LOKALES Modell (LM Studio).
# Paperclip erlaubt beim claude_local-Adapter kein ANTHROPIC_BASE_URL neben einer Abo-/API-Verbindung
# ("provider routing is incompatible"; lokale Provider erst mit PR paperclipai/paperclip#14006).
# Dieses Skript wird deshalb als Process-Command eingetragen. Paperclip streamt den Prompt per stdin,
# die Antwort geht ueber stdout zurueck.
#
# Sicherheitsregeln:
#  - Kein Fallback in die Cloud: Ist LM Studio/das Modell nicht erreichbar, bricht das Skript mit Exit 2 ab.
#  - Abo-Token wird entfernt, eigene leere Claude-Konfiguration (keine Connectoren, keine Plugins).
#
# Installation (als Admin):
#   sudo install -o agents -m 755 scripts/local-llm/paperclip-local-claude.sh /Users/agents/bin/local-claude.sh
set -euo pipefail

: "${LOCAL_BASE_URL:=http://localhost:1234}"
: "${LOCAL_MODEL:=qwen3.6-35b-a3b}"
: "${LOCAL_CONTEXT:=131072}"
: "${LOCAL_MAX_OUTPUT:=16384}"
: "${LOCAL_MAX_TURNS:=40}"
: "${LOCAL_CLAUDE_CONFIG_DIR:=$HOME/.claude-local}"
: "${LOCAL_ALLOWED_TOOLS:=Read,Edit,Write,Glob,Grep,Bash(ls:*),Bash(git diff:*),Bash(git status:*),Bash(npm test:*),Bash(npm run:*),Bash(node --test:*),Bash(pytest:*)}"

export PATH="$HOME/.local/bin:/opt/homebrew/opt/node@24/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"

# Nie mit Cloud-Zugangsdaten laufen
unset CLAUDE_CODE_OAUTH_TOKEN ANTHROPIC_API_KEY
export ANTHROPIC_API_KEY=""
export ANTHROPIC_BASE_URL="$LOCAL_BASE_URL"
export ANTHROPIC_AUTH_TOKEN="lmstudio"
export ANTHROPIC_MODEL="$LOCAL_MODEL"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="$LOCAL_MODEL"
export ANTHROPIC_DEFAULT_SONNET_MODEL="$LOCAL_MODEL"
export ANTHROPIC_DEFAULT_OPUS_MODEL="$LOCAL_MODEL"
export CLAUDE_CODE_MAX_CONTEXT_TOKENS="$LOCAL_CONTEXT"
export CLAUDE_CODE_MAX_OUTPUT_TOKENS="$LOCAL_MAX_OUTPUT"
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1
export CLAUDE_CONFIG_DIR="$LOCAL_CLAUDE_CONFIG_DIR"
mkdir -p "$CLAUDE_CONFIG_DIR"
[[ -f "$CLAUDE_CONFIG_DIR/settings.json" ]] || echo '{"env":{"ENABLE_CLAUDEAI_MCP_SERVERS":"false"}}' > "$CLAUDE_CONFIG_DIR/settings.json"

# Vorabpruefung: lokales Modell muss geladen sein, sonst Abbruch statt Cloud-Fallback
if ! curl -sf --max-time 5 "$LOCAL_BASE_URL/v1/models" | grep -q "\"$LOCAL_MODEL\""; then
  echo "FEHLER: Modell '$LOCAL_MODEL' unter $LOCAL_BASE_URL nicht erreichbar (lms ps / lms load pruefen)." >&2
  exit 2
fi

# Prompt kommt per stdin von Paperclip
exec claude -p \
  --permission-mode acceptEdits \
  --strict-mcp-config \
  --max-turns "$LOCAL_MAX_TURNS" \
  --allowedTools "$LOCAL_ALLOWED_TOOLS" \
  "$@"
