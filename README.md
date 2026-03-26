# My Claude Code Setup

Personal Claude Code configuration with 461 skills, 182 agents, 190 commands, 9 rules, and 9 hooks.

## Installation

```bash
# Clone
git clone https://github.com/manufarbkontrast/my-claude-setup.git

# Copy to ~/.claude/
cp -r skills/* ~/.claude/skills/
cp -r agents/* ~/.claude/agents/
cp -r commands/* ~/.claude/commands/
cp -r rules/* ~/.claude/rules/
cp settings.json ~/.claude/settings.json
```

## Contents

| Component | Count |
|---|---|
| Skills | 461 |
| Agents | 182 |
| Commands | 190 |
| Rules | 9 |
| Hooks | 9 (in settings.json) |

## Sources

Curated from:

- [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) - Core workflow, TDD, hooks
- [anthropics/skills](https://github.com/anthropics/skills) - Official Anthropic skills (pdf, docx, pptx, xlsx, canvas-design, etc.)
- [wshobson/agents](https://github.com/wshobson/agents) - 112 agents, 146 skills, 91 commands across 73 plugins
- [mrgoonie/claudekit-skills](https://github.com/mrgoonie/claudekit-skills) - Shopify, payment-integration, debugging, problem-solving
- [secondsky/claude-skills](https://github.com/secondsky/claude-skills) - 176 skills (Cloudflare, Nuxt, TanStack, Bun, AI SDKs)
- [anthropics/claude-code](https://github.com/anthropics/claude-code) - Official frontend-design plugin
- [kylezantos/design-motion-principles](https://github.com/kylezantos/design-motion-principles) - Motion design audits
- [Dammyjay93/claude-design-skill](https://github.com/Dammyjay93/claude-design-skill) - Interface design engineering
- [hemangjoshi37a/claude-code-frontend-dev](https://github.com/hemangjoshi37a/claude-code-frontend-dev) - Visual testing, closed-loop frontend

## Key Commands

```
/plan               - Implementation planning
/tdd                - Test-driven development
/verify             - Build + types + lint + tests + secrets audit
/code-review        - Security + quality review
/orchestrate        - Chain agents: plan -> tdd -> review -> security
/full-stack-feature - End-to-end backend + frontend + DB
/smart-debug        - AI-powered debugging
/build-fix          - Fix build errors incrementally
/security-sast      - Multi-language security scan
/frontend-dev       - Closed-loop visual frontend testing
```

## Prompt Enhancer CLI

Generate an improved, structured prompt with recommended local skills and agents:

```bash
python3 scripts/prompt_enhancer.py 'baue mir eine cloudflare worker api mit auth und tests'
```

JSON output (debug scores included):

```bash
python3 scripts/prompt_enhancer.py 'review meinen react code auf performance' --json
```

Interactive mode (guided questions):

```bash
python3 scripts/prompt_enhancer.py --interactive
```

Options:

- `--top-skills N` (default: `6`)
- `--top-agents N` (default: `3`)
- `--skills-dir PATH` (default: `skills`)
- `--agents-dir PATH` (default: `agents`)
- `--interactive` ask guided questions and build the prompt from your answers

Note: use single quotes around prompts that contain `$skill` tags, e.g. `'$prompt-optimizer ...'`.
