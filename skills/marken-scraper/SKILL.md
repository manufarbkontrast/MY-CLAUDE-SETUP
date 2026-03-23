---
name: marken-scraper
description: >
  Scrape Produktdaten von Hersteller-Websites und Online-Shops, um Marketplace-Templates
  (Zalando, Amazon, Otto, AboutYou) mit angereicherten Attributen zu befüllen. Nimmt eine
  Quelldatei (JTL CSV, Excel, ERP-Export) und ein Marketplace-Template, identifiziert die
  Marke, scraped Produktdetails (Beschreibung, Material, Sohle, Futter, Verschluss,
  Absatzhöhe, Pflegehinweise) und erzeugt eine ausgefüllte Export-Datei.

  Trigger: "scrape Produktdaten", "Produkte anreichern", "marketplace template füllen",
  "Zalando Export erstellen", "Produktdetails online suchen", "ERP zu Marketplace",
  "product enrichment", "Artikeldaten scrapen", "web enrichment pipeline",
  "marken-scraper", "Marken scraper"

  Keywords: web scraping, product enrichment, marketplace export, zalando, amazon, otto,
  product feed, JTL, ERP, product description, material composition, care instructions,
  openpyxl, firecrawl, WebSearch, WebFetch
user_invocable: true
metadata:
  version: 2.0.0
  last_verified: 2026-03-17
  production_tested: true
  related_skills:
    - web-research-enrichment-pipeline
    - ecommerce-product-classification
    - excel-template-dynamic-mapping
    - jtl-stammdaten
    - xlsx
---

# Marken-Scraper: Interaktiver Wizard

Du bist ein Produkt-Enrichment-Assistent. Führe den User durch den kompletten Prozess:
Quelldateien → Marke erkennen → Online scrapen → Marketplace-Template befüllen → Export.

---

## Ablauf

### Schritt 1: Quelldateien identifizieren

Suche im aktuellen Arbeitsverzeichnis UND im Downloads-Ordner nach relevanten Dateien:

```bash
# Suche nach CSV/Excel-Dateien
Glob: "**/*.csv" und "**/*.xlsx" im Arbeitsverzeichnis
Glob: ~/Downloads/*.csv und ~/Downloads/*.xlsx
```

Verwende `AskUserQuestion` um zu fragen:

**Frage 1 - Quelldatei** (header: "Quelldatei"):
- Zeige gefundene CSV/Excel-Dateien als Optionen
- Oder "Pfad manuell angeben"

**Frage 2 - Marketplace-Template** (header: "Template"):
- Zeige gefundene Excel-Dateien die nach Marketplace-Templates aussehen (z.B. "zalando", "amazon" im Namen)
- Option: "Kein Template (nur Daten extrahieren)"
- Option: "Pfad manuell angeben"

### Schritt 2: Quelldatei analysieren

Lies die Quelldatei und analysiere:

1. **Format erkennen**: CSV (Delimiter? Encoding?) oder Excel (welche Sheets?)
2. **Spalten identifizieren**: Artikelnummer, Name, GTIN, Preis, etc.
3. **Parent-Child-Struktur erkennen**: Gibt es Varianten (Größe, Farbe)?
4. **Marke aus Produktnamen ableiten**: Häufigste Wörter, bekannte Marken

Zeige dem User eine Zusammenfassung:
```
Quelldatei: JTL-Export.csv
  → 1.043 Zeilen, 11 Spalten
  → 131 Parent-Artikel, 912 SKUs
  → Erkannte Marke: PLAKTON (spanische Schuhe)
  → Größen: 25-47 (Kinder + Damen + Herren)
```

**Frage 3 - Marke bestätigen** (header: "Marke"):
- "[Erkannte Marke] ist korrekt"
- "Andere Marke" (Freitext)

**Frage 4 - Scraping** (header: "Scraping"):
- "Ja, Produktdaten online scrapen (Empfohlen)" — Beschreibung, Material, Sohle, Pflegehinweise
- "Nein, nur vorhandene Daten mappen" — Nur JTL-Felder verwenden

### Schritt 3: Web-Scraping (wenn gewählt)

#### 3a. Marken-Website finden

```
WebSearch: "[Marke] official website"
WebSearch: "[Marke] [erste Modellnummer] product details"
```

Identifiziere:
- Offizielle Website (EU, US, AU Varianten prüfen)
- Gute Händler-Quellen (shoesplease.de, spartoo.eu, bergfreunde.eu)
- Pflegehinweise-Seite

#### 3b. Unique Modellnummern extrahieren

Aus den Produktnamen alle einzigartigen Modellnummern extrahieren.
Gruppiere nach Modellnummer, da verschiedene Farb-Varianten dieselben Specs haben.

#### 3c. Parallel scrapen

**WICHTIG: Immer parallel scrapen für Geschwindigkeit!**

Pro Modellnummer (max 3-5 parallel):
```
WebSearch: "[Marke] [Modellnummer] product details materials"
```

Dann die besten Treffer fetchen:
```
WebFetch: [URL] → "Extract ALL product details: description, materials (upper, lining, sole),
                   care instructions, product type, heel height, fastening, features"
```

Zusätzlich einmal:
```
WebSearch: "[Marke] care instructions Pflegehinweise"
WebFetch: [Care-Page-URL] → "Extract complete care instructions"
```

#### 3d. Scraping-Ergebnisse sammeln

Pro Modell sammle in einem Dictionary:

```python
MODEL_DATA = {
    "[modellnummer]": {
        "category": "Sandalen|Pantoletten|Stiefeletten|...",
        "product_type": "Sandale|Pantolette|Zehentrenner|...",
        "description_de": "Deutsche Produktbeschreibung...",
        "sole_material": "Kork mit synthetischer Laufsohle",
        "lining": "Weiches Leder",
        "fastening": "Schnalle|Klettverschluss|...",
        "heel_height": "1.5",
        "toe_shape": "Rund|Offen|...",
        "occasion": "casual",
        "padding_type": "Memory Cushion|Anatomisch|...",
    }
}
```

Zeige Fortschritt: `✓ 15/17 Modelle gescraped`

#### Zielfelder (Priorität)

| Prio | Feld | Fallback wenn nicht gefunden |
|------|------|----------------------------|
| HOCH | Produktbeschreibung (DE) | Generiere aus Name + Material |
| HOCH | Obermaterial | Aus Produktname parsen |
| HOCH | Sohlenmaterial | "Synthetik" |
| HOCH | Futter | "Textil" |
| MITTEL | Verschlussart | "Schnalle" |
| MITTEL | Absatzhöhe | Leer lassen |
| MITTEL | Pflegehinweise | Standard-Leder/Textil-Pflege |
| MITTEL | Decksohle | Leer lassen |
| NIEDRIG | Materialverarbeitung | Leer lassen |

### Schritt 4: Mapping & Export

#### 4a. Produktnamen parsen

Aus jedem Artikelnamen extrahieren:
- **Modellname**: Erstes Wort (ggf. mit Prefix wie "Mam")
- **Modellnummer**: 4-6 stellige Zahl
- **Material**: Bekannte Materialbezeichnungen → Deutsch übersetzen
- **Farbe**: Letztes Wort → Zalando-Farbcode mappen

**Farbmapping**: Longest-match-first!
```python
COLOR_MAP = {
    "ligh khaki": "gruen",   # Typos im Quellsystem mappen!
    "negro": "schwarz",
    "camello": "beige",
    # ...
}
```

#### 4b. Geschlecht aus Größenbereich

```
Größe 25-35 → kids
Größe 36-42 → female
Größe 39-47 → male
Gemischt   → unisex
```

#### 4c. Kategorie bestimmen

1. Gescrapte Modelldaten (beste Quelle)
2. Modellname-Hints (Blogg→Pantoletten, Bolero→Sandalen)
3. Default-Kategorie

#### 4d. Python-Script generieren und ausführen

Erstelle ein Python-Script (`[marke]_zalando_mapper.py`) im Arbeitsverzeichnis das:

1. JTL CSV liest und Parent-Child gruppiert
2. Produktnamen parst (Material, Farbe)
3. Gescrapte MODEL_DATA als Dict einbettet
4. Zalando-Template-Struktur liest (wenn vorhanden)
5. 3-Level Merge: Source → Scraping → Fallback
6. Excel mit openpyxl erstellt:
   - Zusammenfassungs-Sheet
   - Pro Kategorie ein Sheet mit Template-Struktur
   - Model-Rows + SKU-Rows (je Größe mit EAN)
7. Speichert als `[Marke]_Zalando_Export.xlsx`

```bash
python3 [marke]_zalando_mapper.py
```

#### 4e. Ergebnis verifizieren

Nach dem Export:
- Lies die erzeugte Excel und zeige ein Sample-Produkt mit allen befüllten Feldern
- Zeige Statistiken: Produkte, SKUs, Fill-Rate, Kategorien
- Lade die Referenz `references/plakton-example.md` für Vergleich wenn nötig

### Schritt 5: Abschluss

Zeige dem User:

```
✓ Export fertig: [Pfad zur Datei]

  Marke:       [MARKENNAME]
  Produkte:    131 (113 mit Web-Daten angereichert)
  SKUs:        912
  Kategorien:  Sandalen (109), Pantoletten (22)
  Fill-Rate:   25+ Felder pro Produkt

  Angereicherte Felder:
  ✓ Produktbeschreibung (DE)
  ✓ Sohlenmaterial
  ✓ Futter/Innenmaterial
  ✓ Verschlussart
  ✓ Absatzhöhe
  ✓ Pflegehinweise
  ✓ ...
```

---

## Technische Referenz

### CSV-Parsing (deutsche ERPs)

```python
import csv
with open(path, "r", encoding="latin-1") as f:
    reader = csv.reader(f, delimiter=";")
```

### Parent-Child-Gruppierung

```python
parts = artnum.split("-")
if len(parts) >= 3 and parts[-1].replace(".", "").isdigit():
    # Child: "8791-575080-negro-36" → parent=8791, size=36
else:
    # Parent: "8791"
```

### Template-Struktur lesen

```python
import openpyxl
wb = openpyxl.load_workbook(template_path)
for sheet_name in wb.sheetnames:
    ws = wb[sheet_name]
    headers = [cell.value for cell in ws[1]]     # Deutsche Bezeichnungen
    api_keys = [cell.value for cell in ws[2]]     # API-Feldcodes
    levels = [cell.value for cell in ws[3]]        # model/config/simple
    key_to_idx = {k: i for i, k in enumerate(api_keys) if k}
```

### Dynamisches Feld-Mapping

```python
def set_field(row, key_to_idx, field, value):
    """Nur setzen wenn Feld existiert UND Wert vorhanden."""
    if field in key_to_idx and value:
        row[key_to_idx[field]] = value
```

### Scraping Best Practices

- **Parallel**: Max 3-5 WebSearch gleichzeitig
- **AU-Websites** haben oft vollständigere Produktdaten als EU
- **Amazon.de** ist JS-heavy → oft unvollständig, Händler bevorzugen
- **Pflegehinweise**: Einmal pro Marke scrapen, dann pro Material zuordnen
- **Zalando Sheet-Names**: Triple-Spaces möglich (`"T-Shirt   Top"`)

### Fehlervermeidung

| Fehler | Lösung |
|--------|--------|
| Marke = Modellname | Immer übergeordneten Herstellernamen verwenden |
| Farbe enthält Modellnummer | Longest-match-first beim Parsen |
| Alle Produkte in einer Kategorie | Gescrapte Modelldaten für Zuordnung nutzen |
| Pflegehinweise falsch zugeordnet | Material-basiert: Leder ≠ EVA ≠ Textil |

---

## Verwandte Skills

- `web-research-enrichment-pipeline` — JSON-Cache und firecrawl
- `ecommerce-product-classification` — Keyword-basierte Kategorie-Zuordnung
- `excel-template-dynamic-mapping` — Dynamisches Spalten-Mapping
- `jtl-stammdaten` — JTL-Import-Dateien
- `xlsx` — Allgemeines Excel-Handling
