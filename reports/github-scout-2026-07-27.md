# GitHub-Scout-Bericht — 2026-07-27

## Zusammenfassung

12 neue, relevante Repositories gefunden. Keine Überschneidung mit dem bestehenden Setup. Besonders hervorzuheben: **Hallmark** (Anti-Slop Design Skill, direkt kompatibel), **codebase-memory-mcp** (MCP-Server mit Code-Knowledge-Graph), **gstack** (Garry Tans Claude-Code-Setup mit 108K+ Stars) und **Vibe-Trading** (Finanzanalyse-Agent).

---

## Neue Repositories

### 1. garrytan/gstack

| Eigenschaft | Wert |
|-------------|------|
| **Kategorie** | Skill / Workflow |
| **Relevanz** | Hoch |
| **Stars** | ~108.000 |
| **URL** | https://github.com/garrytan/gstack |

**Warum relevant:** 23 spezialisierte Skills und 8 Power-Tools als Slash-Commands für Claude Code. Deckt den gesamten Software-Lifecycle ab (CEO, Designer, Eng Manager, Release Manager, Doc Engineer, QA). Garry Tan (Y Combinator CEO) nutzt es produktiv — 10.000 LOC und 100 PRs pro Woche. Viele Skills könnten das bestehende Setup ergänzen oder als Inspiration dienen.

---

### 2. Nutlope/hallmark

| Eigenschaft | Wert |
|-------------|------|
| **Kategorie** | Skill |
| **Relevanz** | Hoch |
| **Stars** | ~12.300 |
| **URL** | https://github.com/Nutlope/hallmark |

**Warum relevant:** Anti-AI-Slop Design Skill für Claude Code, Cursor und Codex. Führt 57 "Slop-Test"-Gates plus Pre-Emit-Selbstkritik durch. Passt perfekt zur bestehenden `uncodixify.md`-Rule im Setup. Vier Verben: `default` (bauen), `audit` (bewerten), `redesign` (umgestalten), `study` (Design-DNA extrahieren). MIT-Lizenz, direkt als SKILL.md einsetzbar.

---

### 3. DeusData/codebase-memory-mcp

| Eigenschaft | Wert |
|-------------|------|
| **Kategorie** | MCP Server |
| **Relevanz** | Hoch |
| **Stars** | ~35.400 |
| **URL** | https://github.com/DeusData/codebase-memory-mcp |

**Warum relevant:** High-Performance Code-Intelligence MCP-Server, der Codebases in einen persistenten Knowledge-Graph indiziert. Unterstützt 158 Sprachen via Tree-Sitter, Sub-ms-Queries, ~99% weniger Tokens für strukturelle Abfragen. Single static Binary, zero Dependencies. Ideale Ergänzung zum bestehenden MCP-Stack (lightpanda, dbhub, linkedin, gsc-mcp).

---

### 4. HKUDS/Vibe-Trading

| Eigenschaft | Wert |
|-------------|------|
| **Kategorie** | Finanz-Tool |
| **Relevanz** | Hoch |
| **Stars** | ~22.300 |
| **URL** | https://github.com/HKUDS/Vibe-Trading |

**Warum relevant:** KI-gestützter Multi-Agent Finance Workspace der Uni Hongkong. Wandelt natürliche Sprache in ausführbare Trading-Strategien, Backtests und Portfolio-Analysen um. 452 vorgebaute Alpha-Faktoren, Export nach TradingView (Pine Script v6), MetaTrader 5 (MQL5). Monte Carlo, Bootstrap CI, Walk-Forward Validation. Trending +721 Stars/Tag.

---

### 5. iOfficeAI/OfficeCLI

| Eigenschaft | Wert |
|-------------|------|
| **Kategorie** | Tool |
| **Relevanz** | Hoch |
| **Stars** | ~18.000 |
| **URL** | https://github.com/iOfficeAI/OfficeCLI |

**Warum relevant:** Erste Office-Suite speziell für KI-Agenten. Liest, bearbeitet und automatisiert Word, Excel und PowerPoint als Single Binary ohne Office-Installation. 350+ Excel-Funktionen, HTML/PNG-Rendering von Dokumenten. Apache-2.0-Lizenz. Ergänzt die bestehenden `docx`-, `xlsx`-, `pptx`-Skills mit einem CLI-Backend.

---

### 6. diegosouzapw/OmniRoute

| Eigenschaft | Wert |
|-------------|------|
| **Kategorie** | Tool / Infrastruktur |
| **Relevanz** | Mittel |
| **Stars** | ~23.000 |
| **URL** | https://github.com/diegosouzapw/OmniRoute |

**Warum relevant:** Freies AI-Gateway mit einem Endpoint für 290+ Provider (90+ kostenlos) und 500+ Modelle. Smart Routing, Load Balancing, automatisches Fallback, Token-Kompression (15–95% Einsparung). Kompatibel mit Claude Code, Codex, Cursor. Nützlich, wenn man Multi-Provider-Setups betreiben will.

---

### 7. stablyai/orca

| Eigenschaft | Wert |
|-------------|------|
| **Kategorie** | Workflow / Tool |
| **Relevanz** | Mittel |
| **Stars** | ~15.700 |
| **URL** | https://github.com/stablyai/orca |

**Warum relevant:** Agent Development Environment (ADE) für parallele Coding-Agent-Fleets. Läuft auf Desktop, Mobile und VPS. Unterstützt Claude Code, Codex, Cursor CLI, Grok, Copilot CLI und 25+ weitere Agents in isolierten Git Worktrees. MIT-Lizenz. Relevant für parallele Agenten-Orchestrierung.

---

### 8. alirezarezvani/claude-skills

| Eigenschaft | Wert |
|-------------|------|
| **Kategorie** | Skill |
| **Relevanz** | Mittel |
| **Stars** | ~23.000 |
| **URL** | https://github.com/alirezarezvani/claude-skills |

**Warum relevant:** 345 Skills, 30+ Agents, 70+ Custom Commands für Claude Code, Codex, Gemini CLI, Cursor. Deckt Engineering, Marketing, Product, Compliance, C-Level Advisory, Research, Business Ops und Finance ab. Große Überschneidung mit dem bestehenden Setup möglich — aber auch potentiell neue Business-/Finance-Skills als Ergänzung.

---

### 9. google-labs-code/stitch-skills

| Eigenschaft | Wert |
|-------------|------|
| **Kategorie** | Skill / MCP Server |
| **Relevanz** | Mittel |
| **Stars** | ~6.500 |
| **URL** | https://github.com/google-labs-code/stitch-skills |

**Warum relevant:** Googles Agent-Skills-Bibliothek für den Stitch MCP-Server. 14+ Skills für Design-Generierung, React/React Native Code-Output, Design-System-Management. Folgt dem offenen Agent Skills Standard (agentskills.io), kompatibel mit Claude Code. Brücke zwischen Design und Development.

---

### 10. JustVugg/colibri

| Eigenschaft | Wert |
|-------------|------|
| **Kategorie** | Tool / LLM Inference |
| **Relevanz** | Mittel |
| **Stars** | ~14.700 |
| **URL** | https://github.com/JustVugg/colibri |

**Warum relevant:** Pure-C Inference Engine für Frontier-MoE-Modelle auf Consumer-Hardware via Disk-Streamed Expert Loading. Ermöglicht lokale Nutzung großer Modelle ohne Cloud-Abhängigkeit. Ergänzung zum Ollama-Stack für spezialisierte Anwendungsfälle.

---

### 11. xai-org/grok-build

| Eigenschaft | Wert |
|-------------|------|
| **Kategorie** | Inspiration |
| **Relevanz** | Niedrig |
| **Stars** | ~9.300 |
| **URL** | https://github.com/xai-org/grok-build |

**Warum relevant:** xAIs Production-Grade Coding Agent CLI mit vollständiger Transparenz in Context Handling, Tool Execution, Plugins, Skills und MCP-Integration. Interessant als Referenz für Agent-Architektur, aber kein direkter Nutzen für das Claude-Setup.

---

### 12. usestrix/strix

| Eigenschaft | Wert |
|-------------|------|
| **Kategorie** | Tool / Security |
| **Relevanz** | Niedrig |
| **Stars** | ~42.000 |
| **URL** | https://github.com/usestrix/strix |

**Warum relevant:** Open-Source KI-Penetration-Testing-Tool mit dynamischen Tests und Proof-of-Concept-Exploits. Könnte die bestehende `security-review`-Skill und `security.md`-Rule ergänzen, ist aber ein eigenständiges Tool und kein Claude-Skill.

---

## Relevanz-Matrix

| Repo | Stars | Kategorie | Relevanz | Aktion empfohlen |
|------|-------|-----------|----------|------------------|
| garrytan/gstack | 108K | Skill/Workflow | Hoch | Skills evaluieren und selektiv übernehmen |
| Nutlope/hallmark | 12.3K | Skill | Hoch | Als SKILL.md installieren (ergänzt uncodixify) |
| DeusData/codebase-memory-mcp | 35.4K | MCP Server | Hoch | Als MCP-Server hinzufügen |
| HKUDS/Vibe-Trading | 22.3K | Finanz-Tool | Hoch | Für Finanzanalyse-Workflows evaluieren |
| iOfficeAI/OfficeCLI | 18K | Tool | Hoch | Als CLI-Backend für docx/xlsx/pptx nutzen |
| diegosouzapw/OmniRoute | 23K | Infrastruktur | Mittel | Bei Multi-Provider-Bedarf evaluieren |
| stablyai/orca | 15.7K | Workflow | Mittel | Für parallele Agent-Fleets evaluieren |
| alirezarezvani/claude-skills | 23K | Skill | Mittel | Business-/Finance-Skills prüfen |
| google-labs-code/stitch-skills | 6.5K | Skill/MCP | Mittel | Design-to-Code-Workflow prüfen |
| JustVugg/colibri | 14.7K | LLM Inference | Mittel | Bei lokalem MoE-Bedarf evaluieren |
| xai-org/grok-build | 9.3K | Inspiration | Niedrig | Architektur-Referenz |
| usestrix/strix | 42K | Security | Niedrig | Security-Testing ergänzend |

---

## Top-3 Empfehlungen

1. **Hallmark installieren** — Direkt kompatibel als SKILL.md, ergänzt die `uncodixify.md`-Rule mit konkreten Quality-Gates gegen generisches UI.
2. **codebase-memory-mcp als MCP-Server hinzufügen** — Persistenter Code-Knowledge-Graph mit 158 Sprachen, drastisch weniger Token-Verbrauch für Code-Exploration.
3. **gstack-Skills evaluieren** — 23 spezialisierte Skills für den gesamten Dev-Lifecycle, vieles davon direkt übernehmbar.
