## GitHub-Scout-Bericht – 2026-10-12

### Zusammenfassung

14 neue relevante Repositories gefunden, die das bestehende Setup erweitern oder ergänzen könnten. Besonders hervorzuheben: **codebase-memory-mcp** (Code-Intelligence via Knowledge Graph), **n8n-mcp** (n8n-Workflow-Builder direkt aus Claude Code), **NVIDIA/SkillSpector** (Security-Scanner für Skills vor Installation) und **context-mode** (Context-Window-Optimierung mit 98% Token-Reduktion).

---

### Neue Repositories

#### 1. DeusData/codebase-memory-mcp
- **Kategorie:** MCP Server
- **Sterne:** 46.396
- **Relevanz:** Hoch
- **URL:** https://github.com/DeusData/codebase-memory-mcp
- **Beschreibung:** High-Performance Code-Intelligence MCP-Server. Indiziert Codebases als persistenten Knowledge Graph — 158 Sprachen, Sub-Millisekunden-Queries, 99% weniger Tokens. Single Binary, Zero Dependencies.
- **Nutzen:** Könnte die Codebase-Navigation und -Analyse in Claude Code massiv beschleunigen, besonders bei großen Projekten. Ergänzt den bestehenden MCP-Stack (dbhub, linkedin) um Code-Intelligence.

#### 2. czlonkowski/n8n-mcp
- **Kategorie:** MCP Server / Workflow
- **Sterne:** 23.055
- **Relevanz:** Hoch
- **URL:** https://github.com/czlonkowski/n8n-mcp
- **Beschreibung:** MCP-Server, der Claude Code, Windsurf und Cursor direkt n8n-Workflows bauen lässt. Natürliche Sprache → n8n-Workflow.
- **Nutzen:** Perfekte Ergänzung zum bestehenden n8n-Skills-Setup. Statt nur Skills für Workflow-Wissen hätte Claude direkten Zugriff auf n8n-Workflow-Erstellung.

#### 3. NVIDIA/SkillSpector
- **Kategorie:** Tool / Security
- **Sterne:** 19.995
- **Relevanz:** Hoch
- **URL:** https://github.com/NVIDIA/SkillSpector
- **Beschreibung:** Security-Scanner für AI Agent Skills. Erkennt Schwachstellen, bösartige Muster, Prompt Injection, Datenexfiltration und Supply-Chain-Risiken in Skills vor der Installation.
- **Nutzen:** Bei 466 installierten Skills essenziell für Security-Hygiene. Ergänzt die bestehende `security.md`-Rule und den `scv-scan`-Skill von Trail of Bits.

#### 4. mksglu/context-mode
- **Kategorie:** Skill / Tool
- **Sterne:** 26.743
- **Relevanz:** Hoch
- **URL:** https://github.com/mksglu/context-mode
- **Beschreibung:** Context-Window-Optimierung für AI Coding Agents. Sandboxt Tool-Output (98% Reduktion), persistiert Session-Memory und erzwingt Routing über 17 Plattformen via MCP + Hooks.
- **Nutzen:** Direkte Verbesserung der Context-Effizienz in Claude Code. Ergänzt die bestehende `performance.md`-Rule mit konkreter Tool-Unterstützung.

#### 5. czlonkowski/n8n-skills
- **Kategorie:** Skill
- **Sterne:** 6.407
- **Relevanz:** Hoch
- **URL:** https://github.com/czlonkowski/n8n-skills
- **Beschreibung:** n8n-Skillset für Claude Code zum Erstellen fehlerfreier n8n-Workflows. Vom gleichen Autor wie n8n-mcp.
- **Nutzen:** Spezifische n8n-Expertise als Claude-Code-Skill — komplementär zum MCP-Server.

#### 6. tt-a1i/archify
- **Kategorie:** Skill / Visualisierung
- **Sterne:** 82.267
- **Relevanz:** Mittel
- **URL:** https://github.com/tt-a1i/archify
- **Beschreibung:** Verwandelt Ideen, Pläne oder Codebases in interaktive Architektur-Diagramme. Agent-Skill für Claude Code und Codex.
- **Nutzen:** Architektur-Visualisierung als Ergänzung zu den bestehenden Design- und Frontend-Skills.

#### 7. JuliusBrussee/caveman
- **Kategorie:** Skill / Performance
- **Sterne:** 111.116
- **Relevanz:** Mittel
- **URL:** https://github.com/JuliusBrussee/caveman
- **Beschreibung:** Viraler Skill + Proxy, der 65% Token-Verbrauch spart durch komprimierte Kommunikation. "Why use many token when few token do trick."
- **Nutzen:** Token-Kostenreduktion, ergänzt die `performance.md`-Rule. Allerdings kontrovers — komprimierte Ausgabe kann Lesbarkeit beeinträchtigen.

#### 8. irinabuht12-oss/google-ads-meta-ads-mcp
- **Kategorie:** MCP Server / Marketing
- **Sterne:** 4.499
- **Relevanz:** Mittel
- **URL:** https://github.com/irinabuht12-oss/google-ads-meta-ads-mcp
- **Beschreibung:** Google Ads + Meta Ads + GA4 + Search Console in einem gehosteten Remote-MCP. OAuth-Login, keine API-Keys, 7-Tage-Trial.
- **Nutzen:** Ergänzt das SEO-Setup um Ads-Management und GA4-Analytics direkt aus Claude Code. Passt zum bestehenden GSC-MCP.

#### 9. sansan0/TrendRadar
- **Kategorie:** Tool / Monitoring
- **Sterne:** 62.823
- **Relevanz:** Mittel
- **URL:** https://github.com/sansan0/TrendRadar
- **Beschreibung:** AI-getriebener Trend- und Meinungsmonitor mit Multi-Plattform-Aggregation, RSS und Smart Alerts. MCP-Architektur, Docker, Telegram/Slack/Mail-Push.
- **Nutzen:** Trend-Monitoring für Marketing und Content-Strategie. Ergänzt die SEO-Skills um Echtzeit-Trend-Daten.

#### 10. marc-shade/world-intel-mcp
- **Kategorie:** MCP Server
- **Sterne:** 914
- **Relevanz:** Mittel
- **URL:** https://github.com/marc-shade/world-intel-mcp
- **Beschreibung:** 139-Tool MCP-Server für Echtzeit-Weltnachrichten: Märkte, SEC-Filings, Cyber, Klima, News aus 30+ Domänen. Kostenlos, keine API-Keys, MIT-Lizenz.
- **Nutzen:** Globale Markt- und Nachrichten-Intelligence direkt in Claude Code. Relevant für Finanzanalyse und Reporting.

#### 11. coldteadotai/abide
- **Kategorie:** Skill
- **Sterne:** 578
- **Relevanz:** Mittel
- **URL:** https://github.com/coldteadotai/abide
- **Beschreibung:** Erzwingt die Einhaltung aller Projektregeln durch den Coding Agent. Erstellt am 18.09.2026.
- **Nutzen:** Ergänzt das bestehende Rules-System (9 Rules). Automatische Compliance-Prüfung statt manueller Review.

#### 12. sno-ai/sno-station-skills
- **Kategorie:** Skill / Multi-Agent
- **Sterne:** 257
- **Relevanz:** Mittel
- **URL:** https://github.com/sno-ai/sno-station-skills
- **Beschreibung:** 31 getestete Skills für Cross-Vendor Peer Review, automatischen Agent-Handoff bei Quota-Limit, Morning Brief und selbstlernende Nachtschleifen. Erstellt am 01.10.2026.
- **Nutzen:** Ergänzt den `agents.md`-Rule um Multi-Agent-Koordination und automatisches Rate-Limit-Management.

#### 13. EtienneLescot/n8n-as-code
- **Kategorie:** Tool / n8n
- **Sterne:** 1.605
- **Relevanz:** Mittel
- **URL:** https://github.com/EtienneLescot/n8n-as-code
- **Beschreibung:** 537 n8n-Nodes mit vollständigen Schemas, 7.700+ Templates, Git-Sync und TypeScript-Workflows. Gibt dem AI Agent "n8n-Superpowers".
- **Nutzen:** Code-First-Ansatz für n8n-Workflows. Ergänzt n8n-mcp und n8n-skills um Versionskontrolle und TypeScript-Support.

#### 14. teng-lin/notebooklm-py
- **Kategorie:** Tool / Skill
- **Sterne:** 19.704
- **Relevanz:** Niedrig
- **URL:** https://github.com/teng-lin/notebooklm-py
- **Beschreibung:** Inoffizielle Python-API und Agent-Skill für Google NotebookLM. Voller programmatischer Zugriff auf NotebookLM-Features — auch solche, die die Web-UI nicht bietet.
- **Nutzen:** Nische, aber nützlich wenn NotebookLM als Research-Tool genutzt wird.

---

### Bereits bekannte Repos (keine Änderung)

| Repository | Status |
|-----------|--------|
| `stickerdaniel/linkedin-mcp-server` (3.827★) | Bereits als MCP-Server konfiguriert |
| `bytebase/dbhub` (3.631★) | Bereits als MCP-Server konfiguriert |
| `coreyhaines31/marketingskills` (54.273★) | Bereits in SEO-Setup integriert |
| `VoltAgent/awesome-agent-skills` (35.542★) | Bekannte Ressource, keine neue Integration nötig |
| `OthmanAdi/planning-with-files` (27.400★) | Bereits via trailofbits installiert |

---

### Prioritäten-Empfehlung

| Priorität | Repository | Aktion |
|-----------|-----------|--------|
| 1 | `DeusData/codebase-memory-mcp` | Als MCP-Server hinzufügen |
| 2 | `czlonkowski/n8n-mcp` | Als MCP-Server hinzufügen |
| 3 | `NVIDIA/SkillSpector` | Als Security-Tool integrieren |
| 4 | `mksglu/context-mode` | Als Skill/Plugin installieren |
| 5 | `czlonkowski/n8n-skills` | Skills installieren |
| 6 | `irinabuht12-oss/google-ads-meta-ads-mcp` | Als MCP-Server für Ads-Management |
