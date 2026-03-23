---
name: resume-session
description: Resume work from last session - works with or without Git repo
---

# Resume Session

Lade den letzten Session-Kontext und bereite die Weiterarbeit vor.

Funktioniert mit und ohne Git-Repo. Sucht Kontext an mehreren Orten.

---

## Your Task

### 1. Detect Environment

Pruefe ob ein Git-Repository vorhanden ist:

```bash
git rev-parse --is-inside-work-tree 2>/dev/null
```

Setze intern:
- `HAS_GIT = true/false`
- `PROJECT_ROOT` = Git-Root, oder Verzeichnis mit Projekt-Marker, oder aktuelles Arbeitsverzeichnis

### 2. Find Context (Reihenfolge)

Suche den Session-Kontext in dieser Reihenfolge:

1. `<PROJECT_ROOT>/.claude/context/latest.md` (Projekt-lokal)
2. `<PROJECT_ROOT>/.claude/context/` (neueste Datei nach Name)
3. `~/.claude/context/latest.md` (global, fuer Standalone-Sessions)
4. `~/.claude/context/` (global, neueste Datei nach Name)

Verwende den ersten Treffer. Falls nichts gefunden:
- Ausgabe: "Kein Session-Kontext gefunden. Starte frisch oder nutze /save-session am Ende der naechsten Session."
- Stoppe hier.

Merke dir den Speicherort als `CONTEXT_SOURCE` (projekt-lokal oder global).

### 3. Pull Latest Changes (nur mit Git)

**Falls HAS_GIT = true:**

Pruefe ob es neue Aenderungen auf dem Remote gibt:

```bash
git fetch origin 2>/dev/null
git log HEAD..@{upstream} --oneline 2>/dev/null
```

- Falls neue Commits vorhanden: Zeige sie an und frage ob ein `git pull` ausgefuehrt werden soll
- Falls keine neuen Commits: Weiter
- Falls kein Upstream oder fetch fehlschlaegt: Weiter ohne Warnung

**Falls HAS_GIT = false:**
- Ueberspringe diesen Schritt

### 4. Verify Branch (nur mit Git)

**Falls HAS_GIT = true:**

Vergleiche den aktuellen Branch mit dem Branch aus dem Snapshot:

- Falls gleich: Weiter
- Falls unterschiedlich: Warnung ausgeben: "Du bist auf Branch [aktuell], aber der Snapshot war auf [snapshot-branch]. Moechtest du wechseln?"

**Falls HAS_GIT = false:**
- Vergleiche den aktuellen Pfad mit dem Pfad aus dem Snapshot
- Falls unterschiedlich: Hinweis ausgeben

### 5. Display Summary

Zeige eine uebersichtliche Zusammenfassung:

**Mit Git:**
```
Resume Session
==============

Projekt: [PROJECT_NAME]
Branch:  [branch]
Letzter Commit: [hash] [message]
Snapshot vom: [datum]
Quelle: [projekt-lokal / global]

Was zuletzt gemacht wurde:
  - [aenderung 1]
  - [aenderung 2]

Offene Aufgaben:
  1. [aufgabe 1]
  2. [aufgabe 2]
  3. [aufgabe 3]

Blocker / Hinweise:
  - [blocker oder "Keine"]
```

**Ohne Git:**
```
Resume Session (lokal)
======================

Projekt: [PROJECT_NAME oder "Standalone"]
Pfad:    [Arbeitsverzeichnis]
Snapshot vom: [datum]
Quelle: [projekt-lokal / global]

Was zuletzt gemacht wurde:
  - [aenderung 1]
  - [aenderung 2]

Offene Aufgaben:
  1. [aufgabe 1]
  2. [aufgabe 2]
  3. [aufgabe 3]

Blocker / Hinweise:
  - [blocker oder "Keine"]
```

### 6. Create TodoWrite List

Erstelle eine TodoWrite-Liste mit allen offenen Aufgaben aus dem Snapshot. Setze die erste Aufgabe auf `in_progress`.

### 7. Ready

Ausgabe:

```
Kontext geladen. Bereit weiterzuarbeiten.

Erste Aufgabe: [aufgabe 1]
```

Warte auf weitere Anweisungen des Users.

---

## Error Handling

- **Kein Context-Verzeichnis**: Freundlicher Hinweis, nicht abbrechen
- **Git fetch fehlgeschlagen**: Warnung, aber weitermachen mit lokalem Stand
- **Branch-Wechsel gewuenscht**: Nur ausfuehren wenn User bestaetigt
- **Kein Git-Repo**: Kein Fehler - arbeite mit lokalen Dateien
- **Snapshot-Pfad stimmt nicht mit aktuellem Pfad ueberein**: Hinweis ausgeben, weitermachen
