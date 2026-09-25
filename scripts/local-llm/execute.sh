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

PROMPT="Setze den folgenden Plan exakt um. Halte dich an die genannten Dateien und Schritte.
Fuehre am Ende den Testbefehl aus dem Plan aus. Keine Commits, keine Aenderungen ausserhalb des Plans.

--- PLAN ---
$(cat "$PLAN_ABS")"

if [[ -n "$FEEDBACK" && -s "$FEEDBACK" ]]; then
  PROMPT="$PROMPT

--- FEEDBACK AUS DER LETZTEN RUNDE (zuerst beheben) ---
$(cat "$FEEDBACK")"
fi

cd "$WORKTREE"
ANTHROPIC_BASE_URL="$EXECUTOR_BASE_URL" \
ANTHROPIC_AUTH_TOKEN="$EXECUTOR_TOKEN" \
ANTHROPIC_API_KEY="" \
ANTHROPIC_MODEL="$EXECUTOR_MODEL" \
ANTHROPIC_DEFAULT_HAIKU_MODEL="$EXECUTOR_MODEL" \
ANTHROPIC_DEFAULT_SONNET_MODEL="$EXECUTOR_MODEL" \
ANTHROPIC_DEFAULT_OPUS_MODEL="$EXECUTOR_MODEL" \
CLAUDE_CODE_MAX_CONTEXT_TOKENS="$EXECUTOR_CONTEXT" \
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 \
  claude -p "$PROMPT" \
    --permission-mode acceptEdits \
    --allowedTools "$EXECUTOR_ALLOWED_TOOLS" >&2

echo "$WORKTREE"
