# Paperclip als Kontroll-Ebene (Benutzer `agents`)

Stand 25.09.2026, Paperclip 2026.916.1. Läuft unter eigenem macOS-Standardbenutzer `agents` (ohne Apple-ID,
ohne Admin-Rechte). LM Studio (`:1234`) und Kritiker-Server (`:8080`) werden über localhost mitbenutzt.
Oberfläche: http://localhost:3100 (nur loopback).

## Einrichtung (was tatsächlich funktioniert hat)

Als Admin (`manuwolfram`):

```bash
brew install node@24 bash          # Node für alle Benutzer; bash 5 für den Installer
sudo -u agents -i                  # Sitzungswechsel immer als einzelnen Befehl einfügen
```

Als `agents`:

```bash
echo 'setopt interactivecomments' >> ~/.zshrc
for f in ~/.zshrc ~/.zprofile; do
  echo 'export PATH="/opt/homebrew/opt/node@24/bin:/opt/homebrew/bin:$HOME/.local/bin:$PATH"' >> "$f"
done
curl -fsSL https://claude.ai/install.sh | bash
curl -fsSLO https://paperclip.ing/install.sh && curl -fsSLO https://paperclip.ing/install.sh.sha256
shasum -a 256 -c install.sh.sha256
npx --yes paperclipai@2026.916.1 install --version 2026.916.1 --yes   # install.sh reicht --no-prompt falsch durch
paperclipai onboard --yes --bind loopback --no-install-service
```

## Stolpersteine

| Problem | Ursache | Lösung |
|---|---|---|
| `${value,,}: bad substitution` | macOS-bash 3.2 | `/opt/homebrew/bin/bash install.sh` |
| `unknown option '--no-prompt'` | install.sh und CLI passen nicht zusammen | CLI direkt: `npx paperclipai@<ver> install --yes` |
| claude.ai-Connectoren (Gmail, Drive, Slack …) im `agents`-Claude aktiv | hängen am claude.ai-Konto, nicht am Mac-Benutzer | `~/.claude/settings.json` von `agents`: `ENABLE_CLAUDEAI_MCP_SERVERS=false` + `permissions.deny` für jeden `mcp__claude_ai_*`-Server und `mcp__plugin_figma_figma`; prüfen mit `claude -p --output-format stream-json --verbose` (init: `mcp_tools: []`) |
| `Command not found in PATH: "claude"` | LaunchAgent startet mit `/usr/bin:/bin:/usr/sbin:/sbin` ([#12215](https://github.com/paperclipai/paperclip/issues/12215)) | `scripts/local-llm/paperclip-fix-path.sh` (als Admin) oder `PATH` + `CLAUDE_CODE_EXECUTABLE` in den Agent-Env-Variablen |
| `service start` löscht den PATH wieder | Paperclip schreibt die plist bei jedem start/restart/update neu | danach erneut `paperclip-fix-path.sh` |
| `launchctl kickstart … gui/502` schlägt fehl | aus `sudo -u agents`-Sitzung nicht erlaubt | Dienst als Admin mit `sudo launchctl bootout/bootstrap gui/502 …` steuern |
| `Bootstrap failed: 5: Input/output error` | alter Prozess fährt noch herunter oder Dienst ist schon geladen | warten; `launchctl print` prüfen – läuft er, ist alles gut |

## Offen

- Engine im Claude-Formular auf **CLI** statt ACP (nur dann greifen `~/.claude/settings.json`-Regeln sicher)
- Drei Agenten: Planer (claude_local, Abo), Umsetzer (claude_local mit `ANTHROPIC_BASE_URL=http://localhost:1234`),
  Kritiker (process-Adapter → `critic.sh`)
- `dangerouslySkipPermissions` bewusst setzen, Freigaben (Approvals) aktivieren
