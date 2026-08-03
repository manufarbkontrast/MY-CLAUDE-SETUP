---
description: "Produziere ein komplettes YouTube-Skript aus einem Referenz-Video. Input: YouTube-URL. Output: 3-Tab Produktionsdokument (Translation DE|EN, VO-Script mit Mood-Tags, Editor EN)."
---

# YouTube Video-Produktion

Du erhaeltst eine YouTube-URL als Referenz-Video. Erstelle daraus ein KOMPLETT NEUES, EIGENSTAENDIGES deutsches YouTube-Skript mit 3-Tab Produktionsdokument.

## Argumente
$ARGUMENTS = die YouTube-URL des Referenz-Videos

## Workflow

### Schritt 1: Audio herunterladen + Whisper-Transkription
```bash
cd "/Users/manuwolfram/Downloads/Youtube Scraper"
mkdir -p transcripts

# Video-ID extrahieren
VIDEO_ID=$(echo "$ARGUMENTS" | grep -oP '(?<=v=)[^&]+' || echo "$ARGUMENTS" | grep -oP '[^/]+$')

# Metadaten holen
.venv/bin/yt-dlp --print title --print channel --print duration_string --skip-download "$ARGUMENTS"

# Audio als WAV herunterladen (16kHz mono, optimal fuer Whisper)
.venv/bin/yt-dlp -x --audio-format wav --postprocessor-args "-ar 16000 -ac 1" -o "transcripts/${VIDEO_ID}.%(ext)s" "$ARGUMENTS"

# Whisper-Transkription (medium Modell fuer gute Balance aus Qualitaet und Speed)
/Library/Frameworks/Python.framework/Versions/3.13/bin/whisper "transcripts/${VIDEO_ID}.wav" \
  --model medium \
  --language en \
  --output_format txt \
  --output_dir transcripts/ \
  --task transcribe
```

Das erzeugt `transcripts/<VIDEO_ID>.txt` mit hochwertigem Transkript.

**Warum Whisper statt YouTube-Untertitel:**
- Deutlich hoehere Genauigkeit (keine Auto-Caption-Fehler)
- Korrekte Satzzeichen und Grossschreibung
- Funktioniert auch wenn das Video keine Untertitel hat
- Bessere Erkennung von Fachbegriffen und Artnamen

**Fallback:** Falls Whisper fehlschlaegt (z.B. zu langer Audio), nutze YouTube-Auto-Captions:
```bash
.venv/bin/yt-dlp --write-auto-sub --sub-lang en --sub-format vtt --skip-download -o "transcripts/${VIDEO_ID}" "$ARGUMENTS"
```
Dann VTT parsen: Timestamps entfernen, [Music]/[Applause] raus, Plaintext erstellen.

### Schritt 2: Archive.org Grounding
Suche auf Archive.org nach dem Thema:
`https://archive.org/advancedsearch.php?q=<thema>&fl[]=identifier&fl[]=title&fl[]=creator&fl[]=year&sort[]=downloads+desc&rows=15&output=json`

Relevante Treffer lesen via: `https://archive.org/stream/<identifier>/<identifier>_djvu.txt`

Extrahiere: konkrete Fakten, Masse, Fundorte, Jahreszahlen, Zitate.

### Schritt 3: Neues Skript schreiben
Komplett NEUES deutsches Skript (~2.000 Woerter, 10-12 Min). Das Transkript dient NUR als Themen-Verstaendnis — NICHT umschreiben/uebersetzen.

**Strikte Regeln:**
- Hook: Max 50 Woerter, filmischer Einstieg (Szene/Bild/Behauptung)
- KEINE Begruessung, KEINE CTAs, KEINE Clickbait-Floskeln
- Du-Form durchgehend
- Jede Zahl mit greifbarem Alltagsvergleich
- Spannung durch "Doch/Aber"-Eskalation
- Kurze Fragment-Saetze nach langen Erklaerungen
- Fakten in Narration eingebettet, nie als Aufzaehlung
- Archive.org-Quellen natuerlich einweben
- Artnamen fett markiert
- Ende: Rueckbezug auf Kernthese mit leichter Drehung
- Keine Editor-Anweisungen im Text

### Schritt 4: Produktionsdokument erstellen
HTML-Datei nach `/Users/manuwolfram/Downloads/Youtube Scraper/output/<slug>-production.html`

**3 Sektionen mit page-break-before:**

**Sektion 1 — Translation:**
- Header: "Remodeling Video: [URL]" + "Titel: [Titel]"
- Zweispaltige Tabelle: DE links, EN rechts
- Artnamen mit `<strong>` fett
- Ein Absatz pro Tabellenzeile

**Sektion 2 — VO-Script 11Labs:**
- Deutsches Skript mit Mood-Tags: [dramatic], [calm expert], [intense], [slow deliberate], [building tension], [matter-of-fact], [reflective], [curious], [ominous], [grim], [quiet finality], [final statement], etc.
- Werbeumbrueche mit horizontaler Linie

**Sektion 3 — Editor (EN):**
- Englische Uebersetzung in einzelnen Boxen mit Rahmen
- Eine Box = eine Szene, KEIN Regie-Text, nur reiner Sprechtext

**HTML-Styling:** Weiss, schwarz, A4, system sans-serif 11pt, bordered table cells, bordered editor boxes, print-friendly.

### Schritt 5: Aufraeumen + Datei oeffnen
```bash
# Audio-Datei loeschen (spart Speicher)
rm -f "transcripts/${VIDEO_ID}.wav"

open "/Users/manuwolfram/Downloads/Youtube Scraper/output/<slug>-production.html"
```

Melde: Titel, Wortanzahl, geschaetzte Sprechzeit, Dateiname.
