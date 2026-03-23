---
name: images-to-video
description: "Bilder + Skript + Voiceover → Video mit Remotion. Inkl. Shorts-Extraktion."
version: 1.0.0
metadata:
  last_verified: 2026-02-27
  keywords: [remotion, video, voiceover, images, slideshow, shorts, youtube, ffmpeg]
  production_tested: true
  related_skills: [media-processing]
---

# Images-to-Video: Bilder + Skript + Voiceover → Video

Erstellt aus einer Sammlung von Bildern, einem Skript mit Timestamps und einem Voiceover ein fertiges Video mit Remotion. Optional: YouTube Shorts im 9:16-Format.

## Wann diesen Skill nutzen

- User hat **Bilder** (PNG/JPG), ein **Voiceover** (MP3/WAV) und optional ein **Skript** mit Phasen/Timestamps
- Ziel: Zusammengefuegtes Video mit subtilen Zoom-Effekten und Crossfades
- Optional: Vertikale Shorts (YouTube/Instagram/TikTok) aus dem Ergebnis

## Quick Reference: Workflow in 7 Schritten

```
1. ANALYSE     → Bilder zaehlen, Audio-Laenge messen, Skript lesen
2. PROJEKT     → Remotion-Projekt aufsetzen, Assets kopieren
3. MANIFEST    → Bild-Manifest generieren (mit Deduplizierung)
4. TIMING      → Phasen-Dauern aus Skript berechnen, auf Audio skalieren
5. KOMPONENTEN → ImageScene mit Zoom + Crossfade erstellen
6. RENDERN     → Video stumm rendern (--muted)
7. AUDIO-MUX   → Original-Audio per ffmpeg muxen (kein Re-Encoding)
```

Optional:
```
8. SHORTS      → Segmente definieren, 9:16-Compositions, Batch-Render
```

---

## Schritt 1: Analyse

Vor dem Start IMMER pruefen:

```bash
# Audio-Laenge und Format
ffprobe -v quiet -show_entries format=duration,bit_rate -show_entries stream=sample_rate,channels "voiceover.mp3"

# Bild-Dimensionen (erstes Bild)
ffprobe -v quiet -show_entries stream=width,height "images/Phase_0/scene-1.png"

# Bilder zaehlen
find images/ -name "*.png" | wc -l

# Bild-Namensschema erkennen
ls images/Phase_0/ | head -20
```

Wichtige Werte notieren:
- **Audio-Dauer** (exakt, in Sekunden)
- **Bild-Dimensionen** (Breite x Hoehe)
- **Anzahl Bilder** (gesamt und pro Phase/Ordner)
- **Namensschema** (z.B. `scene-N-TIMESTAMP.png`)

## Schritt 2: Projekt aufsetzen

> Lade Reference: `references/project-setup.md` fuer vollstaendiges Setup

```bash
mkdir video-project && cd video-project
npm init -y
npm i remotion @remotion/cli react react-dom
npm i -D typescript @types/react tsx
```

**KRITISCH: Assets KOPIEREN, nicht verlinken!**
Remotion-Bundler kann Symlinks nicht folgen.

```bash
mkdir -p public/images
cp -r /pfad/zu/bildern/* public/images/
cp /pfad/zu/voiceover.mp3 public/voiceover.mp3
```

## Schritt 3: Manifest generieren

> Lade Reference: `references/manifest-and-timing.md` fuer Details

Manifest-Generator (`scripts/generateManifest.ts`):
- Liest alle Bilder aus Phase-Ordnern
- Parsed Dateinamen → Scene-Nummer + Timestamp
- **Dedupliziert**: Bei doppelten Scene-Nummern nur letztes Bild behalten
- Generiert typsichere TypeScript-Datei

```bash
npx tsx scripts/generateManifest.ts
# → src/generatedManifest.ts (automatisch generiert)
```

## Schritt 4: Timing berechnen

Wenn ein Skript mit Timestamps vorhanden:

```
Skalierungsfaktor = Audio-Dauer / Skript-geplante-Dauer
Skalierte Phase-Start = Original-Start × Faktor
```

Beispiel: Skript geplant fuer 508s, Audio ist 590s → Faktor 1.162

Phase-Dauern in `videoConfig.ts` als `approximateDurationSeconds` eintragen.
Die Timing-Utils verteilen Frames proportional auf Phasen und gleichmaessig auf Bilder innerhalb jeder Phase.

## Schritt 5: Komponenten erstellen

> Lade Reference: `references/components.md` fuer alle Varianten

**ImageScene** (Landscape 16:9):
- `object-fit: cover` → Bild fuellt Frame immer komplett
- Subtiler Zoom: 1.0 → 1.05 (alternierend in/out)
- Crossfade: 10 Frames (0.33s) Ueberlappung zwischen Bildern

**Fuer vertikale Shorts** gibt es 4 Display-Modi:
1. **Crop & Pan** → Bild fuellt 9:16 komplett, langsamer horizontaler Pan
2. **Blurred Background** → Unscharfes Bild hinten + scharfes Bild zentriert
3. **Letterbox** → Schwarze Balken oben/unten
4. **Gradient Fade** → Sanfter Uebergang zu Schwarz an den Raendern

## Schritt 6 + 7: Rendern + Audio-Mux

**WICHTIG: Video IMMER stumm rendern, Audio extern muxen!**

Remotion re-encodiert Audio als AAC, was zu wahrnehmbaren Tempo-Aenderungen fuehrt (selbst 0.01% faellt auf). Loesung:

```bash
# 1. Stummes Video
npx remotion render CompositionId out/video-only.mp4 --codec h264 --muted

# 2. Original-Audio muxen (kein Re-Encoding der Quelle)
ffmpeg -y \
  -i out/video-only.mp4 \
  -i public/voiceover.mp3 \
  -c:v copy -c:a aac -b:a 192k -shortest \
  out/final.mp4
```

> Lade Reference: `references/render-pipeline.md` fuer Details + Troubleshooting

## Schritt 8: Shorts (Optional)

> Lade Reference: `references/shorts-extraction.md` fuer vollstaendigen Workflow

Kurz-Zusammenfassung:
1. Beste 3-5 Segmente identifizieren (30-60s, inhaltlich eigenstaendig)
2. `ShortDefinition` pro Segment (Phase, Bild-Indices, Audio-Start/Ende)
3. Separate Compositions in Root.tsx registrieren (1080x1920)
4. Render-Script: Remotion render + ffmpeg Audio-Schnitt + Mux

---

## Wann References laden

| Reference | Laden wenn... |
|-----------|--------------|
| `references/project-setup.md` | Neues Projekt von Null aufsetzen |
| `references/manifest-and-timing.md` | Bild-Manifest erstellen oder Timing anpassen |
| `references/components.md` | ImageScene-Komponenten erstellen oder anpassen |
| `references/render-pipeline.md` | Render-Probleme, Audio-Sync-Issues |
| `references/shorts-extraction.md` | Shorts/Reels/TikTok aus langem Video erstellen |

---

## Checkliste vor Abgabe

- [ ] `ffprobe` zeigt korrekte Aufloesung und FPS
- [ ] Audio-Dauer im Output ≈ Original-Audio-Dauer (Differenz < 0.01s)
- [ ] Kein Audio-Stream im Remotion-Output (erst nach ffmpeg-Mux)
- [ ] Bilder fuellen Frame komplett (kein Weiss/Leere Flaechen)
- [ ] Subtile Zoom-Effekte sichtbar (nicht zu stark)
- [ ] Crossfades zwischen Bildern (kein harter Schnitt)
- [ ] Bilder passen zum gesprochenen Text (Skript-Timestamps pruefen)

## Typische Fehler vermeiden

1. **Symlinks statt Kopien** → Remotion-Bundler 404-Fehler. IMMER `cp -r`.
2. **Audio in Remotion** → Tempo-Drift. IMMER extern per ffmpeg muxen.
3. **Gleichmaessige Verteilung ohne Skript** → Bilder passen nicht zum Text. Skript-Timestamps nutzen.
4. **Duplikate nicht entfernt** → Zu viele Bilder, zu schneller Schnitt. Deduplizierung im Manifest.
5. **Ken-Burns zu stark** → Ablenkend. Max 1.05x Zoom, nicht mehr.
