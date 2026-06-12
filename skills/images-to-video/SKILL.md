---
name: images-to-video
description: "Bilder + Skript + Voiceover → Video mit Remotion. Inkl. Whisper-Alignment + Shorts."
version: 1.1.0
metadata:
  last_verified: 2026-04-08
  keywords: [remotion, video, voiceover, images, slideshow, shorts, youtube, ffmpeg, whisper, alignment]
  production_tested: true
  related_skills: [media-processing]
---

# Images-to-Video: Bilder + Skript + Voiceover → Video

Erstellt aus einer Sammlung von Bildern, einem Skript mit Scene-Markern und einem Voiceover ein fertiges Video mit Remotion. Nutzt Whisper fuer Audio-exaktes Scene-Alignment. Optional: YouTube Shorts im 9:16-Format.

## Wann diesen Skill nutzen

- User hat **Bilder** (PNG/JPG), ein **Voiceover** (MP3/WAV) und optional ein **Skript** mit Szene-Markern
- Ziel: Zusammengefuegtes Video wo Szenen-Wechsel exakt zu den gesprochenen Saetzen passen
- Optional: Vertikale Shorts (YouTube/Instagram/TikTok) aus dem Ergebnis

## Quick Reference: Workflow in 8 Schritten

```
1. ANALYSE        → Bilder zaehlen, Audio-Laenge messen, Skript lesen, Disk-Space pruefen
2. PROJEKT        → Remotion-Projekt aufsetzen, Assets kopieren
3. MANIFEST       → Bild-Manifest generieren (Dedup + scene-0-Filter)
4. TRANSKRIPTION  → Voiceover mit Whisper transkribieren (word-level timestamps)
5. ALIGNMENT      → Skript-Scene-Texte per Whisper-Words zu exakten Startzeiten mappen
6. KOMPONENTEN    → ImageScene mit Zoom + Crossfade erstellen
7. RENDERN        → Video stumm rendern (chunked bei wenig Disk-Space)
8. AUDIO-MUX      → Original-Audio per ffmpeg muxen (kein Re-Encoding)
```

Optional: `9. SHORTS` → Segmente definieren, 9:16-Compositions, Batch-Render

---

## Schritt 1: Analyse

Vor dem Start IMMER pruefen:

```bash
# Audio-Laenge und Format
ffprobe -v quiet -show_entries format=duration,bit_rate -show_entries stream=sample_rate,channels "voiceover.mp3"

# Bild-Dimensionen (erstes Bild)
ffprobe -v quiet -show_entries stream=width,height "images/Phase_0/scene-1.png"

# Bilder zaehlen inkl. pro Phase
find images/ -name "*.png" -o -name "*.jpg" | wc -l
for p in Phase_*; do echo "$p: $(ls $p | wc -l)"; done

# Bild-Namensschema erkennen
ls images/Phase_0/ | head -20

# KRITISCH: Disk-Space pruefen!
df -h /
```

**Wichtige Werte notieren:**
- Audio-Dauer (exakt, in Sekunden)
- Bild-Dimensionen (Breite x Hoehe)
- Anzahl Bilder (gesamt und pro Phase)
- Namensschema (z.B. `scene-N-TIMESTAMP.png`)
- **Freier Disk-Space** — fuer ein 10-Min-1080p-Video brauchst du mindestens **8-10 GB**, besser 15+ GB. Bei weniger: chunked rendering verwenden.

## Schritt 2: Projekt aufsetzen

> Lade Reference: `references/project-setup.md` fuer vollstaendiges Setup

```bash
mkdir video-project && cd video-project
npm init -y
npm i remotion @remotion/cli react react-dom
npm i -D typescript @types/react tsx
```

**KRITISCH: Assets KOPIEREN, nicht verlinken!**
Remotion-Bundler kann Symlinks nicht folgen.

```bash
mkdir -p public/images
cp -r /pfad/zu/bildern/* public/images/
cp /pfad/zu/voiceover.mp3 public/voiceover.mp3
```

## Schritt 3: Manifest generieren

> Lade Reference: `references/manifest-and-timing.md` fuer Details

Manifest-Generator (`scripts/generateManifest.ts`):
- Liest alle Bilder aus Phase-Ordnern
- Parsed Dateinamen → Scene-Nummer + Timestamp
- **Dedupliziert**: Bei doppelten Scene-Nummern nur letztes Bild behalten
- **FILTERT `scene-0-*.png`** — das sind typischerweise Draft/Intro-Bilder die nicht im finalen Skript vorkommen. IMMER pruefen und ausfiltern wenn das Skript bei `[scene 1]` beginnt.
- Generiert typsichere TypeScript-Datei

```bash
npx tsx scripts/generateManifest.ts
# → src/generatedManifest.ts (automatisch generiert)
```

**Verifikation:** Skript-Scene-Count pro Phase == Manifest-Scene-Count pro Phase (+/- bei Skript-Typos).

## Schritt 4: Transkription (Whisper)

> Lade Reference: `references/whisper-alignment.md` fuer Details

**WARUM:** Proportionales Skalieren von Skript-Phase-Dauern (alter Ansatz) fuehrt zu Bildern die NICHT zum gesprochenen Text passen. Whisper gibt word-level timestamps aus dem tatsaechlichen Audio — damit kann jede Scene exakt dort starten wo ihr Text gesprochen wird.

```bash
# Einmalig Whisper installieren (falls noetig)
pip3 install openai-whisper

# Transkription mit word-timestamps als JSON
python3 -m whisper public/voiceover.mp3 \
  --model base \
  --language en \
  --word_timestamps True \
  --output_format json \
  --output_dir transcription
```

Modell-Wahl: `base` reicht meist (dauert ~2 min fuer 10min Audio auf CPU). Fuer kritische Deutsch-/Mischtexte `small` oder `medium` verwenden.

## Schritt 5: Script → Scene-Alignment

> Lade Reference: `references/whisper-alignment.md`

Python-Script `scripts/extractScript.py`:

1. Parsed Skript (z.B. DOCX) und extrahiert **Text-Bloecke pro Scene-Marker** in Reihenfolge (ignoriere die Scene-Nummern — sie haben oft Typos wie doppeltes `[scene 10]` oder fehlendes `[scene 5]`).
2. Laedt Whisper-JSON, flattend alle Words mit `start`-Timestamp.
3. **Sequentielle Anker-Suche**: Fuer jeden Scene-Textblock findet die erste Position im Whisper-Wortstrom ab dem aktuellen Cursor wo die ersten ~6 Woerter uebereinstimmen (normalisiert: lowercase, keine Punctuation). Best-Match-Scoring mit leichter Cursor-Distanz-Strafe.
4. **Mismatch-Handling**: Wenn Skript-Bloecke < Image-Scenes → teile die laengsten Bloecke in der Mitte (nach Word-Count) bis Counts stimmen. Umgekehrt: kuerzen.
5. Output: `src/sceneTimings.json` mit `[{phaseIndex, sceneIndex, startTime, preview}]` pro Scene.

**Verifikation:** Monotonie pruefen (jede startTime >= vorherige). Sample-Output ansehen: passt scene-0 bei `@ 0.00s` zum ersten gesprochenen Satz?

## Schritt 6: Komponenten erstellen

> Lade Reference: `references/components.md` fuer alle Varianten

**ImageScene** (Landscape 16:9):
- `object-fit: cover` → Bild fuellt Frame immer komplett
- Subtiler Zoom: 1.0 → 1.05 (alternierend in/out)
- Crossfade: 10 Frames (0.33s) Ueberlappung zwischen Bildern

**`timing.ts`** liest `sceneTimings.json` und baut:
- `startFrame = round(startTime × FPS)` pro Scene
- `durationFrames = naechster.startFrame - aktueller.startFrame` (letzter bis Audio-Ende)
- KEIN proportionales Verteilen mehr — exakte Whisper-Zeiten nutzen

**Fuer vertikale Shorts** gibt es 4 Display-Modi (siehe `references/components.md`).

## Schritt 7: Rendern

> Lade Reference: `references/render-pipeline.md` fuer Details + Chunked-Strategie

**Standard-Render (wenn 10+ GB Disk frei):**
```bash
npx remotion render src/index.ts MainVideo out/video-only.mp4 --codec h264 --muted
```

**Chunked-Render (wenn < 10 GB Disk frei):**
> KRITISCH: Remotion schreibt ~2-3 GB intermediate JPEG-Frames ins Temp-Dir bevor encodiert wird. Bei 10-Min-1080p-Videos reicht oft 5 GB free nicht aus.

```bash
# 8 Chunks sind ein guter Default — jeder braucht ~400 MB Peak-Temp
bash scripts/renderChunks.sh
```

Das Script rendert in Chunks via `--frames=START-END`, konkateniert mit ffmpeg `-f concat -c copy` (stream copy, kein Re-Encode).

**NIEMALS Render-Output durch `| head` oder `| tee | head` pipen!** Wenn `head` die Pipe schliesst, killt SIGPIPE die gesamte Render-Pipeline. Verwende `nohup cmd > /tmp/log 2>&1 &; disown`.

## Schritt 8: Audio-Mux

**WICHTIG: Video IMMER stumm rendern, Audio extern muxen!**

Remotion re-encodiert Audio als AAC, was zu wahrnehmbaren Tempo-Aenderungen fuehrt (selbst 0.01% faellt auf). Loesung:

```bash
ffmpeg -y \
  -i out/video-only.mp4 \
  -i public/voiceover.mp3 \
  -c:v copy -c:a aac -b:a 192k -shortest \
  out/final.mp4
```

**Cleanup bei wenig Disk:** Vor dem `mv out/final.mp4 <target>` ALLES andere (chunks, video-only.mp4) loeschen, sonst fuellt der finale Output den Rest. `mv` innerhalb desselben Filesystems ist atomar (nur Rename, kein Copy) — funktioniert auch bei vollem Disk. `cp` bricht ab und hinterlaesst truncated File.

## Schritt 9: Shorts (Optional)

> Lade Reference: `references/shorts-extraction.md` fuer vollstaendigen Workflow

Kurz-Zusammenfassung:
1. Beste 3-5 Segmente identifizieren (30-60s, inhaltlich eigenstaendig)
2. `ShortDefinition` pro Segment (Phase, Bild-Indices, Audio-Start/Ende)
3. Separate Compositions in Root.tsx registrieren (1080x1920)
4. Render-Script: Remotion render + ffmpeg Audio-Schnitt + Mux

---

## Wann References laden

| Reference | Laden wenn... |
|-----------|--------------|
| `references/project-setup.md` | Neues Projekt von Null aufsetzen |
| `references/manifest-and-timing.md` | Bild-Manifest erstellen, scene-0 filtern, Manifest debuggen |
| `references/whisper-alignment.md` | **Transkription + Scene-Alignment** (Schritte 4+5) |
| `references/components.md` | ImageScene-Komponenten erstellen oder anpassen |
| `references/render-pipeline.md` | Render-Probleme, Chunked-Render, Audio-Sync-Issues, Disk-Space |
| `references/shorts-extraction.md` | Shorts/Reels/TikTok aus langem Video erstellen |

---

## Checkliste vor Abgabe

- [ ] `ffprobe` zeigt korrekte Aufloesung und FPS
- [ ] Audio-Dauer im Output ≈ Original-Audio-Dauer (Differenz < 0.01s)
- [ ] Kein Audio-Stream im Remotion-Output (erst nach ffmpeg-Mux)
- [ ] Bilder fuellen Frame komplett (kein Weiss/Leere Flaechen)
- [ ] Subtile Zoom-Effekte sichtbar (nicht zu stark)
- [ ] Crossfades zwischen Bildern (kein harter Schnitt)
- [ ] Szenen-Wechsel passen exakt zum gesprochenen Text (spot-check bei 3-5 Stichproben)
- [ ] `scene-0-*` Dateien NICHT im Video (wenn Skript bei scene 1 beginnt)
- [ ] `sceneTimings.json` ist monoton steigend

## Typische Fehler vermeiden

1. **Symlinks statt Kopien** → Remotion-Bundler 404-Fehler. IMMER `cp -r`.
2. **Audio in Remotion** → Tempo-Drift. IMMER extern per ffmpeg muxen.
3. **Proportionales Skalieren statt Whisper** → Bilder passen nicht zum Text. **IMMER Whisper-Alignment nutzen wenn ein Skript mit Scene-Markern vorhanden ist.**
4. **scene-0-Dateien nicht gefiltert** → Falsche Intro-Bilder im Video. Pruefen ob Skript bei scene 1 oder 0 beginnt, entsprechend filtern.
5. **Skript-Scene-Nummern vertrauen** → Skripte enthalten oft Typos (doppeltes `[scene 10]`, fehlendes `[scene 5]`). Bloecke in REIHENFOLGE parsen, Nummern ignorieren, per Split/Merge an Image-Count anpassen.
6. **Duplikate nicht entfernt** → Zu viele Bilder, zu schneller Schnitt. Deduplizierung im Manifest (keep latest timestamp).
7. **Ken-Burns zu stark** → Ablenkend. Max 1.05x Zoom, nicht mehr.
8. **Render pipe durch `| head`** → SIGPIPE killt die Pipeline. Nutze `nohup cmd > log 2>&1 &; disown`.
9. **Render bei wenig Disk ohne Chunking** → ENOSPC auf 68% des Renders. Chunked-Render oder 10+ GB freihalten.
10. **`cp` statt `mv` beim Final-Output auf vollem Disk** → Truncated File. `mv` innerhalb desselben FS ist atomar.
11. **ffmpeg concat.txt Pfade** → Paths sind relativ zur concat.txt Location, NICHT zum cwd. Entweder `cd` ins Chunk-Verzeichnis, oder absolute Pfade verwenden.
