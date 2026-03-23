# Bild-Komponenten (ImageScene Varianten)

## 1. ImageScene (Landscape 16:9)

Fuer das Hauptvideo. Bild fuellt Frame komplett mit `object-fit: cover`.

```tsx
import React from "react";
import { useCurrentFrame, Img, interpolate, staticFile } from "remotion";
import {
  CROSSFADE_FRAMES, ZOOM_SCALE_MIN, ZOOM_SCALE_MAX,
} from "./videoConfig";

interface ImageSceneProps {
  readonly src: string;
  readonly durationInFrames: number;
  readonly zoomDirection: "in" | "out";
  readonly isFirst: boolean;
  readonly isLast: boolean;
}

export const ImageScene: React.FC<ImageSceneProps> = ({
  src, durationInFrames, zoomDirection, isFirst, isLast,
}) => {
  const frame = useCurrentFrame();

  // Zoom: 1.0 → 1.05 oder 1.05 → 1.0
  const [scaleFrom, scaleTo] =
    zoomDirection === "in"
      ? [ZOOM_SCALE_MIN, ZOOM_SCALE_MAX]
      : [ZOOM_SCALE_MAX, ZOOM_SCALE_MIN];

  const scale = interpolate(
    frame, [0, durationInFrames - 1], [scaleFrom, scaleTo],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  // Crossfade: 10 Frames = 0.33s bei 30fps
  const fadeIn = isFirst ? 1
    : interpolate(frame, [0, CROSSFADE_FRAMES], [0, 1],
        { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  const fadeOut = isLast ? 1
    : interpolate(frame,
        [durationInFrames - CROSSFADE_FRAMES, durationInFrames], [1, 0],
        { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  const opacity = Math.min(fadeIn, fadeOut);

  return (
    <div style={{
      width: "100%", height: "100%", overflow: "hidden",
      position: "absolute", top: 0, left: 0,
    }}>
      <Img
        src={staticFile(src)}
        style={{
          width: "100%", height: "100%",
          objectFit: "cover",
          transform: `scale(${scale})`,
          opacity,
        }}
      />
    </div>
  );
};
```

## 2. CropPanImageScene (Vertical 9:16 - Crop & Pan)

Fuer Shorts. Bild fuellt 9:16-Frame komplett, langsamer horizontaler Pan.

```tsx
import React from "react";
import { useCurrentFrame, Img, interpolate, staticFile } from "remotion";
import {
  CROSSFADE_FRAMES, ZOOM_SCALE_MIN, ZOOM_SCALE_MAX,
} from "../videoConfig";

interface CropPanImageSceneProps {
  readonly src: string;
  readonly durationInFrames: number;
  readonly zoomDirection: "in" | "out";
  readonly isFirst: boolean;
  readonly isLast: boolean;
}

export const CropPanImageScene: React.FC<CropPanImageSceneProps> = ({
  src, durationInFrames, zoomDirection, isFirst, isLast,
}) => {
  const frame = useCurrentFrame();

  // Pan: 30% → 70% (oder umgekehrt) horizontal
  const [panFrom, panTo] = zoomDirection === "in" ? [30, 70] : [70, 30];
  const panPosition = interpolate(
    frame, [0, durationInFrames - 1], [panFrom, panTo],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  // Zoom (gleich wie Hauptvideo)
  const [scaleFrom, scaleTo] =
    zoomDirection === "in"
      ? [ZOOM_SCALE_MIN, ZOOM_SCALE_MAX]
      : [ZOOM_SCALE_MAX, ZOOM_SCALE_MIN];
  const scale = interpolate(
    frame, [0, durationInFrames - 1], [scaleFrom, scaleTo],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  // Crossfade
  const fadeIn = isFirst ? 1
    : interpolate(frame, [0, CROSSFADE_FRAMES], [0, 1],
        { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const fadeOut = isLast ? 1
    : interpolate(frame,
        [durationInFrames - CROSSFADE_FRAMES, durationInFrames], [1, 0],
        { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const opacity = Math.min(fadeIn, fadeOut);

  return (
    <div style={{
      width: "100%", height: "100%", position: "absolute",
      top: 0, left: 0, overflow: "hidden", opacity,
    }}>
      <Img
        src={staticFile(src)}
        style={{
          width: "100%", height: "100%",
          objectFit: "cover",
          objectPosition: `${panPosition}% 50%`,
          transform: `scale(${scale})`,
        }}
      />
    </div>
  );
};
```

### Pan-Berechnung

Fuer 1376x768 Bild in 1080x1920 Container:
- `objectFit: cover` skaliert nach Hoehe: 1920/768 = 2.5x
- Skalierte Breite: 1376 × 2.5 = 3440px
- Sichtbar: 1080px → Pan-Range: 2360px
- `objectPosition: 30%-70%` vermeidet extreme Kanten

## 3. VerticalImageScene (Blurred Background)

Fuer Shorts. Unscharfes Bild hinten + scharfes Bild zentriert.

```tsx
import React from "react";
import { useCurrentFrame, Img, interpolate, staticFile } from "remotion";
import {
  CROSSFADE_FRAMES, ZOOM_SCALE_MIN, ZOOM_SCALE_MAX,
} from "../videoConfig";

const BLUR_AMOUNT = 20;
const BG_SCALE = 1.2;
const BG_BRIGHTNESS = 0.6;

export const VerticalImageScene: React.FC</* gleiche Props */> = ({
  src, durationInFrames, zoomDirection, isFirst, isLast,
}) => {
  const frame = useCurrentFrame();
  // ... scale, fadeIn, fadeOut, opacity (gleich wie oben)

  const imageSrc = staticFile(src);

  return (
    <div style={{
      width: "100%", height: "100%", position: "absolute",
      top: 0, left: 0, overflow: "hidden", opacity,
    }}>
      {/* Layer 1: Blurred Background */}
      <Img src={imageSrc} style={{
        position: "absolute", top: "50%", left: "50%",
        width: "100%", height: "100%", objectFit: "cover",
        transform: `translate(-50%, -50%) scale(${BG_SCALE * scale})`,
        filter: `blur(${BLUR_AMOUNT}px) brightness(${BG_BRIGHTNESS})`,
      }} />

      {/* Layer 2: Sharp Foreground */}
      <Img src={imageSrc} style={{
        position: "absolute", top: "50%", left: "50%",
        width: "100%", height: "100%", objectFit: "contain",
        transform: `translate(-50%, -50%) scale(${scale})`,
      }} />
    </div>
  );
};
```

## 4. Letterbox (einfach)

```tsx
// Schwarzer Hintergrund vom Container, Bild zentriert mit contain
<Img src={staticFile(src)} style={{
  width: "100%", height: "100%",
  objectFit: "contain",
  transform: `scale(${scale})`,
  opacity,
}} />
```

## 5. Gradient Fade

```tsx
<>
  <Img src={staticFile(src)} style={{
    width: "100%", height: "100%",
    objectFit: "contain",
    transform: `scale(${scale})`,
    opacity,
  }} />
  {/* Gradient overlay */}
  <div style={{
    position: "absolute", inset: 0, zIndex: 1, opacity,
    background: "linear-gradient(to bottom, black 0%, transparent 25%, transparent 75%, black 100%)",
  }} />
</>
```

## Display-Modus Empfehlung

| Content-Typ | Empfohlener Modus |
|-------------|-------------------|
| Landschaften, Action | **Crop & Pan** |
| Text, Diagramme | **Blurred Background** |
| Praesentation | **Letterbox** |
| Kunst, Portfolio | **Gradient Fade** |
