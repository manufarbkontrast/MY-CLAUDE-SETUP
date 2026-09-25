#!/usr/bin/env bash
# Claude Code gegen ein LOKALES Modell (LM Studio) – als Ersatz fuer `claude` in Paperclip.
# Paperclip erlaubt beim Claude-Code-Adapter kein ANTHROPIC_BASE_URL neben einer Abo-/API-Verbindung
# ("provider routing is incompatible"; lokale Provider erst mit PR paperclipai/paperclip#14006),
# und der Process-Adapter ist in der Oberflaeche noch "Coming soon".
# Deshalb: Claude-Code-Adapter behalten, aber als "Command" dieses Skript eintragen. Es setzt die
# lokalen Variablen erst im Prozess, die Paperclip-Pruefung sieht sie nicht.
#
# Zwei Betriebsarten:
#  - Adapter-Modus (Argumente von Paperclip): Argumente durchreichen, aber --model durch das lokale
#    Modell ersetzen und --dangerously-skip-permissions durch acceptEdits + Allowlist ersetzen.
#  - Handbetrieb (keine Argumente): Prompt per stdin, eigene Flags.
#
# Sicherheitsregeln:
#  - Kein Fallback in die Cloud: Ist LM Studio/das Modell nicht erreichbar, bricht das Skript mit Exit 2 ab.
#  - Abo-Token wird entfernt, eigene leere Claude-Konfiguration (keine Connectoren, keine Plugins).
#
# Installation (als Admin) – Dateiname "claude", damit Paperclip seinen Hello-Test ausfuehrt:
#   sudo install -o agents -m 755 scripts/local-llm/paperclip-local-claude.sh /Users/agents/bin/claude
# In Paperclip: Command = /Users/agents/bin/claude
set -euo pipefail

: "${LOCAL_BASE_URL:=http://localhost:1234}"
: "${LOCAL_MODEL:=qwen3.6-35b-a3b}"
: "${LOCAL_CONTEXT:=131072}"
: "${LOCAL_MAX_OUTPUT:=16384}"
: "${LOCAL_MAX_TURNS:=40}"
: "${LOCAL_CLAUDE_CONFIG_DIR:=$HOME/.claude-local}"
: "${LOCAL_CLAUDE_BIN:=$HOME/.local/bin/claude}"
: "${LOCAL_ALLOWED_TOOLS:=Read,Edit,Write,Glob,Grep,Bash(ls:*),Bash(git diff:*),Bash(git status:*),Bash(npm test:*),Bash(npm run:*),Bash(node --test:*),Bash(pytest:*)}"

export PATH="$HOME/.local/bin:/opt/homebrew/opt/node@24/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"

# Echtes Claude Code absolut aufrufen – nie dieses Skript selbst (es heisst ggf. auch "claude")
SELF="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/$(basename "${BASH_SOURCE[0]}")"
if [[ ! -x "$LOCAL_CLAUDE_BIN" || "$(cd "$(dirname "$LOCAL_CLAUDE_BIN")" && pwd)/$(basename "$LOCAL_CLAUDE_BIN")" == "$SELF" ]]; then
  echo "FEHLER: echtes Claude Code nicht gefunden unter $LOCAL_CLAUDE_BIN" >&2
  exit 2
fi

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
# Von Paperclip gesetztes Config-Verzeichnis respektieren (Skills), sonst eigenes leeres
export CLAUDE_CONFIG_DIR="${CLAUDE_CONFIG_DIR:-$LOCAL_CLAUDE_CONFIG_DIR}"
mkdir -p "$CLAUDE_CONFIG_DIR"
[[ -f "$CLAUDE_CONFIG_DIR/settings.json" ]] || echo '{"env":{"ENABLE_CLAUDEAI_MCP_SERVERS":"false"}}' > "$CLAUDE_CONFIG_DIR/settings.json"

# Versionsabfragen ohne Vorabpruefung durchreichen
case "${1:-}" in --version|-v) exec "$LOCAL_CLAUDE_BIN" "$@" ;; esac

# Vorabpruefung: lokales Modell muss geladen sein, sonst Abbruch statt Cloud-Fallback
if ! curl -sf --max-time 5 "$LOCAL_BASE_URL/v1/models" | grep -q "\"$LOCAL_MODEL\""; then
  echo "FEHLER: Modell '$LOCAL_MODEL' unter $LOCAL_BASE_URL nicht erreichbar (lms ps / lms load pruefen)." >&2
  exit 2
fi

if [[ $# -eq 0 ]]; then
  # Handbetrieb: Prompt per stdin
  exec "$LOCAL_CLAUDE_BIN" -p \
    --permission-mode acceptEdits \
    --strict-mcp-config \
    --max-turns "$LOCAL_MAX_TURNS" \
    --allowedTools "$LOCAL_ALLOWED_TOOLS"
fi

# Adapter-Modus: Argumente von Paperclip umschreiben
ARGS=()
REPLACE_NEXT=""
for a in "$@"; do
  if [[ "$REPLACE_NEXT" == "model" ]]; then ARGS+=("$LOCAL_MODEL"); REPLACE_NEXT=""; continue; fi
  if [[ "$REPLACE_NEXT" == "drop" ]]; then REPLACE_NEXT=""; continue; fi
  case "$a" in
    --model) ARGS+=("--model"); REPLACE_NEXT="model" ;;
    --model=*) ARGS+=("--model=$LOCAL_MODEL") ;;
    --dangerously-skip-permissions|--allow-dangerously-skip-permissions) ;;
    --permission-mode) REPLACE_NEXT="drop" ;;
    --permission-mode=*) ;;
    *) ARGS+=("$a") ;;
  esac
done

exec "$LOCAL_CLAUDE_BIN" "${ARGS[@]}" \
  --permission-mode acceptEdits \
  --allowedTools "$LOCAL_ALLOWED_TOOLS"
