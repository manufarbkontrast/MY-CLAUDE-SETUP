#!/bin/bash
set -euo pipefail

# ----------------------------------------------------------------------
# Claude Office Setup - Installer (macOS)
#
# Installiert eine schlanke, buero-fokussierte Claude-Code-Konfiguration:
# kuratierte Skills + Commands + saubere settings.json nach ~/.claude/
#
# Ausfuehren (aus dem entpackten Ordner):
#   ./install.sh
# ----------------------------------------------------------------------

# Verzeichnis dieses Skripts (das Bundle selbst ist die Quelle)
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="${HOME}/.claude"

echo ""
echo "  Claude Office Setup"
echo "  ==================="
echo ""

# 1. Pruefen, ob Claude Code installiert ist
if command -v claude &>/dev/null; then
  echo "[1/4] Claude Code CLI gefunden: $(claude --version 2>/dev/null || echo 'ok')"
else
  echo "[1/4] HINWEIS: Claude Code wurde nicht im Terminal gefunden."
  echo "      Das ist OK, wenn du die Desktop-App nutzt (https://claude.ai/download)."
  echo "      Fuer die CLI:  npm install -g @anthropic-ai/claude-code"
fi

# 2. Backup einer bestehenden Konfiguration
if [ -e "${CLAUDE_DIR}/settings.json" ]; then
  BACKUP="${CLAUDE_DIR}/settings.json.backup.$(date +%Y%m%d-%H%M%S)"
  cp "${CLAUDE_DIR}/settings.json" "${BACKUP}"
  echo "[2/4] Bestehende settings.json gesichert -> ${BACKUP}"
else
  echo "[2/4] Keine bestehende settings.json - nichts zu sichern"
fi

# 3. Skills + Commands kopieren (bestehende gleichen Namens werden ueberschrieben)
mkdir -p "${CLAUDE_DIR}/skills" "${CLAUDE_DIR}/commands"

SKILL_COUNT=0
for dir in "${SRC_DIR}/skills/"*/; do
  [ -d "$dir" ] || continue
  cp -r "$dir" "${CLAUDE_DIR}/skills/"
  SKILL_COUNT=$((SKILL_COUNT + 1))
done

CMD_COUNT=0
for file in "${SRC_DIR}/commands/"*.md; do
  [ -f "$file" ] || continue
  cp "$file" "${CLAUDE_DIR}/commands/"
  CMD_COUNT=$((CMD_COUNT + 1))
done

echo "[3/4] ${SKILL_COUNT} Skills und ${CMD_COUNT} Commands installiert"

# 4. Saubere settings.json setzen (nur wenn keine eigene existiert,
#    sonst nicht ueberschreiben - der Nutzer entscheidet)
if [ -e "${CLAUDE_DIR}/settings.json" ]; then
  echo "[4/4] settings.json existiert bereits - NICHT ueberschrieben."
  echo "      Vorlage liegt hier:  ${SRC_DIR}/settings.json"
else
  cp "${SRC_DIR}/settings.json" "${CLAUDE_DIR}/settings.json"
  echo "[4/4] Saubere settings.json installiert"
fi

echo ""
echo "  Fertig!"
echo "  ======="
echo ""
echo "  Installiert nach: ${CLAUDE_DIR}"
echo "  Skills:           ${CLAUDE_DIR}/skills"
echo "  Commands:         ${CLAUDE_DIR}/commands"
echo ""
echo "  Naechster Schritt: Claude Code (App oder Terminal) neu starten."
echo "  Anleitung fuer den Einstieg: siehe README.md in diesem Ordner."
echo ""
