# 📡 Anthropic Update-Report – KW 26 (21.–22. Juni 2026)

> Automatisch generiert am 22. Juni 2026

## 🔴 Sofort relevant für dein Setup

### 1. ⚠️ KW25-Handlungsempfehlungen noch OFFEN

Die drei HOCH-Priorität-Items aus dem [KW25-Report](./anthropic-update-kw25-2026.md) wurden **nicht umgesetzt**. Die retired Model-IDs `claude-opus-4-20250514` und `claude-sonnet-4-20250514` stehen weiterhin in 6 Dateien:

| Datei | Zeile | Problem |
|-------|-------|---------|
| `skills/claude-code/references/configuration.md` | 58, 232 | `claude-opus-4-20250514` als empfohlenes Modell |
| `skills/claude-api/templates/extended-thinking.ts` | 251 | Hardcoded retired Model-ID |
| `skills/claude-api/SKILL.md` | 321 | `claude-sonnet-4-20250514` als "Stable version" |
| `skills/claude-api/references/top-errors.md` | 362 | Beispielcode mit retired Model |
| `skills/claude-api/references/api-reference.md` | 119 | Model-Tabelle veraltet |

**Seit 15. Juni geben diese Model-IDs API-Fehler zurück.** Jeder Skill/Agent, der diese IDs übernimmt, produziert Fehler. Ersetzen durch `claude-opus-4-8` / `claude-sonnet-4-6` bzw. Aliase `opus` / `sonnet`.

### 2. ⏰ Fast Mode für Opus 4.6 wird ~27. Juni abgeschaltet

Am 28. Mai wurde Fast Mode für Opus 4.6 deprecated mit "removal approximately 30 days after launch". Das Fenster schließt sich diese Woche. Falls Skills oder Workflows Fast Mode mit Opus 4.6 nutzen, auf Opus 4.8 oder Opus 4.7 umstellen.

## 🟡 Interessant, kein sofortiger Handlungsbedarf

| # | Typ | Änderung | Details |
|---|-----|----------|---------|
| 3 | 🔧 | Stream-Stall-Erkennung angepasst (v2.1.185, 20. Juni) | Threshold von 10s auf 20s erhöht, Meldung geändert zu "Waiting for API response · will retry in …" – reduziert false-positive Retries bei langsamen Responses |
| 4 | 🔧 | Destruktive Git-Befehle (KW25 offen) | 6 Skills verwenden noch `git reset --hard` Patterns, die jetzt im Auto Mode geblockt werden |

## ⚪ Zur Kenntnis

- **Keine neuen Platform/API-Änderungen** seit 15. Juni (Model-Retirement)
- **Keine neuen SDK-Releases** seit v0.111.0 (18. Juni)
- **Claude Code v2.1.185** war das einzige neue Release (20. Juni) – minimale Änderung
- **Docs-Domain** bleibt `platform.claude.com/docs` (Redirect von `docs.anthropic.com` ist permanent/301)

## 📋 Handlungsempfehlungen (kumuliert)

| Priorität | Aktion | Status | Datei(en) |
|-----------|--------|--------|-----------|
| **HOCH** | Retired Model-IDs ersetzen | ❌ Offen seit KW25 | 5 Dateien (siehe oben) |
| **HOCH** | Fast Mode Opus 4.6 → 4.8 Migration prüfen | 🆕 Neu | Settings, Workflows |
| **HOCH** | `git reset --hard` Patterns überarbeiten | ❌ Offen seit KW25 | 6 Skills |
| **MITTEL** | `attribution.sessionUrl` evaluieren | ❌ Offen seit KW25 | `settings.json` |

---

## 💡 Fazit

Ruhige Woche – nur ein Minor-Release (v2.1.185). Die eigentliche Dringlichkeit sind die offenen KW25-Items: 6 Dateien mit retired Model-IDs, die seit 7 Tagen API-Fehler verursachen. Das Fast-Mode-Deprecation-Fenster für Opus 4.6 schließt sich Ende dieser Woche.

---

## Quellen

- [Anthropic Platform Release Notes](https://platform.claude.com/docs/en/release-notes/overview)
- [Claude Code v2.1.185](https://github.com/anthropics/claude-code/releases)
- [anthropic-sdk-python Releases](https://github.com/anthropics/anthropic-sdk-python/releases)
- [KW25-Report](./anthropic-update-kw25-2026.md)
