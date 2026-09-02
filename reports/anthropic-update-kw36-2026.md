# 📡 Anthropic Update-Report – KW 36 (26. Aug – 2. Sep 2026)

> Automatisch generiert am 2. September 2026 — Fable 5.1 Launch-Woche mit Breaking Changes

## 🔴 Sofort relevant für dein Setup

### 1. 📦 Claude Fable 5.1 & Mythos 5.1 (API + Claude Code, 1. Sep.)

Neues Flaggschiff-Modell: `claude-fable-5-1` und `claude-mythos-5-1`. 1M Context, 128k Output, Always-on Adaptive Thinking. Terminal-Bench-Science 52.6% (doppelt so gut wie Fable 5), Terminal-Bench 4.0 +13%. Cache Reads 4x günstiger: $0.25/MTok (0.025x statt 0.1x Base-Preis). Claude Code v2.1.257 setzt Fable 5.1 als Default.

**Typ:** 📦 Neues Modell
**Relevanz:** `rules/performance.md` muss aktualisiert werden — Fable 5.1 als empfohlenes Modell für Code-Tasks. Model-IDs in Skills/Agents prüfen, die `claude-fable-5` explizit referenzieren. Die günstigeren Cache Reads machen längere Kontexte kosteneffizienter.

### 2. 🔧 Breaking Change: `tool_choice` Types `any` und `tool` entfernt (API, 1. Sep.)

Auf Fable 5.1 und Mythos 5.1 geben `tool_choice: "any"` und `tool_choice: {"type": "tool", "name": "..."}` jetzt **400-Fehler**. Nur `"auto"` und `"none"` bleiben unterstützt. Alternative: Strict Tool Use oder Structured Outputs.

**Typ:** 🔧 Breaking Change
**Relevanz:** Direkt betroffen: `skills/project-guidelines-example/SKILL.md` (Zeile 175) nutzt `tool_choice: {"type": "tool", "name": "provide_analysis"}`. Diese Referenz muss auf `auto` + Strict Tool Use umgestellt werden. Die anderen drei Dateien mit `tool_choice`-Referenzen nutzen bereits `"auto"` und sind nicht betroffen.

### 3. 🆕 `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` Environment-Variable (Claude Code v2.1.257, 1. Sep.)

Neue Env-Variable: Erzwingt ein bestimmtes Modell für **alle** Subagenten in einer Session.

**Typ:** 🆕 Neues Feature
**Relevanz:** Direkt relevant für die 182 Agent-Definitionen im Setup. In `rules/agents.md` dokumentieren. Kann in `settings.json` als Env-Variable gesetzt werden, um z.B. alle Subagenten auf Fable 5.1 zu pinnen.

### 4. 🛡️ Containment Escape Rule im Auto-Mode (Claude Code v2.1.257, 1. Sep.)

Neue Sicherheitsregel: Claude Code erkennt und verhindert Container-/Sandbox-Ausbruchsversuche im Auto-Mode.

**Typ:** 🛡️ Security-Verbesserung
**Relevanz:** `rules/security.md` um Hinweis auf die neue Containment-Escape-Regel ergänzen. Betrifft alle Auto-Mode-Nutzung.

### 5. 🔌 Per-Message Effort — Beta (API, 1. Sep.)

Header: `mid-conversation-output-config-2026-07-01`. Effort-Level (`low`/`medium`/`high`) kann pro Nachricht gesetzt werden, ohne den Prompt-Cache zu invalidieren. Verfügbar für Fable 5.1, Mythos 5.1, Opus 5.

**Typ:** 🔌 Neue API-Funktion
**Relevanz:** Ermöglicht dynamische Effort-Steuerung innerhalb einer Konversation — einfache Fragen mit `low`, komplexe mit `high`. In `rules/performance.md` als Optimierungsmuster dokumentieren. `skills/claude-api/references/api-reference.md` erweitern.

### 6. 🔌 Turn-Scoped System Messages — Beta (API, 1. Sep.)

Header: `mid-conversation-system-clear-at-2026-08-21`. System-Nachrichten mit `clear_at: "next_user_message"` gelten nur für den aktuellen Turn und verschwinden danach — ohne Token-Aufbau, ohne Cache-Invalidierung.

**Typ:** 🔌 Neue API-Funktion
**Relevanz:** Ideal für Agent-Workflows mit kontextuellen Instruktionen die nicht akkumulieren sollen. In `rules/agents.md` als neues Pattern dokumentieren.

### 7. 🔌 Thinking Display `"updates"` — Beta (API, 1. Sep.)

Header: `thinking-display-updates-2026-08-18`. Neuer Modus: Gibt kurze Status-Updates als Text zurück, während das volle Reasoning verborgen bleibt. Unterstützt von Fable 5.1, Mythos 5.1, Fable 5.

**Typ:** 🔌 Neue API-Funktion
**Relevanz:** Für Skills/Agents die User-Feedback brauchen ohne volles Thinking zu exponieren. Optional in `rules/performance.md` und `skills/claude-api/references/api-reference.md` ergänzen.

## 🟡 Interessant, kein sofortiger Handlungsbedarf

### 💰 Sonnet 5 Pricing permanent bei $2 / $10 pro MTok (1. Sep.)

Die geplante Preiserhöhung auf $3/$15 zum 1. September wurde endgültig gestrichen. Das Intro-Pricing ist jetzt der Standardpreis.

→ Sonnet 5 bleibt das günstigste leistungsstarke Modell. Relevant für Kosteneinschätzungen in `rules/performance.md`.

### 🔧 Mid-Conversation Tool Changes auf mehr Modellen (Beta)

Jetzt verfügbar auf Fable 5, Mythos 5, Opus 4.8, Opus 5 (Header: `mid-conversation-tool-changes-2026-07-01`). Tools zwischen Turns hinzufügen/entfernen ohne Cache-Invalidierung.

→ Nützlich für dynamische Agentic-Workflows. Kein Setup-Update nötig.

### 🔧 Thinking Block Preservation — neue Controls (Beta)

Neuer Header `thinking-binding-controls-2026-08-01`: API prüft ob Kontext vor Thinking-Blocks unverändert ist. `prefix_mismatch_behavior` steuert Reject vs. Drop. Neue Accounts (ab 31. Aug.) bekommen automatisch 400-Fehler bei Mismatch.

→ Relevant wenn Skills preserved Thinking nutzen. Kein sofortiger Handlungsbedarf.

### 🔧 Web Search/Fetch Domain-Filtering für Managed Agents

`allowed_domains`/`blocked_domains` für `web_search` und `web_fetch` in `agent_toolset_20260401`. Zusätzlich: `max_content_tokens` für web_fetch, `user_location` für web_search.

→ Nützlich für Agents die Web-Zugriff brauchen. Kein Setup-Update nötig.

### 📦 Python SDK v1.1.0–v1.3.0 (26. Aug – 1. Sep.)

Drei Releases in einer Woche:
- **v1.3.0** (1. Sep.): Organization Compliance Settings, User-Profile `order_by`, Memory-Store/Toolset Schema Updates
- **v1.2.0** (27. Aug.): Beta Files/Skills nutzen GA-Shapes, AWS/Bedrock Binary Upload Fix, Tool `view_range` über Size-Cap
- **v1.1.0** (26. Aug.): `updates` Thinking Display Mode, Organization API, Tool Runner `pause_turn` Fix, Legacy Response API entfernt

→ SDK updaten wenn Python-basierte Tools genutzt werden. Kein direktes Setup-Update nötig.

### 🔧 Claude Code v2.1.257 — weitere Änderungen

- "Time format" und `timeZone` Settings für Timestamps
- Zahlreiche Bugfixes für Permissions, MCP-Server, Background-Sessions

→ Claude Code updaten (falls nicht automatisch).

### 🐛 Claude Code v2.1.252 & v2.1.258 — Bug Fixes (31. Aug / 1. Sep.)

- **v2.1.258**: macOS 12 Regression behoben, Remote/Scheduled Sessions "non-empty content" Fix
- **v2.1.252**: Bash "task output swap refused" Fix, "Always allow" Speicher-Fix, Remote Control Stalling Fix

→ Stabilitätsverbesserungen. Updaten.

### 🔧 Content Watermarking & C2PA (1. Sep.)

Text von Fable 5.1/Mythos 5.1 trägt Anthropics Text-Watermark. Bilder/Videos aus Code-Execution tragen C2PA Content Credentials (via Files API).

→ Zur Kenntnis. Keine Setup-Änderung nötig.

### 🔧 Admin API GA (1. Sep.)

User-Management Endpoints (Members, Invites, Groups, Custom Roles) raus aus Beta.

→ Nur Enterprise-relevant.

## ⚪ Zur Kenntnis

- **Fable 5.1 erfordert 30-Tage Data Retention** — kein Zero-Retention ohne Autorisierung
- **Python SDK**: Legacy Response API entfernt (v1.1.0), `import httpx2` direkt statt Alias
- **Fable 5.1 Benchmarks**: Terminal-Bench-Science 52.6% (>2x Fable 5), Terminal-Bench 4.0 +13%

## 📊 Zusammenfassung

| Kategorie | Anzahl |
|-----------|--------|
| 🔴 Sofort relevant | 7 |
| 🟡 Interessant | 9 |
| ⚪ Zur Kenntnis | 3 |

**Top-3 Aktionen diese Woche:**
1. `rules/performance.md` — Fable 5.1 als neues Default-Modell dokumentieren, Per-Message Effort erwähnen
2. `skills/project-guidelines-example/SKILL.md` — `tool_choice: {"type": "tool"}` auf `auto` + Strict Tool Use umstellen
3. `rules/agents.md` — `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` und Turn-Scoped System Messages dokumentieren

---

*Quellen: [Anthropic Platform Release Notes](https://platform.claude.com/docs/en/release-notes/overview) · [API Release Notes](https://platform.claude.com/docs/en/release-notes/api) · [Claude Code Releases](https://github.com/anthropics/claude-code/releases) · [Python SDK Releases](https://github.com/anthropics/anthropic-sdk-python/releases) · [Fable 5.1 Docs](https://platform.claude.com/docs/en/models/fable-5-1/overview)*
