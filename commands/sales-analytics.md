---
description: "Analysiert Verkaufs- und Bestandsdaten aus einer Excel/CSV und erstellt einen 6-Sheet Analyse-Report mit KPIs, Produktbewertung, Größenverteilung, Saisonvergleich, Handlungsempfehlungen und Retouren-Analyse."
allowed-tools:
  ["Read", "Write", "Edit", "Glob", "Grep", "Bash"]
---

# /sales-analytics

Erstelle eine umfassende Verkaufs- und Bestandsanalyse aus einer Excel- oder CSV-Datei.

## Ablauf

### Schritt 1: Datei identifizieren

Frage den User nach der Datei, falls nicht als Argument übergeben. Akzeptiere:
- Dateipfad als Argument: `/sales-analytics /pfad/zur/datei.xlsx`
- Drag & Drop einer Datei
- Dateiname im aktuellen Verzeichnis

### Schritt 2: Spalten erkennen

Lese die Datei mit openpyxl (xlsx) oder csv (csv/tsv). Erkenne automatisch:

| Spaltentyp | Muster |
|---|---|
| SKU | `SKU`, `Artikelnummer`, `EAN`, `GTIN`, `variant SKU` |
| Produkt | `Product title`, `Artikelbezeichnung`, `Produktname`, `Artikel` |
| Variante | `Variant`, `Größe`, `Farbe`, `variant title` |
| Saison | `Saison`, `Season`, `Kollektion` |
| Monatsspalten | `YYYY-MM` Format oder `Jan 25`, `Feb 25` |
| Verkauft | `Verkaufte Summe`, `Sold`, `Qty Sold`, `Menge` |
| Bestand | `Lagerbestand`, `Stock`, `Inventory`, `On Hand` |
| Umsatz | `Total sales`, `Revenue`, `Umsatz`, `Erlös` |
| EK | `EK`, `Cost`, `Einkaufspreis`, `COGS` |

Falls Spalten nicht erkannt werden: User fragen welche Spalte was ist.

### Schritt 3: Markenname extrahieren

Extrahiere den Markennamen aus:
1. Dateiname (z.B. `Genesis Verkauf...` → `Genesis`)
2. Oder frage den User

### Schritt 4: Analyse durchführen

Verwende Python mit openpyxl. Führe ALLE folgenden Analysen durch:

#### 4.1 KPIs berechnen
```
Umsatz (VK) = Σ Total_sales
Verkaufte Stück = Σ Verkaufte_Summe
Rohertrag = Umsatz - Σ(EK × Verkaufte_Summe)
Marge = Rohertrag / Umsatz
Lagerbestand = Σ Lagerbestand
Gebundenes Kapital = Σ(Lagerbestand × EK)
Ø VK = Umsatz / Verkaufte Stück
Ø EK Lager = Gebundenes Kapital / Lagerbestand
```

#### 4.2 Monatliche Verkäufe
Für jede erkannte Monatsspalte:
- Stückzahl = Summe aller positiven Werte
- Geschätzter Umsatz = Σ(Monatsmenge × Ø VK pro Produkt)

#### 4.3 Produktanalyse (gruppiert nach Produkttitel)
Pro Produkt:
- Verkauft, Bestand, Umsatz, EK gesamt, Rohertrag
- Marge = (Umsatz - EK) / Umsatz
- STR = Verkauft / (Verkauft + Bestand)
- Ø VK = Umsatz / Verkauft
- Retouren = Summe negativer Monatswerte
- Retourenquote = |Retouren| / Brutto-Verkäufe

Automatische Bewertung:
- **Nachbestellen**: STR ≥ 70% UND Marge ≥ 40% UND ≥ 3 verkauft
- **Auslisten**: 0 Verkäufe bei Bestand > 0
- **Rabattieren**: STR < 25% bei Bestand ≥ 5
- **Retoure prüfen**: Retourenquote ≥ 40% bei ≥ 2 Retouren
- **Verlustbringer**: Marge < 0%
- **OK**: alles andere

#### 4.4 Größenverteilung
Größe aus Variant-Spalte extrahieren (letzter numerischer Teil).
Pro Größe: Verkauft, Anteil, Bestand, Umsatz, Ø VK.

#### 4.5 Saisonvergleich
Pro Saison: Umsatz, Stück, Bestand, Marge, STR, SKUs, Ø VK.

#### 4.6 Handlungsempfehlungen
Alle Produkte mit Bewertung ≠ OK auflisten mit:
- Aktion, Produkt, Begründung, Bestand, EK gebunden
- Sortiert: Nachbestellen → Rabattieren → Retoure → Auslisten → Verlust

#### 4.7 Retouren
Nur Produkte mit negativen Monatswerten:
- Brutto-Verkäufe, Retouren, Netto, Retourenquote

### Schritt 5: Excel generieren

Erstelle die Datei `{Markenname}_Analyse.xlsx` im gleichen Verzeichnis wie die Input-Datei.

**6 Sheets**: Überblick, Produktlinien, Größen, Saisons, Empfehlungen, Retouren

**Formatting-Regeln:**
- Hintergrund: weiß (#FFFFFF)
- Header: hellgrau (#F2F2F2), Font Aptos 10pt bold
- Titel: Aptos 14pt bold, #1a1a1a
- Body: Aptos 10pt, #333333
- Muted: #888888
- Positiv: #1e7e34 (grün)
- Negativ: #c62828 (rot)
- Warnung: #b8860b (gelb)
- Borders: thin, #E0E0E0

**Zahlenformate (Deutsch):**
- Währung: `#.##0" €"` (ganzzahlig, Punkt als Tausender)
- Ganzzahlen: `#.##0`
- Prozent: `0,0"%"` oder `0"%"`

**Farbcodierung Bewertungszeilen:**
- Nachbestellen: Hintergrund #E6F4EA
- Rabattieren: Hintergrund #FEF7E0
- Auslisten/Verlust/Retoure: Hintergrund #FCE8E6

### Schritt 6: Zusammenfassung

Zeige dem User eine kurze Text-Zusammenfassung:
1. Die 3 wichtigsten Erkenntnisse
2. Top 3 Cash-Cows (höchster Rohertrag + gute STR)
3. Top 3 Problemkinder (Ladenhüter oder Retouren)
4. Saisonalitäts-Muster (welche Quartale stark/schwach)
5. Gesamtes gebundenes Kapital in Ladenhütern

## Beispielaufruf

```
/sales-analytics /Users/craftongmbh/Downloads/Genesis Verkauf und Bestand 01.01.25-18.03.26_fertig.xlsx
```

## Abhängigkeiten

- Python 3 mit openpyxl (`pip install openpyxl` falls nicht vorhanden)
- Nutzt den `sales-analytics` Skill für Berechnungslogik und Formatierung
