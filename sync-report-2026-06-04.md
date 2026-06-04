# Sync-Report – 2026-06-04

## Repository Status

- **Git pull**: Already up to date (no merge conflicts)
- **Branch**: main
- **Letzter Commit**: `bc19e50` — docs: daily sync report 2026-06-03

---

## Skills (453 Verzeichnisse)

### Gesund: 453/453

Alle 453 Skill-Verzeichnisse enthalten mindestens eine Datei.

### Offene Probleme (3) — unveraendert seit 2026-06-03

| # | Problem | Details | Empfehlung |
|---|---------|---------|------------|
| 1 | 7 broken Symlinks | `create-agent-adapter`, `paperclip`, `paperclip-create-agent`, `para-memory-files`, `pr-report`, `release`, `release-changelog` — zeigen auf `/Users/craftongmbh/paperclip/skills/...` | Symlinks entfernen oder Paperclip-Skills als echte Kopien einfuegen |
| 2 | 1 Datei ausserhalb der Konvention | `skills/cli-anything.md` liegt direkt im Root statt in `skills/cli-anything/SKILL.md` | In eigenes Verzeichnis verschieben |
| 3 | 1 Meta-Verzeichnis ohne SKILL.md | `document-skills/` enthaelt Unterordner (docx, pdf, pptx, xlsx) mit eigenen SKILL.md | Kein Handlungsbedarf (strukturelle Gruppierung) |

---

## Agents (182 Dateien)

### Gesund: 181/182

### Offene Probleme (1) — unveraendert seit 2026-06-03

| Problem | Details | Empfehlung |
|---------|---------|------------|
| Leere Datei | `agents/deployment-engineer.md` ist 0 Bytes | Inhalt erstellen oder Datei entfernen |

---

## Commands (192 Dateien)

### Gesund: 192/192

Alle 192 Command-Dateien sind vorhanden und nicht leer.
Unterverzeichnisse: `git/` (3 Commands: cm, cp, pr), `skill/` (1 Command: create).

---

## Rules (9 Dateien)

### Gesund: 9/9

Alle Regeln stimmen mit CLAUDE.md ueberein:
`agents`, `coding-style`, `git-workflow`, `hooks`, `patterns`, `performance`, `security`, `testing`, `uncodixify`

---

## Settings.json

| Kategorie | Anzahl | Status |
|-----------|--------|--------|
| PreToolUse Hooks | 4 | OK |
| PostToolUse Hooks | 5 | OK |
| Plugins | 22 | OK |
| Extra Marketplaces | 5 | OK |
| MCP Servers | 0 | Lokal konfiguriert (nicht in settings.json) |

---

## Aenderungen seit letztem Report

Keine inhaltlichen Aenderungen — nur der Sync-Report vom 2026-06-03 wurde hinzugefuegt.

---

## Zusammenfassung

| Kategorie | Gesamt | Gesund | Probleme |
|-----------|--------|--------|----------|
| Skills | 453 | 453 | 3 (Symlinks, Konvention, Meta-Dir) |
| Agents | 182 | 181 | 1 (leere Datei) |
| Commands | 192 | 192 | 0 |
| Rules | 9 | 9 | 0 |
| Hooks | 9 | 9 | 0 |
| Plugins | 22 | 22 | 0 |
| **Sync-Status** | | | **99.4%** |

---

## Handlungsempfehlungen (priorisiert)

1. **`agents/deployment-engineer.md`** — Inhalt erstellen oder Datei entfernen (0 Bytes seit mindestens 2 Tagen)
2. **7 broken Symlinks** in `skills/` — Alle zeigen auf `/Users/craftongmbh/paperclip/skills/` — entfernen oder durch echte Kopien ersetzen
3. **`skills/cli-anything.md`** — In `skills/cli-anything/SKILL.md` verschieben
4. **MCP-Server-Konfiguration** — lightpanda, dbhub, linkedin ggf. in `settings.json` aufnehmen

---

## Einschraenkungen

- Laufumgebung: Remote-Container (kein Zugriff auf `~/.claude/`)
- `claude mcp list` / `claude mcp add` nicht verfuegbar
- Telegram-Benachrichtigung nicht moeglich
- Keine Pruefung, ob Skills/Agents in der lokalen Claude-Code-Installation aktiv registriert sind
