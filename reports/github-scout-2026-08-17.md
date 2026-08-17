## GitHub-Scout-Bericht – 2026-08-17

Erster Scout-Durchlauf. Kein vorheriger Bericht zum Duplikat-Abgleich vorhanden.

### Suchkategorien

Claude/Anthropic MCP Servers | AI Agents & Automation | Prompt Engineering | n8n Integrations | Claude Skills/Commands/Agents | LLM Tooling | Finanzanalyse & Reporting

---

### Neue relevante Repositories

#### 1. NanoNets/Graft

| Feld | Wert |
|------|------|
| URL | https://github.com/NanoNets/Graft |
| Sterne | 3.121 |
| Erstellt | Juli 2026 |
| Sprache | TypeScript |
| Kategorie | MCP Server / Tool |
| Relevanz | **Hoch** |

MCP Server, der einen Code-Graph (Tree-Sitter) über die Codebasis baut und so kontextbezogenes Verständnis für Claude Code, Cursor und Codex liefert. Reduziert Tokenverbrauch und verbessert Antwortqualität durch gezielte Kontext-Injektion. Sehr aktiv, 271 Forks.

**Nutzen:** Direkter Mehrwert für jede Claude-Code-Session — besseres Codebase-Verständnis ohne manuelles Kontext-Management.

---

#### 2. mksglu/context-mode

| Feld | Wert |
|------|------|
| URL | https://github.com/mksglu/context-mode |
| Sterne | 19.909 |
| Erstellt | Februar 2026 |
| Sprache | TypeScript |
| Kategorie | Skill / MCP Server |
| Relevanz | **Hoch** |

Context-Window-Optimierung für 17+ AI-Coding-Agents. Sandboxt Tool-Output (98% Reduktion), persistiert Session-Memory und erzwingt Routing via MCP + Hooks. Unterstützt Claude Code, Codex, Cursor, OpenClaw u.v.m.

**Nutzen:** Massive Kontext-Einsparung bei langen Sessions. Komplementiert das bestehende Setup, da Hooks und MCP-Server bereits genutzt werden.

---

#### 3. Storybloq/storybloq

| Feld | Wert |
|------|------|
| URL | https://github.com/Storybloq/storybloq |
| Sterne | 694 |
| Erstellt | April 2026 |
| Sprache | TypeScript |
| Kategorie | MCP Server / Skill |
| Relevanz | **Hoch** |

Cross-Session-Kontext für Claude Code. CLI + MCP Server + `/story` Skill, der Tickets, Issues, Handovers und Roadmap in einem `.story/`-Verzeichnis trackt. Session-Kontinuität ohne manuelle Übergaben.

**Nutzen:** Löst das Problem der Session-Fragmentierung. Besonders wertvoll für mehrtägige Feature-Arbeit.

---

#### 4. vshulcz/deja-vu

| Feld | Wert |
|------|------|
| URL | https://github.com/vshulcz/deja-vu |
| Sterne | 640 |
| Erstellt | Juli 2026 |
| Sprache | Go |
| Kategorie | MCP Server / Tool |
| Relevanz | **Hoch** |

Memory für Coding-Agents: Indexiert Sessions von 17 verschiedenen Agents (inkl. Claude Code, Codex), auch Monate rückwirkend. Kein LLM, keine Embeddings — ein lokales Go-Binary. Recall über MCP oder CLI.

**Nutzen:** Retroaktive Session-Suche über alle bisherigen Claude-Code-Sessions. Null Overhead, da kein LLM benötigt.

---

#### 5. MaxFreedomPollard/Compartment

| Feld | Wert |
|------|------|
| URL | https://github.com/MaxFreedomPollard/Compartment |
| Sterne | 604 |
| Erstellt | Juli 2026 |
| Sprache | Python |
| Kategorie | MCP Server / Tool |
| Relevanz | **Mittel** |

Verschlüsselte, vollständig offline Agent-Memory. One-Click-Install, GUI mit Memory-Map. Unterstützt Claude Code, Hermes, OpenClaw. Semantic Search + RAG lokal.

**Nutzen:** Privacy-fokussierte Alternative zu Cloud-Memory-Lösungen. Interessant für vertrauliche Projekte.

---

#### 6. stevesolun/ctx

| Feld | Wert |
|------|------|
| URL | https://github.com/stevesolun/ctx |
| Sterne | 574 |
| Erstellt | April 2026 |
| Sprache | Python |
| Kategorie | Tool / Inspiration |
| Relevanz | **Hoch** |

Repo-aware Empfehlungs-Engine für Skills, Agents, MCP Servers und Harnesses. 79.958-Knoten-Graph mit 68.494 Skills, 467 Agents, 10.790 MCPs. Kann eigenen Bestand nutzen oder den mitgelieferten Graph.

**Nutzen:** Konzeptionell verwandt mit dem eigenen Prompt-Optimizer, aber auf einem anderen Level (Knowledge-Graph statt Keyword-Matching). Potenzielle Inspiration oder Integration.

---

#### 7. wshobson/maverick-mcp

| Feld | Wert |
|------|------|
| URL | https://github.com/wshobson/maverick-mcp |
| Sterne | 645 |
| Erstellt | August 2025 |
| Sprache | Python |
| Kategorie | MCP Server / Finanz-Tool |
| Relevanz | **Hoch** |

Persönlicher Stock-Analyse MCP Server vom gleichen Autor wie `wshobson/agents` (bereits als Quelle im Setup). Technische Analyse, Tiingo-API, Pandas-basiert. FastMCP-Server.

**Nutzen:** Direkte Finanzanalyse aus Claude Code heraus. Passt perfekt in die Kategorie Finanzanalyse & Reporting. Gleicher Autor wie ein bereits bekanntes Repo — hohe Qualitätswahrscheinlichkeit.

---

#### 8. iannuttall/seo

| Feld | Wert |
|------|------|
| URL | https://github.com/iannuttall/seo |
| Sterne | 244 |
| Erstellt | Juli 2026 |
| Sprache | TypeScript |
| Kategorie | MCP Server / Skill |
| Relevanz | **Hoch** |

70+ SEO-Audit-Tools als lokaler CLI + MCP Server. Nutzt eigene Crawl-Daten, Search Console und GA4. Local-first, kein externer Service nötig.

**Nutzen:** Ergänzt das bestehende SEO-Setup (claude-seo, GSC-MCP, firecrawl) um eine umfassende Audit-Suite. Besonders relevant da GA4-Integration enthalten.

---

#### 9. artokun/comfyui-mcp

| Feld | Wert |
|------|------|
| URL | https://github.com/artokun/comfyui-mcp |
| Sterne | 595 |
| Erstellt | Februar 2026 |
| Sprache | TypeScript |
| Kategorie | MCP Server / LLM Tooling |
| Relevanz | **Mittel** |

Local-first Control Plane für ComfyUI. MCP Server + Sidebar-Agent mit 178 Tools und 36 AI Skills. Unterstützt Bild-, Video- und Audio-Generierung direkt aus Claude Code.

**Nutzen:** Brücke zwischen Claude Code und ComfyUI-Workflows. Relevant falls Bildgenerierung/Design-Workflows gewünscht.

---

#### 10. OpenLabs-so/openanalytics

| Feld | Wert |
|------|------|
| URL | https://github.com/OpenLabs-so/openanalytics |
| Sterne | 218 |
| Erstellt | August 2026 (brandneu) |
| Sprache | TypeScript |
| Kategorie | MCP Server / Finanz-Tool |
| Relevanz | **Mittel** |

Privacy-first, cookielose Web-Analytics mit Revenue-Attribution und MCP Server. Self-hosted, Clickhouse-Backend. Plausible-Alternative.

**Nutzen:** Web-Analytics direkt aus Claude Code abfragbar via MCP. Revenue-Attribution ist relevant für E-Commerce/SEO-Reporting.

---

#### 11. OpenOSINT/OpenOSINT

| Feld | Wert |
|------|------|
| URL | https://github.com/OpenOSINT/OpenOSINT |
| Sterne | 1.413 |
| Erstellt | Mai 2026 |
| Sprache | Python |
| Kategorie | MCP Server / Tool |
| Relevanz | **Mittel** |

AI-gestützter OSINT-Agent mit interaktivem REPL, MCP Server und CLI. 19 Tools (Sherlock, Maigret, Holehe). Für autorisierte Sicherheitsforschung.

**Nutzen:** Nützlich für Wettbewerbsanalyse, Domain-Recherche und Security-Audits. Ergänzt den bestehenden Security-Fokus (pen-testing, scv-scan).

---

#### 12. mrpulor-gh/nuphus-mcp

| Feld | Wert |
|------|------|
| URL | https://github.com/mrpulor-gh/nuphus-mcp |
| Sterne | 221 |
| Erstellt | August 2026 (brandneu) |
| Sprache | Rust |
| Kategorie | MCP Server |
| Relevanz | **Niedrig** |

Desktop-Automatisierung MCP Server — Computer Use für jeden AI Agent. Steuert Bildschirm, Fenster, Maus/Tastatur und Chrome via MCP. Rust-basiert.

**Nutzen:** Interessant für E2E-Testing und Desktop-Automatisierung, aber Nischen-Anwendungsfall.

---

### Bekannte Repos mit signifikantem Wachstum

#### affaan-m/ECC (ehem. everything-claude-code)

| Feld | Wert |
|------|------|
| URL | https://github.com/affaan-m/ECC |
| Sterne | 240.574 (!) |
| Kategorie | Skill / Workflow |

Im Setup als `affaan-m/everything-claude-code` referenziert. Massiv gewachsen und zu "ECC" (agent harness performance optimization system) umbenannt. Unterstützt jetzt Claude Code, Codex, Opencode, Cursor und weitere.

**Änderung:** Rebranding, Multi-Agent-Unterstützung, 240k+ Sterne.

---

### Zusammenfassung

| Priorität | Repo | Aktion |
|-----------|------|--------|
| 1 | **Graft** | MCP Server installieren — sofortiger Kontextgewinn |
| 2 | **context-mode** | Hooks/MCP evaluieren — 98% Kontext-Reduktion |
| 3 | **maverick-mcp** | MCP Server installieren — Finanzanalyse-Feature |
| 4 | **deja-vu** | MCP Server installieren — retroaktive Session-Suche |
| 5 | **iannuttall/seo** | MCP Server evaluieren — ergänzt SEO-Stack |
| 6 | **storybloq** | Skill + MCP testen — Session-Kontinuität |
| 7 | **ctx** | Evaluieren — Graph-basierte Skill-Empfehlungen |
| 8 | **openanalytics** | Beobachten — noch sehr neu, aber MCP + Revenue |
| 9 | **comfyui-mcp** | Optional — falls Bildgenerierung relevant |
| 10 | **Compartment** | Optional — verschlüsselte Memory-Alternative |

---

*Nächster Scout-Lauf: 2026-08-18*
