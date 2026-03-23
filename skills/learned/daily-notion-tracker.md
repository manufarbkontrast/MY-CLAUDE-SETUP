---
name: daily-notion-tracker
description: Sammelt Git-Tagesleistung (Commits, Änderungen, Branches) aus allen Repos (inkl. private) des GitHub-Accounts manufarbkontrast und schreibt ausführliche Einträge in die Notion-Datenbank "Tagesleistung".
trigger: "/tagesleistung"
---

# Daily Notion Tracker - Tagesleistung

Dieser Skill sammelt alle Git-Änderungen des aktuellen Tages aus allen Repos (inkl. private) des GitHub-Accounts `manufarbkontrast` und erstellt pro aktivem Repo einen ausführlichen Eintrag in der Notion-Datenbank "Tagesleistung".

## GitHub-Account

- **Account**: `manufarbkontrast`
- **Auth**: `gh` CLI mit `repo`-Scope (sieht auch private Repos)
- **Repos auflisten**: `gh repo list manufarbkontrast --limit 100 --json name,isPrivate,pushedAt,url`

## Notion-Datenbank

- **Database URL**: https://www.notion.so/84ef8978648748f5b2adada7cea60497
- **Data Source ID**: `a8e9e326-6928-4dad-8ef4-46cd0cea8bc0`

## Schema

| Property | Type | Beschreibung |
|----------|------|-------------|
| Zusammenfassung | Title | Beschreibender Satz, was gemacht wurde (KEIN "[REPO] X Commits" Format) |
| Datum | Date | Tag der Leistung |
| Repo | Rich Text | Repository-Name |
| Branch | Rich Text | Aktiver Branch |
| Commits | Number | Anzahl Commits am Tag |
| Dateien geändert | Number | Geänderte Dateien |
| Zeilen hinzugefügt | Number | Insertions |
| Zeilen entfernt | Number | Deletions |
| Status | Select | Abgeschlossen / In Arbeit / Review |
| Typ | Multi Select | feat, fix, refactor, docs, test, chore |
| Repo URL | URL | Link zum Repository |

## Ablauf

### 1. Alle Repos scannen

```bash
gh repo list manufarbkontrast --limit 100 --json name,isPrivate,pushedAt,url
```

### 2. Heutige Commits pro Repo holen

Für jedes Repo mit `pushedAt` von heute:

```bash
TODAY=$(date +%Y-%m-%d)
gh api "repos/manufarbkontrast/{REPO}/commits?since=${TODAY}T00:00:00Z&until=${TODAY}T23:59:59Z" \
  --jq '.[] | "\(.sha[:7]) | \(.commit.message | split("\n")[0]) | \(.commit.author.date)"'
```

### 3. Vollständige Commit-Details holen

Für JEDEN Commit die vollständige Message und Datei-Details abrufen:

```bash
# Volle Commit-Message (nicht nur erste Zeile!)
gh api "repos/manufarbkontrast/{REPO}/commits/{SHA}" --jq '.commit.message'

# Geänderte Dateien mit Stats
gh api "repos/manufarbkontrast/{REPO}/commits/{SHA}" \
  --jq '[.files[] | "\(.filename) | +\(.additions) -\(.deletions) | \(.status)"]'
```

Bei mehreren Commits die Gesamtstatistik über Compare holen:

```bash
gh api "repos/manufarbkontrast/{REPO}/compare/{FIRST_SHA}^...{LAST_SHA}" \
  --jq '{files_changed: (.files | length), additions: ([.files[].additions] | add), deletions: ([.files[].deletions] | add), files: [.files[].filename]}'
```

### 4. Zusammenfassung schreiben

**WICHTIG**: Die Zusammenfassung beschreibt WAS gemacht wurde, nicht nur Zahlen.

**Gutes Format**: `"REPO: Beschreibung der Hauptänderung in einem Satz"`
**Beispiele**:
- `"PRODUCT-UPLOAD: KI-gestützte Schuhbild-Klassifizierung und automatische Sortierung nach Ansichtstyp"`
- `"shoes-please-video-prompts: Fal AI Video-Generierung mit Kling v2.1 integriert"`

**Schlechtes Format** (NICHT verwenden):
- `"[PRODUCT-UPLOAD] 2 Commits - feat"`
- `"[repo] X Commits: Zusammenfassung"`

### 5. Passendes Icon wählen

Wähle ein thematisch passendes Emoji als Icon basierend auf dem Repo-Inhalt:
- Schuhe/Fashion: 👟
- Video/Film: 🎬
- Dashboard: 📊
- Website: 🌐
- Tools/Utils: 🔧
- Security: 🔒
- AI/ML: 🤖

### 6. Notion-Eintrag erstellen

Verwende `mcp__claude_ai_Notion__notion-create-pages` mit ausführlichem Content:

```json
{
  "parent": {
    "data_source_id": "a8e9e326-6928-4dad-8ef4-46cd0cea8bc0"
  },
  "pages": [
    {
      "icon": "👟",
      "properties": {
        "Zusammenfassung": "REPO: Beschreibender Satz was gemacht wurde",
        "date:Datum:start": "YYYY-MM-DD",
        "date:Datum:is_datetime": 0,
        "Repo": "repo-name",
        "Branch": "branch-name",
        "Commits": 2,
        "Dateien geändert": 9,
        "Zeilen hinzugefügt": 626,
        "Zeilen entfernt": 10,
        "Status": "Abgeschlossen",
        "Typ": "[\"feat\"]",
        "Repo URL": "https://github.com/manufarbkontrast/repo"
      }
    }
  ]
}
```

Danach Content mit `mcp__claude_ai_Notion__notion-update-page` (`replace_content`) setzen.

### 7. Content-Vorlage

Der Seiteninhalt folgt dieser Struktur:

```markdown
## Was wurde gemacht?

2-3 Sätze die verständlich erklären, was sich geändert hat und warum.
Technische Details so beschreiben, dass auch Nicht-Entwickler es verstehen.

---

## Neue Features / Änderungen

### 1. Feature-Name
Beschreibung was das Feature macht, wie es funktioniert,
welche Technologien verwendet werden.

### 2. Weiteres Feature
Weitere Details...

---

## Commits

| Commit | Beschreibung |
|--------|-------------|
| `sha1234` | feat: Kurzbeschreibung |
| `sha5678` | fix: Kurzbeschreibung |

---

## Neue Dateien

| Datei | Beschreibung |
|-------|-------------|
| `path/to/new-file.ts` | Was diese Datei macht (+X Zeilen) |

## Geänderte Dateien

| Datei | Änderung | Beschreibung |
|-------|---------|-------------|
| `path/to/file.ts` | +X / -Y | Was geändert wurde |

---

## Statistik

| Metrik | Wert |
|--------|------|
| Commits | X |
| Neue Dateien | X |
| Geänderte Dateien | X |
| Zeilen hinzugefügt | +X |
| Zeilen entfernt | -X |
```

### 8. Bestätigung

Zeige dem User pro Repo:
- Icon + Repo-Name
- Link zur Notion-Seite
- Kurze Zusammenfassung (1 Satz)
- Statistik (Commits, Dateien, Zeilen)

Am Ende eine Gesamtübersicht über alle Repos.

## Sonderfälle

- **Keine Commits heute**: Repo überspringen, nicht eintragen
- **Nur 1 Commit**: Trotzdem vollständige Details mit "Was wurde gemacht?" Abschnitt
- **Viele Commits (>5)**: Features/Fixes gruppieren statt einzeln auflisten
- **Merge-Commits**: Überspringen, nur echte Arbeits-Commits zählen
