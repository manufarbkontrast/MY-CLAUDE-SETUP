"""Bash security hook using an allowlist pattern.

Validates every Bash command before execution. Only explicitly
permitted commands can run — unknown commands are blocked.

Usage:
    Pass `bash_security_hook` to the SDK client's hook registration.
    See sdk-client-setup.py for integration.
"""

import os
import re
import shlex

# -- CONFIGURE THESE ----------------------------------------------------------
ALLOWED_COMMANDS: set[str] = {
    # File inspection
    "ls", "cat", "head", "tail", "wc", "grep",
    # File operations
    "cp", "mkdir", "chmod",
    # Directory
    "pwd",
    # Node.js ecosystem
    "npm", "node", "npx",
    # Version control
    "git",
    # Process management
    "ps", "lsof", "sleep", "pkill",
}

COMMANDS_NEEDING_EXTRA_VALIDATION: set[str] = {"pkill", "chmod"}
ALLOWED_PKILL_TARGETS: set[str] = {"node", "npm", "npx", "vite", "next"}
# -- END CONFIG ---------------------------------------------------------------


def extract_commands(command_string: str) -> list[str]:
    """Extract base command names from a complex shell string."""
    commands: list[str] = []
    segments = re.split(r'(?!["\'"])\s*;\s*(?!["\'])', command_string)

    for segment in segments:
        try:
            tokens = shlex.split(segment)
        except ValueError:
            return []  # Malformed input → fail-safe block

        expect_command = True
        for token in tokens:
            if token in ("|", "||", "&&", "&"):
                expect_command = True
                continue
            if token.startswith("-") or ("=" in token):
                continue
            if expect_command:
                commands.append(os.path.basename(token))
                expect_command = False

    return commands


def validate_pkill(command_string: str) -> tuple[bool, str]:
    tokens = shlex.split(command_string)
    args = [t for t in tokens[1:] if not t.startswith("-")]
    target = args[-1].split()[0] if args else ""
    if target in ALLOWED_PKILL_TARGETS:
        return True, ""
    return False, f"pkill only allowed for dev processes: {ALLOWED_PKILL_TARGETS}"


def validate_chmod(command_string: str) -> tuple[bool, str]:
    if "+x" in command_string:
        return True, ""
    return False, "chmod only allowed with +x (make executable)"


EXTRA_VALIDATORS: dict[str, callable] = {
    "pkill": validate_pkill,
    "chmod": validate_chmod,
}


async def bash_security_hook(
    input_data: dict,
    tool_use_id: str | None = None,
    context: dict | None = None,
) -> dict:
    """PreToolUse hook — return {} to allow, or a block decision."""
    if input_data.get("tool_name") != "Bash":
        return {}

    command = input_data.get("tool_input", {}).get("command", "")
    commands = extract_commands(command)

    if not commands:
        return {"decision": "block", "reason": "Could not parse command"}

    for cmd in commands:
        if cmd not in ALLOWED_COMMANDS:
            return {"decision": "block", "reason": f"'{cmd}' is not in the allowlist"}

        if cmd in COMMANDS_NEEDING_EXTRA_VALIDATION:
            validator = EXTRA_VALIDATORS[cmd]
            allowed, reason = validator(command)
            if not allowed:
                return {"decision": "block", "reason": reason}

    return {}  # All commands passed
