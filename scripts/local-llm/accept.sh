#!/usr/bin/env bash
# Uebernimmt (oder verwirft) das Ergebnis eines Pipeline-Laufs.
# Nutzung (im Projekt-Repo):
#   accept.sh <slug> ["Commit-Nachricht"]   Worktree committen, per Fast-Forward mergen, aufraeumen
#   accept.sh <slug> --discard              Worktree und Branch local/<slug> loeschen
set -euo pipefail

SLUG="${1:?Slug fehlt (z. B. filter-v3)}"
MODE="${2:-}"
REPO_ROOT="$(git rev-parse --show-toplevel)"
WORKTREE="${WORKTREE:-$REPO_ROOT/../$(basename "$REPO_ROOT")-local-$SLUG}"
BRANCH="local/$SLUG"

cleanup() {
  git -C "$REPO_ROOT" worktree remove --force "$WORKTREE"
  git -C "$REPO_ROOT" branch -D "$BRANCH" >/dev/null
}

if [[ "$MODE" == "--discard" ]]; then
  cleanup
  echo "Verworfen: $BRANCH"
  exit 0
fi

MSG="${MODE:-feat: $SLUG (lokal umgesetzt, Kritiker PASS)}"
git -C "$WORKTREE" add -A
git -C "$WORKTREE" diff --cached --quiet || git -C "$WORKTREE" commit -qm "$MSG"
git -C "$REPO_ROOT" merge --ff-only "$BRANCH"
cleanup
echo "Uebernommen: $BRANCH -> $(git -C "$REPO_ROOT" rev-parse --abbrev-ref HEAD)"
