#!/usr/bin/env bash
# Startet Claude Code mit einem lokalen Modell aus LM Studio – so einfach wie `claude`.
#
#   qwen                      interaktive Sitzung mit Qwen
#   gemma                     interaktive Sitzung mit Gemma
#   qwen -p "Frage"           einmalige Antwort (alle claude-Optionen gehen)
#   local-model <lms-id> …    beliebiges Modell aus `lms ls`
#
# Installation (einmalig, als du):
#   ln -sf ~/my-claude-setup/scripts/local-llm/local-model.sh ~/.local/bin/local-model
#   ln -sf ~/my-claude-setup/scripts/local-llm/local-model.sh ~/.local/bin/qwen
#   ln -sf ~/my-claude-setup/scripts/local-llm/local-model.sh ~/.local/bin/gemma
#
# Der Befehlsname (qwen/gemma) waehlt das Modell. Das Skript startet bei Bedarf den LM-Studio-Server,
# laedt das Modell, und startet Claude Code mit schlanker eigener Konfiguration (~/.claude-local),
# damit dein grosses ~/.claude-Setup nicht den Kontext des lokalen Modells fuellt.
# Mit --full nutzt es stattdessen dein normales ~/.claude (Skills, Hooks, Regeln) – kostet Kontext.
set -euo pipefail

NAME="$(basename "$0")"
[[ "$NAME" == "local-model.sh" ]] && NAME="local-model"

# Kurzname -> LM-Studio-Modell (Identifier aus `lms ls`) und Kontextfenster
case "$NAME" in
  qwen)  MODEL="${LOCAL_QWEN_MODEL:-qwen3.6-35b-a3b}"; CONTEXT="${LOCAL_QWEN_CONTEXT:-131072}" ;;
  gemma) MODEL="${LOCAL_GEMMA_MODEL:-gemma-4-31b-it}";  CONTEXT="${LOCAL_GEMMA_CONTEXT:-131072}" ;;
  *)
    MODEL="${1:?Nutzung: local-model <modell-id aus lms ls> [claude-optionen]}"; shift
    CONTEXT="${LOCAL_CONTEXT:-131072}"
    ;;
esac

BASE_URL="${LOCAL_BASE_URL:-http://localhost:1234}"
CONFIG_DIR="${LOCAL_CLAUDE_CONFIG_DIR:-$HOME/.claude-local}"
USE_FULL_CONFIG=0
ARGS=()
for a in "$@"; do
  if [[ "$a" == "--full" ]]; then USE_FULL_CONFIG=1; else ARGS+=("$a"); fi
done

need() { command -v "$1" >/dev/null || { echo "FEHLER: '$1' nicht gefunden." >&2; exit 1; }; }
need claude; need lms; need curl; need jq

# 1. LM-Studio-Server sicherstellen
if ! curl -sf --max-time 3 "$BASE_URL/v1/models" >/dev/null; then
  echo "» Starte LM-Studio-Server …" >&2
  lms server start >/dev/null
fi

# 2. Modell laden, falls noch nicht geladen
state="$(curl -sf --max-time 5 "$BASE_URL/api/v0/models" \
  | jq -r --arg m "$MODEL" '.data[]? | select(.id == $m) | .state' || true)"
if [[ -z "$state" ]]; then
  echo "FEHLER: '$MODEL' ist in LM Studio nicht vorhanden (lms ls)." >&2
  exit 1
fi
if [[ "$state" != "loaded" ]]; then
  echo "» Lade $MODEL (Kontext $CONTEXT) …" >&2
  lms load "$MODEL" --identifier "$MODEL" --context-length "$CONTEXT" -y >/dev/null
fi

# 3. Claude Code gegen das lokale Modell starten
if [[ "$USE_FULL_CONFIG" -eq 0 ]]; then
  export CLAUDE_CONFIG_DIR="$CONFIG_DIR"
  mkdir -p "$CLAUDE_CONFIG_DIR"
  [[ -f "$CLAUDE_CONFIG_DIR/settings.json" ]] || echo '{"env":{"ENABLE_CLAUDEAI_MCP_SERVERS":"false"}}' > "$CLAUDE_CONFIG_DIR/settings.json"
fi
unset CLAUDE_CODE_OAUTH_TOKEN
export ANTHROPIC_BASE_URL="$BASE_URL"
export ANTHROPIC_AUTH_TOKEN="lmstudio"
export ANTHROPIC_API_KEY=""
export ANTHROPIC_MODEL="$MODEL"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="$MODEL"
export ANTHROPIC_DEFAULT_SONNET_MODEL="$MODEL"
export ANTHROPIC_DEFAULT_OPUS_MODEL="$MODEL"
export CLAUDE_CODE_MAX_CONTEXT_TOKENS="$CONTEXT"
export CLAUDE_CODE_MAX_OUTPUT_TOKENS="${LOCAL_MAX_OUTPUT:-16384}"
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1

echo "» $NAME → $MODEL über $BASE_URL (lokal, kein Abo)" >&2
exec claude "${ARGS[@]+"${ARGS[@]}"}"
