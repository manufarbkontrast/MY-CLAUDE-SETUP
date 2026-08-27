## Täglicher Sync-Report – 2026-08-27

### Git Status
- `git pull origin main` — Fast-forward von `a89bf95` auf `6c50274`
- Letzter fremder Commit: `6c50274` (26.08.) — fix: repair frontmatter of 32 nicht ladbarer Skills & Agents

### Inventar

| Kategorie | Anzahl | Veränderung | Status |
|-----------|--------|-------------|--------|
| Skills (Verzeichnisse) | 466 | +0 | OK |
| Skills (mit SKILL.md) | 463 | +0 | OK |
| Skills (Symlinks, broken) | 7 | +0 | bekannt, lokal zu beheben |
| Agents | 182 | +0 | 1 leere Datei (bekannt) |
| Commands | 190 | +0 | OK |
| Rules | 9 | +0 | OK |
| settings.json | — | valides JSON | OK |

---

### Neuer Befund: CRLF-Zeilenenden in jtl-stammdaten

`skills/jtl-stammdaten/SKILL.md` hatte Windows-Zeilenenden (`\r\n`).
YAML-Parser können dadurch `---\r` statt `---` lesen und die Frontmatter
nicht erkennen. Wurde in der gestrigen Validierung (644/645) nicht
aufgefangen, weil die Datei inhaltlich korrekt ist.

→ Behoben: `\r` entfernt, Datei jetzt mit Unix-LF.

**Ladbarkeit nach Fix:** 644/645 bestätigt (jtl-stammdaten war vermutlich
bereits ladbar, das CRLF war aber ein Risiko). Einzige verbleibende
nicht-ladbare Datei: `agents/deployment-engineer.md` (leer, 0 Bytes).

---

### Offene Warnungen (unverändert, lokale Korrektur nötig)

| Datei | Problem | Seit | Tage offen |
|-------|---------|------|------------|
| `agents/deployment-engineer.md` | Datei ist leer (0 Bytes) | 24.06. | 64 |
| `skills/create-agent-adapter` | Broken symlink → `/Users/craftongmbh/paperclip/skills/` | 29.06. | 59 |
| `skills/paperclip` | Broken symlink → dito | 29.06. | 59 |
| `skills/paperclip-create-agent` | Broken symlink → dito | 29.06. | 59 |
| `skills/para-memory-files` | Broken symlink → dito | 29.06. | 59 |
| `skills/pr-report` | Broken symlink → dito | 29.06. | 59 |
| `skills/release` | Broken symlink → dito | 29.06. | 59 |
| `skills/release-changelog` | Broken symlink → dito | 29.06. | 59 |

Empfehlung: Lokal mit `rsync -avL` die Symlink-Ziele materialisieren
oder die 7 Symlinks entfernen, falls die Paperclip-Skills nicht mehr
benötigt werden.

---

### Sync-Status
- Repository: aktuell, kein Delta zu remote nach Pull
- Ladbarkeit Skills/Agents: 644/645 (99,8 %)
- Fix committed: CRLF in jtl-stammdaten behoben
