---
name: autonomous-coding-agent
description: Build long-running autonomous coding agents with multi-session persistence, security sandboxing, and progress tracking. Use when building autonomous agents that work across multiple sessions, need security constraints, or require progress persistence.
version: 1.0.0
license: MIT
metadata:
  last_verified: 2025-02-14
  keywords:
    - autonomous
    - multi-session
    - security
    - persistence
    - claude-sdk
    - sandbox
  related_skills:
    - claude-agent-loop
    - browser-automation-claude
---

# Autonomous Coding Agent

Build long-running autonomous agents that persist state across sessions using the Claude Agent SDK. Based on Anthropic's `claude-quickstarts/autonomous-coding` reference implementation.

## When to Use This Skill

- Building an agent that works across multiple sessions (context window exhaustion)
- Need security sandboxing for agents that execute code
- Want progress tracking for long-running autonomous tasks
- Building with the Claude Agent SDK (claude_code_sdk)

## Quick Start: Two-Agent Pattern

```python
import asyncio
from pathlib import Path
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions

async def run_autonomous(project_dir: Path, model: str):
    tests_file = project_dir / "feature_list.json"
    is_first_run = not tests_file.exists()
    iteration = 0

    while True:
        iteration += 1
        client = create_client(project_dir, model)  # Fresh context each time

        if is_first_run:
            prompt = "Read the spec and create feature_list.json with all features."
            is_first_run = False
        else:
            prompt = "Read feature_list.json. Find next pending feature. Implement it."

        async with client:
            status, _ = await run_session(client, prompt, project_dir)

        if status == "continue":
            await asyncio.sleep(3)  # Auto-continue delay
```

**Agent 1 (Initializer)**: Reads spec, creates `feature_list.json` with all features.
**Agent 2+ (Coding)**: Reads `feature_list.json`, implements next pending feature, commits via git.

## Core Patterns

### 1. Multi-Session Persistence
Fresh client per iteration avoids context bloat. State persists via filesystem (`feature_list.json` + git commits). See `references/multi-session-pattern.md`.

### 2. Security Sandbox
Defense-in-depth: OS sandbox -> permission restrictions -> bash command hooks. Allowlist-based command validation. See `references/security-sandbox.md`.

### 3. Progress Tracking
JSON feature list with status tracking (pending/passing). Git as persistence layer. See `references/progress-tracking.md`.

### 4. SDK Configuration
ClaudeCodeOptions with hooks, permissions, sandbox. Per-project settings file. See `references/sdk-configuration.md`.

## Resources

### References
- `references/multi-session-pattern.md` (~100 lines) - Fresh client pattern, auto-continue, pause/resume, state persistence
- `references/security-sandbox.md` (~130 lines) - Defense-in-depth, bash security hook, allowlist, command parsing
- `references/progress-tracking.md` (~80 lines) - Feature list JSON, status tracking, git persistence, resumability
- `references/sdk-configuration.md` (~100 lines) - ClaudeCodeOptions, permissions, hooks, sandbox config

### Templates
- `templates/multi-session-loop.py` - Outer loop with auto-continue and fresh client
- `templates/security-hook.py` - Bash security hook with allowlist
- `templates/feature-tracker.py` - Feature list JSON management
- `templates/sdk-client-setup.py` - Claude SDK client with security layers
