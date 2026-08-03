# Security Sandbox

## Defense-in-Depth: 3 Layers

```
Layer 1: OS Sandbox (sandbox.enabled = true)
    └── Bash commands run in isolated environment
Layer 2: Permissions (allow list)
    └── File ops restricted to project directory (./**)
Layer 3: Security Hooks (PreToolUse)
    └── Bash commands validated against allowlist
```

Each layer catches attacks the others miss.

## Bash Security Hook (Allowlist Pattern)

The core security mechanism validates every Bash command before execution:

```python
ALLOWED_COMMANDS = {
    "ls", "cat", "head", "tail", "wc", "grep",  # File inspection
    "cp", "mkdir", "chmod",                       # File operations
    "pwd",                                         # Directory
    "npm", "node",                                 # Node.js
    "git",                                         # Version control
    "ps", "lsof", "sleep", "pkill",               # Process management
}

COMMANDS_NEEDING_EXTRA_VALIDATION = {"pkill", "chmod"}

async def bash_security_hook(input_data, tool_use_id=None, context=None):
    if input_data.get("tool_name") != "Bash":
        return {}  # Not a bash command, allow

    command = input_data.get("tool_input", {}).get("command", "")
    commands = extract_commands(command)

    if not commands:
        return {"decision": "block", "reason": "Could not parse command"}

    for cmd in commands:
        if cmd not in ALLOWED_COMMANDS:
            return {"decision": "block", "reason": f"'{cmd}' not allowed"}

        if cmd in COMMANDS_NEEDING_EXTRA_VALIDATION:
            allowed, reason = validate_command(cmd, command)
            if not allowed:
                return {"decision": "block", "reason": reason}

    return {}  # All commands allowed
```

**Why allowlist over blocklist?** Blocklists miss new attack vectors. With an allowlist, only explicitly permitted commands run.

## Command Parsing

Shell commands can be complex (`npm install && node app.js | grep error`). The parser handles:

```python
import shlex, re

def extract_commands(command_string):
    """Extract command names from complex shell strings."""
    commands = []
    # Split on semicolons outside quotes
    segments = re.split(r'(?<!["\'])\s*;\s*(?!["\'])', command_string)

    for segment in segments:
        try:
            tokens = shlex.split(segment)
        except ValueError:
            return []  # Malformed = block (fail-safe)

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
```

## Extra Validation for Sensitive Commands

Some allowed commands need additional checks:

- **pkill**: Only dev processes (node, npm, vite, next)
- **chmod**: Only `+x` variants (making scripts executable)
- **init.sh**: Only `./init.sh` (no arbitrary script execution)

```python
def validate_pkill_command(command_string):
    allowed_targets = {"node", "npm", "npx", "vite", "next"}
    tokens = shlex.split(command_string)
    args = [t for t in tokens[1:] if not t.startswith("-")]
    target = args[-1].split()[0] if args else ""
    if target in allowed_targets:
        return True, ""
    return False, f"pkill only for dev processes: {allowed_targets}"
```

## Filesystem Restrictions

File operations are restricted to the project directory via relative path patterns:

```python
"permissions": {
    "allow": [
        "Read(./**)",    # Only within project dir
        "Write(./**)",
        "Edit(./**)",
        "Glob(./**)",
        "Grep(./**)",
        "Bash(*)",       # Allowed but validated by hook
    ]
}
```

The `cwd` is set to `project_dir`, so `./**` means "only within the project".
