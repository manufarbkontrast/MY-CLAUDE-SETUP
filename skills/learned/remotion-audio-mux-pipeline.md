# Remotion: Audio extern per ffmpeg muxen

**Extracted:** 2026-02-27
**Context:** Remotion-Projekte mit externem Voiceover/Musik wo Audio-Tempo exakt bleiben muss

## Problem

Remotion re-encodiert Audio als AAC beim Rendern. Das kann zu wahrnehmbaren Tempo-Aenderungen fuehren (selbst bei nur 0.06s Differenz auf 590s faellt es auf). User berichten "Audio klingt schneller" obwohl der technische Unterschied minimal ist.

## Solution

1. `<Audio>` Komponente aus der Remotion-Composition entfernen
2. Video stumm rendern mit `--muted` Flag
3. Original-Audio per ffmpeg muxen (kein Re-Encoding der Audioquelle)

```bash
# Schritt 1: Stummes Video rendern
npx remotion render CompositionId out/video-only.mp4 --codec h264 --muted

# Schritt 2: Original-Audio muxen
ffmpeg -y \
  -i out/video-only.mp4 \
  -i "original-audio.mp3" \
  -c:v copy -c:a aac -b:a 192k -shortest \
  out/final.mp4

# Fuer Segment-Schnitte (z.B. Shorts):
ffmpeg -y \
  -i out/video-only.mp4 \
  -ss START_SECONDS -t DURATION -i "original-audio.mp3" \
  -c:v copy -c:a aac -b:a 192k -shortest \
  out/segment.mp4
```

Key flags:
- `-c:v copy`: Video-Stream nicht re-encodieren (schnell, verlustfrei)
- `-c:a aac -b:a 192k`: Audio nur einmal encodieren (aus MP3-Quelle)
- `-shortest`: Stoppt wenn kuerzester Stream endet
- `-ss` vor `-i`: Seek im Input (schneller als nach Input)

## Example

```typescript
// AICrisisVideo.tsx - KEIN <Audio> Element
export const AICrisisVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      {/* Audio wird extern per ffmpeg gemuxed */}
      {allImages.map((img, index) => (
        <Sequence key={index} from={img.startFrame} durationInFrames={img.duration}>
          <ImageScene src={img.path} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
```

## When to Use

- Voiceover oder Musik muss exakt im Original-Tempo bleiben
- User berichtet "Audio klingt schneller/langsamer"
- Professionelle Audio-Qualitaet wichtig
- Mehrere Segmente aus demselben Audio geschnitten werden (Shorts)
