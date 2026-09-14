# GitHub Scout Report – 2026-09-14

> Automatischer Scan nach neuen/trending Repositories relevant für das Claude-Setup.

## Zusammenfassung

**14 neue relevante Repositories** gefunden. Besonders hervorzuheben: mehrere hochwertige MCP-Server (n8n, Chrome DevTools, Codebase Memory, Context Mode), ein Anti-Faulheits-Skill und neue Agent-Organisationstools. Kein bereits im Setup vorhandenes Repo erneut aufgeführt.

---

## Hoch relevant

### 1. ChromeDevTools/chrome-devtools-mcp
- **Kategorie:** MCP Server
- **Sterne:** 51.876
- **URL:** https://github.com/ChromeDevTools/chrome-devtools-mcp
- **Warum relevant:** Offizieller Chrome DevTools MCP Server — ermöglicht Browser-Debugging direkt aus Claude Code. Könnte lightpanda für DevTools-Szenarien ersetzen oder ergänzen. Puppeteer-basiert, sehr aktiv.

### 2. DeusData/codebase-memory-mcp
- **Kategorie:** MCP Server
- **Sterne:** 43.163
- **URL:** https://github.com/DeusData/codebase-memory-mcp
- **Warum relevant:** Indiziert Codebases als persistenten Knowledge Graph. 158 Sprachen, sub-ms Queries, 99% weniger Token-Verbrauch. Single Binary, zero Dependencies. Ideal für große Projekte mit vielen Skills/Agents.

### 3. czlonkowski/n8n-mcp
- **Kategorie:** MCP Server / Workflow
- **Sterne:** 22.884
- **URL:** https://github.com/czlonkowski/n8n-mcp
- **Warum relevant:** MCP Server der es Claude erlaubt, n8n-Workflows direkt zu erstellen und zu verwalten. Perfekte Ergänzung zum bestehenden n8n-Workflow-Setup. Sehr aktiv gepflegt.

### 4. mksglu/context-mode
- **Kategorie:** Skill / MCP Server
- **Sterne:** 22.717
- **URL:** https://github.com/mksglu/context-mode
- **Warum relevant:** Context-Window-Optimierung für AI Coding Agents. 98% Output-Reduktion durch Sandbox-Routing, Session Memory, Hooks-Integration. Unterstützt 17 Plattformen inkl. Claude Code. Als Plugin verfügbar.

### 5. Leonxlnx/unlazy
- **Kategorie:** Skill
- **Sterne:** 3.335
- **URL:** https://github.com/Leonxlnx/unlazy
- **Warum relevant:** Anti-Faulheits-Skill basierend auf der "Depth Tree"-Methode — splittet Tasks N Ebenen tief und gibt jedem Blatt das volle Zeitbudget. Basiert auf aktueller Forschung zu LLM-Laziness (2025–2026). Direkt als Claude Code Skill nutzbar.

### 6. tigerless-labs/agent-memory
- **Kategorie:** Tool / MCP Server
- **Sterne:** 1.385 (erstellt 01.09.2026)
- **URL:** https://github.com/tigerless-labs/agent-memory
- **Warum relevant:** Long-Term Memory Runtime mit Markdown als Source of Truth. Lokale Retrieval, Sleep-Time Manage Layer. Claude Code und Codex teilen einen Store. Kein API-Key nötig. Ergänzt die bestehenden Memory-Skills (memory-palace etc.).

### 7. cbrock84/headcount
- **Kategorie:** Skill / Plugin
- **Sterne:** 1.373 (erstellt 28.08.2026)
- **URL:** https://github.com/cbrock84/headcount
- **Warum relevant:** Agent-Organisation als Firmenstruktur — 15+ Abteilungen, 125+ Skills, einzeln installierbar. Claude Code Plugin. Könnte als komplementäre Skill-Bibliothek neben den bestehenden 466 Skills dienen.

---

## Mittel relevant

### 8. sansan0/TrendRadar
- **Kategorie:** Tool / MCP Server
- **Sterne:** 62.232
- **URL:** https://github.com/sansan0/TrendRadar
- **Warum relevant:** AI-gesteuerte Trend- und Meinungsüberwachung mit Multi-Plattform-Aggregation, RSS und MCP-Server-Integration. Unterstützt Telegram, Slack, E-Mail-Push. Könnte für automatisiertes Markt-/SEO-Monitoring nützlich sein.

### 9. wshobson/maverick-mcp
- **Kategorie:** MCP Server / Finanz-Tool
- **Sterne:** 671
- **URL:** https://github.com/wshobson/maverick-mcp
- **Warum relevant:** Persönlicher Stock-Analysis MCP Server vom gleichen Autor wie das bereits genutzte wshobson/agents. Technische Analyse, Backtesting, yfinance-Integration. Direkt als MCP Server für Claude nutzbar. Relevant für Finanzanalyse-Kategorie.

### 10. activepieces/activepieces
- **Kategorie:** Workflow
- **Sterne:** 24.433
- **URL:** https://github.com/activepieces/activepieces
- **Warum relevant:** AI Agents & MCP Workflow Automation mit ~400 MCP-Servern. Self-hosted n8n-Alternative mit nativer AI-Agent-Integration. Könnte als Ergänzung zu n8n für MCP-spezifische Workflows interessant sein.

### 11. nateherkai/scroll-craft
- **Kategorie:** Skill
- **Sterne:** 2.407 (erstellt 22.08.2026)
- **URL:** https://github.com/nateherkai/scroll-craft
- **Warum relevant:** Skill für scroll-driven, immersive Websites. Accessibility, Design-System, Scroll-Animationen. Als Claude Code Plugin verfügbar. Ergänzt die bestehenden Frontend-Dev-Skills.

### 12. FlorianBruniaux/claude-code-ultimate-guide
- **Kategorie:** Inspiration / Referenz
- **Sterne:** 5.964
- **URL:** https://github.com/FlorianBruniaux/claude-code-ultimate-guide
- **Warum relevant:** Umfassendstes Claude Code Guide (430K+ Zeilen). Enthält agentic Workflows, Hooks, Skills, MCP Server Templates und Quizze. Gute Quelle für fehlende Skills/Patterns.

### 13. google/artemis
- **Kategorie:** Tool
- **Sterne:** 4.924 (erstellt 13.08.2026)
- **URL:** https://github.com/google/artemis
- **Warum relevant:** Googles Open-Source Android-Automatisierung über natürliche Sprache. 99%+ Erfolgsrate auf AndroidWorld Benchmark. Integration mit Claude Code. Relevant für Mobile-Testing-Workflows.

### 14. yetone/cumora
- **Kategorie:** Tool / Workflow
- **Sterne:** 3.592 (erstellt 17.08.2026)
- **URL:** https://github.com/yetone/cumora
- **Warum relevant:** Cross-Platform Team-Chat mit AI Agents als First-Class-Teammates. Cloud- oder BYOK-Modus (Claude Code / Codex). Interessant für Multi-Agent-Kollaboration.

---

## Niedrig relevant (Notiz)

| Repo | Sterne | Grund |
|------|--------|-------|
| ruvnet/ruflo | 72.368 | Multi-Player Agent Swarms, zu breit für direkten Setup-Import |
| Pinvou/pinvou-agent | 1.927 | Desktop AI Agent, eher eigenständiges Produkt als Claude-Ergänzung |
| zebbern/claude-code-guide | 4.621 | Guide/Tutorial, keine neuen Skills zum Importieren |
| Nanako0129/sepia | 2.591 | De-AI Writing Skill, Nische (Fiction/Prose) |

---

## Übersprungen (bereits im Setup)

| Repo | Grund |
|------|-------|
| bytebase/dbhub | Bereits als MCP Server konfiguriert |
| stickerdaniel/linkedin-mcp-server | Bereits als MCP Server konfiguriert |
| OthmanAdi/planning-with-files | Bereits via trailofbits/skills-curated installiert |
| davepoon/buildwithclaude | Hub/Directory, kein Plugin |
| n8n-io/n8n | Plattform selbst, kein Claude-spezifisches Tool |

---

## Top-3 Empfehlungen zur Installation

1. **n8n-mcp** — Sofort installierbar als MCP Server, direkte n8n-Workflow-Steuerung aus Claude
2. **codebase-memory-mcp** — Knowledge Graph für große Codebases, massive Token-Einsparung
3. **context-mode** — Context-Window-Optimierung als Plugin, reduziert Token-Verbrauch um 98%

---

*Nächster Scout-Scan: 2026-09-15*
