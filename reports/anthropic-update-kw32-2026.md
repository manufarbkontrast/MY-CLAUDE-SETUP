# 📡 Anthropic Update-Report – KW 32 (29. Juli – 5. August 2026)

> Automatisch generiert am 5. August 2026

## 🔴 Sofort relevant für dein Setup

### 1. 🛡️ PreToolUse Auto-Allow Hooks: Bypass in Background Agents gefixt (v2.1.222, 4. Aug.)

Auto-Allow-Hooks konnten bisher Tool-Restrictions in Background Agent Tasks umgehen. Jetzt werden PreToolUse-Hooks auch dort korrekt durchgesetzt.

**Typ:** 🐛 Bugfix (sicherheitsrelevant)
**Relevanz:** Das Setup hat PreToolUse-Hooks für dev-server-blocking, git-push-Warnungen und .md/.txt-Blocking. Diese greifen jetzt zuverlässig auch in Hintergrund-Agents. **Kein Handlungsbedarf**, aber die Hooks sind jetzt deutlich robuster.

### 2. 🛡️ Bash Permission-Check Bypass via zsh Regex gefixt (v2.1.221, 4. Aug.)

Bash-Permission-Checks konnten über zsh-Regex-Conditionals umgangen werden.

**Typ:** 🐛 Bugfix (sicherheitsrelevant)
**Relevanz:** Betrifft die grundlegende Sandbox-Sicherheit. **Aktion:** In `rules/security.md` als bekannten (jetzt gefixten) Angriffsvektor vermerken, damit bei eigenen Hook-Commands keine zsh-spezifischen Regex-Konstrukte als Workaround verwendet werden.

### 3. 🔧 Worktree-Isolation jetzt vollständig (v2.1.222, 4. Aug.)

Erweiterung des Fixes aus KW 29: Worktree-Isolation gilt jetzt auch für Dateibearbeitungen (Edit/Write) und Bash, nicht nur für Git-Operationen.

**Typ:** 🐛 Bugfix
**Relevanz:** 27 Dateien im Setup referenzieren Worktrees (u.a. `git-worktree-manager`, `agenthub`, `root-cause-tracing`). Agents mit `isolation: 'worktree'` sind jetzt vollständig isoliert. **Kein Handlungsbedarf**, aber Worktree-basierte Workflows sind jetzt produktionsreif.

### 4. 🆕 `prompt-audit` Subcommand für `claude-api` Skill (v2.1.221, 4. Aug.)

Neuer Subcommand, der Prompts auf Best Practices prüft — passt zum Prompt Optimizer im Setup.

**Typ:** 🆕 Neues Feature
**Relevanz:** **Aktion:** Prüfen ob `prompt-audit` in den Prompt-Optimizer-Workflow (`src/optimize-prompt.ts`) integriert werden kann. Könnte als zusätzlicher Validierungsschritt nach der Prompt-Anreicherung dienen.

### 5. 🔧 `disable-model-invocation` Refusal verbessert (v2.1.222, 4. Aug.)

Wenn Claude ein Skill mit `disable-model-invocation`-Flag invoziert, wird die Ablehnung jetzt klarer kommuniziert.

**Typ:** 🔧 Verbesserung
**Relevanz:** 6 Skills im Setup verwenden `disable-model-invocation` (`skeleton-finder`, `security-pre-commit`, `repository-pattern-scaffold`, `feature-pipeline`, `error-envelope-generator`, `setup-pm`). Die UX bei versehentlicher Invokation wird besser. **Kein Handlungsbedarf.**

### 6. 🆕 Focus View für VSCode (v2.1.221, 4. Aug.)

Neuer Toggle `Ctrl+Alt+F` im Chat-Menü: versteckt Tool-Aktivität hinter expandierbaren Per-Turn-Summaries. Reduziert visuelles Rauschen bei komplexen Workflows.

**Typ:** 🆕 Neues Feature
**Relevanz:** **Aktion:** Unter `CLAUDE.md` → "Key Commands" oder in einem neuen Abschnitt "VSCode Tips" den Shortcut `Ctrl+Alt+F` dokumentieren — besonders nützlich bei `/orchestrate` und Multi-Agent-Workflows.

### 7. 🔌 Python SDK v0.120.2: MCP SDK v2 Support (28. Juli)

Das Python SDK unterstützt jetzt MCP SDK v2 neben v1.

**Typ:** 🔧 Verbesserung
**Relevanz:** Das Setup nutzt 4 MCP-Server (lightpanda, dbhub, linkedin, gsc-mcp). MCP SDK v2 bringt Performance-Verbesserungen. **Aktion:** Bei nächstem `pip install --upgrade anthropic` wird v2-Support automatisch aktiv. Keine Setup-Änderung nötig, aber MCP-Server-Autoren könnten v2-only-Features nutzen.

## 🟡 Interessant, kein sofortiger Handlungsbedarf

### Auto-Mode Security: SendMessage Permission Classifier (v2.1.222)

Nachrichten an andere Agent-Sessions via `SendMessage` werden jetzt vor dem Versand vom Permission Classifier evaluiert. Stärkt die Sicherheit bei Multi-Agent-Orchestrierung — relevant für die 182 Agents im Setup, aber kein Handlungsbedarf.

### Sandbox Credential Masking für Linux/WSL (v2.1.221)

Neuer Mode `"mask"` für Sandbox-Credential-Dateien: erstellt Sentinel-Kopie mit Regex-Extrakt. Nützlich wenn Claude Code auf Linux/WSL mit sensiblen Credentials läuft.

### WebSearch funktioniert jetzt bei Effort xhigh/max (v2.1.221)

WebSearch schlug fehl wenn der Reasoning-Effort auf `xhigh` oder `max` stand und kein Thinking aktiviert war. Jetzt gefixt. Relevant für Skills die WebSearch mit hohem Effort nutzen.

### MCP-Server aus `--mcp-config` in Print Mode (v2.1.221)

MCP-Server die via `--mcp-config` konfiguriert wurden, verbinden sich jetzt vor dem ersten Turn auch im Print Mode. Relevant für CI/CD-Pipelines mit MCP-Servern.

### Dreams unterstützt Claude Opus 5 (1. Aug.)

Die Dreams Research Preview (Managed Agents) unterstützt jetzt auch Claude Opus 5. Betrifft die API, nicht direkt Claude Code.

### Ultraplan entfernt (v2.1.222)

Das experimentelle Ultraplan-Feature wurde entfernt. Keine Referenzen im Setup gefunden — kein Handlungsbedarf.

## ⚪ Zur Kenntnis

| Änderung | Version | Typ |
|----------|---------|-----|
| `/usage-credits` Fehlermeldung korrigiert | v2.1.222 | 🐛 |
| PowerShell Path-Handling mit Anführungszeichen gefixt | v2.1.221 | 🐛 |
| Startup Connectivity Check hinter HTTPS-Proxy gefixt | v2.1.222 | 🐛 |
| Org-restricted Model-Aliase fallen jetzt auf neustes erlaubtes Modell zurück (statt Parent) | v2.1.222 | 🔧 |
| Sandboxed Large Uploads TLS-Fehler gefixt | v2.1.221 | 🐛 |
| Verbesserte `/diff`-Ansicht für Raw Git Blob Content | v2.1.222 | 🔧 |
| Python SDK v0.120.1: MCP extra auf <2 gepinnt | v0.120.1 | 🐛 |

## 📊 Zusammenfassung

| Kategorie | Anzahl |
|-----------|--------|
| 🔴 Sofort relevant | 7 |
| 🟡 Interessant | 6 |
| ⚪ Zur Kenntnis | 7 |
| Davon sicherheitsrelevant | 3 |

**Hinweis:** Die Reports KW 30 und KW 31 fehlen — die Änderungen aus diesen Wochen (insbesondere Claude Opus 5 Launch am 24. Juli) wurden im Kontext erwähnt, aber nicht als separate Reports erstellt.

**Quellen:**
- platform.claude.com/docs/en/release-notes/overview
- github.com/anthropics/claude-code/releases (v2.1.221, v2.1.222)
- github.com/anthropics/anthropic-sdk-python/releases (v0.120.1, v0.120.2)
