# Remotion Projekt-Setup fuer Image-to-Video

## Verzeichnisstruktur

```
video-project/
├── package.json
├── tsconfig.json
├── remotion.config.ts
├── public/
│   ├── images/
│   │   ├── Phase_0/
│   │   │   ├── scene-1-1234567890.png
│   │   │   └── ...
│   │   ├── Phase_1/
│   │   └── ...
│   └── voiceover.mp3
├── scripts/
│   ├── generateManifest.ts
│   └── renderShorts.sh
├── src/
│   ├── index.ts
│   ├── Root.tsx
│   ├── types.ts
│   ├── videoConfig.ts
│   ├── timingUtils.ts
│   ├── generatedManifest.ts  (auto-generiert)
│   ├── AICrisisVideo.tsx      (Haupt-Composition)
│   ├── ImageScene.tsx          (Bild-Komponente)
│   └── shorts/                 (optional)
│       ├── shortsConfig.ts
│       ├── shortsTimingUtils.ts
│       ├── CropPanImageScene.tsx
│       ├── VerticalImageScene.tsx
│       └── ShortComposition.tsx
└── out/
    ├── video-only.mp4
    ├── final.mp4
    └── shorts/
```

## Package Setup

```bash
mkdir video-project && cd video-project
npm init -y
npm i remotion@4 @remotion/cli@4 react react-dom
npm i -D typescript @types/react tsx
```

## tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "jsx": "react-jsx",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "outDir": "dist",
    "rootDir": ".",
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": ["src/**/*", "scripts/**/*"],
  "exclude": ["node_modules", "dist", "out"]
}
```

## remotion.config.ts

```typescript
import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
```

## package.json Scripts

```json
{
  "scripts": {
    "studio": "remotion studio",
    "render": "remotion render AICrisisVideo out/video-only.mp4 --codec h264 --muted",
    "generate-manifest": "tsx scripts/generateManifest.ts",
    "render-shorts": "bash scripts/renderShorts.sh"
  }
}
```

## Assets kopieren (NICHT verlinken!)

```bash
# FALSCH - Remotion-Bundler kann Symlinks nicht folgen:
# ln -s /pfad/zu/bildern public/images  ← FUNKTIONIERT NICHT

# RICHTIG - Assets kopieren:
mkdir -p public/images
cp -r /pfad/zu/bildern/* public/images/
cp /pfad/zu/voiceover.mp3 public/voiceover.mp3
```

**Warum?** Der Remotion-Bundler kopiert `public/` in ein temporaeres Verzeichnis.
Symlinks werden dabei nicht aufgeloest → 404-Fehler beim Rendern.

## Entry Points

### src/index.ts

```typescript
import { registerRoot } from "remotion";
import { RemotionRoot } from "./Root";

registerRoot(RemotionRoot);
```

### src/Root.tsx (Minimal)

```typescript
import React from "react";
import { Composition } from "remotion";
import { MainVideo } from "./MainVideo";
import { VIDEO_CONFIG, TOTAL_FRAMES } from "./videoConfig";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="MainVideo"
      component={MainVideo}
      durationInFrames={TOTAL_FRAMES}
      fps={VIDEO_CONFIG.fps}
      width={VIDEO_CONFIG.width}
      height={VIDEO_CONFIG.height}
    />
  );
};
```

## Voraussetzungen pruefen

```bash
# Node.js >= 18
node --version

# ffmpeg installiert (fuer Audio-Mux)
ffmpeg -version

# ffprobe installiert (fuer Analyse)
ffprobe -version
```
