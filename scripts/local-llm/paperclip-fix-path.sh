#!/usr/bin/env bash
# Setzt den PATH im Paperclip-LaunchAgent des Benutzers "agents" und laedt den Dienst neu.
# Grund: Paperclip schreibt die plist ohne PATH (Issue paperclipai/paperclip#12215); jedes
# `paperclipai service start/restart/update` macht die Korrektur rueckgaengig -> danach dieses Skript.
# Nutzung (als Admin, nicht als agents): scripts/local-llm/paperclip-fix-path.sh
set -euo pipefail

AGENT_USER="${AGENT_USER:-agents}"
AGENT_UID="$(id -u "$AGENT_USER")"
AGENT_HOME="$(dscl . -read "/Users/$AGENT_USER" NFSHomeDirectory | awk '{print $2}')"
LABEL="ing.paperclip.paperclipai"
PLIST="$AGENT_HOME/Library/LaunchAgents/$LABEL.plist"
SERVICE_PATH="$AGENT_HOME/.local/bin:/opt/homebrew/opt/node@24/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"

[[ -f "$PLIST" ]] || { echo "plist fehlt: $PLIST" >&2; exit 1; }

if sudo /usr/libexec/PlistBuddy -c "Print :EnvironmentVariables:PATH" "$PLIST" >/dev/null 2>&1; then
  sudo /usr/libexec/PlistBuddy -c "Set :EnvironmentVariables:PATH $SERVICE_PATH" "$PLIST"
else
  sudo /usr/libexec/PlistBuddy -c "Add :EnvironmentVariables:PATH string $SERVICE_PATH" "$PLIST"
fi
sudo plutil -lint "$PLIST" >/dev/null

sudo launchctl bootout "gui/$AGENT_UID/$LABEL" 2>/dev/null || true

# Warten, bis Paperclip und die eingebettete Datenbank beendet sind (sonst: "Input/output error")
for _ in $(seq 1 60); do
  pgrep -u "$AGENT_USER" -f "paperclipai/dist/index.js run" >/dev/null || break
  sleep 1
done

sudo launchctl bootstrap "gui/$AGENT_UID" "$PLIST"
sleep 5
sudo launchctl print "gui/$AGENT_UID/$LABEL" | grep -E "state =|pid =|PATH =>"
