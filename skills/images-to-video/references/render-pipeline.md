# Render-Pipeline: Remotion + ffmpeg

## Warum Audio extern muxen?

Remotion re-encodiert Audio als AAC. Das fuehrt zu:
- Wahrnehmbarer Tempo-Drift (selbst 0.01% = 0.06s auf 590s faellt auf)
- User berichtet "Audio klingt schneller"
- Technisch messbar: Output-Dauer weicht von Input ab

**Loesung**: Video stumm rendern, Original-Audio per ffmpeg muxen.

## Hauptvideo rendern

```bash
# 1. Stummes Video (Remotion)
npx remotion render MainComposition out/video-only.mp4 \
  --codec h264 \
  --muted

# 2. Original-Audio muxen (ffmpeg)
ffmpeg -y \
  -i out/video-only.mp4 \
  -i public/voiceover.mp3 \
  -c:v copy \
  -c:a aac -b:a 192k \
  -shortest \
  out/final.mp4

# 3. Verifizieren
ffprobe -v quiet -show_entries format=duration -of default=noprint_wrappers=1 out/final.mp4
ffprobe -v quiet -show_entries stream=codec_type,width,height,duration,r_frame_rate -of compact out/final.mp4
```

### ffmpeg-Flags erklaert

| Flag | Bedeutung |
|------|-----------|
| `-y` | Ueberschreibe Output ohne Nachfrage |
| `-i` | Input-Datei |
| `-c:v copy` | Video-Stream nicht re-encodieren (schnell, verlustfrei) |
| `-c:a aac -b:a 192k` | Audio zu AAC, 192kbps (einmaliges Encoding) |
| `-shortest` | Stoppt wenn kuerzester Stream endet |
| `-ss START -t DURATION` | Audio-Segment schneiden (vor -i = schneller Seek) |

## Shorts rendern (Batch-Script)

```bash
#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
AUDIO_SRC="$PROJECT_DIR/public/voiceover.mp3"
OUT_DIR="$PROJECT_DIR/out/shorts"

mkdir -p "$OUT_DIR"

# Format: CompositionId:AudioStartSeconds:AudioEndSeconds
declare -a SHORTS=(
  "Short1-Name:0.0:34.9"
  "Short2-Name:52.3:112.3"
  "Short3-Name:325.0:385.0"
)

for entry in "${SHORTS[@]}"; do
  IFS=':' read -r id start end <<< "$entry"
  duration=$(echo "$end - $start" | bc)

  echo "=== Rendering $id (${duration}s) ==="

  # 1. Remotion: stummes Video
  cd "$PROJECT_DIR"
  npx remotion render "$id" "$OUT_DIR/${id}-video.mp4" --codec h264 --muted

  # 2. ffmpeg: Audio-Segment schneiden + muxen
  ffmpeg -y \
    -i "$OUT_DIR/${id}-video.mp4" \
    -ss "$start" -t "$duration" -i "$AUDIO_SRC" \
    -c:v copy -c:a aac -b:a 192k -shortest \
    "$OUT_DIR/${id}.mp4"

  # 3. Intermediate aufraumen
  rm "$OUT_DIR/${id}-video.mp4"

  echo "=== $id fertig ==="
done

echo "Alle Shorts fertig in $OUT_DIR/"
ls -lh "$OUT_DIR"/*.mp4
```

## Verifikation

### Muss-Checks nach jedem Render

```bash
# Video-Eigenschaften
ffprobe -v quiet -show_entries stream=codec_type,width,height,duration,r_frame_rate -of compact output.mp4

# Erwartete Ausgabe (Hauptvideo):
# stream|codec_type=video|width=1920|height=1080|r_frame_rate=30/1|duration=590.400000|
# stream|codec_type=audio|r_frame_rate=0/0|duration=590.341111

# Erwartete Ausgabe (Short):
# stream|codec_type=video|width=1080|height=1920|r_frame_rate=30/1|duration=60.000000|
# stream|codec_type=audio|r_frame_rate=0/0|duration=60.000000
```

### Audio-Tempo pruefen

```bash
# Original-Audio-Dauer
ffprobe -v quiet -show_entries format=duration -of default=noprint_wrappers=1 public/voiceover.mp3

# Output-Audio-Dauer
ffprobe -v quiet -show_entries stream=duration -select_streams a -of default=noprint_wrappers=1 out/final.mp4

# Differenz sollte < 0.01s sein
```

## Troubleshooting

### "Audio klingt schneller"

1. Pruefen ob `<Audio>` Komponente noch in Remotion ist → ENTFERNEN
2. Pruefen ob `--muted` Flag beim Rendern gesetzt
3. Audio-Dauer vergleichen (Original vs Output)

### Remotion 404-Fehler beim Rendern

```
Error: Could not load voiceover.mp3 - 404
```
→ Assets sind Symlinks statt echte Dateien. `cp -r` statt `ln -s` verwenden.

### ffmpeg "No such file or directory"

→ Pfade mit Leerzeichen muessen in Anfuehrungszeichen stehen:
```bash
ffmpeg -i "out/video only.mp4" ...  # Richtig
ffmpeg -i out/video only.mp4 ...    # Falsch
```

### Render dauert sehr lang

- Hauptvideo (~590s, 17.700 Frames): ~5-10 Minuten
- Pro Short (~60s, 1.800 Frames): ~1-2 Minuten
- Tipp: `--concurrency` Flag fuer paralleles Rendern (Standard: auto)
