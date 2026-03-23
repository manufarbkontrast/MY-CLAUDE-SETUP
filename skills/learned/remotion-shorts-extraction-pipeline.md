# Remotion: Shorts aus langem Video extrahieren

**Extracted:** 2026-02-27
**Context:** YouTube Shorts / Reels / TikTok aus bestehendem Remotion-Langvideo erstellen

## Problem

Ein fertiges Remotion-Video (z.B. 10min) soll in mehrere kurze Clips (30-60s) aufgeteilt werden, jeweils mit dem passenden Audio-Segment. Einfaches Schneiden per ffmpeg verliert die Remotion-Effekte (Zoom, Crossfade) und erlaubt keine Format-Aenderung (z.B. 16:9 → 9:16).

## Solution

Architektur: Separate Remotion-Compositions pro Short + Shell-Script fuer Render+Mux Pipeline.

### 1. Short-Definitionen (shortsConfig.ts)

```typescript
export interface ShortDefinition {
  readonly id: string;           // Remotion Composition ID
  readonly title: string;
  readonly phaseIndex: number;   // Welche Phase/Abschnitt
  readonly imageStartIndex: number;
  readonly imageEndIndex: number; // exclusive
  readonly audioStartSeconds: number;
  readonly audioEndSeconds: number;
}

export const SHORTS_CONFIG = {
  width: 1080,
  height: 1920,
  fps: 30,
} as const;

export const SHORT_DEFINITIONS: readonly ShortDefinition[] = [
  { id: "Short1-Name", phaseIndex: 0, imageStartIndex: 0, imageEndIndex: 9,
    audioStartSeconds: 0.0, audioEndSeconds: 34.9, title: "..." },
  // ... weitere Shorts
];
```

### 2. Generic Short-Composition (ShortComposition.tsx)

```typescript
export const ShortComposition: React.FC<{ definition: ShortDefinition }> = ({ definition }) => {
  const images = PHASE_IMAGES[definition.phaseIndex]
    .slice(definition.imageStartIndex, definition.imageEndIndex);
  const totalFrames = Math.ceil(
    (definition.audioEndSeconds - definition.audioStartSeconds) * SHORTS_CONFIG.fps
  );
  // Frames gleichmaessig verteilen, dann in Sequences rendern
};
```

### 3. Root.tsx - Dynamische Registration

```tsx
{SHORT_DEFINITIONS.map((def) => (
  <Composition
    key={def.id}
    id={def.id}
    component={() => <ShortComposition definition={def} />}
    durationInFrames={computeShortTotalFrames(def)}
    fps={SHORTS_CONFIG.fps}
    width={SHORTS_CONFIG.width}
    height={SHORTS_CONFIG.height}
  />
))}
```

### 4. Render-Pipeline (renderShorts.sh)

```bash
#!/bin/bash
set -euo pipefail
AUDIO_SRC="public/voiceover.mp3"
OUT_DIR="out/shorts"
mkdir -p "$OUT_DIR"

declare -a SHORTS=("Short1-Name:0.0:34.9" "Short2-Name:52.3:112.3")

for entry in "${SHORTS[@]}"; do
  IFS=':' read -r id start end <<< "$entry"
  duration=$(echo "$end - $start" | bc)

  # 1. Remotion: stummes Video
  npx remotion render "$id" "$OUT_DIR/${id}-video.mp4" --codec h264 --muted

  # 2. ffmpeg: Audio-Segment schneiden + muxen
  ffmpeg -y \
    -i "$OUT_DIR/${id}-video.mp4" \
    -ss "$start" -t "$duration" -i "$AUDIO_SRC" \
    -c:v copy -c:a aac -b:a 192k -shortest \
    "$OUT_DIR/${id}.mp4"

  rm "$OUT_DIR/${id}-video.mp4"
done
```

## Bildanzahl pro Short berechnen

Formel: Wenn Phase N Bilder hat ueber D Sekunden, und der Short S Sekunden lang ist:
- Bilder im Short ≈ ceil(S / D * N)
- Start-Index = floor(offset_in_phase / D * N)

## When to Use

- YouTube Shorts aus langem Remotion-Video
- Content-Repurposing (Lang → Kurz)
- Format-Wechsel bei Extraktion (16:9 → 9:16)
- Batch-Rendering mehrerer Clips aus einer Quelle
