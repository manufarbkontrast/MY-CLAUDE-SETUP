#!/usr/bin/env bash
# TRIBE v2 — RunPod fresh-instance setup
# Tested on: RunPod PyTorch 2.4 template, A100 40 GB / 80 GB
#
# Usage on RunPod:
#   1. Start pod: "PyTorch 2.4" template, A100 40GB or larger
#   2. Open Web Terminal
#   3. curl -sL <url-to-this-script> | bash
#      OR copy-paste this whole script
set -euo pipefail

echo "=== TRIBE v2 setup ==="
echo

# 1. GPU check
echo "--- GPU info ---"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
VRAM_MB=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | head -1)
if [ "$VRAM_MB" -lt 32000 ]; then
  echo "⚠️  WARNING: $VRAM_MB MB VRAM — TRIBE v2 needs ~32 GB minimum. Will likely OOM."
  echo "   Continue anyway? (Ctrl-C to abort, Enter to proceed)"
  read -r _
fi
echo

# 2. Python check
echo "--- Python ---"
python3 --version
PY_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [ "$(echo "$PY_VER < 3.11" | bc -l 2>/dev/null || echo 0)" = "1" ]; then
  echo "⚠️  Python $PY_VER — TRIBE v2 needs 3.11+"
  exit 1
fi
echo

# 3. Pin numpy < 2.1 BEFORE any other install (neuralset compat)
echo "--- pinning numpy ---"
pip install --quiet "numpy<2.1"

# 4. Install uv (fast pip)
echo "--- installing uv ---"
pip install --quiet uv

# 5. Install tribev2 with plotting extras
echo "--- installing tribev2 (this takes ~5-10 min, downloads V-JEPA2 / LLaMA-3.2 deps) ---"
uv pip install --system "tribev2[plotting] @ git+https://github.com/facebookresearch/tribev2.git"

# 6. Install ffmpeg for video handling (if missing)
if ! command -v ffmpeg >/dev/null; then
  echo "--- installing ffmpeg ---"
  apt-get update -qq && apt-get install -y -qq ffmpeg
fi

# 7. Workspace
mkdir -p /workspace/tribe-test/cache /workspace/tribe-test/inputs /workspace/tribe-test/outputs
cd /workspace/tribe-test

# 8. Smoke test — just import
echo "--- smoke test ---"
python3 -c "
import torch
print(f'PyTorch: {torch.__version__}')
print(f'CUDA avail: {torch.cuda.is_available()}')
print(f'Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"CPU\"}')
import tribev2
print(f'tribev2: OK')
from tribev2.demo_utils import TribeModel
print(f'TribeModel: OK')
"
echo
echo "=== setup complete ==="
echo "Next: python3 test_merch.py <your-image-or-video-path>"
