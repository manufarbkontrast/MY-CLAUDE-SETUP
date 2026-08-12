# 📡 Anthropic Update-Report – KW 33 (4.–12. August 2026)

> Automatisch generiert am 12. August 2026 (v3 — inkl. v2.1.225–228, Plattform 10.+11. Aug.)

## 🔴 Sofort relevant für dein Setup

### 1. 🔧 Write-Tool: Überschreiben ohne Read bei neueren Modellen (v2.1.228, 11. Aug.)

Neuere Modelle (Opus 4.8+, Opus 5, Fable 5) können mit dem Write-Tool bestehende Dateien überschreiben, ohne sie vorher gelesen zu haben. Das bisherige Read-before-Write-Verhalten galt als implizite Sicherheit.

**Typ:** 🔧 Verbesserung / Behavior Change
**Relevanz:** Falls PreToolUse-Hooks oder Skills auf dem alten Verhalten (Write schlägt fehl ohne Read) aufbauen, funktionieren diese jetzt anders. **Aktion:** `settings.json` Hooks prüfen — der PreToolUse-Hook "block unnecessary .md/.txt files" könnte betroffen sein, da Write jetzt ohne Read durchgeht. In `rules/coding-style.md` ggf. dokumentieren, dass Write ohne Read jetzt modellabhängig erlaubt ist.

### 2. 🛡️ Gehärtete claude.ai-synced Skills: kein Shadowing mehr (v2.1.228, 11. Aug.)

Von claude.ai synchronisierte Skills überschreiben nicht mehr lokale Commands oder MCP-Prompts. Descriptions werden sanitized und gelabelt.

**Typ:** 🛡️ Security-Verbesserung
**Relevanz:** Direkt relevant für dein Setup mit 466 lokalen Skills und 192 Commands. Lokale Definitionen haben jetzt garantiert Vorrang vor Marketplace-Skills. **Aktion:** Kein Handlungsbedarf, aber bei Skill-Konflikten ist jetzt klar: lokal gewinnt. In `rules/security.md` als Security-Improvement erwähnen.

### 3. 🐛 Session-Cleanup löschte Memory-Folder-Inhalte (v2.1.228, 11. Aug.)

Gefixt: Session-Cleanup konnte den Inhalt des Memory-Folders eines Projekts löschen.

**Typ:** 🐛 Bugfix (datenverlust-relevant)
**Relevanz:** Falls Projekte Memory-Folders verwenden (z.B. via `memory-palace`-Plugin aus athola/claude-night-market), war Datenverlust möglich. **Aktion:** Claude Code auf mindestens v2.1.228 updaten.

## 🟡 Interessant, kein sofortiger Handlungsbedarf

### 💰 Claude Sonnet 5 Pricing permanent bei $2 / $10 pro MTok (Plattform, 10. Aug.)

Die geplante Preiserhöhung auf $3/$15 zum 1. September entfällt. Das Intro-Pricing ist jetzt der Standardpreis.

→ Sonnet 5 bleibt das günstigste leistungsstarke Modell. Relevant für Kosteneinschätzungen in `rules/performance.md`.

### 🔌 Compliance API: Lokale Session-Transcripts (Plattform, 11. Aug.)

Enterprise-Orgs können jetzt Transcripts von Claude Code und Cowork Sessions auf lokalen Maschinen abrufen (neue Endpoints `GET /v1/compliance/apps/sessions/local`).

→ Nur Enterprise-relevant. Zeigt, dass Anthropic die Audit-Fähigkeiten ausbaut.

### 🔧 Plugin-Cache-Cleanup bei Symlinks gefixt (v2.1.228, 11. Aug.)

Background-Cache-Cleanup löschte fälschlicherweise Caches von Plugins, deren einzige Version ein symgelinkter Dev-Checkout war.

→ Relevant falls du Plugins lokal per Symlink entwickelst.

### 🔧 Settings-Merge bei Marketplace-Einträgen gefixt (v2.1.228, 11. Aug.)

Ein Settings-Merge-Issue mit Marketplace-Einträgen wurde behoben.

→ Betrifft dein Setup mit 20+ Marketplace-Plugins direkt. Falls du Merge-Konflikte in `settings.json` hattest, ist das jetzt behoben.

### 🔧 Cross-Session-Messages: Inline-Darstellung (v2.1.228, 11. Aug.)

Sender und Body von Cross-Session-Nachrichten werden jetzt inline angezeigt statt zugeklappt.

→ Verbessert die UX für Agents, die Cross-Session kommunizieren (vgl. KW 32 Action Item zu `SendMessage`).

### 🔧 Vertex AI Credential-Handling verbessert (v2.1.228, 11. Aug.)

Abgelaufene/fehlende Vertex AI Credentials schlagen jetzt in Sekunden fehl statt minutenlang zu retrien.

→ Relevant falls du Claude über Google Cloud Vertex nutzt.

### 🔧 Deferred-Tools Reminder: kein doppeltes Senden mehr (v2.1.228, 11. Aug.)

Der Deferred-Tools Reminder wird nach Skill-Invokation nicht mehr doppelt ans Modell gesendet.

→ Reduziert Token-Verbrauch bei Skill-lastigen Sessions. Gut für dein Setup mit 466 Skills.

### 🔧 Slash-Command-Menü visuell verbessert (v2.1.227, 10. Aug.)

Nur die selektierte Zeile wird blau markiert, gematchte Zeichen werden fett dargestellt.

→ Verbessert Orientierung bei 192 Commands.

## ⚪ Zur Kenntnis

| Änderung | Version | Typ |
|----------|---------|-----|
| Interactive Sessions: seltener Layout-Error stoppte Redraw | v2.1.228 | 🐛 |
| Git/Git Bash auf Windows nicht gefunden bei bestimmten Launch-Pfaden | v2.1.228 | 🐛 |
| `/tui` setzte Modell nach `/model`-Wechsel zurück | v2.1.228 | 🐛 |
| Cross-Session Messaging startete ohne Inbox nach Install/Upgrade | v2.1.228 | 🐛 |
| Remote Control `/resume` leakte Titel/History in verbundene Session | v2.1.228 | 🐛 |
| Self-Hosted Runner: Failed bei frischen Runnern wenn Checkout-Hook fehlschlägt | v2.1.228 | 🐛 |
| Self-Hosted Runner: Session endete zwischen Background-Task und Follow-up-Turn | v2.1.228 | 🐛 |
| Tab-Bar-Jitter durch Terminal-Title-Spinner reduziert | v2.1.228 | 🔧 |
| "Auto mode costs more"-Hinweis entfernt (war veraltet) | v2.1.228 | 🔧 |
| Feature-Flags bei abgelaufenem Login-Token korrekt evaluiert | v2.1.227 | 🐛 |
| Bash unter `claude-code-action` mit `allowed_non_write_users` gefixt | v2.1.227 | 🐛 |
| `/tui` gelöschte Konversation nicht mehr wiederhergestellt | v2.1.227 | 🐛 |
| Performance: weniger Event-Loop-Stalls | v2.1.227 | 🔧 |
| Bug fixes and reliability improvements | v2.1.226 | 🐛 |

## 📋 Offene Aktionen aus KW 32 (zur Erinnerung)

1. **`rules/performance.md`** — Modell-Referenzen aktualisieren (Haiku 4.5 → aktuell, Sonnet 4.5 → 5, Opus 4.5 → 5)
2. **`rules/agents.md`** — Cross-Session SendMessage und entferntes 200-Subagent-Cap dokumentieren
3. **`settings.json`** — `crossSessionInbound` konfigurieren
4. **`archive`-Plugin-Quelle** — In Plugin-Dokumentation aufnehmen
5. **`rules/security.md`** — Credential-Masking-Optionen und Sandbox-Bypass-Fixes dokumentieren

## 📊 Zusammenfassung

| Kategorie | Anzahl |
|-----------|--------|
| 🔴 Sofort relevant | 3 |
| 🟡 Interessant | 8 |
| ⚪ Zur Kenntnis | 14 |

**Update-Priorität:** Mittel-Hoch. Claude Code auf v2.1.228 updaten — Memory-Folder-Datenverlust gefixt, Write-Tool Behavior Change, gehärtete Skills.

**Top-3-Aktionen diese Woche:**
1. **Claude Code updaten** auf mindestens v2.1.228 (Memory-Folder-Fix, Skill-Hardening)
2. **`settings.json` PreToolUse-Hooks prüfen**: Write-ohne-Read ist jetzt bei neueren Modellen erlaubt — Hooks die auf das alte Verhalten bauen ggf. anpassen
3. **Offene Aktionen aus KW 32** abarbeiten (s.o.)

**Quellen:**
- platform.claude.com/docs/en/release-notes/overview (10., 11. Aug.)
- github.com/anthropics/claude-code/releases (v2.1.225–v2.1.228)
- github.com/anthropics/anthropic-sdk-python/releases (keine neuen Releases seit v0.121.0)

---

*Nächster Scan: KW 34 (18. August 2026)*
