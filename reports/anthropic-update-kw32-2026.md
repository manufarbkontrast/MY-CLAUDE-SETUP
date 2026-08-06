# 📡 Anthropic Update-Report – KW 32 (29. Juli – 6. August 2026)

> Automatisch generiert am 6. August 2026 (aktualisiert — v2.1.223 + Plattform-Updates vom 5. Aug.)

## 🔴 Sofort relevant für dein Setup

### 1. 🛡️ Vier Security-Fixes in v2.1.223 (6. Aug.)

Kritisches Sicherheitsupdate — vier unabhängige Bypass-Vektoren geschlossen:

- **Bash Permission Bypass:** Speziell konstruierte Commands konnten sich vor Permission-Checks verstecken.
- **Unicode-Padding in Permission-Prompts:** Commands mit Tabs oder unsichtbaren Unicode-Zeichen konnten Teile der Genehmigungsanzeige verbergen.
- **Workflow-Sandbox-Escape:** Workflow-Scripts konnten via dynamisches `import()` Code außerhalb der Sandbox ausführen.
- **Agent `bypassPermissions`:** Die `bypassPermissions`-Option in Agent-Definitionen ignorierte die Org-Policy zum Deaktivieren dieses Modus.

**Typ:** 🐛 Bugfix (sicherheitskritisch)
**Relevanz:** Das Setup hat 182 Agents und diverse Workflow-Scripts. Die `bypassPermissions`-Referenzen in den Claude Agent SDK Skills (`skills/claude-agent-sdk/`) sollten geprüft werden — die Docs dort beschreiben das Feature, das jetzt strenger an Org-Policies gebunden ist. **Aktion:** Claude Code auf v2.1.223 updaten. In `rules/security.md` die neuen Bypass-Vektoren (Unicode-Padding, dynamic imports) als bekannte, jetzt gefixte Risiken dokumentieren.

### 2. 🔧 `/review` ist jetzt Alias von `/code-review` (v2.1.223, 6. Aug.)

`/review` leitet intern auf `/code-review` weiter.

**Typ:** 🔧 Verbesserung
**Relevanz:** Das Setup hat keinen eigenen `commands/review.md` — kein Namenskonflikt. Aber 17 Command-Dateien referenzieren `/code-review` oder Review-Workflows. **Aktion:** In `CLAUDE.md` unter "Key Commands" den Alias `/review` = `/code-review` dokumentieren. Ggf. in `commands/orchestrate.md` und `commands/full-review.md` den kürzeren `/review`-Alias nutzen.

### 3. 🆕 `/code-review ultra` für Deep Cloud Review (v2.1.223, 6. Aug.)

`/code-review` merkt sich jetzt den letzten Effort-Level. Neuer Level `ultra` nutzt Cloud-basierte Deep-Analyse.

**Typ:** 🆕 Neues Feature
**Relevanz:** **Aktion:** In `CLAUDE.md` unter "Key Commands" den Eintrag für `/code-review` erweitern: `— Security + quality review (merkt sich Effort; /code-review ultra für Deep Cloud Review)`. In `commands/orchestrate.md` den Review-Schritt auf `/code-review high` oder `/code-review ultra` upgraden.

### 4. 🛡️ PreToolUse Auto-Allow Hooks: Bypass in Background Agents gefixt (v2.1.222, 4. Aug.)

Auto-Allow-Hooks konnten bisher Tool-Restrictions in Background Agent Tasks umgehen. Jetzt werden PreToolUse-Hooks auch dort korrekt durchgesetzt.

**Typ:** 🐛 Bugfix (sicherheitsrelevant)
**Relevanz:** Das Setup hat PreToolUse-Hooks für dev-server-blocking, git-push-Warnungen und .md/.txt-Blocking. Diese greifen jetzt zuverlässig auch in Hintergrund-Agents. **Kein Handlungsbedarf**, aber die Hooks sind jetzt deutlich robuster.

### 5. 🛡️ Worktree-Isolation jetzt vollständig (v2.1.222, 4. Aug.)

Worktree-isolierte Sessions und Subagents konnten destruktive Git-Commands gegen das Main Checkout ausführen. Gefixt.

**Typ:** 🐛 Bugfix
**Relevanz:** 27 Dateien im Setup referenzieren Worktrees (u.a. `git-worktree-manager`, `agenthub`, `root-cause-tracing`). Agents mit `isolation: 'worktree'` sind jetzt vollständig isoliert. **Kein Handlungsbedarf**, aber Worktree-basierte Workflows sind jetzt produktionsreif.

### 6. 🆕 Owner-Wildcards für Marketplace-Settings (v2.1.223, 6. Aug.)

`strictKnownMarketplaces` und `blockedMarketplaces` akzeptieren jetzt `"owner/*"`-Einträge für Org-weite Repo-Kontrolle.

**Typ:** 🆕 Neues Feature
**Relevanz:** Das Setup nutzt Plugins aus 8 verschiedenen Marketplace-Quellen. **Aktion:** In `settings.json` können jetzt ganze Orgs erlaubt werden, z.B. `"anthropics/*"` oder `"levnikolaevich/*"` statt einzelner Repos. Vereinfacht die Marketplace-Verwaltung.

### 7. 🆕 `/teleport` für Cloud Sessions (v2.1.223, 6. Aug.)

Cloud-Sessions zeigen jetzt einen Hint mit `/teleport`, um die Session lokal fortzusetzen via `claude --teleport <session id>`.

**Typ:** 🆕 Neues Feature
**Relevanz:** **Aktion:** In `CLAUDE.md` unter "Key Commands" oder einem neuen Abschnitt "Cloud/Remote" dokumentieren: `/teleport` — Session lokal fortsetzen.

### 8. 🔌 Python SDK v0.120.2: MCP SDK v2 Support (28. Juli)

Das Python SDK unterstützt jetzt MCP SDK v2 neben v1.

**Typ:** 🔧 Verbesserung
**Relevanz:** Das Setup nutzt 4 MCP-Server (lightpanda, dbhub, linkedin, gsc-mcp). MCP SDK v2 bringt Performance-Verbesserungen. **Aktion:** Bei nächstem `pip install --upgrade anthropic` wird v2-Support automatisch aktiv. Keine Setup-Änderung nötig, aber MCP-Server-Autoren könnten v2-only-Features nutzen.

## 🟡 Interessant, kein sofortiger Handlungsbedarf

### Inference Hooks Beta für Enterprise (Plattform, 5. Aug.)

Enterprise-Organisationen können jetzt einen eigenen AI-Security-Server einbinden, der jeden Prompt (claude.ai, Cowork, Claude Code) vor der Inferenz prüft und erlaubt/ablehnt. Betrifft nur Enterprise-Kunden, aber zeigt die Richtung: externe Compliance-Kontrolle über Claude Code Prompts.

### Claude Opus 4.1 retired (Plattform, 5. Aug.)

`claude-opus-4-1-20250805` gibt jetzt Fehler zurück. Keine Referenzen im Setup gefunden — kein Handlungsbedarf.

### `CLAUDE_CODE_DISABLE_1M_CONTEXT` Verhalten geändert (v2.1.223)

Diese Env-Variable hält jetzt alle Claude-Modelle mit nativem 1M-Fenster auf 200K via Auto-Compaction (vorher nur bestimmte Modelle). Startup-Warning wenn Auto-Compaction nicht auf 200K begrenzt. Keine Referenz im Setup, aber relevant wenn du Kontextfenster manuell steuerst.

### Gateway Model Discovery Fix (v2.1.223)

Claude-Modelle mit Provider-Prefixen (`vertex_ai/claude-*`, `bedrock/anthropic.claude-*`) wurden in der Gateway-Model-Discovery versteckt. Jetzt gefixt. Relevant wenn du Claude Code über Bedrock/Vertex betreibst.

### Auto-Mode Security: SendMessage Permission Classifier (v2.1.222)

Nachrichten an andere Agent-Sessions via `SendMessage` werden jetzt vor dem Versand vom Permission Classifier evaluiert. Stärkt die Sicherheit bei Multi-Agent-Orchestrierung.

### `disable-model-invocation` Refusal verbessert (v2.1.222)

6 Skills im Setup verwenden dieses Flag. Die UX bei versehentlicher Invokation wird besser. Kein Handlungsbedarf.

### Ultraplan entfernt (v2.1.222)

Keine Referenzen im Setup gefunden — kein Handlungsbedarf.

### Dreams unterstützt Claude Opus 5 (Plattform, 1. Aug.)

Dreams Research Preview (Managed Agents) unterstützt jetzt Opus 5. Betrifft die API, nicht direkt Claude Code.

### Model-Restriction-Warnungen für Subagents (v2.1.223)

Workflow-Agents, geforkte Skills, Slash-Commands und wiederaufgenommene Background-Agents zeigen jetzt eine Warnung, wenn ihr angefordertes Subagent-Modell eingeschränkt ist. Verbessert Debugging bei Modellwechseln.

## ⚪ Zur Kenntnis

| Änderung | Version | Typ |
|----------|---------|-----|
| Resumed Sessions nach `/cd` kommen nicht mehr leer zurück | v2.1.223 | 🐛 |
| Managed Settings: Server-Settings deaktivieren nicht mehr lokale `managed-settings.json` | v2.1.223 | 🐛 |
| Sandboxed Commands auf Linux bei `denyWrite` über Working Directory gefixt | v2.1.223 | 🐛 |
| Geforkte Background-Agents bleiben nicht mehr bei "already resuming" hängen | v2.1.223 | 🐛 |
| Resumed Sessions mit malformed Diagnostics-Attachment gefixt | v2.1.223 | 🐛 |
| `/usage-credits` Fehlermeldung auf Team/Enterprise korrigiert | v2.1.222 | 🐛 |
| `/usage` falsche Attribution an MCP-Server gefixt | v2.1.222 | 🐛 |
| Startup Connectivity Check hinter HTTPS-Proxy gefixt | v2.1.222 | 🐛 |
| Stream Idle Timeout bei custom `ANTHROPIC_BASE_URL` gefixt | v2.1.222 | 🐛 |
| `SendMessage` kürzt jetzt lange Summaries statt sie abzulehnen | v2.1.222 | 🔧 |
| Org-restricted Model-Aliase fallen auf neustes erlaubtes Modell zurück | v2.1.222 | 🔧 |
| Verbesserte `/diff`-Ansicht für Raw Git Blob Content | v2.1.222 | 🔧 |
| Vim Mode: Yank-Register und Undo gefixt | v2.1.222 | 🐛 |
| PR-Linking nach Branch-Push (inkl. GitHub REST API) gefixt | v2.1.222 | 🐛 |
| Python SDK v0.120.0: Claude Opus 5 Modell, Tool-Addition/Removal-Blocks | v0.120.0 | 🆕 |
| Python SDK v0.119.0: Neuer Stop-Reason `model_context_window_exceeded` | v0.119.0 | 🆕 |

## 📊 Zusammenfassung

| Kategorie | Anzahl |
|-----------|--------|
| 🔴 Sofort relevant | 8 |
| 🟡 Interessant | 9 |
| ⚪ Zur Kenntnis | 16 |
| Davon sicherheitskritisch | 6 |

**Wichtigste Aktion:** Claude Code auf v2.1.223 updaten — 4 Security-Fixes + `/code-review ultra` + `/review`-Alias.

**Quellen:**
- platform.claude.com/docs/en/release-notes/overview (5. Aug., 1. Aug.)
- github.com/anthropics/claude-code/releases (v2.1.222, v2.1.223)
- github.com/anthropics/anthropic-sdk-python/releases (v0.119.0 – v0.120.2)
