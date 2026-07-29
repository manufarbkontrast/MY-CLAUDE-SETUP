# 📡 Anthropic Update-Report – KW 31 (22.–29. Juli 2026)

> Automatisch generiert am 29. Juli 2026

## 🔴 Sofort relevant für dein Setup

### 1. 📦 Claude Opus 5 ist da — neues Default-Modell in Claude Code (24. Juli)

`claude-opus-5` ist live: 1M Context, 128k Output, $5/$25 per MTok (gleicher Preis wie Opus 4.8). Thinking ist per Default an. Claude Code v2.1.219 setzt Opus 5 als neues Default-Opus-Modell.

**Breaking Change:** Thinking kann bei Effort `xhigh` oder `max` **nicht mehr deaktiviert** werden (`thinking: {"type": "disabled"}` → 400 Error). Bei `high` oder darunter weiterhin möglich.

**Aktion:** `rules/performance.md` aktualisieren — dort stehen noch Opus 4.5, Sonnet 4.5, Haiku 4.5 als Modellempfehlungen. Auf aktuelle Modelle (Opus 5, Sonnet 5, Haiku 4.5) umstellen. Die `claude-api` Skill-Referenz wurde bereits serverseitig auf Opus 5 aktualisiert.

### 2. 🆕 Neuer Hook-Typ: `DirectoryAdded` (v2.1.219, 24. Juli)

Neuer Hook der feuert wenn via `/add-dir` oder SDK `register_repo_root` ein Verzeichnis hinzugefügt wird. Ermöglicht automatisches Setup (Dependencies installieren, Linter konfigurieren etc.) wenn ein neues Projekt-Verzeichnis registriert wird.

**Aktion:** In `rules/hooks.md` den neuen Hook-Typ `DirectoryAdded` dokumentieren. Optional: Hook in `settings.json` anlegen, z.B. um bei neuem Verzeichnis automatisch `npm install` oder Linter-Checks auszuführen.

### 3. 🆕 `sandbox.network.strictAllowlist` Setting (v2.1.219, 24. Juli)

Neues Setting das bei gesandboxten Bash-Commands nicht-erlaubte Hosts **ohne Nachfrage blockiert** statt zu prompten. Verschärft die Netzwerk-Kontrolle für Sandbox-Befehle.

**Aktion:** In `settings.json` prüfen ob dieses Setting für dein Setup sinnvoll ist — besonders relevant für die automatisierten Hooks und Routinen, die keine User-Interaktion erlauben.

### 4. 🆕 `workflowSizeGuideline` als Settings-Key (v2.1.219, 24. Juli)

Der Dynamic Workflow Size Wert (aus KW 29 als `/config`-Option gemeldet) ist jetzt auch als `workflowSizeGuideline` direkt in `settings.json` konfigurierbar. Default: `"medium"` (max ~15 Agents).

**Aktion:** In `settings.json` explizit setzen falls du von `"medium"` abweichen willst. In `rules/agents.md` dokumentieren.

### 5. 🔧 Nested Subagents jetzt bis Tiefe 3 (v2.1.219, 24. Juli)

Subagents können jetzt verschachtelte Subagents bis Tiefe 3 spawnen (vorher: 1). Ermöglicht komplexere Agent-Orchestrierung.

**Aktion:** `rules/agents.md` aktualisieren — die neue maximale Verschachtelungstiefe von 3 eröffnet tiefere Orchestrierungs-Muster (z.B. Planner → Reviewer → Fixer als verschachtelte Kette).

### 6. 🔌 SDK: `tool_change` Events + Tool Addition/Removal Blocks (v0.120.0, 24. Juli)

Die Python SDK unterstützt jetzt das dynamische Hinzufügen/Entfernen von Tools mid-conversation (`mid-conversation-tool-changes-2026-07-01` Beta). Neue Event-Typen: `tool_change`.

**Aktion:** Für Skills/Agents die programmatisch mit der API arbeiten (z.B. `ai-sdk-core`): Templates auf das neue Feature prüfen. `skills/ai-sdk-core/templates/anthropic-setup.ts` referenziert bereits Opus 5.

### 7. 🔌 SDK: Neuer Stop Reason `model_context_window_exceeded` (v0.119.0, 23. Juli)

Neuer Stop Reason wenn das Modell das Context-Fenster überschreitet. Ermöglicht sauberes Error-Handling statt generischer Fehler.

**Aktion:** In `rules/patterns.md` beim API Response Format den neuen Stop Reason dokumentieren. Relevant für Skills die API-Calls machen und Stop Reasons auswerten.

### 8. ⚠️ Fast Mode Opus 4.7 endgültig entfernt (24. Juli)

Wie in KW 29 angekündigt: Fast Mode für Opus 4.7 ist jetzt **entfernt**. Requests mit `speed: "fast"` geben einen 400 Error zurück (kein Fallback auf Standard-Speed wie bei 4.6). `/fast` in Claude Code gilt jetzt nur noch für Opus 5 und 4.8.

**Aktion:** Falls noch Referenzen auf Opus 4.7 Fast Mode existieren → entfernen. Die 3 gefundenen Dateien in `reports/` sind historisch und brauchen kein Update.

## 🟡 Interessant, kein sofortiger Handlungsbedarf

### 9. 🔌 Mid-Conversation Tool Changes Beta (24. Juli, API)

Tools können jetzt mid-conversation hinzugefügt/entfernt werden ohne Prompt-Cache zu invalidieren. Verfügbar auf Fable 5, Mythos 5, Opus 4.8 und Opus 5 mit Beta-Header `mid-conversation-tool-changes-2026-07-01`. Potenziell nützlich für dynamische Agent-Workflows.

### 10. 🔌 Server-Side Fallbacks mit `"default"` Mode (24. Juli, API)

Der `fallbacks`-Parameter unterstützt jetzt `"default"` — Anthropic wählt automatisch das passende Fallback-Modell je nach Refusal-Kategorie. Beta-Header: `server-side-fallback-2026-07-01`.

### 11. 🔧 MCP SDK v2 Support in Python SDK (v0.120.1/v0.120.2, 28. Juli)

Die Python SDK unterstützt jetzt MCP SDK v2 neben v1. Relevant wenn eigene MCP-Server auf v2 migrieren. Kein Handlungsbedarf für bestehende MCP-Server (lightpanda, dbhub, linkedin, gsc-mcp).

### 12. 🔧 Effort als primärer Steuerungsmechanismus für Opus 5 (24. Juli)

Opus 5 unterstützt die volle Effort-Leiter (`low`→`medium`→`high`→`xhigh`→`max`), wobei `max` für kritische Aufgaben gedacht ist. Effort ersetzt zunehmend manuelle Thinking-Budget-Konfiguration.

### 13. 🔧 Claude Code: Binary File Handling in Agent Toolset (SDK v0.119.0, 23. Juli)

Fix für Read/Edit-Tools bei Binärdateien im Agent-SDK. Verhindert Crashes wenn Agents versehentlich Binärdateien lesen.

### 14. 🆕 Managed Agents: Effort-Level + Session-Seeding + Webhooks (22. Juli)

Managed Agents unterstützen jetzt `effort` in der Modell-Konfiguration, Session-Seeding mit bis zu 50 initialen Events, und erweiterte Webhooks für Environment/Memory-Store-Lifecycle. Relevant falls du Managed Agents einsetzt.

## ⚪ Zur Kenntnis

- **Claude Code v2.1.220** (25. Juli): Bug-Fixes und Reliability-Verbesserungen, keine neuen Features.
- **Claude Code v2.1.219 Bugfixes**: `claude -p` Text-Output-Fix bei Mid-Stream-Fehlern, `/model`-Picker-Fix, Remote-Control-Fast-Mode-Status-Fix, Vim-Mode-Fix, Screen-Reader-Fix, GNU-Screen-Copy-Fix.
- **Managed Agents**: `version`-Feld beim Agent-Update jetzt optional, Thread-Event-Stream-Deltas für Subagent-Text-Preview.
- **Managed MCP Allowlist**: `${VAR}`-Einträge in Allowlist/Denylist werden jetzt aus der Startup-Umgebung aufgelöst.

---

## Zusammenfassung

**Große Woche.** Claude Opus 5 ist das dominante Update — neues Default-Modell in Claude Code mit gleicher Pricing wie 4.8, aber deutlich besseren Fähigkeiten. Dazu drei neue Claude-Code-Features die direkt Setup-relevant sind: `DirectoryAdded`-Hook, `sandbox.network.strictAllowlist`, und `workflowSizeGuideline` als Settings-Key.

**Priorität 1:** `rules/performance.md` auf aktuelle Modelle aktualisieren (Opus 5, Sonnet 5).
**Priorität 2:** `rules/hooks.md` um `DirectoryAdded` erweitern.
**Priorität 3:** `rules/agents.md` um nested Subagent-Tiefe 3 und `workflowSizeGuideline` erweitern.
