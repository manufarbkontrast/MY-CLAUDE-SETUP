# MY-CLAUDE-SETUP

Personal Claude Code configuration backup for `~/.claude/`.

## Structure

| Directory | Count | Purpose |
|-----------|-------|---------|
| `skills/` | 474 | Skill definitions (markdown + templates) |
| `agents/` | 182 | Specialized agent definitions |
| `commands/` | 192 | Slash commands |
| `rules/` | 9 | Global behavior rules |
| `settings.json` | — | Hooks, plugins, marketplace config |
| `scripts/` | — | Prompt enhancer CLI |

## Sync Workflow

`~/.claude/` is the source of truth. To update this repo:

```bash
rsync -av --delete ~/.claude/skills/ ./skills/
rsync -av --delete ~/.claude/agents/ ./agents/
rsync -av --delete ~/.claude/commands/ ./commands/
rsync -av --delete ~/.claude/rules/ ./rules/
cp ~/.claude/settings.json ./settings.json
git add -A && git commit -m "feat: sync local setup"
git pull --rebase origin main && git push origin main
```

## Installation (neuer Rechner)

### Schnell-Installation

```bash
git clone https://github.com/manufarbkontrast/MY-CLAUDE-SETUP.git ~/my-claude-setup
cd ~/my-claude-setup
./install.sh
```

Das Script:
1. Prueft Node.js >= 20
2. Installiert Dependencies
3. Kompiliert TypeScript
4. Baut die Registry
5. Registriert `prompt-optimizer` und `po` als globale CLI-Befehle

### Claude Setup kopieren

```bash
cp -r skills/* ~/.claude/skills/
cp -r agents/* ~/.claude/agents/
cp -r commands/* ~/.claude/commands/
cp -r rules/* ~/.claude/rules/
cp settings.json ~/.claude/settings.json
```

## Hooks (in settings.json)

- **PreToolUse**: Block dev server outside tmux, warn on git push, block unnecessary .md/.txt files
- **PostToolUse**: Auto-format mit prettier, TypeScript type-check, console.log warnings, PR URL extraction

## Enabled Plugins

- engineering-skills, fullstack-engineer (claude-code-skills)
- firecrawl, figma, superpowers (claude-plugins-official)
- claude-hud (jarrodwatts/claude-hud)
- claude-code-toolkit (rohitg00/awesome-claude-code-toolkit)
- agile-workflow, codebase-audit-suite, project-bootstrap, optimization-suite, setup-environment (levnikolaevich/claude-code-skills)
- sanctum, conjure, pensive, memory-palace, spec-kit, leyline (athola/claude-night-market)
- security-awareness, planning-with-files, python-code-simplifier, skill-extractor, scv-scan (trailofbits/skills-curated)
- claude-seo (AgriciDaniel/claude-seo) — 25 SEO-Sub-Skills + 18 Agents: technisches Audit mit Headless-Rendering, Schema-Validierung, E-Commerce-SEO, hreflang, GEO/AEO

## MCP Servers

- lightpanda — Browser-Automatisierung
- dbhub (bytebase/dbhub) — Datenbank-MCP für Postgres, MySQL, SQLite etc.
- linkedin (stickerdaniel/linkedin-mcp-server) — LinkedIn Profile, Companies, Jobs
- gsc-mcp (mikusnuz/gsc-mcp) — Google Search Console: Clicks/Impressions/Positionen, URL-Inspektion, Sitemaps, Indexing API. Setup siehe SEO-Setup.

## SEO-Setup

Neue SEO-Skills (Juni 2026, kuratiert aus claudemarketplaces.com / mcpfind.org / discoveraiskills.com):

| Skill | Quelle | Zweck |
|-------|--------|-------|
| `programmatic-seo` | coreyhaines31/marketingskills | Template-Pages mit Daten skalieren (generateStaticParams, Shopify-Kategorien) |
| `ai-seo` | coreyhaines31/marketingskills | LLM-Zitierbarkeit, AI-Search-Optimierung (ChatGPT/Perplexity/AI Overviews) |
| `competitors` | coreyhaines31/marketingskills | Vergleichs-/Alternative-Seiten für E-Commerce |
| `ecommerce-seo-audit` | affilino/ecommerce-seo-audit-skill | Shopify-Audits: Produkt-/Collection-Pages, Facetten-Duplikate, Thin Categories |

Dazu: claude-seo-Plugin (siehe Enabled Plugins) und der `firecrawl-seo-audit`-Workflow im bereits installierten Firecrawl-Plugin.

GSC-MCP einrichten (kostenlos, braucht Google-Cloud-Service-Account mit Zugriff auf die GSC-Property):

```bash
claude mcp add gsc-mcp --env GSC_SERVICE_ACCOUNT_KEY_PATH=/pfad/zu/service-account-key.json -- npx -y @mikusnuz/gsc-mcp
```

## Rules

| Rule | Purpose |
|------|---------|
| `coding-style.md` | Immutability, small files, error handling |
| `git-workflow.md` | Conventional commits, PR workflow |
| `testing.md` | TDD mandatory, 80%+ coverage |
| `performance.md` | Model selection, context management |
| `patterns.md` | Repository pattern, API response format |
| `hooks.md` | Hook types, TodoWrite best practices |
| `agents.md` | Agent orchestration, parallel execution |
| `security.md` | Security checks before commits |
| `uncodixify.md` | Anti-AI-aesthetic UI guidelines |

## Key Commands

```
/plan               — Implementation planning
/tdd                — Test-driven development
/verify             — Build + types + lint + tests + secrets audit
/code-review        — Security + quality review
/orchestrate        — Chain agents: plan → tdd → review → security
/full-stack-feature — End-to-end backend + frontend + DB
/smart-debug        — AI-powered debugging
/build-fix          — Fix build errors incrementally
/frontend-dev       — Closed-loop visual frontend testing
```

## Prompt Optimizer

CLI tool that analyzes a raw prompt and enriches it by identifying relevant skills, agents, and commands.

```bash
prompt-optimizer "Build a Shopify store with Next.js"
po "Build a Shopify store with Next.js"           # Kurzform
po --stats                                         # Registry-Statistiken
po --build                                         # Registry neu bauen
po --help                                          # Hilfe
```

### Output in Zwischenablage (macOS)

```bash
po "Dein Prompt" 2>/dev/null | pbcopy
```

### Claude Code Command

```
/optimize Build a real-time chat app with Next.js and Supabase
```

### Rebuild nach neuen Skills/Agents

```bash
cd ~/my-claude-setup && git pull && po --build
```

### Architecture

```
src/
  cli.ts             - CLI entry point (prompt-optimizer / po)
  types.ts           - TypeScript interfaces for registry entries
  build-registry.ts  - Scans repo and generates registry.json
  matcher.ts         - Keyword + fuzzy matching logic
  optimize-prompt.ts - Prompt analysis and output assembly
```

## Sources

Curated from:
- [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) — Core workflow, TDD, hooks
- [anthropics/skills](https://github.com/anthropics/skills) — Official Anthropic skills
- [wshobson/agents](https://github.com/wshobson/agents) — 112 agents, 146 skills, 91 commands
- [mrgoonie/claudekit-skills](https://github.com/mrgoonie/claudekit-skills) — Shopify, payments, debugging
- [secondsky/claude-skills](https://github.com/secondsky/claude-skills) — 176 skills (Cloudflare, Nuxt, TanStack, Bun)
- [anthropics/claude-code](https://github.com/anthropics/claude-code) — Official frontend-design plugin
- [kylezantos/design-motion-principles](https://github.com/kylezantos/design-motion-principles) — Motion design
- [Dammyjay93/claude-design-skill](https://github.com/Dammyjay93/claude-design-skill) — Interface design
- [hemangjoshi37a/claude-code-frontend-dev](https://github.com/hemangjoshi37a/claude-code-frontend-dev) — Visual testing
- [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) — programmatic-seo, ai-seo, competitors
- [affilino/ecommerce-seo-audit-skill](https://github.com/affilino/ecommerce-seo-audit-skill) — Shopify-SEO-Audits
- [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) — SEO-Plugin (via Marketplace)
