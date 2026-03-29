# Hooks System

## Hook Types

- **PreToolUse**: Before tool execution (validation, parameter modification)
- **PostToolUse**: After tool execution (auto-format, checks)
- **Stop**: When session ends (final verification)

## Conditional Hooks (`if` Field)

Since Claude Code v2.1.85: Das `if`-Feld filtert Hook-Ausführung **vor** dem Prozess-Spawning.
Verwendet Permission-Rule-Syntax als Pre-Filter, `matcher` bleibt für detaillierte Bedingungen.

### Syntax

```json
{
  "matcher": "tool == \"Bash\" && tool_input.command matches \"git push\"",
  "if": "Bash(git push*)",
  "hooks": [{ "type": "command", "command": "..." }]
}
```

### Unterstützte Patterns

| Pattern | Beschreibung |
|---------|-------------|
| `Bash(git *)` | Bash-Befehle die mit "git " starten |
| `Bash(*build*)` | Bash-Befehle die "build" enthalten |
| `Edit(*.ts)` | Edits an TypeScript-Dateien |
| `Write(*.md)` | Schreibzugriffe auf Markdown-Dateien |
| `Read(src/*)` | Lesezugriffe im src-Verzeichnis |

### Kombination mit `||`

```json
"if": "Edit(*.ts) || Edit(*.tsx) || Edit(*.js) || Edit(*.jsx)"
```

### Vorteile

- **Performance**: Kein Prozess-Spawning wenn `if` nicht matcht
- **Effizienz**: `matcher` wird nur evaluiert wenn `if` zutrifft
- **Kompatibilität**: `if` ist optional, bestehende Hooks funktionieren weiterhin

## Auto-Accept Permissions

Use with caution:
- Enable for trusted, well-defined plans
- Disable for exploratory work
- Never use dangerously-skip-permissions flag
- Configure `allowedTools` in `~/.claude.json` instead

## TodoWrite Best Practices

Use TodoWrite tool to:
- Track progress on multi-step tasks
- Verify understanding of instructions
- Enable real-time steering
- Show granular implementation steps

Todo list reveals:
- Out of order steps
- Missing items
- Extra unnecessary items
- Wrong granularity
- Misinterpreted requirements
