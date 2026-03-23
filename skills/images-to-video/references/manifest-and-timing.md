# Manifest-Generator + Timing-Berechnung

## Types (src/types.ts)

```typescript
export interface PhaseDefinition {
  readonly id: number;
  readonly name: string;
  readonly folder: string;
  readonly approximateDurationSeconds: number;
}

export interface ImageEntry {
  readonly path: string;
  readonly phaseIndex: number;
  readonly sceneNumber: number;
  readonly timestamp: number;
}

export interface TimedImageEntry extends ImageEntry {
  readonly startFrame: number;
  readonly durationInFrames: number;
  readonly zoomDirection: "in" | "out";
}

export interface PhaseTimingResult {
  readonly phaseIndex: number;
  readonly startFrame: number;
  readonly durationInFrames: number;
  readonly images: readonly TimedImageEntry[];
}
```

## Manifest-Generator (scripts/generateManifest.ts)

Generiert `src/generatedManifest.ts` aus den Bildern in `public/images/`.

### Dateinamen-Schema

Erwartet: `scene-{SCENE_NUMBER}-{TIMESTAMP}.png`

Beispiele:
- `scene-1-1770888510392.png` → Scene 1, Timestamp 1770888510392
- `scene-0-1770888412345.png` → Scene 0, Timestamp 1770888412345

### Deduplizierung

Bei mehreren Bildern mit gleicher Scene-Nummer:
→ Nur das mit dem hoechsten Timestamp behalten (= aktuellste Version)

```typescript
function deduplicateBySceneNumber(
  images: readonly ParsedImage[]
): readonly ParsedImage[] {
  const byScene = new Map<number, ParsedImage>();
  for (const img of images) {
    const existing = byScene.get(img.sceneNumber);
    if (!existing || img.timestamp > existing.timestamp) {
      byScene.set(img.sceneNumber, img);
    }
  }
  return [...byScene.values()].sort((a, b) => a.sceneNumber - b.sceneNumber);
}
```

### Vollstaendiger Generator

```typescript
import * as fs from "node:fs";
import * as path from "node:path";

interface ParsedImage {
  readonly filename: string;
  readonly folder: string;
  readonly phaseIndex: number;
  readonly sceneNumber: number;
  readonly timestamp: number;
}

// Anpassen an Projektstruktur:
const PHASE_FOLDERS = ["Phase_0", "Phase_1", "Phase_2" /* ... */];
const PUBLIC_IMAGES_DIR = path.resolve(__dirname, "../public/images");
const OUTPUT_FILE = path.resolve(__dirname, "../src/generatedManifest.ts");

function parseFilename(
  filename: string, folder: string, phaseIndex: number
): ParsedImage | null {
  const match = filename.match(/^scene-(\d+)-(\d+)\.png$/);
  if (!match) return null;
  return {
    filename, folder, phaseIndex,
    sceneNumber: parseInt(match[1], 10),
    timestamp: parseInt(match[2], 10),
  };
}

function buildManifest(): readonly (readonly ParsedImage[])[] {
  return PHASE_FOLDERS.map((folder, phaseIndex) => {
    const dirPath = path.join(PUBLIC_IMAGES_DIR, folder);
    const files = fs.readdirSync(dirPath).filter((f) => f.endsWith(".png"));
    const parsed = files
      .map((f) => parseFilename(f, folder, phaseIndex))
      .filter((p): p is ParsedImage => p !== null);
    const sorted = [...parsed].sort((a, b) =>
      a.sceneNumber !== b.sceneNumber
        ? a.sceneNumber - b.sceneNumber
        : a.timestamp - b.timestamp
    );
    return deduplicateBySceneNumber(sorted);
  });
}

// ... generateTypeScript() + writeFile
```

## Video-Config (src/videoConfig.ts)

```typescript
import type { PhaseDefinition } from "./types";

export const VIDEO_CONFIG = {
  width: 1920,
  height: 1080,
  fps: 30,
  audioDurationSeconds: 590.341111, // ← exakter Wert von ffprobe
} as const;

export const TOTAL_FRAMES = Math.ceil(
  VIDEO_CONFIG.audioDurationSeconds * VIDEO_CONFIG.fps
);

export const CROSSFADE_FRAMES = 10;   // 0.33s bei 30fps
export const ZOOM_SCALE_MIN = 1.0;
export const ZOOM_SCALE_MAX = 1.05;

// Phasen-Definitionen mit skalierten Dauern
export const PHASE_DEFINITIONS: readonly PhaseDefinition[] = [
  { id: 0, name: "Phase 0", folder: "Phase_0", approximateDurationSeconds: 34.9 },
  // ... weitere Phasen
];
```

### Timestamp-Skalierung

Wenn Skript fuer andere Dauer geplant war als das tatsaechliche Audio:

```
Faktor = Audio-Dauer / Skript-geplante-Dauer
Skalierte Dauer = Original-Dauer × Faktor
```

## Timing-Utils (src/timingUtils.ts)

Verteilt Frames proportional auf Phasen und gleichmaessig auf Bilder.

```typescript
import { TOTAL_FRAMES, PHASE_DEFINITIONS } from "./videoConfig";
import type { ImageEntry, TimedImageEntry, PhaseTimingResult } from "./types";

function computePhaseFrames(): readonly number[] {
  const totalSeconds = PHASE_DEFINITIONS.reduce(
    (sum, p) => sum + p.approximateDurationSeconds, 0
  );
  let allocated = 0;
  return PHASE_DEFINITIONS.map((phase, i) => {
    const isLast = i === PHASE_DEFINITIONS.length - 1;
    const frames = isLast
      ? TOTAL_FRAMES - allocated
      : Math.round((phase.approximateDurationSeconds / totalSeconds) * TOTAL_FRAMES);
    allocated += frames;
    return frames;
  });
}

function distributeImageFrames(
  phaseFrames: number, imageCount: number
): readonly number[] {
  const base = Math.floor(phaseFrames / imageCount);
  const remainder = phaseFrames - base * imageCount;
  return Array.from({ length: imageCount }, (_, i) =>
    i < remainder ? base + 1 : base
  );
}

export function computeTimeline(
  phaseImages: readonly (readonly ImageEntry[])[]
): readonly PhaseTimingResult[] {
  const phaseFramesList = computePhaseFrames();
  let globalOffset = 0;

  return phaseImages.map((images, phaseIndex) => {
    const phaseFrames = phaseFramesList[phaseIndex];
    const imageDurations = distributeImageFrames(phaseFrames, images.length);
    let localOffset = globalOffset;

    const timedImages: readonly TimedImageEntry[] = images.map((img, imgIndex) => {
      const entry: TimedImageEntry = {
        ...img,
        startFrame: localOffset,
        durationInFrames: imageDurations[imgIndex],
        zoomDirection: imgIndex % 2 === 0 ? "in" : "out",
      };
      localOffset += imageDurations[imgIndex];
      return entry;
    });

    const result: PhaseTimingResult = {
      phaseIndex, startFrame: globalOffset,
      durationInFrames: phaseFrames, images: timedImages,
    };
    globalOffset += phaseFrames;
    return result;
  });
}
```

### Wie die Verteilung funktioniert

Beispiel: Phase mit 87.1s, 22 Bilder, 30fps = 2613 Frames

```
Frames pro Bild: floor(2613 / 22) = 118
Remainder: 2613 - 118*22 = 17
→ Erste 17 Bilder: 119 Frames (3.97s)
→ Restliche 5 Bilder: 118 Frames (3.93s)
→ Summe: 17×119 + 5×118 = 2023 + 590 = 2613 ✓
```
