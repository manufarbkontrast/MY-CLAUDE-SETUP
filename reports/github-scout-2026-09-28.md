## GitHub-Scout-Report – 2026-09-28

Erster systematischer Scan nach neuen, relevanten Repositories fuer das Claude-Setup.
Durchsucht: MCP Server, AI Agents, Prompt Engineering, n8n, Claude Skills, LLM Tooling, Finanz-Tools.

---

### Hoch relevant

#### 1. fast-jev-compaction
- **URL:** https://github.com/tamaratran/fast-jev-compaction
- **Sterne:** 7.049 | **Erstellt:** 17.09.2026
- **Kategorie:** Plugin / Tool
- **Warum relevant:** Claude-Code-Plugin, das die eingebaute Compaction durch Jev-basierte Entscheidungen ersetzt — jeder Tool-Call wird bewertet, veraltete werden gekuerzt oder entfernt. Direkt als Plugin installierbar, verbessert Context-Management bei langen Sessions erheblich.

#### 2. golive-skill
- **URL:** https://github.com/mikehasa/golive-skill
- **Sterne:** 1.023 | **Erstellt:** 23.09.2026
- **Kategorie:** Skill
- **Warum relevant:** Agent-Skill, der vibe-gecodete Projekte live deployt: Hosting, DB, Domain, Payments — alles auf eigenen Accounts (Vercel, Netlify, Cloudflare, Supabase, Neon). Zero-Dependency CLI, kein GoLive-Account noetig. Schliesst die Luecke zwischen "Agent baut App" und "App ist online".

#### 3. agentsys
- **URL:** https://github.com/agent-sh/agentsys
- **Sterne:** 990 | **Aktiv**
- **Kategorie:** Skill / Workflow / Quelle
- **Warum relevant:** 24 Plugins, 49 Agents, 44 Skills fuer Claude Code, Codex, Cursor, Kiro. Aehnlich wie wshobson/agents, aber mit Fokus auf Automatisierung und Plugin-Oekosystem. Potenzielle neue Quelle fuer fehlende Skills.

#### 4. jevgrep
- **URL:** https://github.com/dzhng/jevgrep
- **Sterne:** 942 | **Erstellt:** 26.09.2026
- **Kategorie:** Tool
- **Warum relevant:** CLI, die Code semantisch durchsucht (per Jev) statt per Regex. Findet relevante Dateien basierend auf Beschreibung ("was macht der Code") statt Muster. Nützlich als MCP-Tool oder CLI fuer Coding Agents.

#### 5. caliber-ai-org/ai-setup
- **URL:** https://github.com/caliber-ai-org/ai-setup
- **Sterne:** 1.288 | **Aktiv**
- **Kategorie:** Tool / Inspiration
- **Warum relevant:** Synchronisiert AI-Setups (Skills, MCPs, CLAUDE.md) ueber Claude Code, Cursor und Codex hinweg mit einem Befehl. Direkt vergleichbar mit dem eigenen my-claude-setup-Ansatz — interessant fuer Ideen zur Sync-Automatisierung und Cross-Tool-Kompatibilitaet.

#### 6. hermes-jev-skills
- **URL:** https://github.com/kerpopule/hermes-jev-skills
- **Sterne:** 879 | **Erstellt:** 18.09.2026
- **Kategorie:** Skill / Plugin
- **Warum relevant:** Jev-basiertes Model Routing, Memory-Management, Compaction und Skill-Selektion fuer Hermes-Agents (auch Claude Code und Codex kompatibel). Ergaenzt fast-jev-compaction um weitere Jev-Faehigkeiten.

#### 7. agent-console
- **URL:** https://github.com/LockedinLabs-AI/agent-console
- **Sterne:** 538 | **Erstellt:** 20.09.2026
- **Kategorie:** Tool / FinOps
- **Warum relevant:** Local-first Observability fuer Claude-Code- und Codex-Sessions: Tokens, Cache, Modelle, Kosten pro Session. Presenting Mode, Policy Hooks, Team Hub. Perfekt fuer Kostenmonitoring und Session-Analyse.

---

### Mittel relevant

#### 8. mcp-grafana
- **URL:** https://github.com/grafana/mcp-grafana
- **Sterne:** 3.503 | **Aktiv**
- **Kategorie:** MCP Server / Finanz-Tool
- **Warum relevant:** Offizieller MCP-Server fuer Grafana — ermoeglicht Claude den Zugriff auf Dashboards, Metriken und Alerts. Nuetzlich fuer Monitoring-Setups und KPI-Dashboards.

#### 9. agent-device (callstack)
- **URL:** https://github.com/callstack/agent-device
- **Sterne:** 4.793 | **Aktiv**
- **Kategorie:** MCP Server / Tool
- **Warum relevant:** Mobile-App-Automatisierung und -Verifikation fuer AI Coding Agents. CLI, MCP Server und Node.js API fuer iOS, Android, macOS. Relevant bei Mobile-Entwicklung.

#### 10. oh-my-design
- **URL:** https://github.com/kwakseongjae/oh-my-design
- **Sterne:** 524 | **Aktiv**
- **Kategorie:** Skill / Inspiration
- **Warum relevant:** 500+ qualitaetsbewertete DESIGN.md-Referenzen von echten Firmen fuer AI Coding Agents. Ein Befehl installiert Design-System-Referenzen. Ergaenzt den bestehenden Design-Skill-Stack (Dammyjay93, kylezantos).

#### 11. cortex-docs/cortex
- **URL:** https://github.com/cortex-docs/cortex
- **Sterne:** 3.229 | **Aktiv**
- **Kategorie:** MCP Server / Tool
- **Warum relevant:** Generiert interaktive API-Docs, typisierte SDKs und MCP-Server aus OpenAPI, AsyncAPI, GraphQL, gRPC. Automatische MCP-Server-Erstellung aus bestehenden API-Specs.

#### 12. MCPJam/inspector
- **URL:** https://github.com/MCPJam/inspector
- **Sterne:** 2.223 | **Aktiv**
- **Kategorie:** Tool
- **Warum relevant:** Test- und Debug-Plattform fuer MCP-Server mit Chat, Inspektion und Tracing. Nuetzlich zur Qualitaetssicherung der eigenen MCP-Konfiguration.

#### 13. AiSOC
- **URL:** https://github.com/beenuar/AiSOC
- **Sterne:** 2.372 | **Erstellt:** 02.05.2026
- **Kategorie:** MCP Server / Tool
- **Warum relevant:** Open-Source AI Security Operations Center mit MCP-Server. Alert-Fusion, LLM-Agent-Triage, MITRE ATT&CK. Ergaenzt den bestehenden security-awareness-Skill.

#### 14. magpie
- **URL:** https://github.com/yetone/magpie
- **Sterne:** 1.400 | **Erstellt:** 23.09.2026
- **Kategorie:** Tool
- **Warum relevant:** Menu-Bar-App fuer macOS: Codex auf DeepSeek, Claude Code auf Kimi etc. routbar. Model-Routing ueber alle Coding Agents hinweg.

#### 15. selfhost-ai
- **URL:** https://github.com/kossakovsky/selfhost-ai
- **Sterne:** 936 | **Aktiv**
- **Kategorie:** Workflow / Tool
- **Warum relevant:** Ein-Befehl-Installer fuer selbst-gehosteten AI-Stack: n8n, Ollama, Open WebUI, Dify, ComfyUI, Supabase, Qdrant + 30 Tools. Docker Compose, Auto-HTTPS. Interessant als Referenz fuer Self-Hosted-Setups.

#### 16. NornicDB
- **URL:** https://github.com/orneryd/NornicDB
- **Sterne:** 887 | **Aktiv**
- **Kategorie:** MCP Server / Tool
- **Warum relevant:** Graph+Vector-DB mit integriertem MCP-Server. Sub-Millisekunden HNSW-Suche, Neo4j-Bolt-kompatibel. Interessant als lokale RAG-Datenbank mit MCP-Anbindung.

#### 17. data-goblin/power-bi-agentic-development
- **URL:** https://github.com/data-goblin/power-bi-agentic-development
- **Sterne:** 944 | **Aktiv**
- **Kategorie:** Skill / Finanz-Tool
- **Warum relevant:** Power-BI- und Microsoft-Fabric-Skills fuer Claude Code. DAX, TMDL, AI-Dashboards. Relevant fuer Business-Intelligence- und Reporting-Workflows.

---

### Niedrig relevant / Inspiration

#### 18. nanobot (HKUDS)
- **URL:** https://github.com/HKUDS/nanobot
- **Sterne:** 48.633 | **Aktiv**
- **Kategorie:** Workflow / Inspiration
- **Warum relevant:** Ultra-leichtes, selbst-gehostetes AI-Agent-Framework mit WebUI, MCP, Multi-Agent-Workflows. Potenzielle n8n-Alternative fuer Agent-Orchestrierung.

#### 19. anidoodle
- **URL:** https://github.com/alexgreensh/anidoodle
- **Sterne:** 601 | **Erstellt:** 22.09.2026
- **Kategorie:** Skill
- **Warum relevant:** Art- und Animations-Skill fuer Claude Code: Illustrationen, Loops, interaktive Web-Art in diversen Stilen. Nische, aber kreativ.

#### 20. lemo-opuscar
- **URL:** https://github.com/lemomo-ai/lemo-opuscar
- **Sterne:** 432 | **Erstellt:** 26.09.2026
- **Kategorie:** Skill / Inspiration
- **Warum relevant:** 39 Film-Stile als wiederverwendbare Style-Prompts + Code-basierte Kurzfilme von Claude Opus 5.5. Kreativ-Coding-Referenz.

#### 21. geo-sleuth
- **URL:** https://github.com/Oldcircle/geo-sleuth
- **Sterne:** 491 | **Erstellt:** 18.09.2026
- **Kategorie:** Skill
- **Warum relevant:** Geolocation-Skill: findet per OSM, Elevation, Satellit und Street View, wo ein Foto aufgenommen wurde. Nische, aber einzigartige Faehigkeit.

---

### Bereits im Setup (uebersprungen)
- `stickerdaniel/linkedin-mcp-server` — bereits als MCP-Server konfiguriert
- `wshobson/maverick-mcp` — Autor (wshobson) bereits als Quelle gelistet
- `OthmanAdi/planning-with-files` — bereits via trailofbits/skills-curated installiert
- `FlorianBruniaux/claude-code-ultimate-guide` — Guide, kein Plugin/Skill
- `zebbern/claude-code-guide` — Guide, kein Plugin/Skill
- `davepoon/buildwithclaude` — Hub/Verzeichnis, kein direktes Plugin

---

### Top-3 Empfehlungen fuer sofortige Integration

| Prio | Repo | Aktion |
|------|------|--------|
| 1 | `tamaratran/fast-jev-compaction` | Als Plugin installieren — verbessert Context-Management |
| 2 | `mikehasa/golive-skill` | Als Deployment-Skill hinzufuegen |
| 3 | `LockedinLabs-AI/agent-console` | Fuer Kosten-Tracking evaluieren |

---

*Naechster Scan: 2026-09-29*
