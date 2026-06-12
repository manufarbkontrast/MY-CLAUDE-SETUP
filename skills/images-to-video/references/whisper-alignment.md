# Whisper-basiertes Scene-Alignment

## Warum dieser Ansatz?

Das alte proportionale Skalieren (Phase-Dauer aus Skript × Audio/Skript-Faktor, dann gleichmaessig auf Bilder verteilen) fuehrt regelmaessig zu **Bildern die nicht zum gesprochenen Text passen**. Ursachen:

- Sprecher redet in manchen Phasen schneller, in anderen langsamer
- Gleichmaessige Verteilung ignoriert Satz-Laengen (kurze Saetze = kurze Scenes, lange Saetze = lange Scenes)
- Skripte enthalten Typos: doppelte Scene-Marker, fehlende Nummern

**Loesung:** Whisper transkribiert das Audio mit word-level timestamps. Fuer jeden Scene-Textblock aus dem Skript suchen wir die Position im Whisper-Wortstrom wo der Text beginnt, und nehmen dessen Start-Zeitstempel als exakten Scene-Start.

Ergebnis: Bild N wechselt EXAKT dann, wenn der zugehoerige Satz im Voiceover beginnt.

---

## Setup

```bash
# OpenAI-Whisper (Python-basiert, laeuft lokal auf CPU)
pip3 install openai-whisper

# Verify
python3 -m whisper --help | head
```

Modell-Wahl:
- `tiny` (~75 MB) — sehr schnell, fuer Tests
- `base` (~140 MB) — guter Kompromiss, **Standard**
- `small` (~470 MB) — deutlich besser fuer schwierige Audios
- `medium` (~1.5 GB) — sehr gut, langsamer
- `large` (~3 GB) — Premium, nur wenn Zeit egal ist

Fuer klar gesprochenes Englisch/Deutsch reicht `base` fast immer. Modell wird beim ersten Lauf nach `~/.cache/whisper/` gecached.

## Transkription ausfuehren

```bash
cd video-project
mkdir -p transcription

python3 -m whisper public/voiceover.mp3 \
  --model base \
  --language en \
  --word_timestamps True \
  --output_format json \
  --output_dir transcription \
  --verbose False
```

Dauert ca. 1-2 Minuten fuer 10 Minuten Audio auf einem M1/M2 Mac (CPU-only).

**Output:** `transcription/voiceover.json` mit dieser Struktur:

```json
{
  "text": "...",
  "segments": [
    {
      "id": 0,
      "start": 0.0,
      "end": 3.44,
      "text": " This is Bob, and he's got a huge problem.",
      "words": [
        {"word": " This", "start": 0.0, "end": 0.22, "probability": 0.70},
        {"word": " is", "start": 0.22, "end": 0.36, "probability": 0.98},
        {"word": " Bob,", "start": 0.36, "end": 0.62, "probability": 0.99}
      ]
    }
  ],
  "language": "en"
}
```

---

## Alignment-Script (Python)

`scripts/extractScript.py` — Parsed Skript (DOCX/TXT/MD), aligniert gegen Whisper, schreibt `src/sceneTimings.json`.

### Kernlogik

```python
import json, re, html, zipfile
from pathlib import Path

def docx_text(path: Path) -> str:
    """Extrahiert Plain-Text aus einer .docx Datei."""
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    xml = re.sub(r"<w:p[^>]*>", "\n", xml)
    xml = re.sub(r"<[^>]+>", " ", xml)
    return html.unescape(xml).replace("\xa0", " ")

def parse_phase_blocks(text: str):
    """Returns {phase_idx: [text_block, ...]} in document order.
    WICHTIG: Ignoriere die Scene-Nummern — sie haben oft Typos.
    Parse nur die Text-Bloecke ZWISCHEN den Markern, in Reihenfolge.
    """
    phase_header = re.compile(r"PHASE\s+(\d+)\s*:", re.IGNORECASE)
    headers = list(phase_header.finditer(text))
    result = {}
    for i, m in enumerate(headers):
        phase_idx = int(m.group(1))
        start = m.end()
        end = headers[i+1].start() if i+1 < len(headers) else len(text)
        phase_text = text[start:end]

        # Production-Notes am Ende entfernen
        notes = re.search(r"PRODUCTION\s+NOTES", phase_text, re.IGNORECASE)
        if notes:
            phase_text = phase_text[:notes.start()]

        # Scene-Marker finden (tolerant: [scene N], ]scene N], [scene N ], [sceneN])
        scene_marker = re.compile(r"[\[\]]\s*scene\s*\d+\s*\]", re.IGNORECASE)
        matches = list(scene_marker.finditer(phase_text))
        blocks = []
        for j, mm in enumerate(matches):
            text_start = mm.end()
            text_end = matches[j+1].start() if j+1 < len(matches) else len(phase_text)
            block = re.sub(r"\s+", " ", phase_text[text_start:text_end]).strip()
            if block:
                blocks.append(block)
        result[phase_idx] = blocks
    return result

def normalize(word: str) -> str:
    """Lowercase, strip punctuation — used for word comparison."""
    return re.sub(r"[^a-z0-9]", "", word.lower())

def load_whisper_words(path: Path):
    """Flatten alle Words aus allen Segments mit normalisiertem text."""
    with open(path) as f:
        data = json.load(f)
    words = []
    for seg in data["segments"]:
        for w in seg.get("words", []):
            nw = normalize(w["word"])
            if nw:
                words.append({"text": nw, "start": w["start"], "end": w["end"]})
    return words

def find_anchor(scene_words, whisper_words, cursor, look_ahead=80):
    """Finde Position in whisper_words wo scene_words am besten matchen,
    startend ab cursor. Returned Index.

    Scoring: count of matching initial words (window of up to 6),
    minus small penalty for distance from cursor (prefer nearby matches).
    Breaks early on perfect match.
    """
    best_pos = cursor
    best_score = -1
    end = min(cursor + look_ahead, len(whisper_words))
    for start in range(cursor, end):
        check = min(6, len(scene_words), len(whisper_words) - start)
        if check == 0:
            continue
        score = sum(
            1 for k in range(check)
            if whisper_words[start + k]["text"] == scene_words[k]
        )
        adjusted = score - (start - cursor) * 0.04
        if adjusted > best_score:
            best_score = adjusted
            best_pos = start
            if score == check:
                break  # perfect match, stop searching
    return best_pos

def split_longest_block(items, needed_splits):
    """Wenn Skript weniger Text-Bloecke hat als Bilder, splitte die
    laengsten Bloecke in der Mitte (nach Word-Count).
    `items` = [{text, words_norm}, ...]
    """
    out = list(items)
    for _ in range(needed_splits):
        longest_idx = max(
            (i for i in range(len(out)) if len(out[i]["words_norm"]) >= 4),
            key=lambda i: len(out[i]["words_norm"]),
            default=None,
        )
        if longest_idx is None:
            break
        item = out[longest_idx]
        mid = len(item["words_norm"]) // 2
        words = item["text"].split()
        first = {"text": " ".join(words[:mid]), "words_norm": item["words_norm"][:mid]}
        second = {"text": " ".join(words[mid:]), "words_norm": item["words_norm"][mid:]}
        out = out[:longest_idx] + [first, second] + out[longest_idx+1:]
    return out
```

### Alignment ausfuehren

```python
def main():
    text = docx_text(DOCX)
    phase_blocks = parse_phase_blocks(text)
    manifest_counts = parse_manifest_counts()  # {0: 12, 1: 6, 2: 23, ...}
    whisper_words = load_whisper_words(WHISPER)

    cursor = 0
    results = []
    for phase_idx in sorted(phase_blocks.keys()):
        blocks = phase_blocks[phase_idx]
        target = manifest_counts.get(phase_idx, 0)

        items = [
            {"text": b, "words_norm": [normalize(w) for w in b.split() if normalize(w)]}
            for b in blocks
        ]

        # Match item count to image count by splitting longest blocks
        if len(items) < target:
            items = split_longest_block(items, target - len(items))
        elif len(items) > target:
            items = items[:target]

        assert len(items) == target

        for sc_idx, item in enumerate(items):
            pos = find_anchor(item["words_norm"], whisper_words, cursor)
            pos = min(pos, len(whisper_words) - 1)
            results.append({
                "phaseIndex": phase_idx,
                "sceneIndex": sc_idx,
                "startTime": round(whisper_words[pos]["start"], 3),
                "preview": item["text"][:70],
            })
            # Advance cursor by approximate length of matched block
            cursor = pos + max(1, len(item["words_norm"]) - 2)

    with open(OUT, "w") as f:
        json.dump(results, f, indent=2)
```

---

## Umgang mit Skript-Typos

Sehr haeufige Problem-Muster und ihre Loesung:

### 1. Doppeltes `[scene N]`

```
[scene 10] Text eins... [scene 10] Text zwei... [scene 13]
```

→ Parser ignoriert die Nummern, sieht 3 Bloecke (fuer scene 10, 10, 13). Wenn Manifest 4 Images hat (10,11,12,13), dann `split_longest_block` teilt den laengsten der 3 Bloecke. Ergebnis: 4 Anker-Bloecke fuer 4 Images, alle grob im richtigen Text-Bereich.

### 2. Fehlendes `[scene N]`

```
[scene 4]...[scene 6]
```

Scene 5 existiert als Bild aber nicht im Skript. `split_longest_block` teilt den laengsten Block im Phase — typischerweise den `[scene 4]`-Block wenn er am laengsten ist. Ergebnis: ein zusaetzlicher Anker in der Naehe der richtigen Stelle.

### 3. Inkonsistente Marker-Formate

```
[scene 1]
[scene10]       ← fehlendes Leerzeichen
]scene 11]      ← Klammer-Typo
[scene 17 ]     ← Trailing space
cy[scene 13]    ← An vorheriges Wort geklebt
```

Die Regex `[\[\]]\s*scene\s*(\d+)\s*\]` matcht alle diese Varianten weil sie nur ein fuehrendes `[` ODER `]` und ein schliessendes `]` mit optionalen Whitespaces dazwischen erwartet.

---

## Verifikation

Nach dem Alignment IMMER pruefen:

```python
# 1. Monotonie
with open("src/sceneTimings.json") as f:
    data = json.load(f)
prev = -1
for r in data:
    assert r["startTime"] >= prev, f"Non-monotonic at {r}"
    prev = r["startTime"]

# 2. Count match
assert len(data) == sum(manifest_counts.values())

# 3. Spot-check: erste, mittlere, letzte Scene
for r in [data[0], data[len(data)//2], data[-1]]:
    print(f"P{r['phaseIndex']}.S{r['sceneIndex']} @ {r['startTime']:.2f}s  {r['preview']}")
```

Erwartung:
- Erste Scene @ ~0.0s
- Letzte Scene endet vor Audio-Ende (innerhalb ~5s)
- Previews matchen erkennbar das was im Audio gesprochen wird

## Integration in `timing.ts`

```typescript
import rawTimings from "./sceneTimings.json";

type RawTiming = {
  phaseIndex: number;
  sceneIndex: number;
  startTime: number;
  preview: string;
};

const SCENE_TIMINGS = rawTimings as RawTiming[];

export const buildTiming = (): VideoTiming => {
  const totalFrames = Math.round(AUDIO_DURATION_SECONDS * FPS);

  // Flat scenes in manifest order, with exact start frames
  const flatScenes: SceneTiming[] = [];
  let flatCursor = 0;
  MANIFEST.forEach((phaseEntry, phaseIndex) => {
    phaseEntry.scenes.forEach((sceneEntry, sceneIndexInPhase) => {
      const timing = SCENE_TIMINGS[flatCursor];
      // Sanity check: manifest and timings must agree on order
      if (timing.phaseIndex !== phaseIndex || timing.sceneIndex !== sceneIndexInPhase) {
        throw new Error(`Timing mismatch at ${flatCursor}`);
      }
      flatScenes.push({
        phaseIndex,
        sceneIndex: sceneIndexInPhase,
        publicPath: sceneEntry.publicPath,
        startFrame: Math.round(timing.startTime * FPS),
        durationFrames: 0, // filled below
      });
      flatCursor += 1;
    });
  });

  // Duration = gap to next scene (last scene extends to audio end)
  return {
    totalFrames,
    flatScenes: flatScenes.map((scene, i) => ({
      ...scene,
      durationFrames: Math.max(
        1,
        (i + 1 < flatScenes.length ? flatScenes[i + 1].startFrame : totalFrames)
          - scene.startFrame,
      ),
    })),
    // phases view derived from flatScenes...
  };
};
```

**Wichtig:** `tsconfig.json` braucht `"resolveJsonModule": true`.

---

## Alternative: Manuelles Nachjustieren

`sceneTimings.json` ist menschenlesbar. Wenn ein Alignment schief ist, User kann direkt die `startTime` aendern und `npm run render` neu starten — Whisper muss NICHT erneut laufen. Das macht iterative Verbesserung sehr schnell.
