# Eigene Messungen: MacBook Pro M5 Max, 128 GB

Setup: macOS 26.6, `iogpu.wired_limit_mb=112000`, Python 3.12, mlx 0.32.2, mlx-lm 0.31.3.
Gemessen mit `mlx_lm.generate` (Einzelanfrage, kein Batching).

| Datum | Modell | Quant | Prompt-Token | Prompt t/s | Generierung t/s | Peak Memory |
|---|---|---|---|---|---|---|
| 2026-09-25 | mlx-community/Qwen3.6-35B-A3B-8bit | 8-bit | 38 | (Warm-up) | 98,8 | 37,0 GB |
| 2026-09-25 | mlx-community/Qwen3.6-35B-A3B-8bit | 8-bit | 12.216 | 3.654 | 93,4 | 38,9 GB |

## Einordnung

- 12K Token Prompt in ~3,3 s: Claude Codes ~20K-Token-Kontext liegt damit bei ~6 s für die erste Runde.
- Generierung fällt von 4K auf 12K Kontext nur um ~5 %.
- 12K Kontext kosten ~2 GB zusätzlich; bei 64K Kontext sind grob ~48 GB zu erwarten.

## Befehle

```bash
source ~/.venvs/mlx/bin/activate
M=~/.lmstudio/models/mlx-community/Qwen3.6-35B-A3B-8bit
# kurz
mlx_lm.generate --model $M --max-tokens 400 --prompt "…"
# lang (Repo-Code als Prompt)
(cat src/*.ts; echo "Fasse die Architektur zusammen.") | mlx_lm.generate --model $M --max-tokens 300 --prompt -
```

## Executor-Läufe (Claude Code headless gegen Qwen3.6-35B-A3B 8-bit)

Aufgabe: Plan `filter-v2` (2 Dateien, 5 Schritte, 5+ neue Tests) im Testprojekt `~/local-llm-test`.

| Lauf | Konfiguration | Dauer | Autocompact | Tests |
|---|---|---|---|---|
| v2 | volles `~/.claude`, 64K Fenster | 3:44 | thrashing | 11/11 grün |
| v2b | leere Konfiguration, 64K Fenster | 2:05 | thrashing | 1 rot (Test-Erwartung falsch, Code korrekt) |
| v2c | leere Konfiguration, 128K Fenster, 16K max. Antwort | **1:02** | ok | 14/14 grün (Executor durfte `node --test` nicht selbst ausführen) |

Erkenntnisse:
- Kontextfenster für Claude Code mindestens 128K angeben und Antwortlänge begrenzen, sonst Autocompact-Schleifen.
- Der Code des lokalen Modells war in allen Läufen korrekt; selbst ausgedachte Test-Erwartungen nicht immer
  → Kern-Tests gibt der Plan wörtlich vor (`/local-delegate`), der Kritiker prüft Test vs. Code.
