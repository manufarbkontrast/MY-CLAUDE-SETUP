# 📡 Anthropic Update-Report – KW 32 (3.–9. August 2026)

> Automatisch generiert am 8. August 2026 (v2 — inkl. v2.1.224–226, SDK v0.121.0, Plattform 7. Aug.)

## 🔴 Sofort relevant für dein Setup

### 1. 🆕 Cross-Session SendMessage über Maschinen hinweg (v2.1.224, 7. Aug.)

Agents können jetzt via `SendMessage` Nachrichten an Claude-Sessions auf anderen Rechnern senden — nicht nur innerhalb derselben Session. Neue Settings `crossSessionInbound` und `dialogExpiry` steuern Genehmigung und Timeout.

**Typ:** 🆕 Neues Feature
**Relevanz:** 31 Dateien im Setup referenzieren `SendMessage` oder Cross-Session-Patterns (u.a. `agents/closed-loop-coordinator.md`, `agents/frontend-tester.md`). **Aktion:** In `rules/agents.md` die neue Cross-Machine-Fähigkeit dokumentieren. In `settings.json` `crossSessionInbound` konfigurieren (default: Genehmigung erforderlich). Agents wie `closed-loop-coordinator` könnten Cross-Machine-Orchestrierung nutzen.

### 2. 🆕 `archive` Plugin-Quelle für ZIP-Installationen (v2.1.224, 7. Aug.)

Plugins können jetzt direkt von HTTPS-ZIP-URLs installiert werden, mit SHA-256-Pinning für Integrität.

**Typ:** 🆕 Neues Feature
**Relevanz:** Das Setup nutzt 20+ Plugins aus verschiedenen Quellen. **Aktion:** In `skills/claude-code/references/hooks-and-plugins.md` die neue `archive`-Quelle dokumentieren. Nützlich für private/interne Plugins die nicht auf GitHub liegen.

### 3. 🆕 200-Subagent-Cap pro Session entfernt (v2.1.224, 7. Aug.)

Das bisherige Limit von 200 Subagents pro Session existiert nicht mehr.

**Typ:** 🔧 Verbesserung
**Relevanz:** 4 Dateien referenzieren Subagent-Limits (`skills/iterative-retrieval/SKILL.md`, `commands/consult-claude.md`). **Aktion:** Referenzen auf das 200-Subagent-Limit in Skills/Commands entfernen. Orchestrierungs-Workflows (z.B. `/orchestrate`) können jetzt größere Agent-Flotten spawnen.

### 4. 🛡️ Vier Security-Fixes in v2.1.223 (6. Aug.)

Vier unabhängige Bypass-Vektoren geschlossen:

- **Bash Permission Bypass:** Speziell konstruierte Commands konnten sich vor Permission-Checks verstecken.
- **Unicode-Padding in Permission-Prompts:** Tabs/unsichtbare Unicode-Zeichen konnten Genehmigungsanzeigen verschleiern.
- **Workflow-Sandbox-Escape:** Dynamisches `import()` in Workflow-Scripts konnte Code außerhalb der Sandbox ausführen.
- **Agent `bypassPermissions`:** Ignorierte Org-Policy zum Deaktivieren dieses Modus.

**Typ:** 🐛 Bugfix (sicherheitskritisch)
**Relevanz:** **Aktion:** Claude Code auf mindestens v2.1.223 updaten. In `rules/security.md` die neuen Bypass-Vektoren als bekannte, gefixte Risiken vermerken.

### 5. 🔧 `/review` ist jetzt Alias von `/code-review` (v2.1.223, 6. Aug.)

`/review` leitet intern auf `/code-review` weiter und unterstützt Effort-Levels.

**Typ:** 🔧 Verbesserung
**Relevanz:** **Aktion:** In `CLAUDE.md` unter "Key Commands" den Alias `/review` = `/code-review` dokumentieren.

### 6. 🆕 Owner-Wildcards für Marketplace-Settings (v2.1.223, 6. Aug.)

`strictKnownMarketplaces` und `blockedMarketplaces` akzeptieren jetzt `"owner/*"`-Einträge.

**Typ:** 🆕 Neues Feature
**Relevanz:** Das Setup nutzt Plugins aus 8 Marketplace-Quellen. **Aktion:** In `settings.json` ganze Orgs erlauben, z.B. `"anthropics/*"` oder `"levnikolaevich/*"` statt einzelner Repos.

### 7. 🛡️ PreToolUse Auto-Allow Hooks: Bypass in Background Agents gefixt (v2.1.222, 4. Aug.)

Auto-Allow-Hooks konnten Tool-Restrictions in Background Agent Tasks umgehen. Jetzt korrekt durchgesetzt.

**Typ:** 🐛 Bugfix (sicherheitsrelevant)
**Relevanz:** Das Setup hat PreToolUse-Hooks für dev-server-blocking, git-push-Warnungen, .md/.txt-Blocking. Diese greifen jetzt auch in Hintergrund-Agents. **Kein Handlungsbedarf**, Hooks sind jetzt robuster.

### 8. 🛡️ Worktree-Isolation vollständig (v2.1.222, 4. Aug.)

Worktree-isolierte Sessions konnten destruktive Git-Commands gegen das Main Checkout ausführen. Gefixt.

**Typ:** 🐛 Bugfix
**Relevanz:** 27 Dateien referenzieren Worktrees. Agents mit `isolation: 'worktree'` sind jetzt vollständig isoliert. **Kein Handlungsbedarf.**

### 9. 🆕 Sandbox Credential-Masking (v2.1.224, 7. Aug.)

Neue Masking-Optionen für Credentials in der Sandbox: JWT, AWS SigV4, strukturierte Env-Werte. Zusätzlich: `mode: "mask"` für Credential-Dateien auf Linux/WSL (v2.1.221).

**Typ:** 🆕 Neues Feature
**Relevanz:** **Aktion:** In `rules/security.md` die neuen Masking-Optionen dokumentieren. Für Projekte mit AWS/JWT-Auth können Credentials jetzt sicherer in der Sandbox gehandhabt werden.

### 10. 🔌 Python SDK v0.121.0: Mid-Conversation Tool Changes Beta (7. Aug.)

Neues Feature: Tools können jetzt zwischen Turns einer Conversation hinzugefügt/entfernt werden, ohne den Prompt-Cache zu invalidieren (`mid-conversation-tool-changes-2026-07-01` Beta-Header). Außerdem: Session Budgets, Advisor Tool, Inference-Location-Pinning, Skills Auto-Loading von GitHub.

**Typ:** 🆕 Neues Feature / 🔌 Neue API-Funktion
**Relevanz:** Mid-Conversation Tool Changes ist direkt relevant für agentic Workflows. **Aktion:** In `skills/claude-api/` und `rules/performance.md` dokumentieren. Ermöglicht effizientere Multi-Step-Agents die Tools dynamisch laden.

## 🟡 Interessant, kein sofortiger Handlungsbedarf

### Self-Hosted Environments (v2.1.224, 7. Aug.)

Neuer Befehl `claude self-hosted-runner` für Team/Enterprise — eigene Infrastruktur für Claude Code Sessions. Betrifft nur Team/Enterprise-Pläne.

### Gateway Spend-Limit Support (v2.1.225, 8. Aug.)

Usage-Warnungen zeigen jetzt Gateway-Spend-Limits mit Cap-Details und Reset-Zeit. Nützlich für Kostenkontrolle.

### Workspace Trust für `claude agents` (v2.1.225, 8. Aug.)

`claude agents` zeigt jetzt einen Trust-Prompt für untrusted Directories. Stärkt Security bei Agent-Ausführung in fremden Repos.

### Managed Agents: Session Budgets + Advisor (Plattform, 7. Aug.)

Sessions können jetzt ein Spend-Budget bekommen (pausiert bei Erreichen). Advisor-Modell als strategischer Berater für den Primary Thread konfigurierbar. Skills aus GitHub-Repos werden automatisch geladen.

### Managed Agents Skills von GitHub (Plattform, 7. Aug.)

Sessions laden jetzt automatisch Skills aus dem `.claude/skills`-Verzeichnis eines gemounteten GitHub-Repos. Dein Setup-Repo könnte direkt als Skill-Quelle für Managed Agents dienen.

### Inference Hooks Beta für Enterprise (Plattform, 5. Aug.)

Enterprise-Organisationen können einen AI-Security-Server einbinden, der jeden Prompt vor der Inferenz prüft.

### Claude Opus 4.1 retired (Plattform, 5. Aug.)

`claude-opus-4-1-20250805` gibt Fehler zurück. Keine aktiven Referenzen im Setup — kein Handlungsbedarf.

### VSCode Focus View (v2.1.221, 4. Aug.)

`Ctrl+Alt+F` blendet Tool-Aktivität hinter Summaries aus. Verbessert die UX bei langen Agentic-Sessions.

### `prompt-audit` Subcommand (v2.1.221, 4. Aug.)

Neuer Subcommand im `claude-api` Skill. Das Setup hat diesen Skill installiert.

### Remote Control Verbesserungen (v2.1.225, 8. Aug.)

Photos aus der Claude App werden direkt angezeigt, SendMessage kann Remote-Sessions by name starten, diverse Fixes für Session-Management.

### Auto-Mode: Safety-Filter-Refusals zählen nicht mehr gegen Block-Limit (v2.1.225, 8. Aug.)

Safety-Filter-Ablehnungen zählen nicht mehr zum consecutive-block-limit im Auto-Mode. Verhindert vorzeitiges Stoppen.

### Ultraplan entfernt (v2.1.222)

Feature komplett entfernt. Keine Referenzen im Setup.

## ⚪ Zur Kenntnis

| Änderung | Version | Typ |
|----------|---------|-----|
| OAuth 401-Fehler bei Token-Erneuerung gefixt | v2.1.225 | 🐛 |
| MCP OAuth auf macOS: Keychain-Timeout-401s gefixt | v2.1.225 | 🐛 |
| Cross-Session-Messages ohne Expiry in Headless Sessions gefixt | v2.1.225 | 🐛 |
| Conversation History nach Remote Control Resume gefixt | v2.1.225 | 🐛 |
| Long project paths (>200 chars) falsche Session-Directories gefixt | v2.1.224 | 🐛 |
| Sandbox deny-Einträge mit Trailing Slashes bypassbar — gefixt | v2.1.224 | 🛡️ |
| MCP Tools mid-turn deferred ohne Names — gefixt | v2.1.224 | 🐛 |
| Plugin-Install-Records: korrupte Duplikate gefixt | v2.1.224 | 🐛 |
| Remote Control Auto-Start "credentials fetch failed" gefixt | v2.1.224 | 🐛 |
| Worktree-isolierte Sessions Git-Bypass gefixt | v2.1.222 | 🛡️ |
| Stream Idle Timeout bei custom Gateways gefixt | v2.1.222 | 🐛 |
| `/usage` falsche Attribution an MCP-Server gefixt | v2.1.222 | 🐛 |
| Org-restricted Model-Aliase: Fallback auf neustes erlaubtes | v2.1.222 | 🔧 |
| Bash Permission Check Bypass via zsh Regex gefixt | v2.1.221 | 🛡️ |
| PowerShell Permission Checks: Pfade mit Quotes gefixt | v2.1.221 | 🐛 |
| Thinking Toggle ohne Effekt mid-session gefixt | v2.1.221 | 🐛 |
| WebSearch bei xhigh/max Effort ohne Thinking gefixt | v2.1.221 | 🐛 |
| SDK v0.121.0: Opus 4.1 Modelle entfernt | v0.121.0 | 🔧 |
| Dreams unterstützt Claude Opus 5 | Plattform | 🔧 |
| Bug fixes and reliability improvements | v2.1.226 | 🐛 |

## 📊 Zusammenfassung

| Kategorie | Anzahl |
|-----------|--------|
| 🔴 Sofort relevant | 10 |
| 🟡 Interessant | 12 |
| ⚪ Zur Kenntnis | 20 |
| Davon sicherheitskritisch | 8 |

**Update-Priorität:** Claude Code auf v2.1.226 updaten — 8 Security-Fixes, Cross-Session-Messaging, 200-Subagent-Cap entfernt, Archive-Plugin-Source.

**Top-3-Aktionen diese Woche:**
1. `rules/security.md` aktualisieren: Credential-Masking, Sandbox-Bypass-Fixes, Cross-Session-Permissions
2. `rules/agents.md` aktualisieren: 200-Subagent-Limit entfernt, Cross-Machine-SendMessage, `crossSessionInbound`-Setting
3. `settings.json` prüfen: Owner-Wildcards für Marketplace nutzen, `crossSessionInbound`/`dialogExpiry` konfigurieren

**Quellen:**
- platform.claude.com/docs/en/release-notes/overview (7., 5., 1. Aug.)
- github.com/anthropics/claude-code/releases (v2.1.221–v2.1.226)
- github.com/anthropics/anthropic-sdk-python/releases (v0.121.0)
