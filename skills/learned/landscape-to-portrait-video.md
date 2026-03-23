# Landscape-to-Portrait Video-Konvertierung (16:9 → 9:16)

**Extracted:** 2026-02-27
**Context:** YouTube Shorts, Instagram Reels, TikTok aus Querformat-Material erstellen

## Problem

Querformat-Bilder/Videos (z.B. 1376x768 oder 1920x1080) muessen in Hochformat (1080x1920) konvertiert werden. Einfaches Skalieren wuerde massive schwarze Balken oder starkes Cropping erzeugen.

## Solution

4 Techniken, je nach Anwendungsfall:

### 1. Crop & Pan (Empfohlen fuer visuell interessante Bilder)
Bild fuellt Frame komplett. Langsamer horizontaler Pan zeigt verschiedene Bereiche.

```tsx
// object-fit: cover fuellt den Frame, object-position animiert den Pan
<Img
  src={imageSrc}
  style={{
    width: "100%",
    height: "100%",
    objectFit: "cover",
    objectPosition: `${panPosition}% 50%`,  // 30% → 70% animiert
    transform: `scale(${scale})`,
  }}
/>
```

Berechnung Pan-Range:
- Source 1376x768 in 1080x1920 Container
- Cover skaliert nach Hoehe: 1920/768 = 2.5x
- Skalierte Breite: 1376 * 2.5 = 3440px
- Pan-Range: 3440 - 1080 = 2360px
- `objectPosition` von 30% bis 70% = sanfter Pan ohne Extrempositionen

### 2. Blurred Background (Empfohlen fuer Text-lastige Bilder)
Unscharfes Bild als Hintergrund + scharfes Bild zentriert.

```tsx
{/* Layer 1: Blurred background */}
<Img src={imageSrc} style={{
  objectFit: "cover",
  filter: "blur(20px) brightness(0.6)",
  transform: `scale(1.2)`,  // Extra-Scale verhindert Blur-Raender
}} />

{/* Layer 2: Sharp foreground */}
<Img src={imageSrc} style={{
  objectFit: "contain",  // Behaelt Seitenverhaeltnis
}} />
```

### 3. Schwarze Balken (Letterbox)
Minimalistisch, Kino-Look. Platz fuer Text-Overlays.

```tsx
<Img src={imageSrc} style={{
  objectFit: "contain",
  // Schwarzer Hintergrund vom Container
}} />
```

### 4. Gradient Fade
Bild zentriert, Raender gehen in Schwarz ueber. Eleganter als harter Rand.

```tsx
{/* Gradient overlay ueber und unter dem Bild */}
<div style={{
  background: "linear-gradient(to bottom, black 0%, transparent 30%, transparent 70%, black 100%)",
  position: "absolute", inset: 0, zIndex: 1,
}} />
<Img src={imageSrc} style={{ objectFit: "contain" }} />
```

## When to Use

- YouTube Shorts aus bestehendem Querformat-Content
- Instagram Reels / TikTok Content-Repurposing
- Remotion-Projekte mit vertikalen Compositions
- Jede 16:9 → 9:16 Konvertierung

Empfehlung nach Content-Typ:
- **Landschaften/Action**: Crop & Pan
- **Text/Diagramme**: Blurred Background (ganzes Bild sichtbar)
- **Praesentation**: Letterbox mit Text-Overlay
- **Kunst/Portfolio**: Gradient Fade
