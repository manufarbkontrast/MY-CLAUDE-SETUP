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

---

## Chunked Render (bei wenig Disk-Space)

Remotion schreibt intermediate JPEG-Frames in `/tmp` bevor ffmpeg encodiert. Ein 10-min 1080p Video braucht dabei leicht **2-3 GB Temp-Space**. Bei weniger als 8-10 GB frei: chunked rendering verwenden.

### Strategie

1. Video in N gleich grosse Chunks aufteilen via `--frames=START-END`
2. Jeden Chunk einzeln rendern → `out/chunks/part-NN.mp4`
3. Mit ffmpeg concat-demuxer konkatenieren (stream copy, kein Re-Encode)
4. Original-Audio muxen wie gewohnt

Faustregel: **8 Chunks** sind ein guter Default. Jeder Chunk braucht ~`TOTAL_FRAMES/8 × ~150KB` Peak-Temp.

### Render-Script (`scripts/renderChunks.sh`)

```bash
#!/usr/bin/env bash
# Renders the video in chunks to keep peak temp-disk usage low,
# then concatenates with ffmpeg (stream copy, no re-encode).
set -euo pipefail

cd "$(dirname "$0")/.."

TOTAL=19540    # totalFrames from videoConfig
CHUNKS=8
CHUNK_SIZE=$(( (TOTAL + CHUNKS - 1) / CHUNKS ))

mkdir -p out/chunks
> out/chunks/concat.txt

for i in $(seq 0 $((CHUNKS - 1))); do
  START=$(( i * CHUNK_SIZE ))
  END=$(( START + CHUNK_SIZE - 1 ))
  if [ "$END" -ge "$TOTAL" ]; then
    END=$(( TOTAL - 1 ))
  fi
  OUT="out/chunks/part-$(printf '%02d' "$i").mp4"
  echo "=== Chunk $i: frames $START..$END -> $OUT ==="
  npx remotion render src/index.ts MainVideo "$OUT" \
    --codec h264 \
    --muted \
    --frames="$START-$END"
  # WICHTIG: relativer Pfad in concat.txt (ohne 'chunks/' prefix)
  # weil wir unten ins chunks-Verzeichnis cd-en
  echo "file 'part-$(printf '%02d' "$i").mp4'" >> out/chunks/concat.txt
done

echo "=== Concatenating ==="
# KRITISCH: ffmpeg concat-demuxer interpretiert Pfade RELATIV ZUR concat.txt,
# nicht zum cwd. Daher ins chunks-Verzeichnis cd-en.
(cd out/chunks && ffmpeg -y -f concat -safe 0 -i concat.txt -c copy ../video-only.mp4)
echo "Done: out/video-only.mp4"
```

### Wenn ein Chunk trotzdem ENOSPC wirft

Die letzten/groesseren Chunks kann man nochmal halbieren:

```bash
# Statt part-07.mp4 rendern, zwei Sub-Chunks
npx remotion render src/index.ts MainVideo out/chunks/part-07a.mp4 --codec h264 --muted --frames=17093-18316
npx remotion render src/index.ts MainVideo out/chunks/part-07b.mp4 --codec h264 --muted --frames=18317-19539

# concat.txt dann entsprechend erweitern
```

### Disk-Budget Cheatsheet

| Total-Frames | Chunks | Peak-Temp/Chunk | Gesamt frei noetig |
|-------------:|-------:|----------------:|-------------------:|
| ~5k          | 1      | ~0.8 GB         | ~2 GB              |
| ~10k         | 4      | ~0.4 GB         | ~1.5 GB            |
| ~20k         | 8      | ~0.4 GB         | ~2 GB + Output     |
| ~20k         | 5      | ~0.8 GB         | ~2.5 GB + Output   |
| ~30k         | 10     | ~0.5 GB         | ~3 GB + Output     |

Output-File selbst: ca. 80-90 MB pro Minute 1080p h264.

---

## Kritische Gotchas

### 1. Niemals Render-Output durch `| head` pipen

```bash
# FALSCH: head schliesst die Pipe nach 80 Zeilen → SIGPIPE killt Remotion
npx remotion render ... | tee /tmp/log | head -80

# RICHTIG: nohup + disown, Log in Datei
nohup npx remotion render ... > /tmp/render.log 2>&1 &
disown
```

### 2. ffmpeg concat-demuxer Pfade sind relativ zur `concat.txt`

```bash
# FALSCH: wenn concat.txt in out/chunks/ und ffmpeg aus cwd ausgefuehrt wird
cat > out/chunks/concat.txt <<EOF
file 'chunks/part-00.mp4'
EOF
ffmpeg -f concat -safe 0 -i out/chunks/concat.txt -c copy out/video-only.mp4
# → sucht 'out/chunks/chunks/part-00.mp4' (doppelter prefix)

# RICHTIG: entweder cd-en
(cd out/chunks && ffmpeg -f concat -safe 0 -i concat.txt -c copy ../video-only.mp4)
# oder absolute Pfade in concat.txt verwenden
```

### 3. `cp` vs `mv` bei fast vollem Disk

Bei wenig Disk-Space: der finale Output kann den Rest fuellen. Cleanup VOR dem Verschieben:

```bash
# FALSCH: cp dupliziert, kann ENOSPC werfen und truncated File hinterlassen
cp out/final.mp4 /target/final.mp4

# RICHTIG: zuerst aufraumen, dann mv (atomar, nur Rename innerhalb FS)
rm -rf out/chunks out/video-only.mp4
mv out/final.mp4 /target/final.mp4
```

`mv` innerhalb desselben Filesystems ist nur ein inode-rename — funktioniert auch bei 0 B free. Cross-FS `mv` wird zu copy+delete und kann dann wieder ENOSPC werfen.

### 4. Disk-Space vor Start pruefen

```bash
df -h /
# Wenn < 10 GB free bei 10-min 1080p → chunked rendering
# Wenn < 5 GB free → mindestens 8 chunks, ggf. 10-12
```
