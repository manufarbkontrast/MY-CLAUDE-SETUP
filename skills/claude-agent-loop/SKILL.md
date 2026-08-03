---
name: claude-agent-loop
description: Build custom AI agents with the Anthropic SDK. Agent loop, tool execution, message history management, MCP integration. Use when building autonomous agents, tool-using assistants, or multi-step LLM workflows with Claude.
version: 1.0.0
license: MIT
metadata:
  last_verified: 2025-02-14
  keywords:
    - agent
    - tool-use
    - mcp
    - anthropic-sdk
    - autonomous
    - agent-loop
  related_skills:
    - autonomous-coding-agent
    - browser-automation-claude
    - langchain-architecture
---

# Claude Agent Loop

Build custom AI agents from scratch using the Anthropic SDK. Based on the reference implementation from `anthropics/claude-quickstarts/agents/`.

## When to Use This Skill

- Building an autonomous AI agent with tool access
- Implementing a custom agent loop (not using LangChain/LangGraph)
- Integrating MCP servers into a custom agent
- Managing conversation history with token-aware truncation
- Need a lightweight agent without framework overhead

## Quick Start

```python
from anthropic import Anthropic

client = Anthropic()

def agent_loop(system: str, user_input: str, tools: list, tool_handlers: dict):
    messages = [{"role": "user", "content": user_input}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=system,
            messages=messages,
            tools=tools,
        )

        messages.append({"role": "assistant", "content": response.content})

        tool_calls = [b for b in response.content if b.type == "tool_use"]
        if not tool_calls:
            return response  # Done - no more tool calls

        tool_results = []
        for call in tool_calls:
            result = tool_handlers[call.name](**call.input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": call.id,
                "content": str(result),
            })
        messages.append({"role": "user", "content": tool_results})
```

## Core Patterns

### 1. Agent Loop
Infinite loop: API call -> check for tool_use blocks -> execute tools -> feed results back. Exits when Claude responds without tool calls.

### 2. Message History
Token-aware truncation removes oldest message pairs when context limit exceeded. Adds truncation notice to maintain coherence.

### 3. Tool System
Dataclass-based Tool base class. Parallel execution via `asyncio.gather`. Error handling per tool call.

### 4. MCP Integration
Dynamic tool loading from MCP servers via `AsyncExitStack`. Supports stdio and SSE connections.

### 5. Prompt Caching
Adds `cache_control: {"type": "ephemeral"}` to the last message for cost savings in agent loops.

## Resources

### References
- `references/core-loop.md` (~120 lines) - Agent loop pattern, response processing, exit conditions
- `references/message-history.md` (~130 lines) - Token tracking, smart truncation, prompt caching
- `references/tool-system.md` (~120 lines) - Tool base class, parallel execution, error handling
- `references/mcp-integration.md` (~130 lines) - MCP connections (stdio/SSE), dynamic tool loading, cleanup

### Templates
- `templates/minimal-agent.py` - Simplest possible agent (~40 lines)
- `templates/agent-with-tools.py` - Agent with custom tools
- `templates/agent-with-mcp.py` - Agent with MCP server integration
- `templates/custom-tool.py` - Template for creating your own tools
