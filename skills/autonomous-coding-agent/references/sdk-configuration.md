# SDK Configuration

## ClaudeCodeOptions

The Claude Agent SDK client is configured with `ClaudeCodeOptions`:

```python
from claude_code_sdk import ClaudeCodeOptions, ClaudeSDKClient
from claude_code_sdk.types import HookMatcher

client = ClaudeSDKClient(
    options=ClaudeCodeOptions(
        model="claude-sonnet-4-20250514",
        system_prompt="You are an expert full-stack developer.",
        allowed_tools=["Read", "Write", "Edit", "Glob", "Grep", "Bash"],
        hooks={
            "PreToolUse": [
                HookMatcher(matcher="Bash", hooks=[bash_security_hook]),
            ],
        },
        max_turns=1000,
        cwd=str(project_dir.resolve()),
        settings=str(settings_file.resolve()),
    )
)
```

## Security Settings File

Written to the project directory, read by the SDK client:

```python
import json

security_settings = {
    "sandbox": {
        "enabled": True,
        "autoAllowBashIfSandboxed": True,
    },
    "permissions": {
        "defaultMode": "acceptEdits",
        "allow": [
            "Read(./**)",
            "Write(./**)",
            "Edit(./**)",
            "Glob(./**)",
            "Grep(./**)",
            "Bash(*)",
        ],
    },
}

settings_file = project_dir / ".claude_settings.json"
with open(settings_file, "w") as f:
    json.dump(security_settings, f, indent=2)
```

## Permission Modes

- **`acceptEdits`**: Auto-approve file edits within allowed directories. The agent can read/write/edit without prompts.
- **Bash**: Allowed via `Bash(*)` but every command is validated by the security hook before execution.

## Hook Registration

Hooks intercept tool calls before execution:

```python
hooks={
    "PreToolUse": [
        HookMatcher(
            matcher="Bash",           # Only trigger for Bash tool
            hooks=[bash_security_hook] # Async function to validate
        ),
    ],
}
```

The hook function signature:
```python
async def bash_security_hook(input_data, tool_use_id=None, context=None):
    # Return {} to allow
    # Return {"decision": "block", "reason": "..."} to block
```

## MCP Server Integration

Add MCP servers for additional capabilities:

```python
mcp_servers={
    "puppeteer": {
        "command": "npx",
        "args": ["puppeteer-mcp-server"],
    }
}
```

Then add the MCP tool names to `allowed_tools`:
```python
allowed_tools=[
    "Read", "Write", "Edit", "Glob", "Grep", "Bash",
    "mcp__puppeteer__puppeteer_navigate",
    "mcp__puppeteer__puppeteer_screenshot",
    "mcp__puppeteer__puppeteer_click",
]
```

## Client Lifecycle

The SDK client uses an async context manager:

```python
client = create_client(project_dir, model)
async with client:
    await client.query(prompt)
    async for msg in client.receive_response():
        # Process messages
```

**Important**: Create a new client for each session to get a fresh context window.
