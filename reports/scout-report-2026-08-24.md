# GitHub-Scout-Report — 2026-08-24

**Erster Lauf dieser Routine.** Im Repository existierten bisher keine Scout-Berichte
(nur `sync-report-*` und `anthropic-update-*`), daher gibt es keine Ausschlussliste —
alle unten genannten Repos werden als neu geführt. Ab dem nächsten Lauf dient dieser
Bericht als Gedächtnis: bereits genannte Repos erscheinen nur wieder bei >10 % Sterne-Zuwachs,
Major-Release oder neuer Kategorie-Relevanz.

**Methodik:** Entdeckung per Websuche und Aggregatoren, Verifikation jedes einzelnen Repos
per Abruf der GitHub-Repo-Seite und des `commits.atom`-Feeds. Sternezahlen sind die auf der
Repo-Seite angezeigten (gerundeten) Werte, Stand 2026-08-24. Zahlen aus Blogs und Aggregatoren
wurden verworfen — mehrere Quellen nannten offensichtlich falsche Werte.

**Filter:** >500 Sterne, Commit innerhalb der letzten 7 Tage.

---

## Relevanz Hoch

### MCP Server

| Repo | Sterne | Letzter Commit |
|------|--------|----------------|
| [upstash/context7](https://github.com/upstash/context7) | 61,1k | 2026-08-21 |

Zieht versionsgenaue, aktuelle Library-Dokumentation direkt in den Prompt. Für den
Next.js-/Shopify-/Supabase-Stack der wirksamste Einzel-Fix gegen veraltete API-Vorschläge —
ergänzt die bestehenden Coding-Rules, ohne mit ihnen zu kollidieren.

| Repo | Sterne | Letzter Commit |
|------|--------|----------------|
| [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) | 49,6k | 2026-08-21 |

Offizieller MCP-Server des Chrome-DevTools-Teams: steuert und inspiziert eine echte
Chrome-Session (Performance-Traces, Netzwerk, Konsole). Schließt die Lücke zwischen dem
leichtgewichtigen `lightpanda` und den SEO-/`frontend-dev`-Workflows, die echtes Rendering brauchen.

| Repo | Sterne | Letzter Commit |
|------|--------|----------------|
| [oraios/serena](https://github.com/oraios/serena) | 28,4k | 2026-08-20 |

LSP-basiertes semantisches Code-Toolkit: Symbol-Level-Navigation und -Refactoring statt
Textsuche. Spart in größeren Repos massiv Kontext — passt direkt zu `rules/performance.md`
sowie zu `/build-fix` und `/smart-debug`.

### Skills & Skill-Tooling

| Repo | Sterne | Letzter Commit |
|------|--------|----------------|
| [virgiliojr94/book-to-skill](https://github.com/virgiliojr94/book-to-skill) | 24,9k | 2026-08-23 |

Wandelt PDFs, EPUBs und Doku-Ordner in strukturierte Skills um (Mental Models,
Kapitel-Referenzen, Glossar, Decision Tables) statt Rohtext in den Kontext zu kippen;
laut README 24×–51× weniger Tokens. Bei 466 vorhandenen Skills ist das ein Skill-*Generator*
statt nur weiterer Content — die interessanteste Neuentdeckung dieser Runde.

| Repo | Sterne | Letzter Commit |
|------|--------|----------------|
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | 30,4k | 2026-08-21 |

Acht Erstanbieter-Skills von Vercel: React-Best-Practices, Web-Design-Standards,
Performance-Optimierung, View Transitions, React Native. Sinnvolle Ergänzung und Gegenprobe
zu `rules/uncodixify.md` und den vorhandenen Design-Skills.

| Repo | Sterne | Letzter Commit |
|------|--------|----------------|
| [google/skills](https://github.com/google/skills) | 18,6k | 2026-08-22 |

Offizielle Skills für Google-Produkte im gleichen Format wie `anthropics/skills`, u.a.
Analytics Admin/Data API, Google Ads API, BigQuery, Cloud Run, Firebase. Die Analytics-/Ads-Teile
docken direkt an das bestehende SEO-Setup mit `gsc-mcp` an, BigQuery ergänzt `dbhub`.

### Prompt Engineering

| Repo | Sterne | Letzter Commit |
|------|--------|----------------|
| [gepa-ai/gepa](https://github.com/gepa-ai/gepa) | 6,2k | 2026-08-19 |

Optimiert beliebige Textparameter (Prompts, Code, Agent-Architekturen, Configs) per
LLM-Reflection und Pareto-Evolution. Die logische Ausbaustufe für den eigenen
`prompt-optimizer`/`po`-CLI: messbare Optimierung statt Keyword-Matching.

| Repo | Sterne | Letzter Commit |
|------|--------|----------------|
| [ai-boost/awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering) | 3,7k | 2026-08-23 |

200+ kuratierte Referenzen zu Agent-Loops, Context-Compaction, Tool-Schemas, Permissions,
Memory, Orchestrierung und Verification-Loops. Praktisch ein Review-Katalog für die
9 `rules/`-Dateien und die Agent-Orchestrierung.

### Finanz- & BI-Tools

| Repo | Sterne | Letzter Commit |
|------|--------|----------------|
| [Canner/WrenAI](https://github.com/Canner/WrenAI) | 17,4k | 2026-08-21 |

Governed Text-to-SQL über einen Semantic Layer für 20+ Datenquellen — genau die Schicht,
die verhindert, dass ein Agent falsche Umsatzzahlen halluziniert. Bringt einen eigenen
MCP-Server mit, ist also direkt ankoppelbar.

| Repo | Sterne | Letzter Commit |
|------|--------|----------------|
| [lightdash/lightdash](https://github.com/lightdash/lightdash) | 6,1k | 2026-08-23 (Release 1.238.0) |

Positioniert sich explizit als "Agentic BI": Metriken, Dashboards und Data Apps werden per
Lightdash-MCP-Server und Agent Skills aus Terminal/Editor gebaut. KPI-Definitionen einmal
versioniert, den Report baut Claude Code.

| Repo | Sterne | Letzter Commit |
|------|--------|----------------|
| [evidence-dev/evidence](https://github.com/evidence-dev/evidence) | 6,9k | 2026-08-23 |

"BI as code" — Reports als SQL + Markdown, versionierbar in Git. Das Repo enthält selbst
`CLAUDE.md`/`AGENTS.md` und bewirbt Entwicklung mit Claude Code. Ideal für wiederkehrende
Monats-/Quartalsreports.

| Repo | Sterne | Letzter Commit |
|------|--------|----------------|
| [JerBouma/FinanceToolkit](https://github.com/JerBouma/FinanceToolkit) | 5,3k | 2026-08-18 (v2.2.0) |

500+ transparent dokumentierte Finanzkennzahlen als Python-Lib **plus offiziellem MCP-Server**.
Belastbare Kennzahlenlogik statt selbstgebauter Formeln.

### Workflows / n8n

| Repo | Sterne | Letzter Commit |
|------|--------|----------------|
| [EtienneLescot/n8n-as-code](https://github.com/EtienneLescot/n8n-as-code) | 1,5k | 2026-08-20 |

Macht ein Repo zum n8n-Workspace: TypeScript-Workflows, GitOps-Pull/Push gegen Live-Instanzen,
537 Node-Schemas, 7.700+ Templates, portable AI-Skills und ein eigenes Claude-Code-Plugin.
Ergänzt das bekannte `czlonkowski/n8n-mcp` um die Code- und Git-Seite statt nur Lesezugriff.

### Agent-Frameworks (als Referenz, nicht als Zubau)

| Repo | Sterne | Letzter Commit |
|------|--------|----------------|
| [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | 80,8k | 2026-08-24 |

Long-Horizon-Agent-Harness mit Sandboxes, Memory, Skills, Subagents und Message-Gateway —
also genau die Orchestrierungsschicht, die `/orchestrate` derzeit per Markdown nachbaut.
Wertvoll als Muster-Referenz für Subagent- und Memory-Patterns.

---

## Relevanz Mittel

| Repo | Sterne | Letzter Commit | Kategorie | Kurz |
|------|--------|----------------|-----------|------|
| [metabase/metabase](https://github.com/metabase/metabase) | 48,9k | 2026-08-24 | Finanz-Tool | Pragmatischster Weg zu KPI-Dashboards ohne SQL-Zwang; inzwischen mit eigenen AI-Abfragen ("Metabot"), über REST-API bzw. `dbhub` befüllbar. |
| [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | 52,9k | 2026-08-24 (CI-täglich) | Inspiration | Zentraler, täglich aktualisierter Index für Skills, Agents, Hooks, Plugins. Als wiederkehrende Quelle für `po --build`-Runden, nicht als Installation. |
| [PrimeIntellect-ai/prime-agent](https://github.com/PrimeIntellect-ai/prime-agent) | 18,1k | 2026-08-21 | Inspiration | Self-improving Agent mit Continual Harness und daemon-gestützter Session-Kontinuität; Vergleichsharness für lange autonome Läufe. |
| [BerriAI/litellm](https://github.com/BerriAI/litellm) | 57,1k | 2026-08-22 | Tool | AI-Gateway vor 100+ Providern mit Cost-Tracking und Guardrails — zentrale Kostentransparenz über alle Agents; die Nutzungsdaten sind selbst ein KPI-Datensatz. |
| [enescingoz/awesome-n8n-templates](https://github.com/enescingoz/awesome-n8n-templates) | 24,9k | 2026-08-23 | Workflow | 280+ importfertige Workflow-JSONs in 18 Kategorien; als lokaler Template-Korpus, damit ein Agent adaptiert statt von null zu bauen. |
| [cloudflare/computer](https://github.com/cloudflare/computer) | 8,6k | 2026-08-21 | Inspiration | Virtuelles Dateisystem in einem Durable Object als Agent-Execution-Surface. Eher Infrastruktur als Setup-Zubau. |
| [anthropics/claude-plugins-community](https://github.com/anthropics/claude-plugins-community) | 1,1k | aktiv | Inspiration | Read-only-Mirror des offiziellen Plugin-Marketplace; nützlich als Discovery-Quelle. |

---

## Relevanz Niedrig

| Repo | Sterne | Grund |
|------|--------|-------|
| [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates) | 30,4k | Starke inhaltliche Überschneidung mit dem Bestand; interessant nur als Vergleichsquelle für Hook-/Analytics-Setups (überlappt mit `claude-hud`). |
| [jqueryscript/awesome-claude-code](https://github.com/jqueryscript/awesome-claude-code) | 504 | Erfüllt die Kriterien knapp, ist aber eine reine Linkliste. |

---

## Geprüft und ausgeschlossen

**Aktivitätskriterium verfehlt (kein Commit in 7 Tagen):**

| Repo | Sterne | Letzter Commit |
|------|--------|----------------|
| `OpenBB-finance/OpenBB` | 72,2k | 2026-07-20 — stark und mit MCP-Server, aber Fokus auf Wertpapierdaten statt eigener Unternehmens-KPIs |
| `Zie619/n8n-workflows` | 56,2k | 2026-06-24 |
| `stanfordnlp/dspy` | 37,6k | 2026-08-21 — aktiv, aber etabliert; GEPA ist der neuere Hebel |
| `n8n-io/self-hosted-ai-starter-kit` | 15,2k | 2026-07-23 |
| `travisvn/awesome-claude-skills` | 14,8k | 2026-04-28 |
| `midday-ai/midday` | 14,9k | 2026-06-13 — inhaltlich bester Fit für Solo-Buchhaltung, aber letzter Commit "Wind down billing"; Projekt wirkt eingestellt |
| `restyler/awesome-n8n` | 3,0k | 2026-01-20 |
| `nerding-io/n8n-nodes-mcp` | 3,0k | 2026-01-02 |

**Sonstige Ausschlüsse:**

- `microsoft/playwright-mcp` (36,4k, 2026-08-19) — Browser-Automatisierung ist mit `lightpanda`
  bereits abgedeckt; `chrome-devtools-mcp` bringt den größeren Zuwachs.
- `actualbudget/actual` (28,3k) — Privatfinanzen statt Unternehmens-Reporting.
- `Shopify/dev-mcp` — inhaltlich der naheliegendste Kandidat für den Shopify-Teil,
  liegt aber mit ~400–490 Sternen unter der Schwelle. Für kommende Läufe im Blick behalten.
- `jeremylongshore/claude-code-plugins-plus-skills` (2,7k) — trotz großer Marketing-Zahlen
  wenig Traktion und stark redundant zum Bestand.
- Buchhaltungs-spezifische MCP-Server (Xero-MCP ~350, `norman-finance/norman-mcp-server`) —
  deutlich unter 500 Sternen.

**Bereits im Setup vorhanden, daher nicht als neu geführt:** `obra/superpowers`,
`anthropics/skills`, `anthropics/claude-plugins-official`, `coreyhaines31/marketingskills`,
`trailofbits/skills`, `czlonkowski/n8n-mcp` (22,8k), `ollama/ollama`, `n8n-io/n8n`.

---

## Beobachtungen

**n8n ist auffällig dünn.** Die großen Sammlungen (Zie619, restyler,
self-hosted-ai-starter-kit) sind seit Wochen bis Monaten unangetastet. Nur `n8n-as-code`
und `awesome-n8n-templates` erfüllen beide Kriterien.

**Vorschlag für einen Finanz-Reporting-Stack:** n8n (Datenzufluss) → Postgres über das
vorhandene `dbhub`-MCP → Lightdash oder Evidence (versionierte KPI-Definitionen und Reports)
→ FinanceToolkit-MCP (Kennzahlenlogik). WrenAI zusätzlich, sobald Ad-hoc-Fragen in
natürlicher Sprache ohne Halluzinationsrisiko beantwortet werden sollen.

**Zur Belastbarkeit der Zahlen:** Alle Sternezahlen stammen aus der gerenderten GitHub-Seite
des jeweiligen Repos, nicht aus der API und nicht aus Blogs. Sie sind auf 100er gerundet
und können sich täglich ändern — als Vergleichsbasis für den nächsten Lauf sind sie
ausreichend genau, als exakte Werte nicht zu lesen.
