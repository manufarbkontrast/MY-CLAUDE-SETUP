---
name: jtl-stammdaten
description: Erstellt JTL-Einspieltabellen und Bestellmengen-CSVs aus Hersteller-Orderfiles (Excel/CSV). Fragt nach Saison, Jahr und Quelldateien.
user_invocable: true
---

# JTL Stammdaten-Agent Skill

Du erstellst JTL-Import-Dateien aus Hersteller-Orderfiles.

## Ablauf

### Schritt 1: Saison und Jahr abfragen

Frage den User IMMER zuerst nach:
- **Saison**: HW (Herbst/Winter) oder FS (Frühjahr/Sommer)
- **Jahr**: z.B. 2026

Verwende `AskUserQuestion` mit diesen Optionen:
- Saison: "HW (Herbst/Winter)" oder "FS (Frühjahr/Sommer)"
- Jahr: Freitext

Der HAN-Wert wird daraus gebildet: `[Jahr][Saison]` → z.B. `2026HW` oder `2026FS`

### Schritt 2: Quelldateien identifizieren

Suche im aktuellen Arbeitsverzeichnis nach Excel-Dateien (.xlsx, .xls, .csv).
Zeige die gefundenen Dateien und frage, welche verarbeitet werden sollen.

### Schritt 3: Marke erkennen und Mapping anwenden

Erkenne die Marke anhand der Dateiinhalte und wende das passende Mapping an.
Führe das Python-Skript `scripts/jtl_generator.py` aus.

### Schritt 4: Ausgabe

Pro Quelldatei werden **2 Dateien** erstellt:
1. `Einspieltabelle_[MARKENCODE]_[SAISON]_[DATUM].csv` — Vater- und Kindartikel
2. `Bestellmengen_[MARKENCODE]_[SAISON]_[DATUM].csv` — EAN, Menge, EK

## Bekannte Marken

| Marke | Hersteller-Name | Code | Kategorie | Warengruppe |
|-------|----------------|------|-----------|-------------|
| Universal Works | `UNIVERSAL` | `UNIV` | Shopify Shoesplease | Bekleidung/Accessoires |
| Giove | `GIOVE` | `GIOV` | Shopify Shoesplease | Schuhe |
| Pedro Miralles | `PEDRO MIRALLES` | `PEDR` | Shopify Shoesplease | Schuhe |
| Ilse Jacobsen | `ILSE JACOBSEN` | `ILSE` | Shopify Shoesplease | — |
| Voile Blanche | `VOILE BLANCHE` | `VOIL` | Shopify Shoesplease | Schuhe |

## Ausführung

```bash
python3 ~/.claude/skills/jtl-stammdaten/scripts/jtl_generator.py \
  --saison "HW" \
  --jahr "2026" \
  --input "/pfad/zur/datei.xlsx" \
  --output "/pfad/zum/ausgabeordner/" \
  --marke "auto"
```

Wenn `--marke auto` gesetzt ist, wird die Marke automatisch erkannt.
