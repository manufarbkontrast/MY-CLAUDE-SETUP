#!/usr/bin/env bash
set -euo pipefail

# install-new-tools.sh — Installiert die 6 neuen Tools (Juli 2026)
# Ausfuehren: chmod +x install-new-tools.sh && ./install-new-tools.sh

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

ok()   { echo -e "${GREEN}[OK]${NC} $1"; }
fail() { echo -e "${RED}[FEHLER]${NC} $1"; }
info() { echo -e "${YELLOW}[INFO]${NC} $1"; }

echo ""
echo "============================================"
echo "  6 neue Tools installieren (Juli 2026)"
echo "============================================"
echo ""

# 1. codebase-memory-mcp
echo "--- 1/6: codebase-memory-mcp (Code-Knowledge-Graph MCP Server) ---"
if command -v codebase-memory-mcp &>/dev/null; then
  ok "codebase-memory-mcp bereits installiert ($(codebase-memory-mcp --version 2>/dev/null || echo 'version unknown'))"
else
  info "Installiere codebase-memory-mcp..."
  if curl -fsSL https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh | bash; then
    ok "codebase-memory-mcp installiert"
    if command -v codebase-memory-mcp &>/dev/null; then
      info "Registriere als MCP-Server bei Claude Code..."
      codebase-memory-mcp install 2>/dev/null || claude mcp add codebase-memory -- codebase-memory-mcp 2>/dev/null || info "Bitte manuell registrieren: claude mcp add codebase-memory -- codebase-memory-mcp"
    fi
  else
    fail "Installation fehlgeschlagen. Manual: https://github.com/DeusData/codebase-memory-mcp/releases"
  fi
fi
echo ""

# 2. claude-video Plugin
echo "--- 2/6: claude-video (/watch Command) ---"
info "Pruefe Dependencies: yt-dlp und ffmpeg..."
if ! command -v yt-dlp &>/dev/null; then
  info "Installiere yt-dlp..."
  pip install yt-dlp 2>/dev/null || pip3 install yt-dlp 2>/dev/null || brew install yt-dlp 2>/dev/null || fail "yt-dlp konnte nicht installiert werden"
else
  ok "yt-dlp vorhanden"
fi
if ! command -v ffmpeg &>/dev/null; then
  info "Installiere ffmpeg..."
  brew install ffmpeg 2>/dev/null || apt-get install -y ffmpeg 2>/dev/null || fail "ffmpeg konnte nicht installiert werden"
else
  ok "ffmpeg vorhanden"
fi
info "Registriere claude-video Marketplace + Plugin..."
claude plugin enable "watch@bradautomates-claude-video" 2>/dev/null && ok "claude-video Plugin aktiviert" || info "Plugin manuell aktivieren: claude plugin enable watch@bradautomates-claude-video"
echo ""

# 3. strix (AI-Pentesting)
echo "--- 3/6: strix-agent (AI-Pentesting) ---"
if command -v strix &>/dev/null; then
  ok "strix bereits installiert ($(strix --version 2>/dev/null || echo 'version unknown'))"
else
  PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "0.0")
  PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
  PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)
  if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 12 ]; then
    info "Installiere strix-agent (Python $PYTHON_VERSION)..."
    pipx install strix-agent 2>/dev/null || pip install strix-agent 2>/dev/null || pip3 install strix-agent
    ok "strix-agent installiert"
  else
    fail "Python $PYTHON_VERSION zu alt (braucht >= 3.12). Upgrade: brew install python@3.12"
    info "Danach: pipx install strix-agent"
  fi
fi
echo ""

# 4. Agent-Reach (Social-Media-Zugriff)
echo "--- 4/6: Agent-Reach (Social-Media-Content) ---"
if command -v agent-reach &>/dev/null; then
  ok "agent-reach bereits installiert ($(agent-reach --version 2>/dev/null || echo 'version unknown'))"
else
  info "Installiere agent-reach..."
  pipx install "https://github.com/Panniantong/agent-reach/archive/main.zip" 2>/dev/null \
    || pip install "https://github.com/Panniantong/agent-reach/archive/main.zip" 2>/dev/null \
    || pip3 install "https://github.com/Panniantong/agent-reach/archive/main.zip"
  if command -v agent-reach &>/dev/null; then
    ok "agent-reach installiert"
    info "Konfiguriere Backends..."
    agent-reach install --env=auto --safe 2>/dev/null || info "Backends manuell konfigurieren: agent-reach install --env=auto"
  else
    fail "Installation fehlgeschlagen"
  fi
fi
echo ""

# 5. CodexBar (macOS only)
echo "--- 5/6: CodexBar (AI-Provider-Monitor) ---"
if [[ "$(uname -s)" == "Darwin" ]]; then
  if command -v codexbar &>/dev/null || [ -d "/Applications/CodexBar.app" ]; then
    ok "CodexBar bereits installiert"
  else
    info "Installiere CodexBar via Homebrew..."
    brew install --cask codexbar 2>/dev/null && ok "CodexBar installiert" || fail "Installation fehlgeschlagen. Manual: https://github.com/steipete/CodexBar/releases"
  fi
else
  info "CodexBar ist macOS-only. Ueberspringe auf $(uname -s)."
fi
echo ""

# 6. Astryx (React Design System)
echo "--- 6/6: Astryx (React Design System) ---"
info "Astryx ist eine Projekt-Dependency, kein globales Tool."
info "In React-Projekten installieren: npm install @anthropic/astryx"
info "Docs: https://facebook.github.io/astryx/"
echo ""

# Zusammenfassung
echo "============================================"
echo "  Installation abgeschlossen"
echo "============================================"
echo ""
echo "Verifiziere:"
command -v codebase-memory-mcp &>/dev/null && ok "codebase-memory-mcp" || fail "codebase-memory-mcp"
command -v yt-dlp &>/dev/null && ok "yt-dlp (fuer claude-video)" || fail "yt-dlp"
command -v ffmpeg &>/dev/null && ok "ffmpeg (fuer claude-video)" || fail "ffmpeg"
command -v strix &>/dev/null && ok "strix-agent" || fail "strix-agent (braucht Python 3.12+)"
command -v agent-reach &>/dev/null && ok "agent-reach" || fail "agent-reach"
if [[ "$(uname -s)" == "Darwin" ]]; then
  (command -v codexbar &>/dev/null || [ -d "/Applications/CodexBar.app" ]) && ok "CodexBar" || fail "CodexBar"
fi
echo ""
info "Settings synchronisieren:"
echo "  cp settings.json ~/.claude/settings.json"
echo ""
info "Agent-Reach Backends pruefen:"
echo "  agent-reach doctor"
echo ""
