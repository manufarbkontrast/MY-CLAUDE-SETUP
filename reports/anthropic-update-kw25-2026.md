# 📡 Anthropic Update-Report – KW 25 (14.–20. Juni 2026)

> Automatisch generiert am 20. Juni 2026

## 🔴 Sofort relevant für dein Setup

### 1. 📦 Claude Sonnet 4 & Opus 4 endgültig abgeschaltet (15. Juni)

`claude-sonnet-4-20250514` und `claude-opus-4-20250514` geben jetzt Fehler zurück.

**Handlungsbedarf:** `skills/claude-code/references/configuration.md:58` referenziert explizit `claude-opus-4-20250514` als empfohlenes Modell für komplexe Tasks. Durch `claude-opus-4-8` oder `claude-opus-4-6` ersetzen.

### 2. 🔧 Destruktive Git-Befehle in Auto Mode geblockt (v2.1.183, 19. Juni)

Claude Code blockiert jetzt automatisch: `git reset --hard`, `git checkout -- .`, `git clean -fd`, `git stash drop`, `git commit --amend` (wenn nicht vom Agent erstellt), `terraform destroy`.

**Handlungsbedarf:** Mindestens 18 Stellen in Skills/Agents verwenden diese Befehle als Rollback-Muster:

- `skills/engineering/agenthub/references/agent-templates.md` (4× `git checkout -- .`)
- `skills/git-advanced-workflows/SKILL.md` (4× `git reset --hard`)
- `skills/open-source-contributions/` (2× `git reset --hard`)
- `skills/claude-code-bash-patterns/references/git-workflows.md` (3× `git reset --hard`)
- `skills/engineering/autoresearch-agent/SKILL.md` (1× `git reset --hard`)

Diese Patterns werden im Auto Mode jetzt vom System geblockt. Empfehlung: Auf `git revert` oder `git stash` umstellen, oder explizit dokumentieren dass der User bestätigen muss.

### 3. 🆕 Neues Setting: `attribution.sessionUrl` (v2.1.183)

Ermöglicht das Unterdrücken der claude.ai-Session-URL in Commits und PRs.

**Handlungsbedarf:** In `settings.json` aufnehmen, falls die Session-URLs in Commits unerwünscht sind. Relevant für die Git-Hooks in `commands/git/cp.md` und `commands/git/cm.md`, die bereits AI-Attribution-Signaturen blocken.

## 🟡 Interessant, kein sofortiger Handlungsbedarf

| # | Typ | Änderung | Relevanz |
|---|-----|----------|----------|
| 4 | 🆕 | `/config key=value` Inline-Syntax (v2.1.181) | Könnte in Commands/Rules dokumentiert werden |
| 5 | 🆕 | `CLAUDE_CLIENT_PRESENCE_FILE` Env-Variable | Push-Unterdrückung am Rechner |
| 6 | 🔧 | Subagent-Panel: Auto-Hide, 5-Level-Depth-Limit | Betrifft `agents.md` Rule |
| 7 | 🔧 | Auto-Retry bei API-Connection-Drops mid-thinking | Stabilität bei langen Agent-Runs |
| 8 | 🔧 | Model Deprecation Warnings in Claude Code | Warnt bei veralteten Model-IDs |
| 9 | 🔌 | Python SDK v0.110.0: `code_execution_20260120` Tool | API-Integrationen |
| 10 | 🆕 | `sandbox.allowAppleEvents` Setting (macOS) | osascript-basierte Workflows |

## ⚪ Zur Kenntnis

- **SDK v0.111.0** (18. Juni): Refusal-Fallback-Middleware Tagging
- **SDK v0.110.0 Bugfixes**: Bedrock Stream-Events, Header-Merge-Fix
- **Bun 1.4 Upgrade** (v2.1.181)
- **Streaming**: Zeilenweises statt blockweises Rendering langer Absätze
- **~25 Bugfixes** in v2.1.181 (Prompt-Caching, Write/Edit auf Network-Drives, Startup-Regression)
- **Bugfixes v2.1.183**: thinking.disabled.display 400-Fehler, WebSearch in Subagents, tmux-Panes
- **`/config --help`**: Listet alle Shorthand-Keys
- **Docs-URLs migriert**: `docs.anthropic.com` → `platform.claude.com/docs`

## 📋 Handlungsempfehlungen

| Priorität | Aktion | Datei(en) |
|-----------|--------|-----------|  
| **HOCH** | `claude-opus-4-20250514` durch `claude-opus-4-8` ersetzen | `skills/claude-code/references/configuration.md` |
| **HOCH** | `git reset --hard` / `git checkout -- .` Patterns überarbeiten | 6 Skills (siehe oben) |
| **MITTEL** | `attribution.sessionUrl` Setting evaluieren | `settings.json`, `commands/git/cm.md`, `commands/git/cp.md` |
| **NIEDRIG** | `/config key=value` Syntax dokumentieren | Optional in Rules/Commands |

---

## Quellen

- [Anthropic Platform Release Notes](https://platform.claude.com/docs/en/release-notes/overview)
- [Claude Code v2.1.183](https://github.com/anthropics/claude-code/releases)
- [Claude Code v2.1.181](https://github.com/anthropics/claude-code/releases)
- [anthropic-sdk-python v0.110.0–v0.111.0](https://github.com/anthropics/anthropic-sdk-python/releases)
