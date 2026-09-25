#!/usr/bin/env bash
# Startet den Kritiker (gpt-oss-120b) als OpenAI-kompatiblen Server ueber mlx_lm.
# Nutzung: critic-server.sh   (laeuft im Vordergrund, Ctrl+C beendet)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/models.conf"
: "${MLX_VENV:=$HOME/.venvs/mlx}"

source "$MLX_VENV/bin/activate"
exec mlx_lm.server --model "$CRITIC_MODEL_PATH" --port "$CRITIC_PORT"
