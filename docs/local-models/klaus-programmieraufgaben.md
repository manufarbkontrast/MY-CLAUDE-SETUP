# Programmieraufgaben (lokale Umsetzung)

Programmieraufgaben setzt du NICHT selbst um. Du planst, ein lokales Modell (Qwen) setzt um,
ein zweites lokales Modell (Gemma) prüft. Du bewertest das Ergebnis und berichtest.

## Ablauf
1. Repo bestimmen: Projekte liegen unter `/Users/agents/work/<projekt>` (Übungs-Repo: `demo`).
   Arbeitsverzeichnis muss sauber sein (`git status`).
2. Plan schreiben nach `/Users/agents/work/<projekt>/.plans/<slug>.md`, genau mit diesen Abschnitten:
   - `## Ziel` (1–2 Sätze)
   - `## Dateien` (jede Datei mit Pfad)
   - `## Schritte` (nummeriert, klein, konkret: Funktionsnamen, Signaturen, Verhalten)
   - `## Akzeptanzkriterien` (prüfbar)
   - `## Vorgegebene Tests` (3–6 Testfälle als fertiger Code in eigener Datei, z. B. `test/<slug>.pinned.test.js`;
     rechne jede Erwartung selbst nach – das lokale Modell darf sie nicht ändern)
   - `## Nicht tun`
   - eine Zeile `test_command: <befehl>` (z. B. `test_command: node --test`)
3. Plan committen: `git add .plans && git commit -m "plan: <slug>"`
4. Pipeline starten (dauert Minuten; Bash-Timeout 600000 ms verwenden):
   `cd /Users/agents/work/<projekt> && /Users/agents/local-llm/pipeline.sh .plans/<slug>.md`
   - Exit 0 = PASS, Exit 2 = Eskalation nach 3 Runden oder lokales Modell nicht geladen.
5. Ergebnis prüfen im Worktree `/Users/agents/work/<projekt>-local-<slug>`:
   - `git diff`, Tests selbst laufen lassen
   - vorgegebene Tests unverändert? (mit dem Plan vergleichen)
   - Logs: `.plans/logs/<slug>/` (round-N-review.json, timings.txt)
6. Übernehmen NICHT selbst. In der Aufgabe berichten: Runden, Urteil des Kritikers, deine Prüfung,
   offene Punkte – und den Menschen um Freigabe bitten. Übernahme erst nach Freigabe:
   `/Users/agents/local-llm/accept.sh <slug>` (verwerfen: `--discard`).

## Grenzen
- Meldet die Pipeline „Modell … nicht geladen“: nicht selbst umsetzen, sondern den Menschen bitten,
  `qwen`/`gemma` in LM Studio zu laden.
- Kein `git push`, keine Änderungen außerhalb von `/Users/agents/work`.
