"""Claude Agent SDK client configuration with security layers.

Sets up a ClaudeSDKClient with:
- Sandboxed execution
- File-system restricted permissions
- Bash allowlist security hook

Usage:
    from sdk_client_setup import create_client

    client = create_client(Path("./my-project"), "claude-sonnet-4-20250514")
    async with client:
        await client.query("Implement the login page")
"""

import json
from pathlib import Path

from claude_code_sdk import ClaudeCodeOptions, ClaudeSDKClient
from claude_code_sdk.types import HookMatcher

from security_hook import bash_security_hook

# -- CONFIGURE THESE ----------------------------------------------------------
DEFAULT_MODEL = "claude-sonnet-4-20250514"
DEFAULT_MAX_TURNS = 1000
SYSTEM_PROMPT = "You are an expert full-stack developer."

ALLOWED_TOOLS = [
    "Read", "Write", "Edit", "Glob", "Grep", "Bash",
]
# -- END CONFIG ---------------------------------------------------------------


def write_security_settings(project_dir: Path) -> Path:
    """Write the security settings JSON and return its path."""
    settings = {
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
        json.dump(settings, f, indent=2)
    return settings_file


def create_client(
    project_dir: Path,
    model: str = DEFAULT_MODEL,
) -> ClaudeSDKClient:
    """Create a fresh SDK client with full security configuration."""
    settings_file = write_security_settings(project_dir)

    return ClaudeSDKClient(
        options=ClaudeCodeOptions(
            model=model,
            system_prompt=SYSTEM_PROMPT,
            allowed_tools=ALLOWED_TOOLS,
            hooks={
                "PreToolUse": [
                    HookMatcher(
                        matcher="Bash",
                        hooks=[bash_security_hook],
                    ),
                ],
            },
            max_turns=DEFAULT_MAX_TURNS,
            cwd=str(project_dir.resolve()),
            settings=str(settings_file.resolve()),
        )
    )
