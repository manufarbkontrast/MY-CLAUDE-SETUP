#!/usr/bin/env bash
# Fuehrt einen Plan mit einem lokalen Modell in einem isolierten Git-Worktree aus.
# Nutzung: execute.sh <plan.md> [feedback.txt]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/models.conf"

PLAN="${1:?Plan-Datei fehlt}"
FEEDBACK="${2:-}"
PLAN_ABS="$(cd "$(dirname "$PLAN")" && pwd)/$(basename "$PLAN")"
SLUG="$(basename "$PLAN" .md)"
REPO_ROOT="$(git rev-parse --show-toplevel)"
WORKTREE="${WORKTREE:-$REPO_ROOT/../$(basename "$REPO_ROOT")-local-$SLUG}"
BRANCH="local/$SLUG"

if [[ ! -d "$WORKTREE" ]]; then
  git -C "$REPO_ROOT" worktree add -b "$BRANCH" "$WORKTREE" >&2
fi

# Testbefehl aus dem Plan freigeben, damit der Executor seine Arbeit selbst pruefen kann
TEST_CMD="$(sed -n 's/^test_command:[[:space:]]*//p' "$PLAN_ABS" | head -1)"
ALLOWED_TOOLS="$EXECUTOR_ALLOWED_TOOLS"
[[ -n "$TEST_CMD" ]] && ALLOWED_TOOLS="$ALLOWED_TOOLS,Bash($TEST_CMD:*),Bash($TEST_CMD)"

PROMPT="Setze den folgenden Plan exakt um. Halte dich an die genannten Dateien und Schritte.
Fuehre am Ende den Testbefehl aus dem Plan aus. Keine Commits, keine Aenderungen ausserhalb des Plans.
Schlaegt ein Test fehl: pruefe zuerst an den Testdaten, ob die Erwartung im Test stimmt, bevor du den Code aenderst.
Tests, die der Plan woertlich vorgibt, darfst du nicht aendern.

--- PLAN ---
$(cat "$PLAN_ABS")"

if [[ -n "$FEEDBACK" && -s "$FEEDBACK" ]]; then
  PROMPT="$PROMPT

--- FEEDBACK AUS DER LETZTEN RUNDE (zuerst beheben) ---
$(cat "$FEEDBACK")"
fi

if [[ ! -d "$EXECUTOR_CONFIG_DIR" ]]; then
  mkdir -p "$EXECUTOR_CONFIG_DIR"
  echo '{}' > "$EXECUTOR_CONFIG_DIR/settings.json"
fi

cd "$WORKTREE"
CLAUDE_CONFIG_DIR="$EXECUTOR_CONFIG_DIR" \
ANTHROPIC_BASE_URL="$EXECUTOR_BASE_URL" \
ANTHROPIC_AUTH_TOKEN="$EXECUTOR_TOKEN" \
ANTHROPIC_API_KEY="" \
ANTHROPIC_MODEL="$EXECUTOR_MODEL" \
ANTHROPIC_DEFAULT_HAIKU_MODEL="$EXECUTOR_MODEL" \
ANTHROPIC_DEFAULT_SONNET_MODEL="$EXECUTOR_MODEL" \
ANTHROPIC_DEFAULT_OPUS_MODEL="$EXECUTOR_MODEL" \
CLAUDE_CODE_MAX_CONTEXT_TOKENS="$EXECUTOR_CONTEXT" \
CLAUDE_CODE_MAX_OUTPUT_TOKENS="$EXECUTOR_MAX_OUTPUT" \
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 \
  claude -p "$PROMPT" \
    --permission-mode acceptEdits \
    --strict-mcp-config \
    --allowedTools "$ALLOWED_TOOLS" >&2

echo "$WORKTREE"
