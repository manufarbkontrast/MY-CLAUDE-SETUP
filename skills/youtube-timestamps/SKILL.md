---
name: youtube-timestamps
description: "Generiert YouTube-Kapitel-Zeitstempel aus einem video-project."
version: 1.0.0
metadata:
  last_verified: 2026-03-10
  keywords: [youtube, timestamps, chapters, video, remotion]
  production_tested: true
  related_skills: [images-to-video, media-processing]
user_invocable: true
trigger: "/youtube-timestamps"
---

# YouTube Timestamps Generator

Liest die `videoConfig.ts` eines Remotion-Video-Projekts und generiert daraus fertige YouTube-Kapitel-Zeitstempel.

## Wann diesen Skill nutzen

- Nach dem Rendern eines Videos mit dem `images-to-video` Workflow
- User moechte YouTube-Kapitelmarken fuer die Videobeschreibung
- Es existiert eine `videoConfig.ts` mit `WHISPER_SCENES` und Phase-Zuordnungen

## Ablauf

### 1. videoConfig.ts finden

Suche nach `videoConfig.ts` in diesen Pfaden (Reihenfolge):
1. Argument des Users (falls angegeben)
2. `video-project/src/videoConfig.ts` im aktuellen Verzeichnis
3. Beliebiger `**/src/videoConfig.ts` im Arbeitsverzeichnis

### 2. Phasen-Startzeiten extrahieren

Aus der `WHISPER_SCENES` Liste:
- Gruppiere Szenen nach `folder` (z.B. `Phase_0`, `Phase_1`, ...)
- Nimm den `startSeconds` der **ersten Szene** jeder Phase
- Sortiere aufsteigend nach Startzeit

### 3. Phase-Titel bestimmen

Versuche Phase-Titel aus dem zugehoerigen DOCX-Skript zu lesen:
- Suche `Skript*.docx` oder `*Scene*.docx` im Quellordner
- Parse `PHASE N: TITEL` Zeilen
- Fallback: `Phase 0`, `Phase 1`, etc.

Falls kein DOCX vorhanden, nutze den User-Input oder generische Titel.

### 4. Zeitstempel formatieren

Format: `M:SS Titel` (YouTube-kompatibel)

```
0:00 Cold Open
0:59 Title & Promise
1:14 Metaphor & World-Building
2:40 System Mechanics
```

Regeln:
- Erster Zeitstempel MUSS `0:00` sein (YouTube-Pflicht)
- Format `M:SS` fuer < 10 Minuten, `MM:SS` fuer >= 10 Minuten, `H:MM:SS` fuer >= 1 Stunde
- Keine fuehrende Null bei Minuten unter 10 (z.B. `1:14` nicht `01:14`)

### 5. Ausgabe

Gib die Zeitstempel als kopierbaren Codeblock aus:

```
0:00 Titel 1
1:23 Titel 2
...
```

## Implementierung (Python-Einzeiler)

```python
python3 -c "
import re

with open('VIDEO_CONFIG_PATH') as f:
    content = f.read()

pattern = r'startSeconds:\s*([\d.]+),\s*folder:\s*\"(Phase_\d+)\".*?//\s*S(\d+):\s*(.*)'
matches = re.findall(pattern, content)

phases = {}
for start, folder, scene_num, text in matches:
    phase_num = int(folder.split('_')[1])
    if phase_num not in phases:
        phases[phase_num] = float(start)

for phase_num in sorted(phases.keys()):
    secs = phases[phase_num]
    m, s = int(secs // 60), int(secs % 60)
    h = m // 60
    if h > 0:
        print(f'{h}:{m % 60:02d}:{s:02d} Phase {phase_num}')
    else:
        print(f'{m}:{s:02d} Phase {phase_num}')
"
```

## Optionale Erweiterungen

### Titel aus DOCX extrahieren

```python
import zipfile, xml.etree.ElementTree as ET, re
ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
with zipfile.ZipFile('SCRIPT_PATH') as z:
    xml = z.read('word/document.xml')
root = ET.fromstring(xml)
titles = {}
for p in root.iter(f'{{{ns}}}p'):
    text = ''.join(t.text for t in p.iter(f'{{{ns}}}t') if t.text)
    m = re.match(r'PHASE\s+(\d+):\s*(.+)', text, re.IGNORECASE)
    if m:
        titles[int(m.group(1))] = m.group(2).strip().split('(')[0].strip()
```

### Szenen-Level Zeitstempel

Falls der User detailliertere Kapitel will, koennen auch einzelne Szenen als Zeitstempel ausgegeben werden. Nutze dafuer die `startSeconds` jeder einzelnen Szene statt nur der ersten pro Phase.
