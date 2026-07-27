# Installationsanleitung — Hallmark + codebase-memory-mcp + OfficeCLI

Erstellt am 27.07.2026. Zum Einrichten auf einem neuen/anderen Rechner.

---

## 1. Hallmark (Anti-Slop Design Skill)

Keine Binary nötig — reine Skill-Dateien.

```bash
# Option A: Aus diesem Repo kopieren (wenn Repo geklont)
cp -r ~/my-claude-setup/skills/hallmark ~/.claude/skills/hallmark

# Option B: Direkt von GitHub installieren
npx skills add nutlope/hallmark

# Option C: Manuell klonen
git clone --single-branch --depth 1 https://github.com/Nutlope/hallmark.git /tmp/hallmark
cp -r /tmp/hallmark/skills/hallmark ~/.claude/skills/hallmark
rm -rf /tmp/hallmark
```

**Prüfen:** `ls ~/.claude/skills/hallmark/SKILL.md` sollte existieren.

**Nutzung:** Automatisch aktiv bei jedem UI-Build. Oder explizit:
- `audit` — bestehendes UI gegen Anti-Patterns scoren
- `redesign` — UI umbauen mit neuem Fingerprint
- `study` — Design-DNA aus URL/Screenshot extrahieren

---

## 2. codebase-memory-mcp (Code-Intelligence Knowledge-Graph)

### Installation

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh | bash

# Danach Shell neu starten
source ~/.bashrc  # oder source ~/.zshrc
```

Der Installer:
- Lädt die Binary nach `~/.local/bin/codebase-memory-mcp`
- Konfiguriert Claude Code automatisch (MCP-Eintrag in `~/.claude.json`)
- Installiert Skill, Hooks (Grep/Glob Augmenter, Session-Reminder)

**Prüfen:**
```bash
codebase-memory-mcp --version  # sollte 0.9.0+ zeigen
# In Claude Code:
/mcp                           # sollte codebase-memory-mcp listen
```

### MCP-Config (falls manuell nötig)

In `~/.claude.json` unter `mcpServers`:
```json
{
  "codebase-memory-mcp": {
    "command": "codebase-memory-mcp",
    "args": []
  }
}
```

### Nutzung

```
# Codebase indizieren (einmalig pro Projekt)
> Indiziere dieses Repository

# Dann Fragen stellen
> Welche Funktionen rufen die API auf?
> Zeig mir den Call-Graph von handleAuth
> Finde toten Code
> Welche Module hängen von der DB ab?
```

---

## 3. OfficeCLI (Office-Suite für AI Agents)

### Installation

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/iOfficeAI/OfficeCLI/main/install.sh | bash

# Alternativ via Homebrew (macOS)
brew install officecli

# Alternativ via npm
npm install -g @officecli/officecli
```

### MCP-Server registrieren

```bash
officecli mcp claude
```

**Prüfen:**
```bash
officecli --version  # sollte 1.0.142+ zeigen
# In Claude Code:
/mcp                 # sollte officecli listen
```

### MCP-Config (falls manuell nötig)

In `~/.claude.json` unter `mcpServers`:
```json
{
  "officecli": {
    "command": "officecli",
    "args": ["mcp"]
  }
}
```

### Nutzung

```
# Excel erstellen
> Erstelle eine Excel-Tabelle mit Umsatzdaten Q1-Q4

# Word-Dokument bearbeiten
> Öffne report.docx und füge ein Inhaltsverzeichnis hinzu

# PowerPoint bauen
> Erstelle eine 10-Folien-Präsentation zum Thema X

# Dokument rendern (Feedback-Schleife)
> Zeig mir die Präsentation als HTML-Preview
```

---

## Schnell-Installation (alles auf einmal)

```bash
# 1. Repo klonen (falls nicht vorhanden)
git clone https://github.com/manufarbkontrast/MY-CLAUDE-SETUP.git ~/my-claude-setup

# 2. Hallmark Skill kopieren
cp -r ~/my-claude-setup/skills/hallmark ~/.claude/skills/hallmark

# 3. codebase-memory-mcp installieren
curl -fsSL https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh | bash

# 4. OfficeCLI installieren
curl -fsSL https://raw.githubusercontent.com/iOfficeAI/OfficeCLI/main/install.sh | bash
officecli mcp claude

# 5. settings.json aktualisieren (MCP-Configs)
cp ~/my-claude-setup/settings.json ~/.claude/settings.json

# 6. Shell neu starten
source ~/.bashrc
```

---

## Zusammenfassung

| Tool | Typ | Binary | MCP | Skill |
|------|-----|--------|-----|-------|
| Hallmark | Skill | - | - | `~/.claude/skills/hallmark/` |
| codebase-memory-mcp | MCP Server | `~/.local/bin/codebase-memory-mcp` | `~/.claude.json` | auto-installiert |
| OfficeCLI | MCP Server | System-PATH | `~/.claude.json` | `~/.claude/skills/officecli/` |
