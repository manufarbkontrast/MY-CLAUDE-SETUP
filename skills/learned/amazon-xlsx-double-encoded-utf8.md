# Amazon XLSX Double-Encoded UTF-8 Fix

**Extracted:** 2026-02-26
**Context:** Amazon Lagerbestandsbuch/inventory XLSX files containing German product titles with mojibake (umlauts like ü→Ã¼, ä→Ã¤, ß→Ã&#x178;)

## Problem

Amazon's Lagerbestandsbuch XLSX stores product titles where original UTF-8 bytes were read as Windows-1252, producing mojibake. Examples:

- "ü" (UTF-8: C3 BC) → "Ã¼" (C3=Ã, BC=¼ in cp1252)
- "ä" (UTF-8: C3 A4) → "Ã¤"
- "ö" (UTF-8: C3 B6) → "Ã¶"
- "ß" (UTF-8: C3 9F) → "Ã&#x178;" (9F=&#x178; in cp1252)

This happens when openpyxl reads the XLSX and the data was already double-encoded at creation time.

## Solution

Re-encode as cp1252 then decode as UTF-8:

```python
def fix_double_encoded(text: str) -> str:
    """Fix double-encoded UTF-8 text from Amazon XLSX exports."""
    try:
        return text.encode("cp1252").decode("utf-8")
    except (UnicodeDecodeError, UnicodeEncodeError):
        return text  # already correct or unfixable
```

**CRITICAL**: Use `cp1252`, NOT `latin-1`.

latin-1 fails for ß because byte 0x9F is a control character in latin-1 but maps to &#x178; (U+0178) in cp1252. Since Amazon data frequently contains ß in German titles, latin-1 will silently break those entries while cp1252 handles them correctly.

## Example

```python
# Before fix (mojibake from openpyxl):
title = "Schirmmütze für Männer"  # actually stored as "SchirmmÃ¼tze fÃ¼r MÃ¤nner"

# After fix:
fixed = title.encode("cp1252").decode("utf-8")
# → "Schirmmütze für Männer"
```

## When to Use

- Reading Amazon XLSX exports (openpyxl) with German product titles showing Ã¼, Ã¤, Ã¶, Ã&#x178;
- Any XLSX where UTF-8 data was misinterpreted as Windows-1252 during creation
- Symptom: two-byte sequences like Ã+{x} where {x} is a latin character
- Common in: Lagerbestandsbuch, inventory reports, product catalogs from Amazon Seller Central
