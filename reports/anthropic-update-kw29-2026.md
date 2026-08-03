# 📡 Anthropic Update-Report – KW 29 (8.–15. Juli 2026)

> Automatisch generiert am 15. Juli 2026

## 🔴 Sofort relevant für dein Setup

### 1. ⚠️ Breaking: `autoMode` nicht mehr aus `settings.local.json` (v2.1.208, 14. Juli)

`autoMode`-Einstellungen werden **nicht mehr** aus `.claude/settings.local.json` gelesen. Nur noch `~/.claude/settings.json` wird akzeptiert.

**Aktion:** Prüfen ob lokale `settings.local.json`-Dateien in Projekten `autoMode`-Overrides enthalten — diese werden jetzt ignoriert. Ggf. nach `~/.claude/settings.json` migrieren.

### 2. ⚠️ Breaking: `pluginConfigs` nicht mehr aus Projekt-`.claude/settings.json` (v2.1.208)

Plugin-Konfigurationen werden **nicht mehr** aus projektbezogenen `.claude/settings.json`-Dateien geladen. Nur noch `~/.claude/settings.json` zählt. Betrifft potenziell alle 23 aktivierten Plugins.

**Aktion:** Prüfen ob in Projekten lokale `.claude/settings.json` mit Plugin-Overrides existieren. Falls ja: nach `~/.claude/settings.json` verschieben.

### 3. 🔧 Shell-Injection-Fix: `${user_config.*}` in Hooks geblockt (v2.1.207, 11. Juli)

Hook-Commands die `${user_config.*}` Variablen verwenden, werden jetzt als Shell-Injection abgelehnt. Stattdessen: exec-Form oder Environment-Variablen nutzen.

**Aktion:** Die `settings.json` im Setup verwendet kein `${user_config.*}` — **kein Handlungsbedarf**. Aber `rules/hooks.md` sollte dieses Anti-Pattern dokumentieren.

### 4. 🆕 `/doctor` ist jetzt Full Setup Checkup (v2.1.205, 8. Juli)

`/doctor` wurde zum kompletten Setup-Diagnose-Tool erweitert. `/checkup` ist Alias. Prüft u.a. ob eingecheckte `CLAUDE.md`-Dateien Trimming brauchen (v2.1.206).

**Aktion:** In `CLAUDE.md` unter "Key Commands" `/doctor` ergänzen. Der bestehende `/verify`-Command deckt Build/Types/Lint ab — `/doctor` ist komplementär für Setup-Diagnose.

### 5. 🔧 `/review <pr>` zurück zu Single-Pass (v2.1.202, 6. Juli)

`/review <pr>` nutzt wieder einen schnellen Single-Pass-Durchlauf. Für Multi-Agent-Review: `/code-review <level> <pr#>`.

**Aktion:** `CLAUDE.md` unter "Key Commands" präzisieren: `/code-review` ist der Multi-Agent-Review, `/review` der schnelle Einzelpass.

### 6. 🆕 Dynamic Workflow Size Setting (v2.1.202, 6. Juli)

Neues Setting in `/config` → "Dynamic workflow size". Steuert wie viele Agents Workflows standardmäßig spawnen.

**Aktion:** In `rules/agents.md` als Konfigurations-Option dokumentieren. Nützlich für Token-Budget-Steuerung bei Routinen.

### 7. 🆕 Worktree-Isolation gefixt (v2.1.210, 14. Juli)

Subagents mit `isolation: 'worktree'` konnten git-mutierende Befehle im Haupt-Repo statt im Worktree ausführen. Jetzt gefixt.

**Aktion:** Kein direkter Handlungsbedarf, aber Agents die Worktree-Isolation nutzen sind jetzt deutlich sicherer. Die 182 Agents im Setup profitieren.

### 8. 🛡️ Agent Tool gegen Prompt Injection gehärtet (v2.1.210)

Der Agent-Tool-Mechanismus wurde gegen indirekte Prompt Injection gehärtet. Zusammen mit dem Fix, dass `ultracode` nicht mehr auf Non-Human-Input (Webhooks, PR-Comments) feuert.

**Aktion:** `rules/security.md` um Hinweis ergänzen, dass Agent-Prompts von externen Quellen (GitHub-Webhooks, PR-Comments) jetzt besser geschützt sind. Positiv für die PR-Watch-Routinen.

### 9. ⏰ Fast Mode Opus 4.7 Deadline: 24. Juli (noch 9 Tage!)

Erinnerung aus KW25: Fast Mode für Opus 4.7 wird am **24. Juli** entfernt. Danach: 400 Error. Migration auf Opus 4.8 ist Pflicht.

**Aktion:** Alle Referenzen auf Fast Mode für Opus 4.7 identifizieren und auf Opus 4.8 migrieren. Frist: 9 Tage.

## 🟡 Interessant, kein sofortiger Handlungsbedarf

| # | Typ | Änderung | Details |
|---|-----|----------|---------|
| 10 | 🆕 | Screen Reader Mode (v2.1.208) | `--ax-screen-reader` / `CLAUDE_AX_SCREEN_READER=1` — Barrierefreiheit für Terminal |
| 11 | 🆕 | `vimInsertModeRemaps` Setting (v2.1.208) | Zwei-Tasten-Sequenzen in Vim-Mode konfigurierbar (z.B. `jj` → Escape) |
| 12 | 🆕 | `CLAUDE_CODE_PROCESS_WRAPPER` (v2.1.208) | Corporate Launcher Compliance — relevant für Enterprise-Setups |
| 13 | 🔧 | Auto Mode Permission Classifier → Sonnet 5 (v2.1.210) | Default-Modell für Shell-Command-Klassifizierung gewechselt |
| 14 | 🔧 | Memory writes über Limit → explizite Fehler (v2.1.210) | Statt stiller Truncation jetzt klar Fehlermeldung |
| 15 | 🔧 | Catastrophic Removal Commands prompts in Auto Mode (v2.1.208) | `rm -rf` auf unresolved Variables fragt jetzt nach |
| 16 | 🔧 | Auto Mode ohne Env-Var auf Bedrock/Vertex/Foundry (v2.1.207) | `CLAUDE_CODE_ENABLE_AUTO_MODE` nicht mehr nötig, `disableAutoMode` zum Deaktivieren |
| 17 | 🔧 | `/cd` Verzeichnis-Vorschläge (v2.1.206) | Autocomplete-Verbesserung |
| 18 | 🔧 | `/commit-push-pr` auto-allows Push (v2.1.206) | Weniger Permission-Prompts |
| 19 | 🔧 | `/code-review` Qualität auf Opus 4.8 verbessert (v2.1.206) | Bessere Review-Ergebnisse |
| 20 | 🔌 | Admin API: User Management (Platform, 14. Juli) | Enterprise-Feature, Beta — `ce-user-management-2026-07-13` |
| 21 | 🔌 | Dreams unterstützen Fable 5 + Sonnet 5 (Platform, 10. Juli) | Managed Agents Dreaming-Feature erweitert |
| 22 | 🔌 | API Key Expiration in Console (Platform, 8. Juli) | Presets, Custom Duration, Email-Warnung vor Ablauf |
| 23 | 🔌 | `agent-memory-2026-07-22` Header aktiv ab 22. Juli (Platform, 2. Juli) | Memory-Store-Listing-Verhalten ändert sich, neue Pagination-Regeln |
| 24 | 🔌 | SDK v0.116.0 (2. Juli) | `agent-memory-2026-07-22` Beta Header Support |

## ⚪ Zur Kenntnis

- **v2.1.210 Bugfixes**: Elapsed-Time-Counter im Tool-Summary, Grep-Pagination gefixt, Hook-Callback-Timeouts korrekt reported, `cd`-Tracking, MCP-Server-Teardown bei Re-Sync, Plugin-Cache auf Windows/Network-FS, Background-Workers Crash-Loop auf Connection-Reset
- **v2.1.209**: `/model`-Dialog in Background-Sessions gefixt
- **v2.1.208 Performance**: Tool-Call CPU-Overhead um bis zu 7x reduziert (Tool-Pool-Caching), 16 MB File-Edit-Cache statt 1000-File-Pins, Session-Transkript bis 79x kleiner (superseded File-Backups), Memory-Leaks gefixt (eingefügte Bilder, MCP stderr 64 MB/Server, LSP 50-doc Cap)
- **v2.1.207 Bugfixes**: Terminal-Freeze bei langen Listen/Tabellen, Remote-Managed-Settings-Bypass, Agent-Team Crash-Loop, Bedrock Default auf Opus 4.8
- **v2.1.206 Bugfixes**: Login-Expiry-Error, MCP `request_timeout_ms` respektiert, OAuth-MCP Re-Auth nach Token-Refresh, `/usage` Stale-Cache, Ctrl+X entfernt completed Sessions permanent
- **v2.1.205 Bugfixes**: Auto-Update streamt auf Disk (spart ~400 MB Memory), Project-Verify-Skills nicht mehr jede Session neu geschrieben, Cowork VM-Mode gefixt
- **v2.1.204**: SessionStart-Hooks in Headless-Sessions streamen jetzt Events
- **v2.1.203 Performance**: macOS 15-20s Stalling gefixt, Binary-Size -7 MB, Startup-Memory -7 MB (Lazy Loading), Context-Usage analysiert nicht mehr ganzes Transkript, Subagent-Behavior verbessert (weniger Re-Delegation)
- **v2.1.202**: Workflow OpenTelemetry-Attribute (`workflow.run_id`, `workflow.name`), mTLS-Rotation gefixt, Voice-Dictation unbounded Retry gefixt, re-invoked Skills ohne Duplikat-Instruktionen

## 📋 Handlungsempfehlungen (kumuliert)

| Priorität | Aktion | Status | Datei(en) |
|-----------|--------|--------|-----------|
| **KRITISCH** | `rules/performance.md` — Model-IDs komplett veraltet (4.5er) | ❌ Offen seit KW28 | `rules/performance.md` |
| **DRINGEND** | Fast Mode Opus 4.7 → 4.8 Migration (**Deadline 24. Juli, 9 Tage!**) | ⏰ Frist läuft | Skills, Workflows |
| **HOCH** | Breaking: `pluginConfigs` / `autoMode` Location-Changes prüfen | 🆕 Neu | Projekt-`.claude/settings.json` |
| **HOCH** | `/doctor` in CLAUDE.md Key Commands ergänzen | 🆕 Neu | `CLAUDE.md` |
| **HOCH** | `/review` vs `/code-review` Unterschied dokumentieren | 🆕 Neu | `CLAUDE.md` |
| **HOCH** | Dynamic Workflow Size dokumentieren | 🆕 Neu | `rules/agents.md` |
| **HOCH** | `${user_config.*}` Anti-Pattern in hooks.md dokumentieren | 🆕 Neu | `rules/hooks.md` |
| **HOCH** | Background-Default für Subagents dokumentieren | ❌ Offen seit KW28 | `rules/agents.md` |
| **HOCH** | Hook-Typen `agent_needs_input`/`agent_completed` | ❌ Offen seit KW28 | `rules/hooks.md`, `settings.json` |
| **HOCH** | AskUserQuestion-Behavior in Agents prüfen | ❌ Offen seit KW28 | 5+ Skills, Commands |
| **HOCH** | Background-Agent Auto-Commit dokumentieren | ❌ Offen seit KW28 | `rules/git-workflow.md` |
| **HOCH** | Stacked Skill-Invocations dokumentieren | ❌ Offen seit KW28 | `CLAUDE.md` |
| **HOCH** | Retired Model-IDs ersetzen | ❌ Offen seit KW25 | 5 Dateien |
| **HOCH** | `sandbox.credentials` konfigurieren | ❌ Offen seit KW27 | `settings.json`, `rules/security.md` |
| **HOCH** | `autoMode.classifyAllShell` evaluieren | ❌ Offen seit KW27 | `settings.json` |
| **HOCH** | Hook Exact-Match dokumentieren | ❌ Offen seit KW27 | `rules/hooks.md` |
| **MITTEL** | `CLAUDE_CODE_RETRY_WATCHDOG` für Routinen | ❌ Offen seit KW26 | Env-Variablen |
| **MITTEL** | `po --build` ausführen (Registry) | ❌ Offen seit KW26 | Registry |

---

## 💡 Fazit

**Umfangreiche Woche** mit **10 Claude-Code-Releases** (v2.1.201–v2.1.210), **2 SDK-Releases**, und **3 Platform-Updates**.

Die größten Auswirkungen auf das Setup:

1. **Breaking Changes in v2.1.208**: `autoMode` und `pluginConfigs` werden nicht mehr aus projekt-lokalen Settings gelesen. Bei 23 aktivierten Plugins und mehreren Projekten unbedingt prüfen, ob lokale Overrides existieren.

2. **Massive Performance-Verbesserungen**: Tool-Call-Overhead 7x reduziert, Transkript-Größe bis 79x kleiner, Binary -7 MB, diverse Memory-Leaks gefixt. Alle Routinen und Background-Agents profitieren direkt.

3. **Security-Härtung**: Agent-Tool gegen Prompt Injection, Worktree-Isolation, `ultracode`-Keyword nicht mehr auf Webhooks, catastrophic-rm-Prompts. Die PR-Watch- und Background-Agent-Workflows sind deutlich sicherer.

4. **⏰ Fast Mode Opus 4.7 Deadline in 9 Tagen** (24. Juli) — die seit KW25 offene Migration wird jetzt dringend.

Offene Punkte akkumulieren sich: **16 Handlungsempfehlungen** sind offen, davon 2 seit KW25/KW26. Empfehlung: Block von 2-3 Stunden für die Setup-Pflege einplanen.
