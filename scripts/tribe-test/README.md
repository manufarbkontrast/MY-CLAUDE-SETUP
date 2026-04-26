# TRIBE v2 — RunPod-Test in 30 Minuten

Lokaler Smoke-Test für Meta TRIBE v2 auf einem geliehenen A100 in der Cloud. Schätzkosten: **2-5 €**.

⚠️ **Lizenz**: TRIBE v2 ist CC-BY-NC. Outputs **nicht kommerziell verwenden** ohne separate Lizenz von Meta.

## 1. Pod starten

1. RunPod-Account: https://runpod.io
2. **Deploy** → **GPU Pod**
3. **Template**: `RunPod PyTorch 2.4` (oder neuer)
4. **GPU**: A100 SXM 40 GB (~0.79 €/h) oder A100 80 GB (~1.50 €/h)
5. **Storage**: 50 GB Container Disk (für Model-Weights), 50 GB Volume (Outputs)
6. **Deploy** → ~2 min Wartezeit

## 2. Setup

Web-Terminal öffnen, dann:

```bash
mkdir -p /workspace/tribe-test && cd /workspace/tribe-test
# Skripte hochladen (per RunPod Web-UI „Upload" oder per scp/rsync von deinem Rechner)
# erwartete Dateien: runpod-setup.sh, test_merch.py

bash runpod-setup.sh
```

Setup-Dauer: 5-10 min (Python-Deps + Encoder-Weights vorab).

## 3. Erster Run — eingebaute Samples

```bash
python3 test_merch.py
```

Was passiert:
- `video_blender` — Sintel-Trailer (Open-Source-Movie) — Video-Modalität testen
- `text_marketing` — Drop-Announcement-Text — Marketing-Sprache testen
- `text_neutral` — Annual-Report-Text — Vergleichs-Baseline

Output landet in `./outputs/`:
```
video_blender_preds.npy      ~ 16 MB  (T × 20484 float32)
video_blender_segments.csv
video_blender_brain.png      ~ Cortex-Heatmap erste 15 Zeitschritte
video_blender_summary.json   ~ {mean, max, peak_timestep, top10_vertices}
text_marketing_*.{npy,csv,png,json}
text_neutral_*.{npy,csv,png,json}
```

## 4. Eigenes Asset testen

### Foto
```bash
python3 test_merch.py /workspace/tribe-test/inputs/produkt.jpg
```

### Video
```bash
python3 test_merch.py /workspace/tribe-test/inputs/ad.mp4
```

### Text (z.B. Produktbeschreibung)
```bash
python3 test_merch.py --text "Limited Drop. Friday 18:00. Only 100 pieces. Hand-printed in Berlin."
```

### Multimodal (Video + Text)
```bash
python3 test_merch.py --video ad.mp4 --text "Drop incoming. Sign up now."
```

## 5. Outputs verstehen

Pro Asset bekommst du:

| File | Inhalt |
|---|---|
| `*_preds.npy` | Numpy-Array `(T, 20484)` — pro Zeitschritt T (≈1.5s) für 20484 Cortex-Voxel ein BOLD-Wert |
| `*_segments.csv` | Welche Stimulus-Abschnitte zu welchem T gehören |
| `*_brain.png` | Heatmap-Visualisierung der ersten 15 Zeitschritte |
| `*_summary.json` | mean / max / peak-Timestep / Top-10-aktivste Voxel |

### Vergleich zwischen Assets
```python
import numpy as np
a = np.load("outputs/text_marketing_preds.npy")
b = np.load("outputs/text_neutral_preds.npy")
print("Marketing mean activation:", a.mean())
print("Neutral mean activation:  ", b.mean())
print("Diff (marketing - neutral):", a.mean() - b.mean())
```

Höhere mittlere Aktivierung ≈ stärkere neuronale Reaktion. Aber: das Modell sagt `wie viel`, nicht `wie positiv` — saliency ≠ valence.

## 6. Pod stoppen

**Wichtig**: GPU kostet pro Sekunde, auch wenn du nichts machst.

```bash
# alles synchronisieren falls Outputs lokal landen sollen
# (RunPod Volume bleibt erhalten, Container-Disk wird gelöscht beim Stop)
```

→ RunPod-Dashboard → Pod → **Stop** (Volume bleibt) oder **Terminate** (alles weg).

Volume-Storage kostet ~0,07 €/GB/Monat — 50 GB = ~3,50 €/Monat. Für sporadisches Testen: jedes Mal Terminate + neu deploy.

## 7. Was du gelernt hast

Nach dem Test weißt du:
- ✅ Läuft das Modell auf A100 ohne OOM?
- ✅ Wie lange dauert die Inferenz pro Asset (Sekunden bis Minuten)?
- ✅ Liefern die Outputs sinnvolle Unterschiede zwischen Assets?
- ✅ Lohnt sich Hardware-Kauf oder reicht weiterhin Cloud-mieten?

## Troubleshooting

**OOM beim Laden** → A100 80 GB nehmen oder zu Single-Modality wechseln (nur `--text` oder nur `--audio`).

**`numpy` Fehler** → Setup-Script führt `pip install "numpy<2.1"` BEVOR tribev2 installiert wird. Bei Fehler: `pip install --force-reinstall "numpy<2.1"` und Python-Prozess neu starten.

**Download hängt** → Hugging-Face-Token setzen falls Rate-Limit:
```bash
huggingface-cli login
# oder: export HF_TOKEN=hf_...
```

**Plot-Backend-Fehler** → `apt install libgl1` (für matplotlib) und `export MPLBACKEND=Agg`.
