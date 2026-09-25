# Local Delegate — Claude plant, lokales Modell setzt um

Du bist der Planer. Ein lokales Modell (siehe `scripts/local-llm/models.conf`) setzt den Plan um,
ein zweites lokales Modell prüft ihn. Details: `docs/local-models/PLAN.md`.

## Aufgabe

$ARGUMENTS

## Vorgehen

1. **Verstehen:** Lies die relevanten Dateien. Kläre offene Fragen mit dem Nutzer, bevor du planst.
2. **Plan schreiben** nach `.plans/<kurzer-slug>.md` mit genau diesen Abschnitten:
   - `## Ziel` — ein bis zwei Sätze
   - `## Dateien` — jede Datei, die angelegt oder geändert wird, mit Pfad
   - `## Schritte` — nummeriert, jeder Schritt klein und konkret (Funktionsnamen, Signaturen, erwartetes Verhalten).
     Ein lokales 27B–35B-Modell muss ihn ohne Rückfragen umsetzen können.
   - `## Akzeptanzkriterien` — prüfbare Aussagen
   - `## Vorgegebene Tests` — die 3–6 wichtigsten Testfälle wörtlich (Eingabe + erwartetes Ergebnis, am besten als
     fertiger Testcode). Lokale Modelle verrechnen sich bei selbst ausgedachten Erwartungen; diese Tests darf der
     Umsetzer nicht ändern, er ergänzt nur weitere.
   - `## Nicht tun` — was ausdrücklich außerhalb des Scopes liegt
   - eine eigene Zeile `test_command: <befehl>` (z. B. `test_command: npm test -- src/foo`)
   Wenn es noch keine Tests gibt: Schritt 1 ist, die Tests zu schreiben.
3. **Prüfen, ob der lokale Server läuft:**
   `curl -s http://localhost:1234/v1/models` (LM Studio) bzw. `curl -s http://localhost:11434/api/tags` (Ollama).
   Läuft keiner, sag dem Nutzer, welches Modell er starten soll, und stoppe hier.
4. **Pipeline starten:** `scripts/local-llm/pipeline.sh .plans/<slug>.md` (im Hintergrund, dauert Minuten).
5. **Ergebnis bewerten:**
   - Exit 0 (PASS): Diff im Worktree `../<repo>-local-<slug>` selbst reviewen, dann dem Nutzer die Übernahme
     von Branch `local/<slug>` vorschlagen (`scripts/local-llm/accept.sh <slug>`).
     Vorher prüfen, dass die vorgegebenen Tests unverändert sind.
   - Exit 2 (Eskalation): Logs in `.plans/logs/<slug>/` lesen, Plan präzisieren und erneut starten —
     oder die Aufgabe selbst übernehmen, wenn sie für das lokale Modell zu schwer ist.
6. Fasse zusammen: Runden, Urteil des Kritikers, was du geprüft hast, was offen ist.

## Nur Kritik (Modus B)

Wenn der Nutzer nur eine zweite Meinung zu vorhandenen Änderungen will:
`scripts/local-llm/critic.sh .plans/<slug>.md main` und die Findings bewerten — nicht blind übernehmen.
