# Social Media Dashboard Update

Aktualisiert das Social Media Dashboard in Notion mit den neuesten KPI-Daten und Shopify Kunden.

## Optionen

| Modus | Beschreibung |
|-------|--------------|
| **Standard** | Daten aus Notion DB holen und Dashboard aktualisieren |
| `--live` | Live-Daten von Instagram/TikTok via Browser holen, DB updaten, Dashboard aktualisieren |
| `--verify` | Nur Live-Daten pruefen ohne DB/Dashboard zu aendern |
| `--shopify` | Shopify Kundendaten aktualisieren |

## Accounts

| Account | Plattform | URL |
|---------|-----------|-----|
| Shoes Please Studio | Instagram | instagram.com/shoespleasestudio |
| Shoes Please Rostock | Instagram | instagram.com/shoes.please.rostock |
| Jeans & Co | Instagram | instagram.com/jeansandco.de |
| Shoes Please TikTok | TikTok | tiktok.com/@shoespleasestudio |
| Jeans & Co TikTok | TikTok | tiktok.com/@jeansandcozwickau |

## Workflow

### 1. Daten abrufen

**Option A: Aus Notion DB (Standard)**
```
notion-search mit data_source_url: collection://5570f462-1747-43c3-82f0-b7fdb290261f
```

**Option B: Live via Browser (--live)**
1. Browser Tab oeffnen mit `tabs_context_mcp` und `tabs_create_mcp`
2. Instagram-Profile besuchen und Screenshot machen:
   - Follower, Following, Posts aus Header extrahieren
3. TikTok-Profile besuchen:
   - Gefolgt, Follower, Gefaellt mir aus Header extrahieren
4. Neue Eintraege in Notion DB erstellen mit `notion-create-pages`

### 2. Metriken berechnen

Fuer jeden Account (aktuell vs. Vorwoche):
- **Follower Growth**: absolut und prozentual
- **Posts neu**: Differenz der Post-Anzahl
- **FF-Ratio**: Following / Follower
- **Likes Gesamt Change** (TikTok)

Aggregationen:
- Instagram gesamt vs. TikTok gesamt
- Gesamtsumme aller Accounts
- Best Performer identifizieren

### 3. Dashboard aktualisieren

```
notion-update-page mit:
- page_id: 2f3da9d3ee72815d968accb6e8fd6185
- command: replace_content_range
- selection_with_ellipsis: "> 📊 **Social Med...## 🗂️ Alle Daten"
```

**Dashboard-Struktur:**
```
📊 Header-Callout (Datum, Update-Info)
───
🌐 Gesamtuebersicht (Tabelle mit Vorwoche)
───
📱 Account-Details (5x farbige Callouts mit Tabellen)
   📸 Shoes Please Studio {color="purple"}
   📸 Shoes Please Rostock {color="pink"}
   📸 Jeans & Co {color="orange"}
   🎵 Shoes Please TikTok {color="blue"}
   🎵 Jeans & Co TikTok {color="green"}
───
📈 Wochenvergleich-Tabelle
───
🏷️ Plattform-Vergleich-Tabelle
───
🏆 Best Performer
───
🛍️ Shopify Kunden (Neue Kunden pro Filiale) {color="yellow"}
───
🗂️ Alle Daten (eingebettete DBs bleiben!)
```

**Trend-Indikatoren:**
- 🟢 +X = positiv
- 🔴 -X = negativ
- 🏆 = Top Performer Highlight

## Wichtige IDs

| Ressource | ID |
|-----------|-----|
| Dashboard Page | `2f3da9d3ee72815d968accb6e8fd6185` |
| KPI Database | `371dd3bb99554e8a93f6c074c93e2954` |
| KPI Data Source | `collection://5570f462-1747-43c3-82f0-b7fdb290261f` |
| Shopify Database | `84cf34bba6324c7abd0daa795c999805` |
| Shopify Data Source | `collection://081888c4-78a4-43fb-abf1-c609efa6fed8` |

## Shopify Integration

### Filialen (POS-Tags)

| Tag | Filiale |
|-----|---------|
| POS-SPZ | Zwickau |
| POS-SPW | Warnemuende |
| POS-SPR | Rostock |
| POS-J&C | Jeans & Co |

### Shopify Sync

Via Python-Script:
```bash
cd "/Users/craftongmbh/Downloads/Scraper Social Media/social-media-scraper"
python shopify_sync.py --test    # Test-Modus
python shopify_sync.py           # Produktiv
```

Via Notion MCP (fuer Dashboard-Integration):
```
1. Shopify API abfragen (curl oder Python)
2. Eintraege in Notion erstellen mit notion-create-pages
   parent: {"data_source_id": "081888c4-78a4-43fb-abf1-c609efa6fed8"}
3. Dashboard-Sektion aktualisieren
```

## Live-Daten Extraktion (Browser)

**Instagram** (aus Screenshot):
```
[Posts] Beitraege  [Follower] Follower  [Following] Gefolgt
```

**TikTok** (aus Screenshot):
```
[Following] Gefolgt  [Follower] Follower*innen  [Likes] Gefaellt mir
```

## Beispiel-Ausgabe

Nach dem Update zeigen:

```
✅ Dashboard aktualisiert (05.02.2026)

📊 Zusammenfassung:
| Account | Follower | +/- | Wachstum |
|---------|----------|-----|----------|
| Shoes Please Studio | 3,662 | +18 | +0.49% |
| Shoes Please Rostock | 1,510 | +24 | +1.62% |
| Jeans & Co | 531 | +6 | +1.14% |
| Shoes Please TikTok | 866 | +99 | +12.91% 🏆 |
| Jeans & Co TikTok | 26 | +2 | +8.33% |
| **Gesamt** | **6,595** | **+149** | **+2.31%** |

🏆 Best Performer: Shoes Please TikTok (+12.91%)
📈 TikTok waechst 15x schneller als Instagram

🔗 https://www.notion.so/2f3da9d3ee72815d968accb6e8fd6185
```

## Python Scraper (Alternative)

Falls der Python-Scraper funktioniert:

```bash
cd "/Users/craftongmbh/Downloads/Scraper Social Media/social-media-scraper"
python main.py --dashboard
```

Hinweis: Erfordert funktionierendes SSL und installierte Dependencies (instaloader).
