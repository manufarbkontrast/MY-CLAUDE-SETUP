---
name: save-session
description: Lightweight session context snapshot - works with or without Git repo, pushes if possible
---

# Save Session Context

Erstelle einen leichtgewichtigen Session-Kontext-Snapshot. Funktioniert mit und ohne Git-Repo.

- Mit Git: Commit + Push
- Ohne Git: Speichert lokal oder global

---

## Your Task

### 1. Detect Environment

Pruefe ob ein Git-Repository vorhanden ist:

```bash
git rev-parse --is-inside-work-tree 2>/dev/null
```

Setze intern eine Variable:
- `HAS_GIT = true` falls der Befehl "true" zurueckgibt
- `HAS_GIT = false` falls der Befehl fehlschlaegt

Pruefe ob ein Projekt-Root erkennbar ist (package.json, Cargo.toml, go.mod, pyproject.toml, oder anderer Projekt-Marker im aktuellen oder uebergeordneten Verzeichnis).

Setze intern:
- `PROJECT_ROOT` = Verzeichnis mit Projekt-Marker, oder aktuelles Arbeitsverzeichnis
- `PROJECT_NAME` = Name aus Projekt-Marker (z.B. aus package.json "name") oder Verzeichnisname

### 2. Gather Session State

**Falls HAS_GIT = true:**
- `git branch --show-current` (aktueller Branch)
- `git log -1 --format="%h %s"` (letzter Commit)
- `git status --short` (uncommitted changes)
- `git diff --stat HEAD~5..HEAD 2>/dev/null` (letzte Aenderungen)

**Falls HAS_GIT = false:**
- Arbeitsverzeichnis ermitteln: `pwd`
- Dateien auflisten die kuerzlich geaendert wurden (falls moeglich)
- Branch/Commit Felder im Snapshot mit "Kein Git-Repo" fuellen

### 3. Determine Storage Location

**Falls HAS_GIT = true oder PROJECT_ROOT erkannt:**
- Speicherort: `<PROJECT_ROOT>/.claude/context/`
- Erstelle das Verzeichnis falls noetig: `mkdir -p <PROJECT_ROOT>/.claude/context`

**Falls kein Projekt erkennbar (z.B. Ad-hoc Session, Einzeldateien, reines Chat):**
- Speicherort: `~/.claude/context/`
- Erstelle das Verzeichnis falls noetig: `mkdir -p ~/.claude/context`
- Dateinamen mit Projekt-Prefix versehen: `YYYY-MM-DD-standalone-<topic>.md`

### 4. Determine Topic

- Falls `$ARGUMENTS` angegeben: Verwende es als Topic
- Falls nicht: Leite ein kurzes Topic (2-3 Worte, kebab-case) aus den Aenderungen der Session ab
- Fallback: "general-session"

### 5. Create Snapshot File

Erstelle `<speicherort>/YYYY-MM-DD-<topic>.md` mit folgendem Inhalt:

```markdown
## Session: [YYYY-MM-DD] - [Topic]

### Umgebung
- **Projekt**: [PROJECT_NAME oder "Standalone"]
- **Pfad**: [PROJECT_ROOT oder Arbeitsverzeichnis]
- **Git**: [ja/nein]

### Branch & Stand
- **Branch**: [aktueller Branch oder "Kein Git-Repo"]
- **Letzter Commit**: [hash message oder "N/A"]
- **Uncommitted Changes**: [ja/nein, Anzahl Dateien oder "N/A"]

### Was wurde gemacht
- [Aenderung 1 mit betroffenen Dateien]
- [Aenderung 2 mit betroffenen Dateien]
- [...]

### Offene Aufgaben
- [ ] [naechster Schritt 1]
- [ ] [naechster Schritt 2]
- [ ] [...]

### Architektur-Entscheidungen
- [Entscheidung + Begruendung] (falls zutreffend)
- oder: Keine neuen Entscheidungen

### Kontext fuer naechste Session
- [Worauf muss geachtet werden]
- [Abhaengigkeiten oder Blocker]
```

### 6. Update latest.md

Kopiere den gesamten Inhalt der neuen Snapshot-Datei nach `<speicherort>/latest.md` (ueberschreiben falls vorhanden).

### 7. Update CLAUDE.md Reference (einmalig, nur bei Projekt)

Nur ausfuehren falls HAS_GIT = true oder PROJECT_ROOT erkannt:

Falls die `CLAUDE.md` im Projekt-Root existiert und noch KEINEN Verweis auf `.claude/context/` enthaelt, fuege am Ende hinzu:

```markdown

## Session Context
Aktuelle Session-Snapshots: `.claude/context/`
Letzter Stand: `.claude/context/latest.md`
```

Falls keine `CLAUDE.md` existiert, ueberspringe diesen Schritt.

### 8. Commit & Push (nur mit Git)

**Falls HAS_GIT = true:**

a) Stage die Context-Dateien:
```bash
git add .claude/context/
git add CLAUDE.md  # nur falls geaendert
```

b) Commit:
```bash
git commit -m "chore: save session context YYYY-MM-DD"
```
Falls CLAUDE.md nicht geaendert wurde, stage sie nicht.

c) Push:
- Pruefe ob ein Remote-Tracking-Branch existiert: `git rev-parse --abbrev-ref @{upstream} 2>/dev/null`
- Falls JA: `git push`
- Falls NEIN: `git push -u origin <aktueller-branch>`
- Falls der Push fehlschlaegt (z.B. diverged history, rejected): STOPPE und zeige dem User die Fehlermeldung. Fuehre NIEMALS `git push --force` aus.

**Falls HAS_GIT = false:**
- Ueberspringe Commit und Push
- Hinweis: "Kein Git-Repo - Snapshot nur lokal gespeichert."

### 9. Output Summary

Zeige eine kurze Zusammenfassung:

**Mit Git:**
```
Session Context gespeichert und gepusht.

Projekt:  <PROJECT_NAME>
Snapshot: .claude/context/YYYY-MM-DD-<topic>.md
Branch:   <branch>
Commit:   <hash>
Remote:   gepusht / nicht gepusht (+ Grund)

Naechste Session starten mit: /resume-session
```

**Ohne Git:**
```
Session Context lokal gespeichert.

Projekt:  <PROJECT_NAME oder "Standalone">
Snapshot: <vollstaendiger-pfad>/YYYY-MM-DD-<topic>.md
Hinweis:  Kein Git-Repo - nicht gepusht

Naechste Session starten mit: /resume-session
```

---

## Error Handling

- **Kein Git-Repo**: KEIN Fehler - speichere lokal und ueberspringe Commit/Push
- **Kein Projekt erkennbar**: Speichere in `~/.claude/context/` als Standalone
- **Keine Aenderungen zum committen**: Erstelle trotzdem den Snapshot, aber ueberspringe den Commit. Hinweis ausgeben.
- **Push fehlgeschlagen**: Snapshot ist lokal gespeichert. User informieren dass manuell gepusht werden muss.
- **Merge-Konflikte**: NIEMALS automatisch resolven. User informieren.
- **Schreibrechte fehlen**: Fehlermeldung mit Pfad ausgeben.
