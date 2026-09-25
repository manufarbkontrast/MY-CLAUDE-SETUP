#!/usr/bin/env bash
# Plan -> lokaler Executor -> Tests -> lokaler Kritiker, bis PASS oder MAX_ROUNDS.
# Nutzung: pipeline.sh <plan.md> [base-ref=HEAD]
# Der Plan braucht eine Zeile "test_command: <befehl>".
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/models.conf"

PLAN="${1:?Plan-Datei fehlt}"
BASE="$(git rev-parse "${2:-HEAD}")"
SLUG="$(basename "$PLAN" .md)"
TEST_CMD="$(sed -n 's/^test_command:[[:space:]]*//p' "$PLAN" | head -1)"
LOG_DIR="$(git rev-parse --show-toplevel)/.plans/logs/$SLUG"
mkdir -p "$LOG_DIR"
FEEDBACK=""
TIMINGS="$LOG_DIR/timings.txt"

# Dauer eines Schritts protokollieren (Sekunden + freier Speicher laut macOS)
log_time() {
  local label="$1" start="$2"
  local free="?"
  command -v memory_pressure >/dev/null && free="$(memory_pressure 2>/dev/null | sed -n 's/.*percentage: //p')"
  echo "$label: $((SECONDS - start))s, Speicher frei: $free" | tee -a "$TIMINGS" >&2
}

for ROUND in $(seq 1 "$MAX_ROUNDS"); do
  echo "== Runde $ROUND/$MAX_ROUNDS: Executor ($EXECUTOR_MODEL)" >&2
  T0=$SECONDS
  WORKTREE="$("$SCRIPT_DIR/execute.sh" "$PLAN" "$FEEDBACK" | tail -1)"
  log_time "Runde $ROUND Executor" "$T0"

  TEST_LOG="$LOG_DIR/round-$ROUND-tests.log"
  TEST_STATUS=0
  if [[ -n "$TEST_CMD" ]]; then
    echo "== Tests: $TEST_CMD" >&2
    T0=$SECONDS
    (cd "$WORKTREE" && bash -c "$TEST_CMD") >"$TEST_LOG" 2>&1 || TEST_STATUS=$?
    log_time "Runde $ROUND Tests" "$T0"
  fi

  # Neue Dateien sichtbar machen, damit sie im Diff des Kritikers auftauchen
  git -C "$WORKTREE" add -N -- . >/dev/null 2>&1 || true
  echo "== Kritiker ($CRITIC_MODEL)" >&2
  REVIEW="$LOG_DIR/round-$ROUND-review.json"
  T0=$SECONDS
  "$SCRIPT_DIR/critic.sh" "$PLAN" "$BASE" "$TEST_LOG" "$WORKTREE" >"$REVIEW"
  log_time "Runde $ROUND Kritiker" "$T0"
  VERDICT="$(jq -r .verdict "$REVIEW")"

  if [[ "$TEST_STATUS" -eq 0 && "$VERDICT" == "PASS" ]]; then
    echo "PASS nach $ROUND Runde(n). Worktree: $WORKTREE" >&2
    echo "Naechster Schritt: Claude-Endreview, dann Branch local/$SLUG uebernehmen." >&2
    exit 0
  fi

  FEEDBACK="$LOG_DIR/round-$ROUND-feedback.txt"
  {
    [[ "$TEST_STATUS" -ne 0 ]] && { echo "Tests schlagen fehl (Exit $TEST_STATUS):"; tail -n 80 "$TEST_LOG"; echo; }
    echo "Kritiker-Findings:"
    jq -r '.findings[] | "- [\(.severity)] \(.file): \(.issue) -> \(.fix)"' "$REVIEW"
  } >"$FEEDBACK"
done

echo "ESKALATION: nach $MAX_ROUNDS Runden kein PASS. Logs: $LOG_DIR" >&2
exit 2
