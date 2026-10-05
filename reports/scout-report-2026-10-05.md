## GitHub-Scout-Report – 2026-10-05

### Zusammenfassung

11 relevante Repositories gefunden, davon 10 neu und 1 signifikantes Update eines bekannten Repos. Besonders interessant: neue Finanz-MCP-Server, ein GEO/SEO-Scoring-Tool mit MCP, und ein Token-Optimierungs-Proxy.

---

### Neue Repositories

#### 1. wshobson/maverick-mcp
- **URL:** https://github.com/wshobson/maverick-mcp
- **Sterne:** 701
- **Kategorie:** MCP Server / Finanz-Tool
- **Relevanz:** Hoch
- **Beschreibung:** MCP-Server für Yahoo Finance: Aktiendaten, technische Analyse, Portfolio-Tracking und Python-Backtesting. Läuft lokal ohne API-Key für Basis-Tools.
- **Warum relevant:** wshobson ist bereits als Quelle im Setup gelistet (agents). Dieser MCP-Server ergänzt perfekt die Finanz-Kategorie und lässt sich direkt in das bestehende Setup integrieren.

#### 2. jianruntech/geo-score
- **URL:** https://github.com/jianruntech/geo-score
- **Sterne:** 619
- **Kategorie:** MCP Server / SEO-Tool
- **Relevanz:** Hoch
- **Beschreibung:** GEO-Score (Generative Engine Optimization): Misst, ob AI-Suchmaschinen (ChatGPT, Perplexity, Gemini, Claude) eine Website zitieren können. 0–100 Readiness-Score, Citation-Tracking, MCP-Server. Erstellt im September 2026.
- **Warum relevant:** Direktes Pendant zum bestehenden `ai-seo`-Skill (coreyhaines31). Ergänzt den SEO-Stack um konkrete GEO-Metriken und AI-Sichtbarkeits-Tracking.

#### 3. noskillish/bankmcp
- **URL:** https://github.com/noskillish/bankmcp
- **Sterne:** 274
- **Kategorie:** MCP Server / Finanz-Tool
- **Relevanz:** Hoch
- **Beschreibung:** Self-hosted, read-only MCP-Server für eigene Bankkonten via Open Banking (Enable Banking / PSD2). Getestet mit Claude und Ollama. Erstellt im September 2026.
- **Warum relevant:** Ermöglicht direkte Finanzanalyse über Claude – Kontostände, Transaktionen, Umsatz-Reporting. Zusammen mit maverick-mcp ein starkes Finanz-Duo.

#### 4. JuliusBrussee/caveman
- **URL:** https://github.com/JuliusBrussee/caveman
- **Sterne:** 109.885
- **Kategorie:** Skill / Tool
- **Relevanz:** Hoch
- **Beschreibung:** Viraler Skill + Proxy für Coding Agents, der 65% der Tokens einspart durch komprimierte Kommunikation. Go-basiert.
- **Warum relevant:** Massive Token-Einsparung für Claude Code Sessions. Bei 466 Skills und komplexen Workflows direkt kostenrelevant.

#### 5. mksglu/context-mode
- **URL:** https://github.com/mksglu/context-mode
- **Sterne:** 25.436
- **Kategorie:** Skill / Tool
- **Relevanz:** Hoch
- **Beschreibung:** Context-Window-Optimierung für AI-Coding-Agents. Sandboxt Tool-Output (98% Reduktion), persistiert Session-Memory, erzwingt Routing über 17 Plattformen via MCP + Hooks.
- **Warum relevant:** Ergänzt das bestehende Hook-System und optimiert die Context-Nutzung, was bei großen Skill-Sammlungen wie diesem Setup besonders wertvoll ist.

#### 6. artokun/comfyui-mcp
- **URL:** https://github.com/artokun/comfyui-mcp
- **Sterne:** 789
- **Kategorie:** MCP Server / Tool
- **Relevanz:** Mittel
- **Beschreibung:** Local-first MCP-Server für ComfyUI – 178 Tools, 36 AI Skills, 55 Installer-Packs. Steuert ComfyUI-Workflows in natürlicher Sprache über Claude, ChatGPT oder Ollama.
- **Warum relevant:** Das Setup listet ComfyUI bereits als Kategorie. Dieser MCP-Server macht ComfyUI direkt aus Claude Code steuerbar – Bildgenerierung, Video, Audio.

#### 7. tt-a1i/archify
- **URL:** https://github.com/tt-a1i/archify
- **Sterne:** 77.697
- **Kategorie:** Skill
- **Relevanz:** Mittel
- **Beschreibung:** Agent-Skill der Ideen, Pläne oder Codebases in interaktive Architektur-Diagramme umwandelt (Mermaid, Flowcharts, Sequenz-Diagramme). Claude Code + Codex Plugin.
- **Warum relevant:** Ergänzt die bestehenden Design- und Engineering-Skills um automatische Architektur-Visualisierung.

#### 8. farion1231/cc-switch
- **URL:** https://github.com/farion1231/cc-switch
- **Sterne:** 140.127
- **Kategorie:** Tool
- **Relevanz:** Mittel
- **Beschreibung:** Cross-Platform Desktop All-in-One Assistant für Claude Code, Codex, OpenCode, Grok Build und mehr. Rust/Tauri-basiert. Skills-Management, Provider-Switching.
- **Warum relevant:** Könnte als einheitliche Oberfläche für verschiedene Coding Agents nützlich sein, besonders für den Wechsel zwischen Providern.

#### 9. ruvnet/ruflo
- **URL:** https://github.com/ruvnet/ruflo
- **Sterne:** 73.888
- **Kategorie:** Workflow / Tool
- **Relevanz:** Mittel
- **Beschreibung:** Multi-Agent-Swarm-Framework: autonome Workflows, adaptive Memory, Self-Learning, Federation, Vector RAG. Nativ integriert mit Claude Code, Codex und Hermes.
- **Warum relevant:** Könnte das bestehende Agent-Orchestrierungs-System (182 Agents) um autonome Multi-Agent-Koordination erweitern.

#### 10. viettranx/3dviz-pro-max
- **URL:** https://github.com/viettranx/3dviz-pro-max
- **Sterne:** 658
- **Kategorie:** Skill
- **Relevanz:** Niedrig
- **Beschreibung:** Agent-Skill für 3D-Visualisierung: Three.js/Blender-Szenen aus Ideen generieren. 223 Rezepte, 440 Knowledge Records. Erstellt im September 2026.
- **Warum relevant:** Nischen-Skill für 3D-Visualisierung – interessant für Kreativ-Projekte, aber nicht direkt relevant für das Kern-Setup.

---

### Bekanntes Repo mit signifikantem Update

#### affaan-m/ECC (ehemals everything-claude-code)
- **URL:** https://github.com/affaan-m/ECC
- **Sterne:** 273.162 (massiver Anstieg)
- **Kategorie:** Skill / Tool
- **Relevanz:** Hoch
- **Was sich verändert hat:** Das Repo wurde von `everything-claude-code` zu `ECC` umbenannt und ist jetzt ein vollständiges "Agent Harness Performance Optimization System" mit Skills, Instincts, Memory, Security und Research-First Development. Unterstützt neben Claude Code auch Codex, Opencode und Cursor. Die Sternezahl ist von einem bereits hohen Niveau auf 273k explodiert.
- **Aktion:** Der Quellenverweis in CLAUDE.md zeigt noch auf `affaan-m/everything-claude-code` – sollte aktualisiert werden.

---

### Bereits im Setup (keine Aktion nötig)

Die folgenden Repos aus den Suchergebnissen sind bereits Teil des Setups:
- `stickerdaniel/linkedin-mcp-server` — MCP Server (konfiguriert)
- `bytebase/dbhub` — MCP Server (konfiguriert)
- `coreyhaines31/marketingskills` — Skills (installiert)
- `OthmanAdi/planning-with-files` — Plugin (trailofbits/skills-curated)

---

### Empfohlene Aktionen (Priorität)

1. **maverick-mcp installieren** — `claude mcp add maverick-mcp -- uvx maverick-mcp` (Finanz-MCP, kein API-Key nötig)
2. **geo-score installieren** — GEO-Scoring als MCP-Server für den SEO-Stack
3. **bankmcp evaluieren** — Benötigt Enable Banking API-Zugang, prüfen ob relevant
4. **caveman testen** — 65% Token-Einsparung testen, Kosten-Impact evaluieren
5. **context-mode evaluieren** — Kompatibilität mit bestehendem Hook-System prüfen
6. **CLAUDE.md aktualisieren** — `affaan-m/everything-claude-code` → `affaan-m/ECC`
