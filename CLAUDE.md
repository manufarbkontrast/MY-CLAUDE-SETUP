# MY-CLAUDE-SETUP

Personal Claude Code configuration backup for `~/.claude/`.

## Structure

| Directory | Count | Purpose |
|-----------|-------|---------|
| `skills/` | 461 | Skill definitions (markdown + templates) |
| `agents/` | 182 | Specialized agent definitions |
| `commands/` | 190 | Slash commands |
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

## MCP Servers

- lightpanda — Browser-Automatisierung
- dbhub (bytebase/dbhub) — Datenbank-MCP für Postgres, MySQL, SQLite etc.
- linkedin (stickerdaniel/linkedin-mcp-server) — LinkedIn Profile, Companies, Jobs

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
