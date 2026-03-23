# Plakton Scraping-Referenz (Beispiel-Implementierung)

Dieses Dokument zeigt das konkrete Ergebnis einer Scraping-Session für die Marke **Plakton** (spanischer Schuhhersteller). Verwende es als Vorlage für neue Marken.

## Identifizierte Quellen

| Quelle | URL | Qualität | Besonderheit |
|--------|-----|----------|-------------|
| EU Official | eu.plaktonsandals.com | Hoch | Produktnamen, aber keine Modellnummern in URLs |
| Australia | plakton.com.au | Sehr hoch | Vollständige Specs (Material, Sohle, Absatz) |
| USA Official | plaktonfootwear.com | Hoch | Pflegehinweise, Brand-Info |
| shoesplease.de | shoesplease.de | Mittel | DE-Daten, aber JS-heavy |
| GDC Boutique | gdcboutique.com | Hoch | FR → Materialangaben komplett |
| Robin Elt Shoes | robineltshoes.co.uk | Hoch | UK → detaillierte Beschreibungen |
| Plakton UK | plakton.co.uk | Hoch | EN → Gewicht, Zertifikate |

## Scraping-Ergebnisse nach Modell

### Modell 575080 (Mam Alou - Damen-Sandale)
- **Typ:** Sandale mit überkreuzten Riemen
- **Obermaterial:** Premium-Leder
- **Sohle:** Kork mit synthetischer Basis
- **Innensohle:** Konturierte Bios-Einlegesohle
- **Verschluss:** Klettverschluss (Hook-and-loop)
- **Absatz:** 1.5 cm
- **Zehenform:** Rund
- **Quelle:** plakton.com.au

### Modell 180010 (Beta - Damen-Sandale)
- **Typ:** Zwei-Riemen-Slide-Sandale
- **Obermaterial:** Hochwertiges Leder
- **Sohle:** Kork
- **Futter:** Weiches Leder (atmungsaktiv)
- **Verschluss:** Schnalle (individuell verstellbar)
- **Absatz:** 2.5 cm
- **Technologie:** Memory Cushion
- **Quelle:** shoesunlimited.co.nz

### Modell 181539 (Blogg - Pantolette/Mule)
- **Typ:** Mule/Pantolette
- **Obermaterial:** Leder (verschiedene Ausführungen)
- **Sohle:** Gummi
- **Futter:** Weiches Textil
- **Innensohle:** Anatomische Leder-Einlegesohle
- **Verschluss:** Schnalle
- **Quelle:** gdcboutique.com

### Modell 181671 (Bolero - Zehentrenner)
- **Typ:** Thong Sandal / Zehentrenner
- **Obermaterial:** Premium-Leder (Metallic-Finish möglich)
- **Sohle:** Kork mit EVA-Laufsohle
- **Verschluss:** Verstellbare Schnalle
- **Absatz:** 2.5 cm
- **Technologie:** Memory Cushion
- **Quelle:** plakton.com.au

### Modell 760010 (Wanda - EVA Slide)
- **Typ:** Ultraleichte wasserfeste Pantolette
- **Material:** Ökologisch recycelbares EVA
- **Sohle:** EVA (rutschfest)
- **Verschluss:** Doppelschnalle
- **Absatz:** 2.0 cm
- **Gewicht:** 200g pro Schuh
- **Zertifikat:** INESCOP (Qualität + Vegan)
- **Besonderheit:** Vegan, Antibakteriell, Wasserfest
- **Quelle:** eu.plaktonsandals.com, plakton.co.uk

### Modell 175857 (Barna - Herren-Sandale)
- **Typ:** Herren Zwei-Riemen-Sandale
- **Obermaterial:** Weiches Leder / Nubuk
- **Sohle:** Synthetik mit Plakton-Grip
- **Futter:** Leder
- **Verschluss:** Metallschnalle (nickelfrei)
- **Technologie:** Memory Cushion mit Memory-Schaum
- **Quelle:** plakton.com.au, plakton.fr

### Modell 126095 (Poli - Kinder-Sandale)
- **Typ:** Kinder-Sandale
- **Obermaterial:** Hochwertiges Leder
- **Sohle:** Kork mit synthetischer Laufsohle
- **Verschluss:** 2x Schnalle + 1x Klettverschluss
- **Innensohle:** Leder mit Memory Cushion
- **Absatz:** 1.5 cm
- **Größen:** 24-35
- **Quelle:** bergfreunde.eu, winkids.it

## Pflegehinweise (Brand-weit)

### Leder-Produkte
> Leder regelmäßig mit geeignetem Leder-Reiniger pflegen. Nicht längere Zeit
> Wasser aussetzen. Bei Nässe an einem schattigen, belüfteten Ort
> lufttrocknen lassen. Nicht in direktes Sonnenlicht, an Heizkörper oder
> Heizungen stellen. In kühler, trockener Umgebung im Originalkarton oder
> Baumwollbeutel aufbewahren. Regelmäßig Leder-Conditioner auftragen.

### EVA-Produkte (Wanda-Linie)
> Mit einem feuchten Tuch abwischen. Wasserfest – kann nach dem Tragen
> einfach abgespült werden. An der Luft trocknen lassen. Nicht in der
> Waschmaschine waschen.

**Quelle:** plaktonfootwear.com/blogs/oak-sandals/how-to-care-for-your-cork-sandals

## Farbmapping (Plakton-spezifisch)

| Spanisch (Plakton) | Zalando-Code | Anmerkung |
|---------------------|-------------|-----------|
| negro | schwarz | |
| camello | beige | Kamelfarben |
| leno | braun | Hellbraun |
| cuero | braun | "Leder"-Farbe |
| mushroom | beige | Pilz/Champignon |
| military | gruen | Olivgrün |
| roose | rosa | Nicht "rose" |
| plata | silber | Metallic |
| grafito | grau | Dunkelgrau metallic |
| antique | braun | Vintage-Braun |
| fuxia | rosa | Nicht "fuchsia" |
| plomo | grau | Bleigrau |
| ligh khaki | gruen | Typo im System! |
| moresco | braun | Maurisch-Braun |
| trebol | gruen | Kleeblatt-Grün |

## Kategorie-Zuordnung

| Modellname | Zalando-Kategorie | Begründung |
|-----------|-------------------|-----------|
| Mam Alou, Mam Coco, Mam Vali, Mam Vita, Mam Ambo, Mam Date | Sandalen | Riemchensandalen |
| Bibi, Beta, Bala, Bom | Sandalen | Offene Sandalen |
| Bolero, Zomba | Sandalen | Zehentrenner |
| Bis 3 | Sandalen | Ledersandale mit Riemen |
| Blogg, Blog, Bloggie | Pantoletten | Mules/Clogs |
| Wanda | Pantoletten | EVA-Slides |
| Benito | Pantoletten | Herren-Slides |
| Barna | Sandalen | Herren-Sandale |
| Poli | Sandalen | Kinder-Sandale |
