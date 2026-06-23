# 📡 Anthropic Update-Report – KW 26 (16.–23. Juni 2026)

> Automatisch generiert am 23. Juni 2026 (Update: v2.1.186 ergänzt)

## 🔴 Sofort relevant für dein Setup

### 1. ⚠️ KW25-Handlungsempfehlungen noch OFFEN — retired Model-IDs

Die retired Model-IDs `claude-opus-4-20250514` und `claude-sonnet-4-20250514` stehen weiterhin in 5 Dateien. **Seit 15. Juni geben diese IDs API-Fehler zurück.**

| Datei | Zeile | Problem |
|-------|-------|---------|
| `skills/claude-code/references/configuration.md` | 58, 232 | `claude-opus-4-20250514` als empfohlenes Modell |
| `skills/claude-api/templates/extended-thinking.ts` | 251 | Hardcoded retired Model-ID |
| `skills/claude-api/SKILL.md` | 321 | `claude-sonnet-4-20250514` als "Stable version" |
| `skills/claude-api/references/top-errors.md` | 362 | Beispielcode mit retired Model |
| `skills/claude-api/references/api-reference.md` | 119 | Model-Tabelle veraltet |

**Aktion:** Alle durch `claude-opus-4-8` / `claude-sonnet-4-6` ersetzen.

### 2. ⏰ Fast Mode für Opus 4.6 wird diese Woche abgeschaltet

Deprecated am 28. Mai mit "removal ~30 days after launch". Deadline ist ~27. Juni. Falls Skills/Workflows Fast Mode mit Opus 4.6 nutzen → auf Opus 4.8 oder 4.7 umstellen.

### 3. 🆕 `claude mcp login <name>` / `claude mcp logout <name>` (v2.1.186)

Neue CLI-Befehle zur MCP-Server-Authentifizierung ohne interaktives `/mcp`-Menü. Inkl. `--no-browser` für SSH-Sessions.

**Aktion:** Relevant für LinkedIn-MCP, Firecrawl und gsc-mcp Setup. In `CLAUDE.md` Abschnitt "MCP Servers" ergänzen, z.B. `claude mcp login linkedin` nach der Installation.

### 4. 🆕 `!` Bash-Befehle triggern automatische Claude-Antwort (v2.1.186)

Neu: `!`-prefixed Bash-Befehle lassen Claude automatisch auf den Output reagieren. Deaktivierbar via `"respondToBashCommands": false` in Settings.

**Aktion:** In `settings.json` explizit konfigurieren (an/aus je nach Präferenz). In `CLAUDE.md` Hooks-Abschnitt dokumentieren.

### 5. 🆕 Skill-Frontmatter akzeptiert jetzt kebab-case, snake_case UND camelCase (v2.1.186)

Flexiblere YAML-Header-Erkennung. Fehlerhafte SKILL.md werden jetzt mit leeren Metadaten geladen statt silent zu failen.

**Aktion:** Bei 466 Skills relevant. `po --build` (Registry-Rebuild) ausführen — eventuell werden Skills erkannt, die vorher silent ignoriert wurden. Prüfen ob die Skill-Zählung sich ändert.

### 6. 🔧 Agent Deny-Rules und Allowed-Types Restrictions gefixt (v2.1.186)

Named subagent spawns werden jetzt korrekt durch Deny-Rules und Agent-Type-Restrictions eingeschränkt. Vorher konnten benannte Subagents die Regeln umgehen.

**Aktion:** Bei 182 Agents relevant. Falls `agents.md`-Rule oder `settings.json` Agent-Restrictions definiert → diese greifen jetzt tatsächlich. Testen ob bestehende Workflows noch funktionieren.

### 7. 🔧 Background-Subagents Permission-Prompts im Main-Session (v2.1.186)

Vorher wurden Permissions im Background automatisch verweigert (auto-deny). Jetzt werden sie im Hauptfenster angezeigt.

**Aktion:** Betrifft `/orchestrate` und andere Multi-Agent-Workflows. `settings.json` Permissions prüfen — was vorher auto-denied wurde, wird jetzt abgefragt. Ggf. Permission-Allowlists erweitern.

## 🟡 Interessant, kein sofortiger Handlungsbedarf

| # | Typ | Änderung | Details |
|---|-----|----------|---------|
| 8 | 🆕 | Status-Filtering (`f`) in `/workflows` Agent-View (v2.1.186) | Agents lassen sich nach Status filtern — nützlich für komplexe Workflows |
| 9 | 🆕 | Skills-Section im `/plugin` Installed Tab (v2.1.186) | Skills werden jetzt direkt im Plugin-Tab sichtbar |
| 10 | 🆕 | `teammateMode: "iterm2"` Setting (v2.1.186) | Warnung wenn Auto-Mode das `it2` CLI nicht findet — nur relevant bei iTerm2-Nutzung |
| 11 | 🔧 | `/review <pr>` nutzt jetzt `/code-review medium` Engine (v2.1.186) | Konsistentere Reviews — der `/review`-Command im Setup profitiert automatisch |
| 12 | 🔧 | `CLAUDE_CODE_MAX_RETRIES` capped bei 15 (v2.1.186) | Neues `CLAUDE_CODE_RETRY_WATCHDOG` für unattended Sessions. Relevant für automatisierte Routinen |
| 13 | 🔧 | Memory Compaction Reminder bei Größenlimit (v2.1.186) | Warnt bevor der Kontext voll ist |
| 14 | 🔧 | `claude mcp get/remove` Typo-Korrektur (v2.1.186) | Schlägt nächsten konfigurierten Server vor bei Tippfehler |
| 15 | 🔌 | SDK v0.110.0: `code_execution_20260120` Tool-Support (18. Juni) | Neuer Code-Execution-Tool-Typ in der Python-SDK |
| 16 | 🔌 | SDK v0.111.0: Refusal-Fallback Middleware Tagging (18. Juni) | Requests werden mit `fallback-refusal-middleware` getaggt |

## ⚪ Zur Kenntnis

- **v2.1.185** (20. Juni): Stream-Stall-Threshold von 10s auf 20s erhöht, Meldungstext geändert
- **v2.1.186 Bugfixes**: Streaming nach Machine-Sleep gefixt, Strikethrough-Rendering, Subagent-Transcript-Scroll, Chrome-Tab-Group-Isolation, Esc/Ctrl+C bei Background-Agents, Session-Cost für Enterprise/Team
- **Workflow Abort**: `agent({schema})` Subagents brechen nach 5 Validierungsfehlern ab statt endlos zu loopen
- **Keine neuen Platform/API-Änderungen** seit 15. Juni
- **Docs-Domain** ist permanent `platform.claude.com/docs` (301-Redirect)

## 📋 Handlungsempfehlungen (kumuliert)

| Priorität | Aktion | Status | Datei(en) |
|-----------|--------|--------|-----------|
| **HOCH** | Retired Model-IDs ersetzen | ❌ Offen seit KW25 | 5 Dateien (siehe #1) |
| **HOCH** | Fast Mode Opus 4.6 → 4.8 Migration | ❌ Deadline ~27. Juni | Settings, Workflows |
| **HOCH** | `claude mcp login` in MCP-Doku ergänzen | 🆕 Neu | `CLAUDE.md` |
| **HOCH** | `respondToBashCommands` konfigurieren | 🆕 Neu | `settings.json` |
| **HOCH** | `po --build` ausführen (Skill-Frontmatter-Fix) | 🆕 Neu | Registry |
| **HOCH** | Agent-Restrictions testen nach Bugfix | 🆕 Neu | `settings.json`, Agents |
| **HOCH** | Permission-Allowlists für Background-Agents prüfen | 🆕 Neu | `settings.json` |
| **MITTEL** | `CLAUDE_CODE_RETRY_WATCHDOG` für Routinen evaluieren | 🆕 Neu | Env-Variablen |
| **MITTEL** | `git reset --hard` Patterns in Skills überarbeiten | ❌ Offen seit KW25 | 6 Skills |

---

## 💡 Fazit

Deutlich mehr los als letzte Woche: **Claude Code v2.1.186** (22. Juni) ist ein umfangreiches Release mit 7 neuen Features und 11 Bugfixes. Die wichtigsten Handlungspunkte: MCP-Login-Commands dokumentieren, `respondToBashCommands` konfigurieren, Registry neu bauen (Skill-YAML-Fix), und Agent-Restrictions nach dem Bugfix testen. Die KW25-Altlasten (retired Model-IDs, Fast-Mode-Migration) sind weiterhin offen und werden mit jedem Tag dringender.

---

## Quellen

- [Anthropic Platform Release Notes](https://platform.claude.com/docs/en/release-notes/overview)
- [Claude Code v2.1.186](https://github.com/anthropics/claude-code/releases/tag/v2.1.186)
- [Claude Code v2.1.185](https://github.com/anthropics/claude-code/releases/tag/v2.1.185)
- [anthropic-sdk-python v0.111.0](https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.111.0)
- [anthropic-sdk-python v0.110.0](https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.110.0)
- [KW25-Report](./anthropic-update-kw25-2026.md)
