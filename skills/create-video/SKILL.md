---
name: create-video
description: "Bilder + Skript (DOCX) + Voiceover → fertiges Video mit Whisper-Timing, Remotion-Render und ffmpeg-Audio-Mux."
version: 1.0.0
metadata:
  last_verified: 2026-03-10
  keywords: [remotion, video, voiceover, whisper, images, slideshow, ffmpeg, docx]
  production_tested: true
  related_skills: [youtube-timestamps, media-processing]
user_invocable: true
trigger: "/create-video"
---

# Create Video: Bilder + Skript + Voiceover → Video

Automatisierter 7-Schritt-Workflow: Liest Bilder aus Phase-Ordnern, parst ein DOCX-Skript, transkribiert das Voiceover mit Whisper (Wort-Level-Timestamps), und rendert ein fertiges Video mit Remotion + ffmpeg.

## Wann diesen Skill nutzen

- User hat **Bilder** (PNG) in `Phase_N`-Ordnern, ein **Voiceover** (MP3/M4A/WAV) und ein **DOCX-Skript** mit `[Scene N]`-Markern
- Ziel: Video mit exaktem Bild-zu-Audio-Timing, subtilen Ken-Burns-Zooms und Crossfades
- Das Remotion-Projekt unter `video-project/` existiert bereits

## Voraussetzungen

- Node.js >= 18
- ffmpeg + ffprobe
- Python 3 mit `openai-whisper` (`pip3 install openai-whisper`)
- npm packages (werden automatisch installiert): remotion@4, @remotion/cli@4, react@18, react-dom@18, typescript, tsx

## Quick Reference

```
1. VALIDIERUNG  → Eingaben pruefen, Tools verifizieren
2. AUDIO        → Dauer mit ffprobe messen
3. BILDER       → Phase-Ordner erkennen, normalisieren, in public/ kopieren
4. TIMING       → DOCX parsen + Whisper-Transkription + Szenen-Matching
5. DEPENDENCIES → npm install falls noetig
6. RENDER       → Remotion render --muted (stummes Video)
7. AUDIO-MUX    → ffmpeg: Original-Audio muxen (kein Re-Encoding)
```

## Verwendung

```bash
./video-project/scripts/create-video.sh \
  --images /pfad/zu/bildern \
  --audio  /pfad/zu/voiceover.mp3 \
  --script /pfad/zu/skript.docx \
  [--output /pfad/zu/output.mp4] \
  [--width 1920] [--height 1080] [--fps 30]
```

### Typische Ordnerstruktur der Eingabe

```
9.Video_Amazon Lie/
├── Final_Amazon Lie.mp3          ← Voiceover
├── Skript_Scene_Videoschnitt_9.docx  ← Skript mit [Scene N] Markern
├── Phase_0_Amazon Lie/           ← Bilder Phase 0
│   ├── scene-1-1772530817575.png
│   ├── scene-2-1772531033231.png
│   └── ...
├── Phase_1_Amazon Lie/           ← Bilder Phase 1
└── Phase_2_Amazon Lie/           ← etc.
```

### Bild-Namensschema

`scene-{N}-{TIMESTAMP}.png` wobei:
- `N` = Szenen-Nummer (1-basiert, 0 wird ignoriert/uebersprungen)
- `TIMESTAMP` = Unix-Timestamp der Erstellung (fuer Deduplizierung: hoechster gewinnt)

## Die 7 Schritte im Detail

### Schritt 1: Eingaben validieren

- Pflichtargumente: `--images`, `--audio`, `--script`
- Pruefen: Ordner/Dateien existieren
- Tools: `node`, `npm`, `ffmpeg`, `ffprobe`, `python3`, `whisper`
- Default-Output: `video-project/out/final.mp4`

### Schritt 2: Audio analysieren

```bash
ffprobe -v quiet -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 "voiceover.mp3"
```

### Schritt 3: Bilder kopieren + normalisieren

**KRITISCH: Phase-Ordnernamen normalisieren!**

Eingabe-Ordner wie `Phase_0_Amazon Lie` werden zu `Phase_0` normalisiert:

```bash
phase_prefix=$(echo "$phase_name" | grep -oE 'Phase_[0-9]+')
target_dir="$PROJECT_DIR/public/images/$phase_prefix"
```

Regeln:
- `scene-0-*.png` werden uebersprungen (Duplikate/Drafts)
- Nur `scene-N-*.png` mit N >= 1 werden kopiert
- Assets KOPIEREN, nicht verlinken (Remotion-Bundler folgt keinen Symlinks)

### Schritt 4: Whisper-Transkription + Szenen-Timing

Das Python-Skript `extract-timing.py` fuehrt 5 Teilschritte aus:

#### 4a. DOCX-Text extrahieren
Liest `word/document.xml` aus dem DOCX-ZIP, extrahiert allen Text.

#### 4b. Szenen parsen
Erkennt `[Scene N]`-Marker mit permissivem Regex:
```
\[\s*Scene\s*(\d+)     ← matched: [Scene1], [ Scene 3], [Scene7|], [ scene13
```
Ordnet Szenen der aktuellen `PHASE N`-Sektion zu.

#### 4c. Auto-Fix: Duplikate + Out-of-order
- Doppelte Szenen-Nummern: `[Scene28] [Scene28]` → Scene 28, Scene 29
- Out-of-order nach Reset: Scene 40 gefolgt von `[Scene 1]` → Scene 40, Scene 41

#### 4d. Whisper-Matching
- Whisper `base`-Modell transkribiert Audio mit Wort-Level-Timestamps
- Fuer jede Szene: ersten 2-3 Woerter des Skript-Texts im Transkript suchen
- Sequentielles Matching (word_index wird nur vorwaerts bewegt)
- Fallback: lineare Schaetzung basierend auf Scene-Position

#### 4e. Monotonie-Korrektur
Multi-Pass-Algorithmus stellt sicher, dass alle Timestamps streng aufsteigend sind.
Bei Verletzung: Neuer Timestamp = Mittelpunkt zwischen Vorgaenger und naechstem gueltigen Wert.

#### Ausgabe: `src/videoConfig.ts`
Auto-generierte TypeScript-Datei mit:
- `VIDEO_CONFIG` (width, height, fps, audioDurationSeconds)
- `WHISPER_SCENES[]` (startSeconds, folder, file pro Szene)
- `computeTimeline()` Funktion (berechnet startFrame, durationInFrames)
- `CROSSFADE_FRAMES = 10`, `ZOOM_SCALE_MIN = 1.0`, `ZOOM_SCALE_MAX = 1.05`

### Schritt 5: npm Dependencies

```bash
npm i remotion@4 @remotion/cli@4 react@18 react-dom@18 --legacy-peer-deps
npm i -D typescript @types/react tsx --legacy-peer-deps
```

Wird uebersprungen falls `node_modules/remotion/` existiert.

### Schritt 6: Video rendern (stumm)

```bash
npx remotion render MainVideo out/video-only.mp4 --codec h264 --muted
```

**WICHTIG**: Immer `--muted`! Remotion re-encodiert Audio als AAC, was zu wahrnehmbaren Tempo-Aenderungen fuehrt.

### Schritt 7: Audio muxen

```bash
ffmpeg -y \
  -i out/video-only.mp4 \
  -i public/voiceover.mp3 \
  -c:v copy -c:a aac -b:a 192k -shortest \
  out/final.mp4
```

`-c:v copy` = kein Video-Re-Encoding. Original-Audio wird als AAC gemuxed.

## Remotion-Komponenten

### Root.tsx
Registriert `MainVideo` Composition mit korrekter Framezahl aus `TOTAL_FRAMES`.

### MainVideo.tsx
Iteriert ueber `computeTimeline()` und rendert fuer jede Szene eine `<Sequence>` mit `<ImageScene>`.

### ImageScene.tsx
- `object-fit: cover` → Bild fuellt Frame komplett
- **Ken-Burns**: Subtiler Zoom 1.0x → 1.05x (alternierend in/out per Szene)
- **Crossfade**: 10 Frames (0.33s bei 30fps) Ueberblendung zwischen Szenen
- Fade-In fuer nicht-erste, Fade-Out fuer nicht-letzte Szene

## Bekannte Probleme + Loesungen

| Problem | Loesung |
|---------|---------|
| Dateinamen mit Leerzeichen (`scene-10 -...`) | Vor Ausfuehrung umbenennen: `mv "scene-10 -..." "scene-10-..."` |
| Phase-Ordner mit Suffix (`Phase_0_Name`) | create-video.sh normalisiert automatisch zu `Phase_0` |
| Remotion-Cache liefert altes Video | `rm -rf node_modules/.cache .remotion out/video-only.mp4` |
| `| head/tail` killt Render (SIGPIPE) | Pipe-Filtering nur mit `|| true` oder komplett weglassen |
| Whisper-Timestamps nicht monoton | `enforce_monotonic_timestamps()` korrigiert automatisch |
| Szenen-Duplikate im DOCX | `fix_duplicate_scene_numbers()` korrigiert automatisch |
| DOCX hat `[Scene7|]` oder `[ scene13` | Permissiver Regex matched alle Varianten |

## Verifikation nach Abschluss

```bash
ffprobe -v quiet -show_entries stream=codec_type,width,height,duration \
  -of compact out/final.mp4
```

Checkliste:
- [ ] Korrekte Aufloesung (z.B. 1920x1080)
- [ ] Audio-Dauer ≈ Original-Voiceover-Dauer (Differenz < 0.1s)
- [ ] Video-Dauer = Audio-Dauer (`-shortest` Flag)
- [ ] Bilder fuellen Frame komplett (kein Schwarz/Weiss an Raendern)
- [ ] Ken-Burns-Zoom sichtbar aber nicht ablenkend
- [ ] Crossfades zwischen Szenen (kein harter Schnitt)

## Projektstruktur

```
video-project/
├── package.json
├── remotion.config.ts
├── tsconfig.json
├── scripts/
│   ├── create-video.sh        ← Haupt-Workflow (Bash)
│   └── extract-timing.py      ← DOCX + Whisper → videoConfig.ts (Python)
├── src/
│   ├── index.ts               ← Remotion Entry Point
│   ├── Root.tsx                ← Composition Registration
│   ├── MainVideo.tsx           ← Szenen-Sequenz
│   ├── ImageScene.tsx          ← Einzelne Szene mit Zoom + Crossfade
│   └── videoConfig.ts          ← AUTO-GENERIERT: Timing-Daten
├── public/
│   ├── images/Phase_N/         ← Kopierte + normalisierte Bilder
│   └── voiceover.mp3           ← Kopiertes Voiceover
└── out/
    ├── video-only.mp4          ← Stummes Remotion-Video
    └── final.mp4               ← Fertiges Video mit Audio
```
