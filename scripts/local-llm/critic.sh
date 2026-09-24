#!/usr/bin/env bash
# Laesst ein lokales Modell einen Diff gegen den Plan pruefen. Gibt JSON aus:
# {"verdict":"PASS|FAIL","findings":[{"severity":"high|medium|low","file":"...","issue":"...","fix":"..."}]}
# Nutzung: critic.sh <plan.md> [base-ref=main] [test-log] [repo-dir=.]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/models.conf"

PLAN="${1:?Plan-Datei fehlt}"
BASE="${2:-main}"
TEST_LOG="${3:-}"
REPO_DIR="${4:-.}"

DIFF="$(git -C "$REPO_DIR" diff "$BASE" -- . ':!*.lock' ':!package-lock.json' | head -c 200000)"
TESTS="(keine Testausgabe)"
[[ -n "$TEST_LOG" && -f "$TEST_LOG" ]] && TESTS="$(tail -c 20000 "$TEST_LOG")"

SYSTEM='Du bist ein strenger Code-Reviewer. Pruefe, ob der Diff den Plan vollstaendig und korrekt umsetzt.
Achte auf: fehlende Plan-Schritte, verletzte Akzeptanzkriterien, Bugs, Sicherheitsluecken, fehlende Tests.
Keine Stil-Nitpicks. Antworte NUR mit JSON:
{"verdict":"PASS"|"FAIL","findings":[{"severity":"high"|"medium"|"low","file":"...","issue":"...","fix":"..."}]}
FAIL genau dann, wenn es mindestens ein Finding mit severity high oder medium gibt.'

USER="## Plan
$(cat "$PLAN")

## Diff gegen $BASE
$DIFF

## Testausgabe
$TESTS"

REQUEST="$(jq -n --arg m "$CRITIC_MODEL" --arg s "$SYSTEM" --arg u "$USER" \
  '{model:$m, temperature:0.2, messages:[{role:"system",content:$s},{role:"user",content:$u}]}')"

RESPONSE="$(curl -sS "$CRITIC_BASE_URL/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $CRITIC_API_KEY" \
  -d "$REQUEST")"

CONTENT="$(jq -r '.choices[0].message.content // empty' <<<"$RESPONSE")"
# JSON-Block aus der Antwort ziehen (Modelle packen es gern in ```json ... ```)
JSON="$(sed -n '/{/,$p' <<<"$CONTENT" | sed '/^```/d')"
if jq -e '.verdict' >/dev/null 2>&1 <<<"$JSON"; then
  jq . <<<"$JSON"
else
  jq -n --arg raw "$CONTENT" '{verdict:"FAIL",findings:[{severity:"high",file:"-",issue:"Kritiker lieferte kein gueltiges JSON",fix:$raw}]}'
fi
