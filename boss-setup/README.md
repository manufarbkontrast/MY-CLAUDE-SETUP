# Claude Office Setup

Eine schlanke, büro-fokussierte Claude-Code-Konfiguration. Erstellt Word-,
Excel-, PowerPoint- und PDF-Dateien, hilft beim Schreiben von Dokumenten,
bei Recherche und Business-Analysen — ohne Entwickler-Ballast.

## Was ist drin?

**Skills** (werden automatisch aktiv, wenn sie passen):

| Skill | Wofür |
|-------|-------|
| `docx` | Word-Dokumente: Reports, Memos, Briefe, Angebote |
| `xlsx` | Excel: Tabellen, Formeln, Charts, Daten bereinigen |
| `pptx` | PowerPoint: Präsentationen, Pitch-Decks |
| `pdf` | PDFs lesen, zusammenführen, teilen, Formulare ausfüllen |
| `doc-coauthoring` | Strukturiertes Schreiben von Proposals, Specs, Entscheidungs-Docs |
| `excel-template-dynamic-mapping` | Wiederkehrende Reports in feste Excel-Vorlagen füllen |
| `web-research-enrichment-pipeline` | Strukturierte Web-Recherche |
| `firecrawl-scraper` | Webseiten und Daten einsammeln |
| `market-sizing-analysis` | Marktgröße, Business-Cases |
| `sales-analytics` | Verkaufszahlen auswerten |
| `brand-guidelines` | Konsistente Außendarstellung |
| `postmortem-writing` | Saubere Nachbereitung von Projekten/Vorfällen |

**Commands** (mit `/` aufrufbar):

- `/optimize` und `/prompt-optimize` — helfen, eine gute Anweisung zu formulieren
- `/standup-notes` — Team-Updates generieren
- `/plan` — eine Aufgabe strukturiert planen

## Installation (macOS)

1. **Claude Code installieren** (eines von beiden):
   - **Empfohlen — Desktop-App:** https://claude.ai/download → einloggen, fertig.
   - Terminal/CLI: `npm install -g @anthropic-ai/claude-code` (benötigt Node ≥ 20).

2. **Dieses Bundle entpacken** (falls als `.tar.gz` erhalten):
   ```bash
   tar -xzf claude-office-setup.tar.gz
   cd boss-setup
   ```

3. **Installer ausführen:**
   ```bash
   chmod +x install.sh
   ./install.sh
   ```
   Das Skript kopiert Skills und Commands nach `~/.claude/` und sichert eine
   eventuell vorhandene Konfiguration vorher automatisch.

4. **Claude Code neu starten.**

## So arbeitest du gut damit

- **Konkret formulieren, Datei mitgeben.** Beispiel:
  *„Erstelle aus dieser Excel-Datei eine PowerPoint mit 5 Slides zu den
  Q1-Verkäufen."* Datei einfach in den Chat ziehen — der passende Skill
  startet automatisch.
- **Echte Dateien als Ergebnis.** Es entstehen echte `.docx` / `.xlsx` /
  `.pptx` / `.pdf`, die direkt weiterverwendet werden können.
- **Unsicher, wie fragen?** `/optimize` schlägt die passende Vorgehensweise
  und Skills vor.
- **E-Mail, Kalender, Notizen (optional):** Über MCP-Server lassen sich
  Outlook/Gmail, Notion und Google Drive anbinden. Das erfordert eine
  einmalige Anmeldung mit den *eigenen* Konten — nicht weitergegebene Logins
  verwenden.

## Eigene Konfiguration?

Wenn beim Installieren schon eine `~/.claude/settings.json` existierte, wurde
sie **nicht** überschrieben. Die saubere Vorlage liegt als `settings.json` in
diesem Ordner und kann bei Bedarf manuell übernommen werden.
