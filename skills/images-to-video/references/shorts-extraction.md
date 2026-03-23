# Shorts-Extraktion aus langem Video

## Uebersicht

YouTube Shorts (max 60s), Instagram Reels, TikTok-Videos aus bestehendem Remotion-Langvideo erstellen.

## Architektur

```
Bestehend:                    Neu (shorts/):
┌──────────────────┐          ┌──────────────────┐
│ generatedManifest│ ──────→  │ shortsConfig.ts   │ Segment-Definitionen
│ videoConfig.ts   │ ──────→  │ shortsTimingUtils  │ Frame-Verteilung
│ ImageScene.tsx   │ (Vorbild)│ CropPanImageScene  │ 9:16 Display
│ Root.tsx         │ ←──────  │ ShortComposition   │ Generic Comp
└──────────────────┘          └──────────────────┘
```

## Schritt 1: Segmente identifizieren

Kriterien fuer gute Shorts:
- **30-60 Sekunden** (YouTube-Limit: 60s)
- **Inhaltlich eigenstaendig** (ohne Kontext verstaendlich)
- **Starker Einstieg** (Hook in den ersten 3 Sekunden)
- **Visuell interessant** (abwechslungsreiche Bilder)

## Schritt 2: Short-Definitionen

```typescript
// src/shorts/shortsConfig.ts
export interface ShortDefinition {
  readonly id: string;              // Remotion Composition ID
  readonly title: string;           // Beschreibender Titel
  readonly phaseIndex: number;      // Welche Phase
  readonly imageStartIndex: number; // Erstes Bild (inclusive)
  readonly imageEndIndex: number;   // Letztes Bild (exclusive)
  readonly audioStartSeconds: number;
  readonly audioEndSeconds: number;
}

export const SHORTS_CONFIG = {
  width: 1080,
  height: 1920,
  fps: 30,
} as const;

export const SHORT_DEFINITIONS: readonly ShortDefinition[] = [
  {
    id: "Short1-TheHook",
    title: "The Hook",
    phaseIndex: 0,
    imageStartIndex: 0,
    imageEndIndex: 9,
    audioStartSeconds: 0.0,
    audioEndSeconds: 34.9,
  },
  // ... weitere Shorts
];
```

### Bild-Indices berechnen

```
Phase hat N Bilder ueber D Sekunden.
Short startet S Sekunden in die Phase und dauert L Sekunden.

imageStartIndex = floor(S / D * N)
imageEndIndex   = min(ceil((S + L) / D * N), N)
Bildanzahl      = imageEndIndex - imageStartIndex
```

## Schritt 3: Timing-Utils

```typescript
// src/shorts/shortsTimingUtils.ts
export interface ShortTimedImage {
  readonly path: string;
  readonly startFrame: number;
  readonly durationInFrames: number;
  readonly zoomDirection: "in" | "out";
  readonly isFirst: boolean;
  readonly isLast: boolean;
}

export function computeShortTotalFrames(definition: ShortDefinition): number {
  return Math.ceil(
    (definition.audioEndSeconds - definition.audioStartSeconds) * SHORTS_CONFIG.fps
  );
}

function distributeFramesEvenly(
  totalFrames: number, imageCount: number
): readonly number[] {
  const base = Math.floor(totalFrames / imageCount);
  const remainder = totalFrames - base * imageCount;
  return Array.from({ length: imageCount }, (_, i) =>
    i < remainder ? base + 1 : base
  );
}

export function computeShortTimeline(
  definition: ShortDefinition,
  phaseImages: readonly ImageEntry[]
): readonly ShortTimedImage[] {
  const selected = phaseImages.slice(
    definition.imageStartIndex, definition.imageEndIndex
  );
  const totalFrames = computeShortTotalFrames(definition);
  const durations = distributeFramesEvenly(totalFrames, selected.length);

  let offset = 0;
  return selected.map((img, index) => {
    const entry: ShortTimedImage = {
      path: img.path,
      startFrame: offset,
      durationInFrames: durations[index],
      zoomDirection: index % 2 === 0 ? "in" : "out",
      isFirst: index === 0,
      isLast: index === selected.length - 1,
    };
    offset += durations[index];
    return entry;
  });
}
```

## Schritt 4: Generic Composition

```typescript
// src/shorts/ShortComposition.tsx
export const ShortComposition: React.FC<{ definition: ShortDefinition }> = ({
  definition,
}) => {
  const phaseImages = PHASE_IMAGES[definition.phaseIndex];
  const timedImages = computeShortTimeline(definition, phaseImages);

  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      {timedImages.map((img, index) => {
        const overlapBefore = img.isFirst ? 0 : CROSSFADE_FRAMES;
        const overlapAfter = img.isLast ? 0 : CROSSFADE_FRAMES;
        const sequenceFrom = img.startFrame - overlapBefore;
        const sequenceDuration = img.durationInFrames + overlapBefore + overlapAfter;

        return (
          <Sequence key={index} from={sequenceFrom} durationInFrames={sequenceDuration}>
            <CropPanImageScene
              src={img.path}
              durationInFrames={sequenceDuration}
              zoomDirection={img.zoomDirection}
              isFirst={img.isFirst}
              isLast={img.isLast}
            />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
```

## Schritt 5: Registration in Root.tsx

```typescript
import { ShortComposition } from "./shorts/ShortComposition";
import { SHORT_DEFINITIONS, SHORTS_CONFIG } from "./shorts/shortsConfig";
import { computeShortTotalFrames } from "./shorts/shortsTimingUtils";

// Innerhalb RemotionRoot, nach der Haupt-Composition:
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

## Schritt 6: Render + Audio-Mux

Siehe `references/render-pipeline.md` fuer das vollstaendige Render-Script.

Kurzversion pro Short:
```bash
# 1. Stummes Video
npx remotion render "Short1-Name" out/shorts/Short1-video.mp4 --codec h264 --muted

# 2. Audio-Segment schneiden + muxen
ffmpeg -y \
  -i out/shorts/Short1-video.mp4 \
  -ss 0.0 -t 34.9 -i public/voiceover.mp3 \
  -c:v copy -c:a aac -b:a 192k -shortest \
  out/shorts/Short1.mp4
```

## Typische Dateigroessen

| Dauer | Aufloesung | Groesse |
|-------|-----------|---------|
| 35s   | 1080x1920 | ~30-40 MB |
| 60s   | 1080x1920 | ~50-70 MB |

YouTube Shorts Upload-Limit: 256 MB → kein Problem.
