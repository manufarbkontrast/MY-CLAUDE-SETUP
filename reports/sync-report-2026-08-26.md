## Täglicher Sync-Report – 2026-08-26

### Git Status
- `git fetch origin main` — kein Delta, HEAD == origin/main (`a89bf95`)
- Letzter Commit vor diesem Lauf: `a89bf95` — docs: daily sync report 2026-08-16
- Keine neuen Commits seit dem 16.08. (10 Tage)

### Inventar

| Kategorie | Anzahl | Veränderung | Status |
|-----------|--------|-------------|--------|
| Skills (Verzeichnisse) | 466 | +0 | OK (32 Ladefehler behoben) |
| Skills (Symlinks) | 7 | +0 | alle broken (bekannt) |
| Skills (MD-Dateien gesamt) | 2715 | +0 | OK |
| Agents | 182 | +0 | 1 Warnung (leere Datei) |
| Commands | 192 | +0 | OK |
| Rules | 9 | +0 | OK |
| settings.json | — | valides JSON | OK |

---

### ⚠️ Neuer Befund: 32 Skills/Agents waren für Claude Code nicht ladbar

Erstmals wurde die Frontmatter **aller** 645 Skill- und Agent-Dateien strikt
gegen YAML validiert. Ergebnis: 32 Einträge lagen zwar im Repo, konnten von
Claude Code aber nicht registriert werden. Frühere Reports haben nur das
Vorhandensein der Dateien gezählt, nicht ihre Ladbarkeit — der Befund ist
also nicht neu entstanden, sondern war bisher unentdeckt.

**Defekt A — gar keine Frontmatter (16 Dateien)**

Ohne `name:`/`description:` wird ein Skill bzw. Agent nie indexiert und
damit nie ausgelöst.

- Skills (10): `claude-code`, `firecrawl-cache-verification`,
  `firecrawl-sdk-v2-integration`, `google-adk-python`,
  `nextjs-fullstack-type-threading`, `optional-feature-enrichment-pipeline`,
  `project-guidelines-example`, `shopify-pagination-since-id`,
  `social-media-browser-scraping`, `verification-loop`
- Agents (6): `auth-tester`, `constitution-updater`, `monorepo-architect`,
  `project-config-manager`, `service-mesh-expert`, `threat-modeling-expert`

→ Frontmatter ergänzt, `description` jeweils aus dem vorhandenen Inhalt der
Datei abgeleitet (Titel + „When to Use"-Abschnitt).

**Defekt B — ungültiges YAML bzw. fehlendes `name:` (16 Agents)**

Bei 10 Agents enthielt ein unquotierter `description:`-Wert einen Doppelpunkt
(`… Examples:`) und lief anschließend über mehrere Zeilen inkl. `<example>`-
Blöcken weiter — der YAML-Parser bricht dort ab. Bei 6 weiteren Agents fehlte
der `name:`-Key vollständig.

`bun-migration-assistant`, `bun-performance-analyzer`, `bun-troubleshooter`,
`cors-debugger`, `event-notification-setup`, `kv-debugger`, `kv-optimizer`,
`multipart-orchestrator`, `queue-debugger`, `queue-optimizer`,
`r2-setup-automator`, `s3-migration-planner`, `studio-setup-assistant`,
`workers-performance-analyzer`, `workers-security-auditor`,
`workers-test-generator`

→ `description` auf einen YAML-Block-Scalar (`|-`) umgestellt, fehlende
`name:`-Keys aus dem Dateinamen ergänzt. Der Textinhalt wurde dabei **nicht**
verändert: Wort-für-Wort-Vergleich vor/nach dem Eingriff zeigt null Verluste,
die Dateikörper sind byte-identisch. Die Änderung ist reine Einrückung.

**Validierung nach dem Eingriff:** 644 von 645 Dateien parsen sauber und
haben `name` + `description`. Verbleibend: nur `agents/deployment-engineer.md`
(siehe unten).

---

### Offene Warnungen (unverändert, lokale Korrektur nötig)

| Datei | Problem | Seit | Tage offen |
|-------|---------|------|------------|
| `agents/deployment-engineer.md` | Datei ist leer (0 Bytes) | 24.06. | 63 |
| `skills/create-agent-adapter` | Broken symlink → `/Users/craftongmbh/paperclip/skills/` | 29.06. | 58 |
| `skills/paperclip` | Broken symlink → dito | 29.06. | 58 |
| `skills/paperclip-create-agent` | Broken symlink → dito | 29.06. | 58 |
| `skills/para-memory-files` | Broken symlink → dito | 29.06. | 58 |
| `skills/pr-report` | Broken symlink → dito | 29.06. | 58 |
| `skills/release` | Broken symlink → dito | 29.06. | 58 |
| `skills/release-changelog` | Broken symlink → dito | 29.06. | 58 |

Beide Punkte lassen sich nur lokal beheben: Die leere Agent-Datei hat keinen
Inhalt, aus dem sich etwas rekonstruieren ließe, und die 7 Symlinks zeigen auf
einen macOS-Pfad, der im Remote-Container nicht existiert. Empfehlung: lokal
entweder die Inhalte materialisieren (`rsync -avL`) oder die Symlinks entfernen.

---

### Hinweis zum Auftrag

Die Schritte 2–3 des Task-Prompts (`claude mcp add`, Kopieren nach
`~/.claude/agents/`) sind in dieser Umgebung nicht ausführbar und auch
inhaltlich nicht der richtige Mechanismus:

- Der Lauf findet in einem frischen, kurzlebigen Remote-Container statt.
  Das dortige `~/.claude/` ist eine Container-Installation, nicht Manus
  Arbeitsrechner — ein Sync dorthin hätte keinen Effekt.
- Skills und Agents werden in Claude Code **nicht** über `claude mcp add`
  registriert. MCP ist für Server. Skills/Agents sind dateibasiert und werden
  über ihre YAML-Frontmatter entdeckt.

Die „Verknüpfung" mit Claude Code ist deshalb genau das, was oben repariert
wurde: gültige, vollständige Frontmatter. Ein Skill ohne `name`/`description`
ist im Repo vorhanden, für Claude Code aber unsichtbar.

### Sync-Status
- Repository: aktuell, kein Delta zu remote
- Ladbarkeit Skills/Agents: 644/645 (99,8 %) — vorher 613/645 (95,0 %)
- Letzter Sync-Report: 16.08. (10 Tage Lücke)
