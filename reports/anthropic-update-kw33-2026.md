# 📡 Anthropic Update-Report – KW 33 (4.–10. August 2026)

> Automatisch generiert am 11. August 2026 (v2 — inkl. v2.1.227)

## 🟡 Interessant, kein sofortiger Handlungsbedarf

### Claude Code v2.1.227 (10. Aug.)

Einziges neues Release seit dem KW-32-Report.

| Änderung | Typ |
|----------|-----|
| Feature-Flags werden bei abgelaufenem Login-Token jetzt korrekt evaluiert (betraf Max-Plan-Nutzer) | 🐛 Bugfix |
| Bash-Befehle unter `claude-code-action` mit `allowed_non_write_users` funktionieren jetzt | 🐛 Bugfix |
| `/tui` stellt gelöschte Konversationen nicht mehr wieder her | 🐛 Bugfix |
| Slash-Command-Menü: besseres visuelles Feedback und Styling | 🔧 Verbesserung |
| Performance: reduzierte Event-Loop-Delays | 🔧 Verbesserung |

**Setup-Relevanz:** Keine der Änderungen erfordert Anpassungen am Setup. Die `claude-code-action`-Fixes sind relevant falls GitHub Actions mit non-write-Usern genutzt werden.

## ⚪ Zur Kenntnis

Keine neuen Platform-Release-Notes, API-Änderungen oder SDK-Releases seit dem KW-32-Report (8. August).

| Quelle | Letztes Update | Status |
|--------|---------------|--------|
| Claude Code Releases | v2.1.227 (10. Aug.) | ✅ Erfasst |
| Python SDK | v0.121.0 (7. Aug.) | Bereits in KW 32 |
| Platform Release Notes | 7. Aug. | Bereits in KW 32 |

## 💡 Offene Aktionen aus KW 32 (zur Erinnerung)

Die folgenden Empfehlungen aus dem KW-32-Report sind weiterhin offen:

1. **`rules/performance.md`** — Modell-Referenzen aktualisieren (Haiku 4.5 → aktuell, Sonnet 4.5 → 5, Opus 4.5 → 5)
2. **`rules/agents.md`** — Cross-Session SendMessage und entferntes 200-Subagent-Cap dokumentieren
3. **`settings.json`** — `crossSessionInbound` konfigurieren
4. **`archive`-Plugin-Quelle** — In Plugin-Dokumentation aufnehmen

## 📊 Zusammenfassung

| Kategorie | Anzahl |
|-----------|--------|
| 🔴 Sofort relevant | 0 |
| 🟡 Interessant | 1 (v2.1.227) |
| ⚪ Zur Kenntnis | 0 neue |

**Update-Priorität:** Niedrig. v2.1.227 enthält nur Bugfixes und UX-Verbesserungen. Die offenen Aktionen aus KW 32 haben weiterhin höhere Priorität.

**Quellen:**
- platform.claude.com/docs/en/release-notes/overview (keine neuen Einträge)
- github.com/anthropics/claude-code/releases (v2.1.227)
- github.com/anthropics/anthropic-sdk-python/releases (keine neuen Releases)

---

*Nächster Scan: KW 34 (18. August 2026)*
