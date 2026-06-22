# GitHub Scout Report — 22. Juni 2026

> Automatisch generiert am 22. Juni 2026 (erster Lauf, keine Vorgaenger-Berichte)

## Zusammenfassung

14 neue relevante Repositories gefunden, davon 5 mit hoher Relevanz fuer das Claude-Setup. Schwerpunkte: Code Knowledge Graphs als neuer Trend, massive Claude-Skills-Sammlungen, Finanz-MCP-Server und Meta Ads Integration.

---

## Hoch relevant — direkte Integration moeglich

### 1. upstash/context7 — MCP Server fuer Library-Dokumentation

| | |
|---|---|
| **URL** | https://github.com/upstash/context7 |
| **Sterne** | 57.844 |
| **Kategorie** | MCP Server |
| **Relevanz** | **Hoch** |

Liefert version-spezifische Library-Dokumentation (React, Next.js, Prisma etc.) direkt in die Claude-Code-Session. Mit 348.660 Installs das drittbeliebteste Plugin im Anthropic-Verzeichnis. Reduziert Halluzinationen bei API-Aenderungen drastisch.

**Empfehlung:** Als MCP Server installieren — ergaenzt das bestehende Setup perfekt fuer Frontend-/Fullstack-Arbeit.

---

### 2. safishamsi/graphify — Code-zu-Knowledge-Graph Skill

| | |
|---|---|
| **URL** | https://github.com/safishamsi/graphify |
| **Sterne** | 70.433 |
| **Kategorie** | Skill / Tool |
| **Relevanz** | **Hoch** |

Verwandelt Code, SQL-Schemas, Shell-Scripts, Docs und sogar Bilder/Videos in einen abfragbaren Knowledge Graph. Unterstuetzt tree-sitter, GraphRAG und Leiden-Algorithmus. Funktioniert mit Claude Code, Codex, Cursor und mehr.

**Empfehlung:** Als Skill installieren — ideal fuer grosse Codebasen und Cross-Repo-Analysen.

---

### 3. colbymchenry/codegraph — Pre-indexed Code Knowledge Graph MCP

| | |
|---|---|
| **URL** | https://github.com/colbymchenry/codegraph |
| **Sterne** | ~3.700+ (GitHub #2 Trending am Launch-Tag) |
| **Kategorie** | MCP Server / Tool |
| **Relevanz** | **Hoch** |

Lokaler MCP-Server mit tree-sitter + SQLite (FTS5). Benchmarks: 59% weniger Tokens, 49% schnellere Responses, 70% weniger Tool Calls. Auto-Konfiguration fuer Claude Code, Cursor, Codex CLI, Hermes Agent u.a.

**Empfehlung:** Als MCP Server installieren — direkter Performance-Gewinn bei jedem Claude-Code-Lauf.

---

### 4. thedotmack/claude-mem — Persistentes Gedaechtnis

| | |
|---|---|
| **URL** | https://github.com/thedotmack/claude-mem |
| **Sterne** | 83.649 |
| **Kategorie** | Plugin / Tool |
| **Relevanz** | **Hoch** |

Session-uebergreifendes Gedaechtnis: erfasst alles aus einer Session, komprimiert es mit AI, injiziert relevanten Kontext in zukuenftige Sessions. Nutzt ChromaDB, SQLite, Embeddings. Funktioniert mit Claude Code, OpenClaw, Codex, Gemini, Hermes.

**Empfehlung:** Ergaenzt das bestehende memory-palace Plugin (athola/claude-night-market) mit einem robusteren, Embedding-basierten Ansatz.

---

### 5. wshobson/maverick-mcp — Stock Analysis MCP Server

| | |
|---|---|
| **URL** | https://github.com/wshobson/maverick-mcp |
| **Sterne** | 603 |
| **Kategorie** | MCP Server / Finanz-Tool |
| **Relevanz** | **Hoch** |

Persoenlicher Aktienanalyse-MCP-Server mit Technical Analysis, Tiingo-API, pandas. Vom selben Autor wie wshobson/agents (bereits als Quelle im Setup).

**Empfehlung:** Als MCP Server installieren — deckt die Kategorie Finanzanalyse ab, die im Setup bisher fehlt.

---

## Mittel relevant — wertvolle Erweiterungen

### 6. Egonex-AI/Understand-Anything — Interaktiver Knowledge Graph

| | |
|---|---|
| **URL** | https://github.com/Egonex-AI/Understand-Anything |
| **Sterne** | 65.704 |
| **Kategorie** | Skill / Tool |
| **Relevanz** | Mittel |

Verwandelt Code in interaktive, durchsuchbare Knowledge Graphs mit Frage-Antwort-Funktion. Aehnlich wie graphify, aber mit Fokus auf Visualisierung und Exploration.

**Bewertung:** Alternative zu graphify — eines der beiden reicht, graphify ist umfassender.

---

### 7. alirezarezvani/claude-skills — 337 Skills Mega-Sammlung

| | |
|---|---|
| **URL** | https://github.com/alirezarezvani/claude-skills |
| **Sterne** | 18.756 |
| **Kategorie** | Skill-Sammlung |
| **Relevanz** | Mittel |

30+ Agents, 70+ Commands, 330+ Skills. Deckt Engineering, Marketing, Product, Compliance, Finance, C-Level Advisory ab. Funktioniert auch mit Codex, Gemini CLI, Cursor.

**Bewertung:** Groesste Einzel-Sammlung — als Inspirationsquelle fuer fehlende Skills durchstoebern. Ueberschneidung mit bestehendem Setup pruefen.

---

### 8. pipeboard-co/meta-ads-mcp — Meta Ads (Facebook/Instagram) MCP

| | |
|---|---|
| **URL** | https://github.com/pipeboard-co/meta-ads-mcp |
| **Sterne** | 1.006 |
| **Kategorie** | MCP Server |
| **Relevanz** | Mittel |

Kampagnen erstellen, Creatives hochladen, Budgets aendern, Performance analysieren — alles via MCP. Seit 29. April 2026 gibt es zusaetzlich den offiziellen Meta-Remote-MCP unter mcp.facebook.com/ads.

**Bewertung:** Relevant fuer SEO/Marketing-Setup — ergaenzt das bestehende claude-seo Plugin um Paid-Advertising.

---

### 9. OpenBB-finance/OpenBB — Financial Data Platform

| | |
|---|---|
| **URL** | https://github.com/OpenBB-finance/OpenBB |
| **Sterne** | 69.528 |
| **Kategorie** | Finanz-Tool / MCP Server |
| **Relevanz** | Mittel |

Open-Source Finanzplattform mit MCP-Server, REST-API, Python-Umgebung, Excel-Plugin. "Connect once, consume everywhere" — konsolidiert Finanzdaten aus dutzenden Quellen.

**Bewertung:** Fuer umfassende Finanzanalyse die Enterprise-Alternative zu maverick-mcp.

---

### 10. davepoon/buildwithclaude — Claude Skills Hub

| | |
|---|---|
| **URL** | https://github.com/davepoon/buildwithclaude |
| **Sterne** | 3.097 |
| **Kategorie** | Skill-Sammlung / Inspiration |
| **Relevanz** | Mittel |

Single Hub fuer Skills, Agents, Commands, Hooks, Plugins und Marketplace Collections. Aehnlich wie claudemarketplaces.com, aber als durchsuchbares Git-Repository.

**Bewertung:** Gute Discovery-Quelle fuer neue Skills — als Bookmark/Quelle merken.

---

### 11. enescingoz/awesome-n8n-templates — 280+ n8n Workflow Templates

| | |
|---|---|
| **URL** | https://github.com/enescingoz/awesome-n8n-templates |
| **Sterne** | 23.188 |
| **Kategorie** | Workflow / n8n |
| **Relevanz** | Mittel |

Groesste Open-Source n8n-Template-Sammlung: AI Agents, RAG Chatbots, E-Mail-Automatisierung, Social Media, DevOps, Dokumentenverarbeitung.

**Bewertung:** Relevant falls n8n im Einsatz — fertige Workflow-Vorlagen fuer AI-Agent-Pipelines.

---

## Niedrig relevant — zur Kenntnis

### 12. ghostwright/phantom — AI Co-Worker mit MCP

| | |
|---|---|
| **URL** | https://github.com/ghostwright/phantom |
| **Sterne** | 1.433 |
| **Kategorie** | Agent / Tool |
| **Relevanz** | Niedrig |

Autonomer AI-Agent mit eigenem Computer, persistentem Gedaechtnis, Slack-Integration. Gebaut auf dem Claude Agent SDK.

**Bewertung:** Interessantes Konzept, aber eher Inspiration als direkte Integration.

---

### 13. BoundaryML/baml — Prompt Engineering Framework

| | |
|---|---|
| **URL** | https://github.com/BoundaryML/baml |
| **Sterne** | 8.407 |
| **Kategorie** | Tool / Framework |
| **Relevanz** | Niedrig |

Framework fuer Structured Outputs, Guardrails, Prompt Templates. Multi-Language (Python/TS/Ruby/Java/C#/Rust/Go).

**Bewertung:** Relevant fuer eigene LLM-App-Entwicklung, nicht direkt fuer Claude-Code-Setup.

---

### 14. CloudAI-X/claude-workflow-v2 — Universal Workflow Plugin

| | |
|---|---|
| **URL** | https://github.com/CloudAI-X/claude-workflow-v2 |
| **Sterne** | 1.380 |
| **Kategorie** | Plugin / Workflow |
| **Relevanz** | Niedrig |

Universelles Workflow-Plugin mit Agents, Skills, Hooks, Commands. Funktioniert auch mit Codex und Cursor.

**Bewertung:** Ueberschneidung mit bestehendem Setup — nur interessant falls spezifische Workflows fehlen.

---

## Bereits im Setup — keine Aenderung noetig

| Repository | Status |
|------------|--------|
| stickerdaniel/linkedin-mcp-server (2.468 Sterne) | Bereits als MCP Server konfiguriert |
| athola/claude-night-market (314 Sterne) | Bereits als Plugin (sanctum, conjure, pensive, memory-palace, spec-kit, leyline) |
| wshobson/agents | Bereits als Quelle gelistet |
| AgriciDaniel/claude-seo | Bereits als Plugin |

---

## Trend-Beobachtungen

1. **Code Knowledge Graphs** sind der groesste neue Trend (graphify 70k, Understand-Anything 65k, codegraph ~4k Sterne). Die Tools reduzieren Token-Verbrauch und Tool Calls drastisch.

2. **Persistentes Gedaechtnis** (claude-mem 84k Sterne) zeigt, dass Session-uebergreifender Kontext ein Hauptproblem fuer Power-User bleibt.

3. **Meta Ads MCP** zeigt, dass Advertising-Plattformen jetzt nativ MCP unterstuetzen (offizieller Remote-MCP seit April 2026).

4. **n8n + MCP**: n8n hat seit April 2026 einen nativen Instance-Level MCP Server in Public Preview — Claude kann direkt n8n-Workflows bauen, testen und deployen.

5. **OpenClaw/Hermes Agent** (199k Sterne) hat das groesste Momentum im Agent-Bereich, ist aber kein direktes Claude-Code-Tool.

---

## Empfohlene naechste Schritte

| Prioritaet | Aktion |
|------------|--------|
| **HOCH** | `context7` als MCP Server installieren |
| **HOCH** | `codegraph` als MCP Server installieren |
| **HOCH** | `maverick-mcp` als MCP Server fuer Finanzanalyse installieren |
| **MITTEL** | `graphify` als Skill evaluieren |
| **MITTEL** | `claude-mem` als Alternative/Ergaenzung zu memory-palace testen |
| **MITTEL** | `meta-ads-mcp` fuer Paid-Advertising-Workflows evaluieren |
| **NIEDRIG** | `alirezarezvani/claude-skills` als Inspirationsquelle durchstoebern |

---

*Naechster Scout-Lauf: 23. Juni 2026*
