# 📡 Anthropic Update-Report – KW 27 (23.–28. Juni 2026)

> Automatisch generiert am 28. Juni 2026

## 🔴 Sofort relevant für dein Setup

### 1. ⚠️ Fast Mode Opus 4.6 — Deadline ÜBERSCHRITTEN

Deprecated am 28. Mai mit "removal ~30 days after launch". **Deadline war ~27. Juni — gestern.** Abschaltung kann jederzeit erfolgen. Betrifft die aktuelle Session (läuft auf `claude-opus-4-6[1m]`).

Zusätzlich: **Fast Mode für Opus 4.7 deprecated** (25. Juni), Removal am 24. Juli. Requests mit `speed: "fast"` auf `claude-opus-4-7` werden dann Fehler zurückgeben.

**Aktion:** Alle Skills/Workflows, die Fast Mode referenzieren, auf Opus 4.8 umstellen. Betrifft 42 Dateien die `fast mode` oder `opus 4.6/4.7` erwähnen.

### 2. ⚠️ KW25/26-Altlasten weiterhin OFFEN — retired Model-IDs

Die retired Model-IDs `claude-opus-4-20250514` und `claude-sonnet-4-20250514` aus dem [KW26-Report](./anthropic-update-kw26-2026.md) sind weiterhin in 5 Dateien. **Seit 15. Juni Fehler bei API-Aufrufen.**

**Aktion:** Wie in KW26 beschrieben — alle durch `claude-opus-4-8` / `claude-sonnet-4-6` ersetzen.

### 3. 🆕 `sandbox.credentials` Setting (v2.1.187, 23. Juni)

Neues Setting blockiert den Zugriff sandboxed Commands auf Credential-Dateien und geheime Umgebungsvariablen. Direkt relevant für die `security.md`-Rule.

**Aktion:** In `settings.json` ergänzen: `"sandbox": {"credentials": "block"}` (genaue Syntax in der Doku prüfen). In `rules/security.md` als Empfehlung aufnehmen.

### 4. 🆕 `autoMode.classifyAllShell` Setting (v2.1.193, 25. Juni)

Routet **alle** Bash/PowerShell-Befehle durch den Auto-Mode-Classifier, nicht nur Arbitrary-Code-Execution-Patterns. Deny-Gründe erscheinen jetzt auch im Transcript und in `/permissions`.

**Aktion:** In `settings.json` evaluieren: `"autoMode": {"classifyAllShell": true}`. Erhöht die Sicherheit, könnte aber häufigere Permission-Prompts verursachen. Zusammen mit dem bestehenden `respondToBashCommands`-Setting (KW26) testen.

### 5. 🔧 Hook-Matcher: Hyphenated Identifiers jetzt Exact-Match (v2.1.195, 26. Juni)

**Breaking Behavior Change:** Hook-Matcher mit Bindestrichen (z.B. `code-reviewer`, `mcp__brave-search`) matchen nicht mehr als Substring, sondern exakt. Für alle Tools eines MCP-Servers muss jetzt `mcp__brave-search__.*` verwendet werden.

Dein Setup ist **nicht direkt betroffen** — die hooks in `settings.json` nutzen nur `Bash`, `Write`, `Edit` ohne Bindestriche. Aber: bei zukünftigen Hooks für MCP-Tools (LinkedIn, Firecrawl, dbhub) **muss** das neue Matching-Verhalten beachtet werden.

**Aktion:** `rules/hooks.md` um Hinweis zum Exact-Match-Verhalten erweitern.

### 6. 🆕 OTEL Response-Logging — potenzielle Überraschung (v2.1.193)

Neues `claude_code.assistant_response` OpenTelemetry-Event. **Achtung:** Wenn `OTEL_LOG_USER_PROMPTS=1` gesetzt ist, werden ab sofort auch **Antworten** geloggt — ohne explizites Opt-in. Abschaltbar mit `OTEL_LOG_ASSISTANT_RESPONSES=0`.

**Aktion:** Falls OTEL in Produktiv-Workflows genutzt wird, prüfen ob Response-Logging gewollt ist. In `rules/security.md` Hinweis ergänzen.

## 🟡 Interessant, kein sofortiger Handlungsbedarf

| # | Typ | Änderung | Details |
|---|-----|----------|---------|
| 7 | 🆕 | `/rewind` nach `/clear` (v2.1.191) | Conversation lässt sich jetzt nach `/clear` wiederherstellen — nützlicher neuer Command |
| 8 | 🆕 | Live File-Path-Autocomplete in `!` Bash-Mode (v2.1.193) | Verbessert die DX beim Bash-Modus aus KW26 |
| 9 | 🆕 | MCP-Auth Startup-Notice (v2.1.193) | Zeigt Hinweis wenn MCP-Server Authentifizierung brauchen → relevant für LinkedIn-MCP, gsc-mcp |
| 10 | 🔧 | MCP `headersHelper` Auto-Reconnect bei 401/403 (v2.1.193) | Helper wird automatisch erneut ausgeführt und reconnected — verbessert Stabilität von LinkedIn-MCP und Firecrawl |
| 11 | 🔧 | MCP Retry bei transienten Netzwerk-Fehlern (v2.1.191) | `tools/list`, `prompts/list`, `resources/list` retrien jetzt automatisch — alle 5 MCP-Server profitieren |
| 12 | 🔧 | MCP OAuth Retry + Headless-Support (v2.1.191) | OAuth Discovery/Token-Requests retrien; Headless-Environments skippen Browser-Popup |
| 13 | 🔧 | Plugin Auto-Rename (v2.1.193) | Marketplace `renames`-Maps werden automatisch in Settings übernommen — bei 22 aktivierten Plugins relevant |
| 14 | 🔧 | Sandbox Network Permissions per Session (v2.1.191) | Hosts mit "Yes" erlaubt gelten für die gesamte Session statt pro Verbindung |
| 15 | 🔧 | ~37% weniger CPU bei Streaming (v2.1.191) | Text-Updates auf 100ms zusammengefasst — spürbar bei langen Sessions |
| 16 | 🔧 | Memory-Pressure Reaping für idle Background-Shells (v2.1.193) | Idle Hintergrund-Shells werden bei Speicherdruck aufgeräumt. Deaktivierbar mit `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` |
| 17 | 🔌 | Rate Limits erhöht (Platform, 26. Juni) | Sonnet/Haiku-Limits = Opus. Usage-Tiers konsolidiert: Start, Build, Scale |
| 18 | 🔌 | SDK v0.112.0: `system.message` Streaming Events (24. Juni) | Neuer Event-Typ für Mid-Conversation System Messages |
| 19 | 🔌 | SDK v0.112.0: User Profile ID in Request Headers (24. Juni) | Neue API-Funktion, ergänzt SDK-Support |
| 20 | 🔌 | SDK v0.112.0: Neue Refusal-Kategorie (24. Juni) | Erweitertes Refusal-Handling |
| 21 | 🆕 | Claude Tag Launch (23. Juni) | Neues Produkt: Claude als Team-Mitglied in Slack. 65% des Anthropic-Produkt-Team-Codes kommt von der internen Version |

## ⚪ Zur Kenntnis

- **v2.1.190** (24. Juni): Bug-Fixes und Reliability-Verbesserungen (kein detailliertes Changelog)
- **v2.1.191 Bugfixes**: Scroll-Position bei Streaming, Background-Agents resurrect nach Stop, `/voice` Org-Policy-Meldung, Hooks mit Komma-Matchern gefixt, Agent-Panel Scroll, Welcome-Splash Overflow
- **v2.1.193 Bugfixes**: `/model` Stale-State nach `/login`, Backgrounding-Abbruch, Pinned Background-Agents, Phantom-Subagent beim Backgrounding
- **v2.1.195 Bugfixes**: Voice-Dictation macOS/CJK-Sprachen, Plugin-Consent, `/plugin` Enable/Disable, Background-Jobs verschwinden, Background-Agent-Daemon Control-Socket
- **v2.1.187 Bugfixes**: `--resume` Fehler, `--json-schema` Structured Output, MCP-Tool-Timeout (5 Min → Abbruch statt Hang), Korean/CJK-Mojibake, Worktree-Cleanup, VSCode große Sessions
- **v2.1.187**: Org-Model-Restrictions im Model-Picker, Mouse-Click in Fullscreen-Menüs, `/install-github-app` Workflow optional, `/btw` Arrow-Navigation, `/plugin` Cleanup-Vorschläge
- **Docs-Domain** bleibt `platform.claude.com/docs` (permanenter 301-Redirect von docs.anthropic.com)

## 📋 Handlungsempfehlungen (kumuliert)

| Priorität | Aktion | Status | Datei(en) |
|-----------|--------|--------|-----------|
| **KRITISCH** | Fast Mode Opus 4.6 → 4.8 Migration | 🔴 Deadline überschritten | Skills, Workflows |
| **HOCH** | Retired Model-IDs ersetzen | ❌ Offen seit KW25 | 5 Dateien (siehe KW26 #1) |
| **HOCH** | `sandbox.credentials` konfigurieren | 🆕 Neu | `settings.json`, `rules/security.md` |
| **HOCH** | `autoMode.classifyAllShell` evaluieren | 🆕 Neu | `settings.json` |
| **HOCH** | Hook Exact-Match-Verhalten dokumentieren | 🆕 Neu | `rules/hooks.md` |
| **HOCH** | OTEL Response-Logging prüfen | 🆕 Neu | Env-Variablen, `rules/security.md` |
| **HOCH** | `respondToBashCommands` konfigurieren | ❌ Offen seit KW26 | `settings.json` |
| **HOCH** | `claude mcp login` in MCP-Doku ergänzen | ❌ Offen seit KW26 | `CLAUDE.md` |
| **HOCH** | `po --build` ausführen (Skill-Frontmatter-Fix) | ❌ Offen seit KW26 | Registry |
| **MITTEL** | `CLAUDE_CODE_RETRY_WATCHDOG` für Routinen | ❌ Offen seit KW26 | Env-Variablen |
| **MITTEL** | `git reset --hard` Patterns in Skills | ❌ Offen seit KW25 | 6 Skills |

---

## 💡 Fazit

Intensive Woche mit **5 Claude-Code-Releases** (v2.1.187–v2.1.195), einem **SDK-Release** (v0.112.0), und **2 Platform-Updates**. Die wichtigsten Neuerungen: `sandbox.credentials` und `autoMode.classifyAllShell` als neue Security-Settings, das Hook-Matcher-Breaking-Change für hyphenierte Identifier, und die Fast-Mode-Deprecation für Opus 4.7.

**Dringendste Aktion:** Die Fast-Mode-Migration auf Opus 4.8 — die Opus-4.6-Deadline ist überschritten, die 4.7-Deadline folgt am 24. Juli. Zusammen mit den seit KW25 offenen retired Model-IDs staut sich hier technische Schuld auf.

Positiv: Die MCP-Verbesserungen (Auto-Reconnect, Retry, OAuth-Headless) erhöhen die Stabilität aller 5 MCP-Server im Setup ohne eigenes Zutun.

---

## Quellen

- [Anthropic Platform Release Notes](https://platform.claude.com/docs/en/release-notes/overview)
- [Claude Code v2.1.195](https://github.com/anthropics/claude-code/releases/tag/v2.1.195)
- [Claude Code v2.1.193](https://github.com/anthropics/claude-code/releases/tag/v2.1.193)
- [Claude Code v2.1.191](https://github.com/anthropics/claude-code/releases/tag/v2.1.191)
- [Claude Code v2.1.190](https://github.com/anthropics/claude-code/releases/tag/v2.1.190)
- [Claude Code v2.1.187](https://github.com/anthropics/claude-code/releases/tag/v2.1.187)
- [anthropic-sdk-python v0.112.0](https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.112.0)
- [Claude Tag Announcement](https://www.anthropic.com/news/introducing-claude-tag)
- [KW26-Report](./anthropic-update-kw26-2026.md)
