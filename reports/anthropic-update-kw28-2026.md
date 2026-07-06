# 📡 Anthropic Update-Report – KW 28 (29. Juni – 5. Juli 2026)

> Automatisch generiert am 6. Juli 2026

## 🔴 Sofort relevant für dein Setup

### 1. 📦 Claude Sonnet 5 Launch (30. Juni)

Neues Modell `claude-sonnet-5` — $2/$10 pro MTok (Intro bis 31. Aug., danach $3/$15). 1M Context, 128k Output.

**Breaking Changes:**
- Adaptive Thinking immer an (kann nicht deaktiviert werden)
- Manuelles Extended Thinking (`thinking: {type: "enabled", budget_tokens: N}`) entfernt → 400 Error
- Sampling-Parameter (`temperature`, `top_p`, `top_k`) auf nicht-default = 400 Error
- Neuer Tokenizer: ~30% mehr Tokens für gleichen Text

**Aktion:** `rules/performance.md` referenziert noch **Haiku 4.5, Sonnet 4.5, Opus 4.5** — alles veraltete/retired Modelle. Dringend aktualisieren auf die aktuelle Generation (Haiku 4.5, Sonnet 5 / 4.6, Opus 4.8). Hinweis auf Adaptive Thinking und entfallene Sampling-Parameter ergänzen.

### 2. ⚠️ Fast Mode Opus 4.6 — ABGESCHALTET (29. Juni)

Nicht mehr nur deprecated: **Requests mit `speed: "fast"` laufen auf Standard-Speed**, kein Fehler. Die seit KW27 überfällige Migration auf Opus 4.8 ist jetzt unumgänglich. Fast Mode Opus 4.7 folgt am **24. Juli**.

**Aktion:** Alle Referenzen auf Fast Mode für Opus 4.6 entfernen. Migration auf Opus 4.8 abschließen.

### 3. 🆕 Subagents laufen jetzt im Background by default (v2.1.198, 1. Juli)

Fundamentale Verhaltensänderung: Subagents werden standardmäßig im Hintergrund ausgeführt, nicht mehr im Vordergrund. `run_in_background: false` ist weiterhin möglich.

**Aktion:** `rules/agents.md` um Hinweis ergänzen, dass Subagents jetzt default-background sind. Prüfen ob Agent-Definitions in `agents/` explizit `run_in_background: false` setzen müssen für Agents die Ergebnisse vor dem nächsten Schritt brauchen.

### 4. 🆕 Background Agent Hooks: `agent_needs_input` / `agent_completed` (v2.1.198)

Neue Hook-Events für Background-Agent-Benachrichtigungen. `rules/hooks.md` kennt bisher nur `PreToolUse`, `PostToolUse` und `Stop`.

**Aktion:** `rules/hooks.md` um die neuen Hook-Typen erweitern. In `settings.json` Hooks für Desktop-Notifications bei `agent_completed` und `agent_needs_input` konfigurieren.

### 5. 🆕 `/dataviz` Skill jetzt built-in (v2.1.198)

Claude Code liefert ab v2.1.198 einen eingebauten `/dataviz`-Skill für Chart- und Dashboard-Design mit. Kein Custom-Skill mehr nötig.

**Aktion:** Prüfen ob die 4 Dateien in `skills/` die `dataviz` referenzieren (`ui-ux-pro-max`, `threejs`) Konflikte verursachen. Der Built-in-Skill hat Vorrang.

### 6. 🆕 Stacked Slash-Skill Invocations (v2.1.199, 2. Juli)

Neu: `/skill-a /skill-b do XYZ` lädt bis zu **5 Skills gleichzeitig**. Ermöglicht mächtigeres Chaining.

**Aktion:** `/orchestrate` Command und ähnliche Chaining-Commands in `commands/` können von dieser Funktion profitieren. In `CLAUDE.md` unter "Key Commands" dokumentieren.

### 7. 🔧 AskUserQuestion Auto-Continue deaktiviert (v2.1.200, 3. Juli)

**Breaking Behavior Change:** `AskUserQuestion`-Dialoge pausieren jetzt standardmäßig bis der User antwortet. Vorher: Auto-Continue nach Timeout. Opt-in für idle timeout via `/config`.

**Aktion:** Agent-Workflows prüfen, die auf automatische Fortsetzung nach AskUserQuestion basierten. Betrifft vor allem 5 Skills (`marken-scraper`, `jtl-stammdaten`, `interface-design`, `configure-ecc`) und diverse Commands.

### 8. 🔧 Background Agents committen/pushen automatisch (v2.1.198)

Background-Agents aus `claude agents` committen, pushen und öffnen Draft-PRs automatisch wenn sie Code-Arbeit abschließen.

**Aktion:** `rules/git-workflow.md` um Hinweis ergänzen, dass Background-Agents eigenständig committen. Prüfen ob Conventional-Commit-Konventionen eingehalten werden — ggf. PostToolUse-Hook für Commit-Message-Validation.

## 🟡 Interessant, kein sofortiger Handlungsbedarf

| # | Typ | Änderung | Details |
|---|-----|----------|---------|
| 9 | 📦 | Fable 5 / Mythos 5 wiederhergestellt (1. Juli) | Nach vorübergehender Deaktivierung wieder verfügbar |
| 10 | 🔧 | Permission-Modus "default" → "Manual" umbenannt (v2.1.200) | Kosmetisch, aber CLI/VSCode/JetBrains zeigen jetzt "Manual" statt "default" |
| 11 | 🔧 | Explore Agent erbt Session-Model (v2.1.198) | Capped bei Opus — konsistenteres Verhalten bei Model-Wechsel |
| 12 | 🔧 | Subagents/Compaction erben Extended Thinking Config (v2.1.198) | Bessere Konsistenz in Multi-Agent-Workflows |
| 13 | 🔧 | 429 Auto-Retry mit Backoff für Subscriber (v2.1.199) | Transiente Rate-Limit-Errors werden automatisch retried |
| 14 | 🔧 | `CLAUDE_CODE_RETRY_WATCHDOG` verbessert (v2.1.199) | Hebt Default-Retry-Count und Max-Retries-Cap an |
| 15 | 🔧 | Streaming bei Mid-Stream API-Errors erhalten (v2.1.199) | Partial Output wird jetzt bewahrt statt verworfen |
| 16 | 🔧 | Sonnet 5 ohne Mid-Conversation System Role (v2.1.201) | Harness-Reminders werden anders injiziert bei Sonnet 5 |
| 17 | 🆕 | Claude in Chrome GA (v2.1.198) | Browser-Extension allgemein verfügbar |
| 18 | 🔌 | Managed Agents: Event-Delta-Streaming (30. Juni) | Live-Streaming von Agent-Messages vor Completion |
| 19 | 🔌 | Managed Agents: Session-Config-Overrides (30. Juni) | Model, System Prompt, Tools per Session überschreibbar |
| 20 | 🔌 | Managed Agents: Webhooks für Agent/Deployment Lifecycle (30. Juni) | Neue Webhook-Events ohne Polling |
| 21 | 🔌 | SDK v0.114.0: Sonnet 5 Support (30. Juni) | `claude-sonnet-5` in Python SDK verfügbar |
| 22 | 🔌 | SDK v0.116.0: `agent-memory-2026-07-22` Beta Header (2. Juli) | Neues Agent-Memory-Feature in Vorbereitung |
| 23 | 🆕 | Claude Platform on AWS als Upstream-Provider (v2.1.198) | `anthropicAws` Gateway-Option in Claude Code |

## ⚪ Zur Kenntnis

- **v2.1.200 Bugfixes**: Crash bei non-array `disabledMcpServers` in `.claude.json`, Background-Sessions stoppen nicht mehr nach Sleep/Wake, Rate-Limited-Subagents scheitern sauber statt leer, `claude agents --plugin-dir` gefixt, Worktree-Plugin-Loading, tmux 3.4+ Rendering-Flicker behoben
- **v2.1.199 Bugfixes**: SSL-Cert-Errors mit actionable Guidance, Background-Agent-Daemon-Self-Kill auf Linux, SSH-Cold-Start macOS, `claude stop` vs. Respawn, Remote-Session Memory/Flapping-Fixes, Hook-Matcher stderr mit Exit-Code 2, `SendMessage` Misrouting
- **v2.1.198 Bugfixes**: Netzwerk-Drops Mid-Response, Agent-Team-Member-Death, `/diff` Panel Branch-Switch, Markdown-Table-Overflow Fullscreen, `claude --bg` mit `--print`, Workflow-Progress Truncation, Symlinked Rules, Warp URL-Click
- **SDK v0.115.1** (1. Juli): Nonfunctional Types entfernt — Cleanup, kein Feature-Impact
- **`/agents` Wizard entfernt** (v2.1.198): Keine Auswirkung auf Setup, da Commands den Wizard nicht nutzten

## 📋 Handlungsempfehlungen (kumuliert)

| Priorität | Aktion | Status | Datei(en) |
|-----------|--------|--------|-----------|
| **KRITISCH** | `rules/performance.md` — Model-IDs komplett veraltet (4.5er) | 🔴 Dringend | `rules/performance.md` |
| **KRITISCH** | Fast Mode Opus 4.6 Migration abschließen | 🔴 Abgeschaltet seit 29.06. | Skills, Workflows |
| **HOCH** | Background-Default für Subagents dokumentieren | 🆕 Neu | `rules/agents.md` |
| **HOCH** | Neue Hook-Typen `agent_needs_input`/`agent_completed` | 🆕 Neu | `rules/hooks.md`, `settings.json` |
| **HOCH** | AskUserQuestion-Behavior in Agents prüfen | 🆕 Neu | 5+ Skills, Commands |
| **HOCH** | Background-Agent Auto-Commit dokumentieren | 🆕 Neu | `rules/git-workflow.md` |
| **HOCH** | Stacked Skill-Invocations dokumentieren | 🆕 Neu | `CLAUDE.md` |
| **HOCH** | Retired Model-IDs ersetzen | ❌ Offen seit KW25 | 5 Dateien |
| **HOCH** | `sandbox.credentials` konfigurieren | ❌ Offen seit KW27 | `settings.json`, `rules/security.md` |
| **HOCH** | `autoMode.classifyAllShell` evaluieren | ❌ Offen seit KW27 | `settings.json` |
| **HOCH** | Hook Exact-Match dokumentieren | ❌ Offen seit KW27 | `rules/hooks.md` |
| **MITTEL** | Fast Mode Opus 4.7 → 4.8 Migration (Deadline 24. Juli) | ⏳ 18 Tage | Skills, Workflows |
| **MITTEL** | `CLAUDE_CODE_RETRY_WATCHDOG` für Routinen | ❌ Offen seit KW26 | Env-Variablen |
| **MITTEL** | `po --build` ausführen (Registry) | ❌ Offen seit KW26 | Registry |

---

## 💡 Fazit

**Massive Woche** mit **4 Claude-Code-Releases** (v2.1.198–v2.1.201), **4 SDK-Releases** (v0.114.0–v0.116.0), einem **neuen Modell** (Sonnet 5), und der **Abschaltung von Fast Mode für Opus 4.6**.

Die zwei größten Auswirkungen auf das Setup:

1. **`rules/performance.md` ist kritisch veraltet** — referenziert noch Haiku 4.5, Sonnet 4.5, Opus 4.5. Diese Modelle sind teilweise retired. Mit dem Sonnet 5 Launch ist eine komplette Überarbeitung der Model-Selection-Strategie nötig.

2. **Subagent-Background-Default** (v2.1.198) ändert fundamental, wie Multi-Agent-Workflows ablaufen. Die 182 Agents und `rules/agents.md` sollten daraufhin geprüft werden, welche Agents explizit `run_in_background: false` benötigen.

Positiv: Die Retry-Verbesserungen (429 Auto-Retry, SSL-Error-Handling, Streaming-Preservation) erhöhen die Stabilität aller laufenden Routinen und Background-Agents erheblich.

Die **offenen Aktionen aus KW25–KW27 häufen sich** — aktuell 6 überfällige Items. Empfehlung: Dedizierte Session für Cleanup einplanen.

---

## Quellen

- [Anthropic Platform Release Notes](https://platform.claude.com/docs/en/release-notes/overview)
- [Claude Code v2.1.201](https://github.com/anthropics/claude-code/releases/tag/v2.1.201)
- [Claude Code v2.1.200](https://github.com/anthropics/claude-code/releases/tag/v2.1.200)
- [Claude Code v2.1.199](https://github.com/anthropics/claude-code/releases/tag/v2.1.199)
- [Claude Code v2.1.198](https://github.com/anthropics/claude-code/releases/tag/v2.1.198)
- [anthropic-sdk-python v0.116.0](https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.116.0)
- [anthropic-sdk-python v0.115.0](https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.115.0)
- [anthropic-sdk-python v0.114.0](https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.114.0)
- [KW27-Report](./anthropic-update-kw27-2026.md)
