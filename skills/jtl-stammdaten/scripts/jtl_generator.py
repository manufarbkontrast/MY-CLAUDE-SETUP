#!/usr/bin/env python3
"""
JTL Stammdaten-Generator
Erstellt JTL-Einspieltabellen und Bestellmengen-CSVs aus Hersteller-Orderfiles.

Usage:
    python3 jtl_generator.py --saison HW --jahr 2026 --input datei.xlsx --output ./out/ [--marke auto]
"""

import argparse
import csv
import os
import re
import sys
from collections import OrderedDict
from datetime import date
from typing import Any, Dict, List, Optional, Tuple

# ============================================================
# CONSTANTS
# ============================================================

CSV_HEADER = [
    "Artikelnummer (Lieferant)", "HAN", "Lieferant", "Kategorie Ebene 1",
    "Kategorie Ebene 2", "Warengruppe", "Artikelnummer", "GTIN",
    "Identifizierungsspalte Vaterartikel", "Artikelname",
    "Brutto-VK", "UVP", "Durchschnittlicher Einkaufspreis (netto)", "Netto-EK",
    "Artikel aktiv", "UPC", "Hersteller", "Bestandsführung aktiv",
    "Mindestabnahme", "Artikelgewicht", "Herkunftsland", "TARIC-Code",
    "Variationswert 1", "Variationswert 2", "Sortiernummer Variationswert 2",
    "Variationsname 1", "Variationsname 2", "Artikelname (Lieferant)",
    "Jeans&co aktiv Y (YES) oder N (NO)",
    "Shoespleas aktiv Y (YES) oder N (NO)",
    "Hatup aktiv Y (YES) oder N (NO)",
    "Beschreibung", "URL-Pfad", "Titel-Tag (SEO)", "Meta-Description (SEO)",
]

COUNTRY_MAP = {
    "JAPAN": "JP", "INDIA": "IN", "CHINA": "CN", "CINA": "CN",
    "PORTUGAL": "PT", "ITALY": "IT", "ITALIEN": "IT",
    "SPAIN": "ES", "SPANIEN": "ES",
    "TURKEY": "TR", "TÜRKEI": "TR", "TÜRKIYE": "TR",
    "BANGLADESH": "BD", "GERMANY": "DE", "DEUTSCHLAND": "DE",
    "FRANCE": "FR", "FRANKREICH": "FR",
    "VIETNAM": "VN", "INDONESIA": "ID", "THAILAND": "TH",
    "MOROCCO": "MA", "MAROKKO": "MA",
    "CAMBODIA": "KH", "KAMBODSCHA": "KH",
    "PAKISTAN": "PK", "ROMANIA": "RO", "RUMÄNIEN": "RO",
    "POLAND": "PL", "POLEN": "PL",
    "UNITED KINGDOM": "GB", "USA": "US", "UNITED STATES": "US",
    "SERBIA": "RS", "SERBIEN": "RS",
    "TUNISIA": "TN", "TUNESIEN": "TN",
}

PRICE_STEPS = [
    (14.99, "9,99"), (24.99, "19,99"), (34.99, "29,99"), (44.99, "39,99"),
    (54.99, "49,99"), (64.99, "59,99"), (74.99, "69,99"), (84.99, "79,99"),
    (94.99, "89,99"), (104.99, "99,99"), (114.99, "109,99"), (124.99, "119,99"),
    (139.99, "129,99"), (159.99, "149,99"), (179.99, "169,99"), (194.99, "189,99"),
    (224.99, "199,99"), (274.99, "249,99"), (999999, "299,99"),
]

TEXTILE_SORT = {"XS": "1", "S": "2", "M": "3", "L": "4", "XL": "5", "XXL": "6", "3XL": "7", "ONESIZE": "8"}
TROUSER_SORT = {str(i): str(i - 27) for i in range(28, 37)}
SHOE_SORT = {str(s): str(i + 1) for i, s in enumerate(range(35, 49))}

BRAND_CONFIG = {
    "UNIVERSAL": {
        "hersteller": "UNIVERSAL", "code": "UNIV",
        "kategorie1": "Shopify Shoesplease", "kategorie2": "Shopify - nur POS",
        "warengruppe_default": "Bekleidung", "shop_col": "shoesplease",
        "herkunft": "Großbritannien",
        "seo_intro": "Universal Works steht für zeitlose britische Menswear aus Nottingham. "
                     "Inspiriert von traditioneller Arbeitskleidung, verbindet die Marke robuste "
                     "Materialien mit modernem Design.",
    },
    "GIOVE": {
        "hersteller": "GIOVE", "code": "GIOV",
        "kategorie1": "Shopify Shoesplease", "kategorie2": "Shopify - nur POS",
        "warengruppe_default": "Schuhe", "shop_col": "shoesplease",
        "herkunft": "Italien",
        "seo_intro": "Giove vereint italienische Schuhkunst mit zeitgemäßem Design. "
                     "Hochwertige Materialien und sorgfältige Verarbeitung garantieren "
                     "Komfort und Langlebigkeit.",
    },
    "PEDRO MIRALLES": {
        "hersteller": "PEDRO MIRALLES", "code": "PEDR",
        "kategorie1": "Shopify Shoesplease", "kategorie2": "Shopify - nur POS",
        "warengruppe_default": "Schuhe", "shop_col": "shoesplease",
        "herkunft": "Spanien",
        "seo_intro": "Pedro Miralles ist eine spanische Premium-Schuhmarke, die modernes "
                     "Design mit traditioneller Handwerkskunst verbindet. Edles Leder und "
                     "feminine Silhouetten zeichnen die Kollektion aus.",
    },
    "ILSE JACOBSEN": {
        "hersteller": "ILSE JACOBSEN", "code": "ILSE",
        "kategorie1": "Shopify Shoesplease", "kategorie2": "Shopify - nur POS",
        "warengruppe_default": "Schuhe", "shop_col": "shoesplease",
        "herkunft": "Dänemark",
        "seo_intro": "Ilse Jacobsen verbindet skandinavisches Design mit Funktionalität. "
                     "Die dänische Marke ist bekannt für stilvolle Gummistiefel und "
                     "wetterfeste Schuhe mit nordischem Charme.",
    },
    "VOILE BLANCHE": {
        "hersteller": "VOILE BLANCHE", "code": "VOIL",
        "kategorie1": "Shopify Shoesplease", "kategorie2": "Shopify - nur POS",
        "warengruppe_default": "Schuhe", "shop_col": "shoesplease",
        "herkunft": "Italien",
        "seo_intro": "Voile Blanche steht für italienische Sneaker-Kultur auf höchstem Niveau. "
                     "Seit den 1990er Jahren verbindet die Marke aus dem Veneto hochwertige "
                     "Materialien mit urbanem Design und handwerklicher Perfektion.",
    },
    "DATE": {
        "hersteller": "D.A.T.E.", "code": "DATE",
        "kategorie1": "Shopify Shoesplease", "kategorie2": "Shopify - nur POS",
        "warengruppe_default": "Schuhe", "shop_col": "shoesplease",
        "herkunft": "Italien",
        "seo_intro": "D.A.T.E. steht für Design Art Technology Emotion und vereint "
                     "italienische Handwerkskunst mit innovativem Sneaker-Design. "
                     "Seit 2005 begeistert die Marke mit hochwertigen Materialien und urbanem Style.",
    },
    "PORTUGUESE FLANNEL": {
        "hersteller": "PORTUGUESE FLANNEL", "code": "PTFL",
        "kategorie1": "Shopify Shoesplease", "kategorie2": "Shopify - nur POS",
        "warengruppe_default": "Bekleidung", "shop_col": "shoesplease",
        "herkunft": "Portugal",
        "seo_intro": "Portuguese Flannel ist eine portugiesische Marke, die für ihre lässigen "
                     "Hemden und Freizeitmode bekannt ist. Inspiriert von der atlantischen "
                     "Küstenkultur, setzt die Marke auf hochwertige Stoffe und entspannte Schnitte.",
    },
    "CLOSED": {
        "hersteller": "CLOSED", "code": "CLOS",
        "kategorie1": "Shopify Shoesplease", "kategorie2": "Shopify - nur POS",
        "warengruppe_default": "Bekleidung", "shop_col": "shoesplease",
        "herkunft": "Deutschland",
        "seo_intro": "CLOSED steht für zeitlose Mode aus Hamburg mit italienischer Fertigung. "
                     "Die Marke verbindet nachhaltige Materialien mit modernem Design und "
                     "ist bekannt für ihre perfekt sitzenden Jeans und Casual Wear.",
    },
    "ARMED ANGELS": {
        "hersteller": "ARMEDANGELS", "code": "ARMA",
        "kategorie1": "Shopify Shoesplease", "kategorie2": "Shopify - nur POS",
        "warengruppe_default": "Bekleidung", "shop_col": "shoesplease",
        "herkunft": "Deutschland",
        "seo_intro": "ARMEDANGELS ist eine nachhaltige Modemarke aus Köln, die faire "
                     "Produktion und ökologische Materialien in den Mittelpunkt stellt. "
                     "Zeitlose Designs treffen auf verantwortungsvolle Mode.",
    },
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def round_uvp(raw_price):
    # type: (Any) -> str
    """UVP-Preisrundung nach Preistreppe."""
    if raw_price is None or raw_price == "":
        return ""
    try:
        price = float(str(raw_price).replace(",", "."))
    except (ValueError, TypeError):
        return ""
    for threshold, rounded in PRICE_STEPS:
        if price <= threshold:
            return rounded
    return "299,99"


def to_german_decimal(value):
    # type: (Any) -> str
    """Number -> deutsches Dezimalformat (Komma)."""
    if value is None or value == "":
        return ""
    try:
        return f"{float(str(value).replace(',', '.')):.2f}".replace(".", ",")
    except (ValueError, TypeError):
        return str(value).replace(".", ",")


def to_german_weight(value):
    # type: (Any) -> str
    """Gewicht -> deutsches Format; Standard 2 kg wenn leer."""
    if value is None or value == "":
        return "2"
    try:
        num = float(str(value).replace(",", "."))
        return "2" if num == 0 else f"{num}".replace(".", ",")
    except (ValueError, TypeError):
        return "2"


def clean_taric(code):
    # type: (Any) -> str
    """TARIC ohne Punkte, max 8 Stellen."""
    if code is None or code == "":
        return ""
    return str(code).replace(".", "").strip()[:8]


def country_to_iso(name):
    # type: (Any) -> str
    """Laendername -> 2-Buchstaben ISO-Code."""
    if name is None:
        return ""
    n = str(name).strip().upper()
    if len(n) == 2 and n.isalpha():
        return n
    return COUNTRY_MAP.get(n, n)


def normalize_size(size_str):
    # type: (Any) -> str
    """OS -> ONESIZE."""
    s = str(size_str).strip()
    return "ONESIZE" if s.upper() == "OS" else s


def ensure_gtin_13(ean):
    # type: (Any) -> str
    """GTIN immer 13-stellig."""
    if not ean:
        return ""
    s = str(ean).strip()
    if "." in s:
        s = s.split(".")[0]
    if "E" in s.upper():
        try:
            s = str(int(float(ean)))
        except (ValueError, TypeError):
            pass
    if len(s) == 12:
        return "0" + s
    return s


def make_upc(ean):
    # type: (Any) -> str
    """UPC = EAN unveraendert (max 13 Stellen). Keine fuehrende 0 hinzufuegen."""
    if not ean:
        return ""
    s = str(ean).strip()
    if "." in s:
        s = s.split(".")[0]
    if "E" in s.upper():
        try:
            s = str(int(float(ean)))
        except (ValueError, TypeError):
            pass
    return s


def get_size_sort(size_str, warengruppe=""):
    # type: (str, str) -> str
    """Sortiernummer nach Groessentyp."""
    s = str(size_str).strip().upper()
    if s in TEXTILE_SORT:
        return TEXTILE_SORT[s]
    if warengruppe == "Schuhe" and s in SHOE_SORT:
        return SHOE_SORT[s]
    if s in TROUSER_SORT:
        return TROUSER_SORT[s]
    if s in SHOE_SORT:
        return SHOE_SORT[s]
    return ""


def shop_activation(shop_col):
    # type: (str) -> Tuple[str, str, str]
    """Shop-Aktivierungsspalten basierend auf Kategorie."""
    return {
        "jeansco": ("Y", "", ""),
        "shoesplease": ("", "Y", ""),
        "hatup": ("", "", "Y"),
    }.get(shop_col, ("", "", ""))


def safe_color(color):
    # type: (str) -> str
    """Ensure color is never empty -- Shopify requires a non-empty option value."""
    c = str(color).strip() if color else ""
    return c if c else "uni"


def slugify(text):
    # type: (str) -> str
    """Convert text to URL-friendly slug."""
    s = str(text).lower().strip()
    s = s.replace("ae", "ae").replace("oe", "oe").replace("ue", "ue").replace("ss", "ss")
    s = s.replace("\u00e4", "ae").replace("\u00f6", "oe").replace("\u00fc", "ue").replace("\u00df", "ss")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def make_seo_beschreibung(brand_cfg, modellname, warengruppe, farbe):
    # type: (Dict[str, Any], str, str, str) -> str
    """Generate a short SEO product description in SHOES.PLEASE. style."""
    hersteller = brand_cfg["hersteller"]

    if warengruppe == "Schuhe":
        templates = [
            (
                f"{hersteller} pr\u00e4sentiert mit dem {modellname} einen Schuh, der Komfort und Stil vereint. "
                f"Die hochwertige Verarbeitung sorgt f\u00fcr ein angenehmes Tragegef\u00fchl den ganzen Tag. "
                f"Ob zum sportlichen Outfit oder als cooler Kontrast zum femininen Look \u2013 "
                f"mit diesem Schuh liegt Ihr immer richtig. Entdeckt jetzt Euer neues Lieblingspaar!"
            ),
            (
                f"{hersteller} pr\u00e4sentiert den {modellname}! "
                f"Ein absoluter Hingucker f\u00fcr alle modebewussten Frauen und M\u00e4nner. "
                f"Perfekt f\u00fcr den Alltag oder besondere Anl\u00e4sse \u2013 "
                f"dieser Schuh bietet h\u00f6chsten Tragekomfort und einzigartigen Stil. "
                f"Ein Must-have f\u00fcr jede Schuhsammlung!"
            ),
            (
                f"Frischer Wind f\u00fcr Eure Schuhgarderobe! {hersteller} pr\u00e4sentiert mit dem {modellname} "
                f"einen angesagten Schuh. Die Farbgebung ist vielseitig kombinierbar. "
                f"Ob zum sportlichen Outfit oder als Hingucker zum Kleid \u2013 "
                f"mit diesem Schuh seid Ihr stilsicher unterwegs!"
            ),
        ]
    elif warengruppe == "Accessoires":
        templates = [
            (
                f"{hersteller} pr\u00e4sentiert die {modellname}! "
                f"Ein stylisches Accessoire, das Eurem Outfit das gewisse Etwas verleiht. "
                f"Hochwertige Materialien und durchdachtes Design machen dieses St\u00fcck "
                f"zum perfekten Begleiter f\u00fcr jeden Tag."
            ),
            (
                f"Das perfekte Accessoire f\u00fcr jeden Anlass! {hersteller} pr\u00e4sentiert die {modellname}. "
                f"Funktional und stilvoll zugleich \u2013 ein echtes Highlight f\u00fcr alle, "
                f"die Wert auf Qualit\u00e4t und Design legen."
            ),
        ]
    else:  # Bekleidung
        templates = [
            (
                f"{hersteller} pr\u00e4sentiert das {modellname}! "
                f"Hochwertige Materialien und eine sorgf\u00e4ltige Verarbeitung machen dieses St\u00fcck "
                f"zum idealen Begleiter. Ob l\u00e4ssig im Alltag oder schick zum Ausgehen \u2013 "
                f"mit diesem Teil seid Ihr immer bestens angezogen."
            ),
            (
                f"Zeitloser Style von {hersteller}! Das {modellname} \u00fcberzeugt durch "
                f"erstklassige Qualit\u00e4t und modernes Design. "
                f"Vielseitig kombinierbar und perfekt f\u00fcr jede Gelegenheit. "
                f"Entdeckt jetzt Euer neues Lieblingsst\u00fcck!"
            ),
        ]

    idx = sum(ord(c) for c in modellname) % len(templates)
    return templates[idx]


def make_seo_fields(brand_cfg, artikelname, warengruppe, farbe=""):
    # type: (Dict[str, Any], str, str, str) -> Tuple[str, str, str, str]
    """Generate Beschreibung, URL-Pfad, Titel-Tag and Meta-Description for Vaterartikel."""
    hersteller = brand_cfg["hersteller"]
    beschreibung = make_seo_beschreibung(brand_cfg, artikelname, warengruppe, farbe)
    url_pfad = slugify(f"{hersteller} {artikelname}")
    titel_tag = f"{hersteller} {artikelname} | SHOES.PLEASE."
    wg = warengruppe if warengruppe else "Produkte"
    meta_desc = (
        f"{hersteller} {artikelname} jetzt online bei SHOES.PLEASE. kaufen. "
        f"Premium {wg} \u2713 Schneller Versand \u2713 Einfache Retoure \u2713 Top Preise"
    )
    return beschreibung, url_pfad, titel_tag, meta_desc


def build_han(saison, jahr):
    # type: (str, str) -> str
    """HAN aus Saison + Jahr: z.B. HW + 2026 -> 2026HW."""
    return f"{jahr}{saison.upper()}"


def make_date_suffix():
    # type: () -> str
    """Aktuelles Datum als dd_mm_yy."""
    return date.today().strftime("%d_%m_%y")


# ============================================================
# CSV WRITERS
# ============================================================

def write_einspieltabelle(filepath, rows):
    # type: (str, List[List[Any]]) -> int
    """Schreibt die Einspieltabelle CSV (UTF-8 mit BOM fuer Excel)."""
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(CSV_HEADER)
        for row in rows:
            writer.writerow(row)
    return len(rows)


def write_bestellmengen(filepath, rows):
    # type: (str, List[List[Any]]) -> int
    """Schreibt die Bestellmengen CSV (UTF-8 mit BOM fuer Excel)."""
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["EAN", "Bestellmenge", "Netto-EK"])
        for row in rows:
            writer.writerow(row)
    return len(rows)


# ============================================================
# ROW BUILDERS -- 35-column format with SEO fields
# ============================================================

def _vater_row(
    art_lief, han, cfg, wg, vater_nr, aname, uvp, ek,
    weight, country, taric, farbe, aname_lief,
    jc, sp, hu, beschreibung, url_pfad, titel_tag, meta_desc,
):
    # type: (...) -> List[Any]
    """Erstellt eine Vaterartikel-Zeile (35 Spalten)."""
    return [
        art_lief, han, cfg["hersteller"], cfg["kategorie1"], cfg["kategorie2"],
        wg, vater_nr, "",
        "",  # Identifizierungsspalte Vaterartikel (leer = ist Vater)
        aname, uvp, uvp, ek, ek, "Y", "",
        cfg["hersteller"], "Y", "1", weight, country, taric,
        farbe, "", "", "Farbe", "Gr\u00f6\u00dfe", aname_lief,
        jc, sp, hu,
        beschreibung, url_pfad, titel_tag, meta_desc,
    ]


def _kind_row(
    art_lief, han, cfg, wg, kind_nr, gtin, vater_nr, aname, uvp, ek,
    weight, country, taric, farbe, size, sort_nr,
    aname_lief, jc, sp, hu, upc,
):
    # type: (...) -> List[Any]
    """Erstellt eine Kindartikel-Zeile (35 Spalten)."""
    return [
        art_lief, han, cfg["hersteller"], cfg["kategorie1"], cfg["kategorie2"],
        wg, kind_nr, gtin,
        vater_nr,  # Identifizierungsspalte Vaterartikel (gefuellt = Kind)
        aname, uvp, uvp, ek, ek, "Y", upc,
        cfg["hersteller"], "Y", "1", weight, country, taric,
        farbe, size, sort_nr, "Farbe", "Gr\u00f6\u00dfe", aname_lief,
        jc, sp, hu,
        "", "", "", "",
    ]


# ============================================================
# FILE READERS
# ============================================================

def read_xlsx(filepath):
    # type: (str) -> Tuple[List[Any], List[List[Any]]]
    """Read .xlsx file, return (header_row, data_rows)."""
    import openpyxl
    wb = openpyxl.load_workbook(filepath, data_only=True)
    ws = wb.active
    all_rows = list(ws.iter_rows(values_only=True))
    wb.close()
    if not all_rows:
        return [], []
    header = list(all_rows[0])
    data = [list(r) for r in all_rows[1:]]
    return header, data


def read_xls(filepath):
    # type: (str) -> Tuple[List[Any], List[List[Any]]]
    """Read .xls file, return (header_row, all_rows_including_header)."""
    import xlrd
    wb = xlrd.open_workbook(filepath)
    ws = wb.sheet_by_index(0)
    all_rows = []
    for i in range(ws.nrows):
        all_rows.append([ws.cell_value(i, j) for j in range(ws.ncols)])
    wb.release_resources()
    if not all_rows:
        return [], []
    return all_rows[0], all_rows


def read_csv_file(filepath):
    # type: (str) -> Tuple[List[Any], List[List[Any]]]
    """Read CSV file (semicolon or comma delimited), return (header_row, data_rows)."""
    with open(filepath, "r", encoding="utf-8-sig") as f:
        sample = f.read(4096)
        f.seek(0)
        delimiter = ";" if sample.count(";") > sample.count(",") else ","
        reader = csv.reader(f, delimiter=delimiter)
        all_rows = list(reader)
    if not all_rows:
        return [], []
    header = all_rows[0]
    data = all_rows[1:]
    return header, data


def read_source_file(filepath):
    # type: (str) -> Tuple[List[Any], List[List[Any]]]
    """Read any supported file format, return (header_row, data_rows)."""
    ext = os.path.splitext(filepath)[1].lower()
    if ext in (".xlsx", ".xlsm"):
        return read_xlsx(filepath)
    elif ext == ".xls":
        return read_xls(filepath)
    elif ext == ".csv":
        return read_csv_file(filepath)
    else:
        raise ValueError(f"Nicht unterstuetztes Dateiformat: {ext}")


# ============================================================
# BRAND DETECTION
# ============================================================

def detect_brand(filepath):
    # type: (str) -> Optional[str]
    """Erkennt die Marke anhand von Dateiname und Dateiinhalt."""
    fn = os.path.basename(filepath).upper()

    # Filename-based detection
    if "UNIVERSAL" in fn or "UW " in fn or "UW_" in fn:
        return "UNIVERSAL"
    if "PEDRO" in fn or "MIRALLES" in fn or "PEDR" in fn or "EAN13" in fn:
        return "PEDRO MIRALLES"
    if "VOILE" in fn or "BLANCHE" in fn or "BCD_" in fn or "VEORD" in fn:
        return "VOILE BLANCHE"
    if "GIOVE" in fn or "GIO" in fn:
        return "GIOVE"
    if "ILSE" in fn or "JACOBSEN" in fn:
        return "ILSE JACOBSEN"
    if "PORTUGUESE" in fn or "FLANNEL" in fn:
        return "PORTUGUESE FLANNEL"
    if "ARMED" in fn or "ANGEL" in fn or "ARMEDANGEL" in fn:
        return "ARMED ANGELS"
    if "CLOSED" in fn or "OC-" in fn:
        return "CLOSED"
    if "D.A.T.E" in fn or "DATE" in fn or "BARCODE" in fn:
        return "DATE"

    # Content-based detection
    try:
        header, data_rows = read_source_file(filepath)
    except Exception:
        return None

    # Header-based detection
    if header:
        h = " ".join(str(x) for x in header if x).upper()
        if "STYLE" in h and "COLOUR" in h and "BARCODE" in h:
            return "UNIVERSAL"
        if "MODELO" in h and "VARIANTE" in h and "EAN" in h:
            return "PEDRO MIRALLES"
        if "CODICE" in h and "MODELLO" in h and "TAGLIA" in h:
            return "VOILE BLANCHE"
        if "STYLE CODE" in h and "STYLE DESCRIPTION" in h and "EAN CODE" in h:
            return "DATE"
        if "ARTICLE NUMBER" in h and "ARTICLE NAME" in h and "PURCHASE PRICE" in h:
            return "PORTUGUESE FLANNEL"
        if "REC RETAIL PRICE" in h and "EAN NUMBER" in h and "PRODUCT DESCRIPTION" in h:
            return "ILSE JACOBSEN"
        if "ITEM NUMBER" in h and "ITEM DESCRIPTION" in h and "COLOR DESCRIPTION" in h and "PRICE RETAIL" in h:
            return "ARMED ANGELS"
        if "ORDER NO" in h and "SELL PRICE" in h and "TARIC" in h and "COMPOPSITION" in h:
            return "CLOSED"

    # Sample-row-based detection
    sample_rows = data_rows[:5] if data_rows else []
    for row in sample_rows:
        text = " ".join(str(x) for x in row if x).upper()
        if "VOILE BLANCHE" in text:
            return "VOILE BLANCHE"
        if "ILSE JACOBSEN" in text or "HORNB\u00c6K" in text:
            return "ILSE JACOBSEN"
        if "ARMEDANGELS" in text or "ARMED ANGELS" in text:
            return "ARMED ANGELS"

    return None


# ============================================================
# BRAND-SPECIFIC PROCESSORS
# ============================================================

def process_universal_works(filepath, han):
    # type: (str, str) -> Tuple[List[List[Any]], List[List[Any]], str]
    """Verarbeitet Universal Works Excel-Dateien."""
    brand_cfg = dict(BRAND_CONFIG["UNIVERSAL"])
    _header, data_rows = read_xlsx(filepath)

    groups = OrderedDict()  # type: OrderedDict
    for r in data_rows:
        if len(r) < 21 or r[4] is None:
            continue
        key = (str(r[4]).strip(), str(r[6]).strip())
        if key not in groups:
            groups[key] = []
        groups[key].append(r)

    output = []  # type: List[List[Any]]
    orders = []  # type: List[List[Any]]

    for (style, colour), rows in groups.items():
        f = rows[0]
        cat3 = str(f[3]).strip()
        desc = str(f[7]).strip()
        country = str(f[12]).strip()
        hts, weight, ek, rrp = f[13], f[15], f[18], f[19]

        wg = "Accessoires" if cat3.upper() == "BAGS" else "Bekleidung"
        art_lief = f"{style}-{colour}"
        vater_nr = f"{brand_cfg['code']}-{art_lief}"
        sc = safe_color(colour.lower())
        aname = f"{desc} {sc}"
        farbe_lief = colour if colour else sc
        uvp = round_uvp(rrp)
        jc, sp, hu = shop_activation(brand_cfg["shop_col"])
        beschreibung, url_pfad, titel_tag, meta_desc = make_seo_fields(brand_cfg, aname, wg, sc)

        output.append(_vater_row(
            art_lief, han, brand_cfg, wg, vater_nr, aname, uvp,
            to_german_decimal(ek), to_german_weight(weight),
            country_to_iso(country), clean_taric(hts), sc, farbe_lief,
            jc, sp, hu, beschreibung, url_pfad, titel_tag, meta_desc,
        ))

        for r in rows:
            raw_size = str(r[8]).strip() if r[8] else ""
            barcode = str(r[9]).strip() if r[9] else ""
            qty = r[20]
            if not raw_size:
                continue
            size = normalize_size(raw_size)
            gtin = ensure_gtin_13(barcode)
            output.append(_kind_row(
                art_lief, han, brand_cfg, wg,
                f"{brand_cfg['code']}-{art_lief}-{size}", gtin, vater_nr,
                aname, uvp, to_german_decimal(ek), to_german_weight(weight),
                country_to_iso(country), clean_taric(hts), sc, size,
                get_size_sort(size, wg), farbe_lief, jc, sp, hu, make_upc(barcode),
            ))
            if barcode and qty:
                orders.append([gtin, int(qty), to_german_decimal(ek)])

    return output, orders, brand_cfg["code"]


def process_pedro_miralles(filepath, han):
    # type: (str, str) -> Tuple[List[List[Any]], List[List[Any]], str]
    """Verarbeitet Pedro Miralles EAN-Dateien mit Duplikat-Erkennung."""
    brand_cfg = dict(BRAND_CONFIG["PEDRO MIRALLES"])
    _header, data_rows = read_xlsx(filepath)

    groups = OrderedDict()  # type: OrderedDict
    for r in data_rows:
        if r[0] is None:
            continue
        modelo = str(int(r[0])) if isinstance(r[0], (int, float)) else str(r[0]).strip()
        variante = str(r[1]).strip() if r[1] else ""
        color = str(r[2]).strip() if r[2] else ""
        key = (modelo, variante, color)
        if key not in groups:
            groups[key] = []
        ean = str(int(r[12])).strip() if r[12] else ""
        for i, sz in enumerate([37, 38, 39, 40, 41, 42]):
            qty = r[5 + i]
            if qty is not None and qty != "" and float(qty) > 0:
                groups[key].append({"size": str(sz), "qty": int(qty), "ean": ean})
                break

    # Detect duplicate Artikelnames (e.g. two modelos both called "STRASS negro")
    name_counts = {}  # type: Dict[str, int]
    for (modelo, variante, color), _ in groups.items():
        base_name = f"{variante} {color}".strip().lower()
        name_counts[base_name] = name_counts.get(base_name, 0) + 1
    duplicates = {n for n, c in name_counts.items() if c > 1}

    output = []  # type: List[List[Any]]
    orders = []  # type: List[List[Any]]
    jc, sp, hu = shop_activation(brand_cfg["shop_col"])

    for (modelo, variante, color), size_rows in groups.items():
        sc = safe_color(color.lower())
        vater_nr = f"{brand_cfg['code']}-{modelo}-{color}"
        # Bei doppelten Bezeichnungen: Modelo-Nr. vor die Farbe setzen
        base_name = f"{variante} {color}".strip().lower()
        if base_name in duplicates:
            aname = f"{variante} {modelo} {sc}"
        else:
            aname = f"{variante} {sc}"
        farbe_lief = color if color else sc
        beschreibung, url_pfad, titel_tag, meta_desc = make_seo_fields(
            brand_cfg, aname, brand_cfg["warengruppe_default"], sc)

        output.append(_vater_row(
            modelo, han, brand_cfg, brand_cfg["warengruppe_default"],
            vater_nr, aname, "", "", "2", "ES", "", sc, farbe_lief,
            jc, sp, hu, beschreibung, url_pfad, titel_tag, meta_desc,
        ))

        for sr in size_rows:
            gtin = ensure_gtin_13(sr["ean"])
            output.append(_kind_row(
                modelo, han, brand_cfg, brand_cfg["warengruppe_default"],
                f"{brand_cfg['code']}-{modelo}-{color}-{sr['size']}", gtin,
                vater_nr, aname, "", "", "2", "ES", "", sc, sr["size"],
                get_size_sort(sr["size"], "Schuhe"), farbe_lief,
                jc, sp, hu, make_upc(sr["ean"]),
            ))
            if sr["ean"]:
                orders.append([gtin, sr["qty"], ""])

    return output, orders, brand_cfg["code"]


def process_voile_blanche(filepath, han):
    # type: (str, str) -> Tuple[List[List[Any]], List[List[Any]], str]
    """Verarbeitet Voile Blanche .xls-Dateien."""
    brand_cfg = dict(BRAND_CONFIG["VOILE BLANCHE"])
    _header, all_rows = read_xls(filepath)

    # Filter to EAN13 data rows
    data_rows = []  # type: List[List[Any]]
    for r in all_rows:
        if len(r) < 39:
            continue
        if r[0] != "EAN13":
            continue
        ean_val = r[1]
        if not ean_val or (isinstance(ean_val, str) and ean_val.strip() == ""):
            continue
        data_rows.append(r)

    groups = OrderedDict()  # type: OrderedDict
    for r in data_rows:
        articolo = str(r[14]).strip()
        if articolo not in groups:
            groups[articolo] = {"info": r, "sizes": OrderedDict()}

        ean_raw = str(r[1]).strip()
        if "." in ean_raw:
            ean_raw = ean_raw.split(".")[0]
        if "E" in ean_raw.upper():
            try:
                ean_raw = str(int(float(r[1])))
            except (ValueError, TypeError):
                pass

        size = str(r[8]).strip()
        if "." in size:
            size = size.split(".")[0]
        qty = int(r[11]) if r[11] else 0

        if ean_raw not in groups[articolo]["sizes"]:
            groups[articolo]["sizes"][ean_raw] = {"size": size, "qty": 0}
        groups[articolo]["sizes"][ean_raw]["qty"] += qty

    output = []  # type: List[List[Any]]
    orders = []  # type: List[List[Any]]
    jc, sp, hu = shop_activation(brand_cfg["shop_col"])

    for articolo, grp in groups.items():
        r = grp["info"]
        text_modello = str(r[15]).strip()
        text_colore = str(r[17]).strip()
        ek, rrp, taric, origin = r[13], r[38], r[26], str(r[27]).strip()

        vater_nr = f"{brand_cfg['code']}-{articolo}"
        sc = safe_color(text_colore.lower())
        aname = f"{text_modello} {sc}"
        farbe_lief = text_colore if text_colore else sc
        uvp = round_uvp(rrp)

        # Try source columns 47-50, fall back to auto-generated
        src_beschreibung = str(r[47]).strip() if len(r) > 47 and r[47] else ""
        src_url = str(r[48]).strip() if len(r) > 48 and r[48] else ""
        src_titel = str(r[49]).strip() if len(r) > 49 and r[49] else ""
        src_meta = str(r[50]).strip() if len(r) > 50 and r[50] else ""
        gen_beschreibung, gen_url, gen_titel, gen_meta = make_seo_fields(
            brand_cfg, aname, brand_cfg["warengruppe_default"], sc)
        beschreibung = src_beschreibung if src_beschreibung else gen_beschreibung
        url_pfad = src_url if src_url else gen_url
        titel_tag = src_titel if src_titel else gen_titel
        meta_desc = src_meta if src_meta else gen_meta

        output.append(_vater_row(
            articolo, han, brand_cfg, brand_cfg["warengruppe_default"],
            vater_nr, aname, uvp, to_german_decimal(ek), "2",
            country_to_iso(origin), clean_taric(taric), sc, farbe_lief,
            jc, sp, hu, beschreibung, url_pfad, titel_tag, meta_desc,
        ))

        for ean, si in grp["sizes"].items():
            gtin = ensure_gtin_13(ean)
            output.append(_kind_row(
                articolo, han, brand_cfg, brand_cfg["warengruppe_default"],
                f"{brand_cfg['code']}-{articolo}-{si['size']}", gtin, vater_nr,
                aname, uvp, to_german_decimal(ek), "2",
                country_to_iso(origin), clean_taric(taric), sc, si["size"],
                get_size_sort(si["size"], "Schuhe"), farbe_lief,
                jc, sp, hu, make_upc(ean),
            ))
            orders.append([gtin, si["qty"], to_german_decimal(ek)])

    return output, orders, brand_cfg["code"]


def process_date(filepath, han):
    # type: (str, str) -> Tuple[List[List[Any]], List[List[Any]], str]
    """Process D.A.T.E. barcode file (STYLE CODE, STYLE DESCRIPTION, SIZE, EAN CODE, HS CODE)."""
    brand_cfg = dict(BRAND_CONFIG["DATE"])
    _header, data_rows = read_xlsx(filepath)

    groups = OrderedDict()  # type: OrderedDict
    for r in data_rows:
        if len(r) < 4 or r[0] is None:
            continue
        style_code = str(r[0]).strip()
        desc_raw = str(r[1]).strip() if r[1] else ""
        size = str(int(r[2])) if isinstance(r[2], (int, float)) else str(r[2]).strip()
        ean = str(int(r[3])) if isinstance(r[3], (int, float)) else str(r[3]).strip()
        taric = str(int(r[4])) if len(r) > 4 and r[4] else ""

        if style_code not in groups:
            # Parse description: strip trailing cut-code (e.g. M8D, M2B)
            cleaned = re.sub(r"\s+[A-Z]\d[A-Z]\s*$", "", desc_raw)
            parts = cleaned.split()
            # Extract color from end of description
            color_words = {"WHITE", "BLACK", "BLUE", "RED", "GREEN", "GREY", "GRAY",
                           "BEIGE", "BROWN", "NAVY", "PINK", "ORANGE", "CREAM", "SAND"}
            color = ""
            model = cleaned
            if parts:
                last = parts[-1].upper()
                if "-" in last or last in color_words:
                    color = parts[-1]
                    model = " ".join(parts[:-1])

            groups[style_code] = {
                "model": model, "color": color, "taric": taric, "sizes": [],
            }
        groups[style_code]["sizes"].append({"size": size, "ean": ean})

    output = []  # type: List[List[Any]]
    orders = []  # type: List[List[Any]]
    jc, sp, hu = shop_activation(brand_cfg["shop_col"])

    for style_code, grp in groups.items():
        model, color = grp["model"], grp["color"]
        sc = safe_color(color.lower() if color else "")
        vater_nr = f"{brand_cfg['code']}-{style_code}"
        aname = f"{model} {sc}" if color else model
        farbe_lief = color if color else sc
        beschreibung, url_pfad, titel_tag, meta_desc = make_seo_fields(
            brand_cfg, aname, brand_cfg["warengruppe_default"], sc)

        output.append(_vater_row(
            style_code, han, brand_cfg, brand_cfg["warengruppe_default"],
            vater_nr, aname, "", "", "2", "IT", clean_taric(grp["taric"]),
            sc, farbe_lief,
            jc, sp, hu, beschreibung, url_pfad, titel_tag, meta_desc,
        ))

        for si in grp["sizes"]:
            gtin = ensure_gtin_13(si["ean"])
            output.append(_kind_row(
                style_code, han, brand_cfg, brand_cfg["warengruppe_default"],
                f"{brand_cfg['code']}-{style_code}-{si['size']}", gtin, vater_nr,
                aname, "", "", "2", "IT", clean_taric(grp["taric"]),
                sc, si["size"],
                get_size_sort(si["size"], "Schuhe"), farbe_lief,
                jc, sp, hu, make_upc(si["ean"]),
            ))

    return output, orders, brand_cfg["code"]


def process_portuguese_flannel(filepath, han):
    # type: (str, str) -> Tuple[List[List[Any]], List[List[Any]], str]
    """Process Portuguese Flannel format.
    Columns: Article number | article name | color | Purchase price | RRP | EAN |
             Zolltarifnummer | Country of origin | weight | order quantity
    """
    brand_cfg = dict(BRAND_CONFIG["PORTUGUESE FLANNEL"])
    _header, data_rows = read_xlsx(filepath)

    groups = OrderedDict()  # type: OrderedDict
    for r in data_rows:
        if len(r) < 10 or r[0] is None:
            continue
        art_nr = str(r[0]).strip()
        raw_name = str(r[1]).strip() if r[1] else ""
        color_col = str(r[2]).strip() if r[2] and str(r[2]).strip().lower() != "none" else ""
        ek = r[3]
        rrp = r[4]
        ean = str(r[5]).strip() if r[5] else ""
        taric = r[6]
        country = str(r[7]).strip() if r[7] else "PT"
        weight = r[8]
        qty = r[9]

        # Parse article number: SS26.NNN.SIZE[.COLOR]
        parts = art_nr.split(".")
        if len(parts) < 3:
            continue
        base_key = f"{parts[0]}.{parts[1]}"
        size = parts[2]
        color = ".".join(parts[3:]) if len(parts) > 3 else ""

        group_key = f"{base_key}.{color}" if color else base_key

        # Clean article name: strip size/color from parentheses
        model_name = re.sub(r"\s*\([^)]*\)\s*$", "", raw_name).strip()

        if group_key not in groups:
            groups[group_key] = {
                "base_key": base_key, "model": model_name, "color": color,
                "ek": ek, "rrp": rrp, "taric": taric, "country": country,
                "weight": weight, "sizes": [],
            }
        groups[group_key]["sizes"].append({
            "size": size, "ean": ean, "qty": int(qty) if qty else 0,
        })

    output = []  # type: List[List[Any]]
    orders = []  # type: List[List[Any]]
    jc, sp, hu = shop_activation(brand_cfg["shop_col"])

    for group_key, grp in groups.items():
        model, color = grp["model"], grp["color"]
        vater_nr = f"{brand_cfg['code']}-{group_key}"
        sc = safe_color(color.lower() if color else "")
        aname = f"{model} {sc}" if color else model
        farbe_lief = color if color else sc
        uvp = round_uvp(grp["rrp"])
        beschreibung, url_pfad, titel_tag, meta_desc = make_seo_fields(
            brand_cfg, aname, brand_cfg["warengruppe_default"], sc)

        output.append(_vater_row(
            group_key, han, brand_cfg, brand_cfg["warengruppe_default"],
            vater_nr, aname, uvp, to_german_decimal(grp["ek"]),
            to_german_weight(grp["weight"]),
            country_to_iso(grp["country"]), clean_taric(grp["taric"]),
            sc, farbe_lief,
            jc, sp, hu, beschreibung, url_pfad, titel_tag, meta_desc,
        ))

        for si in grp["sizes"]:
            gtin = ensure_gtin_13(si["ean"])
            output.append(_kind_row(
                group_key, han, brand_cfg, brand_cfg["warengruppe_default"],
                f"{brand_cfg['code']}-{group_key}-{si['size']}", gtin, vater_nr,
                aname, uvp, to_german_decimal(grp["ek"]),
                to_german_weight(grp["weight"]),
                country_to_iso(grp["country"]), clean_taric(grp["taric"]),
                sc, si["size"],
                get_size_sort(si["size"], "Bekleidung"), farbe_lief,
                jc, sp, hu, make_upc(si["ean"]),
            ))
            if si["ean"] and si["qty"]:
                orders.append([gtin, si["qty"], to_german_decimal(grp["ek"])])

    return output, orders, brand_cfg["code"]


def process_ilse_jacobsen(filepath, han):
    # type: (str, str) -> Tuple[List[List[Any]], List[List[Any]], str]
    """Process Ilse Jacobsen order format (66 columns).
    Key columns: [2]=Item number, [3]=Product name, [4]=Top categories,
    [27]=Tare weight, [45]=Country of origin, [56]=HS Tarif Code,
    [57]=Color, [58]=Size, [60]=EAN Number, [61]=Quantity,
    [62]=Unit price (EK), [63]=Rec retail price EUR
    """
    brand_cfg = dict(BRAND_CONFIG["ILSE JACOBSEN"])
    _header, data_rows = read_xlsx(filepath)

    groups = OrderedDict()  # type: OrderedDict
    for r in data_rows:
        if len(r) < 64 or r[2] is None:
            continue
        item_nr = str(r[2]).strip()
        product_name = str(r[3]).strip() if r[3] else ""
        top_cat = str(r[4]).strip() if r[4] else ""
        color = str(r[57]).strip() if r[57] else ""
        size = str(r[58]).strip() if r[58] else ""
        ean = str(r[60]).strip() if r[60] else ""
        qty = int(r[61]) if r[61] else 0
        ek = r[62]
        rrp = r[63]
        country = str(r[45]).strip() if r[45] else ""
        taric = r[56]
        weight = r[27]

        key = (item_nr, color)
        if key not in groups:
            wg = "Schuhe"
            if top_cat:
                tc = top_cat.upper()
                if "ACCESSORI" in tc or "BAG" in tc:
                    wg = "Accessoires"
            groups[key] = {
                "product_name": product_name, "wg": wg,
                "ek": ek, "rrp": rrp, "country": country,
                "taric": taric, "weight": weight, "sizes": [],
            }
        groups[key]["sizes"].append({
            "size": size, "ean": ean, "qty": qty,
        })

    output = []  # type: List[List[Any]]
    orders = []  # type: List[List[Any]]
    jc, sp, hu = shop_activation(brand_cfg["shop_col"])

    for (item_nr, color), grp in groups.items():
        product_name = grp["product_name"]
        sc = safe_color(color.lower())
        vater_nr = f"{brand_cfg['code']}-{item_nr}-{color.replace(' ', '-')}"
        aname = f"{product_name} {sc}"
        farbe_lief = color if color else sc
        uvp = round_uvp(grp["rrp"])
        w = grp["weight"]
        # Convert grams to kg if weight > 100
        if w and isinstance(w, (int, float)) and w > 100:
            w = w / 1000
        beschreibung, url_pfad, titel_tag, meta_desc = make_seo_fields(
            brand_cfg, aname, grp["wg"], sc)

        output.append(_vater_row(
            f"{item_nr}-{color}", han, brand_cfg, grp["wg"],
            vater_nr, aname, uvp, to_german_decimal(grp["ek"]),
            to_german_weight(w),
            country_to_iso(grp["country"]), clean_taric(grp["taric"]),
            sc, farbe_lief,
            jc, sp, hu, beschreibung, url_pfad, titel_tag, meta_desc,
        ))

        for si in grp["sizes"]:
            gtin = ensure_gtin_13(si["ean"])
            output.append(_kind_row(
                f"{item_nr}-{color}", han, brand_cfg, grp["wg"],
                f"{brand_cfg['code']}-{item_nr}-{color.replace(' ', '-')}-{si['size']}",
                gtin, vater_nr, aname, uvp, to_german_decimal(grp["ek"]),
                to_german_weight(w),
                country_to_iso(grp["country"]), clean_taric(grp["taric"]),
                sc, si["size"],
                get_size_sort(si["size"], grp["wg"]), farbe_lief,
                jc, sp, hu, make_upc(si["ean"]),
            ))
            if si["ean"] and si["qty"]:
                orders.append([gtin, si["qty"], to_german_decimal(grp["ek"])])

    return output, orders, brand_cfg["code"]


def process_closed(filepath, han):
    # type: (str, str) -> Tuple[List[List[Any]], List[List[Any]], str]
    """Process CLOSED CSV format (semicolon-delimited).
    Columns: [0]=Order No, [1]=Currency, [2]=Name, [3]=SKU, [4]=EAN,
    [5]=Unit Price, [6]=Sell Price, [7]=Quantity, [8]=VAT, [9]=Discount,
    [10]=Weight, [11]=Country of Origin, [12]=TARIC, [13]=Composition, [14]=Gender
    Name pattern: 'MODEL NAME - COLOR - SIZE'
    """
    brand_cfg = dict(BRAND_CONFIG["CLOSED"])
    _header, data_rows = read_csv_file(filepath)

    groups = OrderedDict()  # type: OrderedDict
    for r in data_rows:
        if len(r) < 14 or not r[2]:
            continue
        name_full = str(r[2]).strip()
        sku = str(r[3]).strip() if r[3] else ""
        ean = str(r[4]).strip() if r[4] else ""
        ek_raw = str(r[5]).strip().replace(",", ".") if r[5] else ""
        rrp_raw = str(r[6]).strip().replace(",", ".") if r[6] else ""
        qty_raw = str(r[7]).strip() if r[7] else "0"
        weight_raw = str(r[10]).strip().replace(",", ".") if r[10] else ""
        country = str(r[11]).strip() if r[11] else ""
        taric = str(r[12]).strip() if r[12] else ""

        # Parse name: "MODEL - COLOR - SIZE"
        name_parts = [p.strip() for p in name_full.split(" - ")]
        if len(name_parts) >= 3:
            model = name_parts[0]
            color = name_parts[1]
            size = name_parts[2]
        elif len(name_parts) == 2:
            model = name_parts[0]
            color = ""
            size = name_parts[1]
        else:
            model = name_full
            color = ""
            size = ""

        # Base SKU without size suffix
        sku_base = re.sub(r"[-.](?:XS|S|M|L|XL|XXL|3XL|\d+)\s*$", "", sku, flags=re.IGNORECASE)
        key = (sku_base, color)

        if key not in groups:
            groups[key] = {
                "model": model, "color": color, "ek": ek_raw, "rrp": rrp_raw,
                "weight": weight_raw, "country": country, "taric": taric, "sizes": [],
            }
        try:
            qty = int(float(qty_raw))
        except (ValueError, TypeError):
            qty = 0
        groups[key]["sizes"].append({"size": size, "ean": ean, "qty": qty})

    output = []  # type: List[List[Any]]
    orders = []  # type: List[List[Any]]
    jc, sp, hu = shop_activation(brand_cfg["shop_col"])

    for (sku_base, color), grp in groups.items():
        model = grp["model"]
        sc = safe_color(color.lower() if color else "")
        vater_nr = f"{brand_cfg['code']}-{sku_base}"
        aname = f"{model} {sc}" if color else model
        farbe_lief = color if color else sc
        uvp = round_uvp(grp["rrp"])
        beschreibung, url_pfad, titel_tag, meta_desc = make_seo_fields(
            brand_cfg, aname, brand_cfg["warengruppe_default"], sc)

        output.append(_vater_row(
            sku_base, han, brand_cfg, brand_cfg["warengruppe_default"],
            vater_nr, aname, uvp, to_german_decimal(grp["ek"]),
            to_german_weight(grp["weight"]),
            country_to_iso(grp["country"]), clean_taric(grp["taric"]),
            sc, farbe_lief,
            jc, sp, hu, beschreibung, url_pfad, titel_tag, meta_desc,
        ))

        for si in grp["sizes"]:
            gtin = ensure_gtin_13(si["ean"])
            output.append(_kind_row(
                sku_base, han, brand_cfg, brand_cfg["warengruppe_default"],
                f"{brand_cfg['code']}-{sku_base}-{si['size']}", gtin, vater_nr,
                aname, uvp, to_german_decimal(grp["ek"]),
                to_german_weight(grp["weight"]),
                country_to_iso(grp["country"]), clean_taric(grp["taric"]),
                sc, si["size"],
                get_size_sort(si["size"], "Bekleidung"), farbe_lief,
                jc, sp, hu, make_upc(si["ean"]),
            ))
            if si["ean"] and si["qty"]:
                orders.append([gtin, si["qty"], to_german_decimal(grp["ek"])])

    return output, orders, brand_cfg["code"]


def process_armed_angels(filepath, han):
    # type: (str, str) -> Tuple[List[List[Any]], List[List[Any]], str]
    """Process Armed Angels .xls format.
    Columns: [11]=Item Number, [12]=Item Description, [13]=Color Code,
    [14]=Color Description, [15]=Size, [16]=SKU, [17]=EAN,
    [18]=Quantity, [19]=Price Net, [20]=Price Gross, [21]=Price Retail,
    [22]=Material, [23]=Country of Origin, [24]=Custom Tarif, [28]=Item Weight
    """
    brand_cfg = dict(BRAND_CONFIG["ARMED ANGELS"])
    _header, all_rows = read_xls(filepath)

    groups = OrderedDict()  # type: OrderedDict
    for r in all_rows:
        if len(r) < 25:
            continue
        item_nr = str(r[11]).strip() if r[11] else ""
        if not item_nr or item_nr.upper() == "ITEM NUMBER":
            continue  # skip header row
        item_desc = str(r[12]).strip() if r[12] else ""
        color_code = str(r[13]).strip() if r[13] else ""
        color_desc = str(r[14]).strip() if r[14] else ""
        size = str(r[15]).strip() if r[15] else ""
        ean = str(r[17]).strip() if r[17] else ""
        qty = float(r[18]) if r[18] else 0
        ek = r[19]
        rrp = r[21]
        country = str(r[23]).strip() if r[23] else ""
        taric = r[24]
        weight = r[28] if len(r) > 28 else None

        key = (item_nr, color_code)
        if key not in groups:
            groups[key] = {
                "item_desc": item_desc, "color_desc": color_desc,
                "ek": ek, "rrp": rrp, "country": country,
                "taric": taric, "weight": weight, "sizes": [],
            }
        groups[key]["sizes"].append({
            "size": size, "ean": ean, "qty": int(qty),
        })

    output = []  # type: List[List[Any]]
    orders = []  # type: List[List[Any]]
    jc, sp, hu = shop_activation(brand_cfg["shop_col"])

    for (item_nr, color_code), grp in groups.items():
        item_desc = grp["item_desc"]
        color_desc = grp["color_desc"]
        sc = safe_color(color_desc.lower())
        vater_nr = f"{brand_cfg['code']}-{item_nr}-{color_code}"
        aname = f"{item_desc} {sc}"
        farbe_lief = color_desc if color_desc else sc
        uvp = round_uvp(grp["rrp"])
        beschreibung, url_pfad, titel_tag, meta_desc = make_seo_fields(
            brand_cfg, aname, brand_cfg["warengruppe_default"], sc)

        output.append(_vater_row(
            f"{item_nr}-{color_code}", han, brand_cfg, brand_cfg["warengruppe_default"],
            vater_nr, aname, uvp, to_german_decimal(grp["ek"]),
            to_german_weight(grp["weight"]),
            country_to_iso(grp["country"]), clean_taric(grp["taric"]),
            sc, farbe_lief,
            jc, sp, hu, beschreibung, url_pfad, titel_tag, meta_desc,
        ))

        for si in grp["sizes"]:
            gtin = ensure_gtin_13(si["ean"])
            output.append(_kind_row(
                f"{item_nr}-{color_code}", han, brand_cfg, brand_cfg["warengruppe_default"],
                f"{brand_cfg['code']}-{item_nr}-{color_code}-{si['size']}", gtin, vater_nr,
                aname, uvp, to_german_decimal(grp["ek"]),
                to_german_weight(grp["weight"]),
                country_to_iso(grp["country"]), clean_taric(grp["taric"]),
                sc, si["size"],
                get_size_sort(si["size"], "Bekleidung"), farbe_lief,
                jc, sp, hu, make_upc(si["ean"]),
            ))
            if si["ean"] and si["qty"]:
                orders.append([gtin, si["qty"], to_german_decimal(grp["ek"])])

    return output, orders, brand_cfg["code"]


# ============================================================
# PROCESSORS MAP
# ============================================================

PROCESSORS = {
    "UNIVERSAL": process_universal_works,
    "PEDRO MIRALLES": process_pedro_miralles,
    "VOILE BLANCHE": process_voile_blanche,
    "DATE": process_date,
    "PORTUGUESE FLANNEL": process_portuguese_flannel,
    "ILSE JACOBSEN": process_ilse_jacobsen,
    "CLOSED": process_closed,
    "ARMED ANGELS": process_armed_angels,
}


# ============================================================
# VALIDATION
# ============================================================

def validate_output(rows):
    # type: (List[List[Any]]) -> List[str]
    """Validiert die Ausgabezeilen gegen die 35-Spalten-Struktur."""
    errors = []  # type: List[str]
    for i, row in enumerate(rows):
        if len(row) != 35:
            errors.append(f"Zeile {i + 1}: {len(row)} Spalten statt 35")
            continue
        # col 20 = Herkunftsland
        country = row[20]
        if country and (len(country) != 2 or not country.isalpha()):
            errors.append(f"Zeile {i + 1}: Herkunftsland '{country}' kein 2-Buchstaben-Code")
        # col 21 = TARIC-Code
        taric = row[21]
        if "." in str(taric):
            errors.append(f"Zeile {i + 1}: TARIC '{taric}' enthaelt Punkte")
        # col 22 = Variationswert 1 (Farbe)
        var1 = row[22]
        if var1 and var1 != var1.lower():
            errors.append(f"Zeile {i + 1}: Variationswert 1 '{var1}' nicht kleingeschrieben")
        # col 8 = Identifizierungsspalte Vaterartikel
        vater_ref = row[8]
        if vater_ref:  # Kind
            gtin = row[7]
            if gtin and len(gtin) != 13:
                errors.append(f"Zeile {i + 1}: GTIN '{gtin}' nicht 13-stellig")
            upc = row[15]
            if not upc:
                errors.append(f"Zeile {i + 1}: Kind ohne UPC")
            size = row[23]
            if not size:
                errors.append(f"Zeile {i + 1}: Kind ohne Groesse")
    return errors


# ============================================================
# MAIN
# ============================================================

def main():
    # type: () -> None
    parser = argparse.ArgumentParser(description="JTL Stammdaten-Generator")
    parser.add_argument("--saison", required=True, help="Saison: FS oder HW")
    parser.add_argument("--jahr", required=True, help="Jahr: z.B. 2026")
    parser.add_argument("--input", required=True, help="Pfad zur Quelldatei")
    parser.add_argument("--output", required=True, help="Ausgabeverzeichnis")
    parser.add_argument("--marke", default="auto", help="Marke oder 'auto' fuer Erkennung")
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"FEHLER: Datei nicht gefunden: {args.input}")
        sys.exit(1)

    han = build_han(args.saison, args.jahr)
    date_suffix = make_date_suffix()
    saison_short = f"{args.saison.upper()}{args.jahr[2:]}"

    # Marke erkennen
    if args.marke == "auto":
        brand = detect_brand(args.input)
        if brand is None:
            print(f"FEHLER: Marke konnte nicht erkannt werden fuer: {args.input}")
            sys.exit(1)
        print(f"Marke erkannt: {brand}")
    else:
        brand = args.marke.upper()
        if brand not in BRAND_CONFIG:
            # Try partial match
            for key in BRAND_CONFIG:
                if brand in key or key in brand:
                    brand = key
                    break

    # Verarbeiten
    processor = PROCESSORS.get(brand)
    if processor is None:
        print(f"FEHLER: Kein Prozessor fuer Marke '{brand}' verfuegbar.")
        print(f"Verfuegbare Marken: {', '.join(PROCESSORS.keys())}")
        sys.exit(1)

    print(f"Verarbeite: {os.path.basename(args.input)}")
    print(f"Marke: {brand} | HAN: {han} | Saison: {saison_short}")

    output_rows, order_rows, markencode = processor(args.input, han)

    # Validierung
    errors = validate_output(output_rows)
    if errors:
        print(f"\nVALIDIERUNGSFEHLER ({len(errors)}):")
        for e in errors:
            print(f"  FEHLER: {e}")
    else:
        print("Validierung bestanden")

    # Dateien schreiben
    os.makedirs(args.output, exist_ok=True)

    einspiel_name = f"Einspieltabelle_{markencode}_{saison_short}_{date_suffix}.csv"
    bestell_name = f"Bestellmengen_{markencode}_{saison_short}_{date_suffix}.csv"

    einspiel_path = os.path.join(args.output, einspiel_name)
    bestell_path = os.path.join(args.output, bestell_name)

    n_einspiel = write_einspieltabelle(einspiel_path, output_rows)
    n_bestell = write_bestellmengen(bestell_path, order_rows)

    vater_count = sum(1 for r in output_rows if not r[8])
    kind_count = sum(1 for r in output_rows if r[8])

    print(f"\nERGEBNIS:")
    print(f"  {einspiel_name}: {vater_count} Vater + {kind_count} Kind = {n_einspiel} Zeilen")
    print(f"  {bestell_name}: {n_bestell} EANs")


if __name__ == "__main__":
    main()
