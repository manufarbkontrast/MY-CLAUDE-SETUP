---
name: sales-analytics
description: "Analysiert Verkaufs- und Bestandsdaten aus Excel-Dateien (Shopify-Exporte, ERP-Daten, Marken-Orderfiles) und generiert einen strukturierten Analyse-Report als Excel. Erkennt automatisch Spaltenstruktur (SKU, Produkt, Variante, Saison, Monatsspalten, Summen, Bestand, Umsatz, EK). Trigger: wenn der User eine Excel mit Verkaufs-/Bestandsdaten analysieren will, Begriffe wie 'Verkaufsanalyse', 'Sell-Through', 'Ladenhüter', 'Bestandsanalyse', 'Margenanalyse' verwendet, oder eine Datei mit Spalten wie 'Verkaufte Summe', 'Lagerbestand', 'Total sales', 'EK' referenziert."
---

# Sales Analytics Skill

Analysiert Verkaufs- und Bestandsdaten aus Excel/CSV und generiert einen mehrteiligen Analyse-Report.

## Spalten-Erkennung

Der Skill erkennt automatisch folgende Spaltentypen aus der Header-Zeile:

| Spaltentyp | Erkennungsmuster |
|---|---|
| SKU | `SKU`, `Artikelnummer`, `EAN`, `GTIN` |
| Produkt | `Product title`, `Artikelbezeichnung`, `Produktname` |
| Variante | `Variant`, `Größe`, `Farbe` |
| Saison | `Saison`, `Season`, `Kollektion` |
| Monatsspalten | ISO-Format `YYYY-MM` oder `Jan 25`, `Feb 25` etc. |
| Verkauft | `Verkaufte Summe`, `Sold`, `Qty Sold` |
| Bestand | `Lagerbestand`, `Stock`, `Inventory`, `On Hand` |
| Umsatz | `Total sales`, `Revenue`, `Umsatz`, `Erlös` |
| EK | `EK`, `Cost`, `Einkaufspreis`, `COGS` |

Wenn Spalten nicht automatisch erkannt werden, User fragen.

## Analyse-Module

### 1. Überblick (KPIs)
- Umsatz (VK), Verkaufte Stück, Rohertrag, Marge
- Lagerbestand, Gebundenes Kapital (EK-Wert im Lager)
- Ø VK und Ø EK pro Stück
- Monatliche Verkaufszahlen mit geschätztem Monatsumsatz

### 2. Produktanalyse
Jedes Produkt (gruppiert nach Produkttitel) mit:
- Verkauft, Bestand, Umsatz, EK gesamt, Rohertrag
- **Marge** = (Umsatz - EK) / Umsatz
- **Sell-Through Rate (STR)** = Verkauft / (Verkauft + Bestand)
- **Ø VK** = Umsatz / Verkauft
- Retouren (negative Monatswerte) und Retourenquote
- **Automatische Bewertung:**
  - `Nachbestellen` → STR ≥ 70% UND Marge ≥ 40% UND ≥ 3 verkauft
  - `Auslisten` → 0 Verkäufe bei Bestand > 0
  - `Rabattieren` → STR < 25% bei Bestand ≥ 5
  - `Retoure prüfen` → Retourenquote ≥ 40% bei ≥ 2 Retouren
  - `Verlustbringer` → Marge < 0%
  - `OK` → alles andere

### 3. Größenverteilung
- Verkäufe, Anteil, Bestand, Umsatz und Ø VK pro Größe
- Größe wird aus Variant-Spalte extrahiert (letzter Teil nach `/`)

### 4. Saisonvergleich
- Umsatz, Stück, Bestand, Marge, STR und Ø VK pro Saison
- Zeigt welche Kollektionen performen und welche nicht

### 5. Handlungsempfehlungen
- Konkrete Aktionen pro Produkt mit Begründung
- Sortiert nach Priorität: Nachbestellen → Rabattieren → Retoure → Auslisten → Verlust
- Zeigt gebundenes Kapital (EK × Bestand) pro Aktion

### 6. Retouren-Analyse
- Brutto-Verkäufe, Retouren, Netto, Retourenquote
- Nur Produkte mit negativen Monatswerten

## Excel-Output-Formatierung

### Zahlenformate (Deutsch)
- Währung: `#.##0" €"` (ohne Nachkommastellen)
- Ganzzahlen: `#.##0`
- Prozent mit Dezimal: `0,0"%"`
- Prozent ganzzahlig: `0"%"`

### Styling
- **Hintergrund: weiß** (`#FFFFFF`)
- Header: hellgrau (`#F2F2F2`), Aptos 10pt bold
- Body: Aptos 10pt, Textfarbe `#333333`
- Titel: Aptos 14pt bold, `#1a1a1a`
- Farbcodierung Bewertungszeilen:
  - Nachbestellen: `#E6F4EA` (grün), Font `#1e7e34`
  - Rabattieren: `#FEF7E0` (gelb), Font `#b8860b`
  - Auslisten/Verlust/Retoure: `#FCE8E6` (rot), Font `#c62828`
- Borders: `thin`, Farbe `#E0E0E0`
- Spaltenbreiten: Produkt 48, Zahlenspalten 13-14

### Sheets
6 Sheets: `Überblick`, `Produktlinien`, `Größen`, `Saisons`, `Empfehlungen`, `Retouren`

## Berechnungsregeln

```
Rohertrag = Umsatz - (EK × Verkaufte Stück)
Marge = Rohertrag / Umsatz
STR = Verkauft / (Verkauft + Bestand)
Retourenquote = |negative Monatswerte| / positive Monatswerte
Gebundenes Kapital = Bestand × EK pro Stück
Ø VK = Umsatz / Verkaufte Stück
Monatsumsatz (geschätzt) = Σ (Monatsverkäufe × Ø VK pro Produkt)
```

## Wichtig

- Negative Monatswerte = Retouren, nicht Korrekturen
- Produkte ohne EK: User fragen oder aus Marge schätzen
- Monatsspalten können leer (None/0) sein → als 0 behandeln
- Gruppierung immer nach Produkttitel, nicht nach SKU (SKU = Variante)
- Output-Dateiname: `{Markenname}_Analyse.xlsx` im gleichen Verzeichnis wie Input
