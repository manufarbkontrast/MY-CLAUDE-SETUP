# Sync-Report – 2026-06-03

## Repository Status

- **Git pull**: Already up to date (no merge conflicts)
- **Branch**: main

---

## Skills (453 Verzeichnisse)

### Gesund: 453/453

Alle 453 Skill-Verzeichnisse enthalten mindestens eine Datei.

### Probleme (3)

| Problem | Details | Empfehlung |
|---------|---------|------------|
| 7 broken Symlinks | `create-agent-adapter`, `paperclip`, `paperclip-create-agent`, `para-memory-files`, `pr-report`, `release`, `release-changelog` — zeigen auf `/Users/craftongmbh/paperclip/skills/...` | Entweder Symlinks entfernen oder Paperclip-Skills als echte Kopien einfuegen |
| 1 Datei ausserhalb der Konvention | `skills/cli-anything.md` liegt direkt im Root statt in `skills/cli-anything/SKILL.md` | In eigenes Verzeichnis verschieben |
| 1 Meta-Verzeichnis ohne SKILL.md | `document-skills/` enthaelt nur Unterordner (docx, pdf, pptx, xlsx) | Kein Handlungsbedarf (strukturelle Gruppierung) |

---

## Agents (182 Dateien)

### Gesund: 181/182

### Probleme (1)

| Problem | Details | Empfehlung |
|---------|---------|------------|
| Leere Datei | `agents/deployment-engineer.md` ist 0 Bytes | Inhalt hinzufuegen oder Datei entfernen |

---

## Commands (192 Dateien)

### Gesund: 192/192

Alle 192 Command-Dateien sind vorhanden und nicht leer. 2 Unterverzeichnisse: `git/` (3 Commands), `skill/` (1 Command).

---

## Rules (9 Dateien)

### Gesund: 9/9

Alle 9 Regeln stimmen mit CLAUDE.md ueberein:
`coding-style`, `git-workflow`, `testing`, `performance`, `patterns`, `hooks`, `agents`, `security`, `uncodixify`

---

## Settings.json

| Kategorie | Anzahl | Status |
|-----------|--------|--------|
| PreToolUse Hooks | 4 | OK |
| PostToolUse Hooks | 5 | OK |
| Plugins | 22 | OK |
| MCP Servers | 0 | Nicht in settings.json (lokal auf der Maschine konfiguriert) |

---

## Prompt Optimizer

| Komponente | Status |
|------------|--------|
| Quellcode (`src/`) | 5 TypeScript-Dateien vorhanden |
| Python-Script (`scripts/`) | Vorhanden (Standalone-Alternative) |
| `node_modules/` | Fehlt (erwartet nach Clone) |
| `dist/` | Fehlt (erwartet nach Clone) |
| `registry.json` | Fehlt (muss gebaut werden) |

Nach Clone `./install.sh` ausfuehren, um den Optimizer nutzbar zu machen.

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

1. **`agents/deployment-engineer.md`** — Inhalt erstellen oder Datei entfernen
2. **7 broken Symlinks** in `skills/` — Entfernen oder durch echte Kopien ersetzen
3. **`skills/cli-anything.md`** — In `skills/cli-anything/SKILL.md` verschieben
4. **MCP-Server-Konfiguration** — Ggf. lightpanda, dbhub, linkedin in `settings.json` aufnehmen, damit sie mit-synchronisiert werden

---

## Einschraenkungen dieser Pruefung

- Laufumgebung: Remote-Container (kein Zugriff auf `~/.claude/`)
- `claude mcp list` / `claude mcp add` nicht verfuegbar
- Telegram-Benachrichtigung nicht moeglich
- Keine Pruefung, ob Skills/Agents in der lokalen Claude-Code-Installation registriert sind
