# Lokale Modelle auf dem MacBook Pro M5 Max (128 GB / 8 TB)

Stand: 24.09.2026. Ziel: Claude plant, lokale Modelle setzen um und prüfen gegen.
Das Harness-Gerüst dazu liegt in `scripts/local-llm/` und `commands/local-delegate.md`.

---

## 1. Was die Hardware kann

| Eckdaten | Wert | Was das bedeutet |
|---|---|---|
| Unified Memory | 128 GB | davon standardmäßig ~96 GB für die GPU nutzbar, anhebbar auf ~112 GB |
| Speicherbandbreite | 614 GB/s | bestimmt die Token/s: pro Token werden die **aktiven** Gewichte einmal gelesen |
| SSD | 8 TB | Platz für eine Bibliothek aus 20–40 Modellen (1–2 TB) plus Datensätze |

Faustregel: **MoE-Modelle mit wenigen aktiven Parametern sind auf dem Mac König.**
Ein 80B-MoE mit 3B aktiven Parametern ist schneller als ein dichtes 27B-Modell.

Gemessene Werte auf M5 Max 128 GB mit MLX ([hardware-corner.net](https://www.hardware-corner.net/m5-max-local-llm-benchmarks-20261233/)):

| Modell | Quant | RAM | Prompt t/s (16K) | Generierung t/s (4K → 32K) |
|---|---|---|---|---|
| gpt-oss-120B | Q8 | 64 GB | 2.710 | 88 → 65 |
| Qwen3-Coder-Next (80B-A3B) | 8-bit | 85 GB | 1.802 | 79 → 69 (64K: 48) |
| Qwen3.5-122B-A10B | 4-bit | 70 GB | 1.239 | 66 → 55 |
| Qwen3.5-27B (dicht) | 6-bit | 26 GB | 686 | 24 → 15 |

GPU-Speicherlimit anheben (gilt bis zum Neustart):

```bash
sudo sysctl iogpu.wired_limit_mb=112000   # ~16 GB bleiben für macOS + Apps
```

---

## 2. Modell-Landkarte (Hugging Face, Stand Sept. 2026)

### Passt gut auf 128 GB

| Rolle | Modell | Typ | Quant / RAM | Warum |
|---|---|---|---|---|
| **Executor (Standard)** | **Qwen3.6-35B-A3B** | MoE, 3B aktiv | 8-bit ≈ 37 GB | sehr schnell, für agentisches Coding trainiert, Apache 2.0 |
| **Executor (Qualität)** | **Qwen3.8-27B** | dicht, 262K Kontext | 8-bit ≈ 29 GB | SWE-bench Pro 61,7 %, Terminal-Bench 2.1 73 %; langsamer (~20 t/s) |
| Executor (Alternative) | Qwen3.6-27B | dicht | 8-bit ≈ 29 GB | Vorgänger von 3.8, stark bei Frontend |
| Executor (lange Tasks) | Qwen3-Coder-Next | MoE 80B, 3B aktiv, 256K | 8-bit ≈ 85 GB | explizit für Claude-Code-/Cline-Scaffolds gebaut, gut bei Fehler-Recovery |
| **Kritiker** | **gpt-oss-120B** | MoE | Q8 ≈ 64 GB | schnell, gutes Reasoning, andere Modellfamilie als der Executor |
| Kritiker (Alternative) | Qwen3.5-122B-A10B | MoE, 10B aktiv | 4-bit ≈ 70 GB | stärker im Detail, etwas langsamer |
| Helfer / Router | Qwen3.5-9B, Gemma 4 E4B | dicht, klein | 4–8 GB | Commit-Messages, Klassifizierung, Zusammenfassungen |
| Vision | Gemma 4 31B, Qwen3.8-27B (hat Vision) | | 20–30 GB | Screenshots, UI-Vergleiche |
| Coding klein | Devstral 24B | dicht | ≈ 14 GB | SWE-bench Verified 46,8 %, sehr günstig im RAM |

### Passt **nicht** lokal (nur über API / Cloud)

GLM-5.2 (753B), Kimi K3 (2,8T), Qwen3.8-2.4T-A95B, DeepSeek V4, MiMo-V2.5-Pro.
Diese brauchen 256 GB+ oder mehrere GPUs. Sie sind die Brücke, wenn lokal nicht reicht.

### Kombinationen, die gleichzeitig laufen

| Setup | RAM gesamt (+ KV-Cache) | Nutzen |
|---|---|---|
| Qwen3.6-35B-A3B (8-bit) + gpt-oss-120B (Q8) | ≈ 101 GB + Cache | Executor + Kritiker parallel — **Wired-Limit anheben** |
| Qwen3.6-35B-A3B (4-bit) + gpt-oss-120B (Q8) | ≈ 84 GB + Cache | gleiche Rollen, mehr Luft für 64K Kontext |
| Qwen3.8-27B (8-bit) + Qwen3.5-9B | ≈ 38 GB | Qualitäts-Executor + schneller Helfer, Platz für Docker/Browser |
| Qwen3-Coder-Next (8-bit) allein | ≈ 90 GB bei 32K | lange agentische Sessions |

Hinweis: Kritiker und Executor aus **verschiedenen Familien** wählen (z. B. Qwen + gpt-oss).
Gleiche Modelle übersehen dieselben Fehler.

---

## 3. Software-Stack

| Baustein | Empfehlung | Wofür |
|---|---|---|
| Inferenz-Server | **LM Studio** (MLX-Engine) oder **Ollama** | beide sprechen die Anthropic Messages API (`/v1/messages`) → Claude Code kann direkt ran |
| Schnellste Engine | `mlx-lm` / `mlx_lm.server` | 20–50 % mehr Durchsatz als llama.cpp auf M5 |
| Modellformat | MLX (`mlx-community/*`) bevorzugt, GGUF (`unsloth/*`) als Fallback | |
| Coding-Agent lokal | **Claude Code selbst** mit `ANTHROPIC_BASE_URL` | gleiche Tools, Hooks, Skills wie gewohnt |
| Alternativen | Qwen Code, OpenCode, Aider | falls Tool-Calling mit Claude Code hakt |
| Routing (optional) | LiteLLM-Proxy oder claude-code-router | ein Endpoint, Modell je Rolle |

Installation (einmalig):

```bash
brew install ollama jq
brew install --cask lm-studio
pip install -U mlx-lm huggingface_hub
# Modelle ziehen (Beispiel LM Studio CLI)
lms get qwen3.6-35b-a3b@8bit
lms get qwen3.8-27b@8bit
lms get gpt-oss-120b
```

Modellordner auf die 8-TB-Platte legen und in LM Studio/Ollama (`OLLAMA_MODELS`) eintragen.

---

## 4. Der Harness: Claude plant, lokal setzt um, lokal prüft

```
 ┌────────────────────┐   .plans/<task>.md   ┌───────────────────────────┐
 │ Claude (Cloud)     │ ───────────────────▶ │ Executor (lokal)          │
 │ /local-delegate    │                      │ claude -p im Git-Worktree │
 │ Plan + Akzeptanz-  │                      │ ANTHROPIC_BASE_URL=local  │
 │ kriterien + Tests  │                      │ Qwen3.6-35B-A3B           │
 └─────────▲──────────┘                      └────────────┬──────────────┘
           │                                              │ Diff
           │ Eskalation nach N Runden                     ▼
           │                                 ┌───────────────────────────┐
           │                                 │ Verify: Tests, Lint, Types│
           │                                 └────────────┬──────────────┘
           │                                              ▼
           │      verdict=FAIL + Findings    ┌───────────────────────────┐
           └──────────────◀──────────────────│ Kritiker (lokal)          │
                     (zurück an Executor)    │ gpt-oss-120B, JSON-Urteil │
                                             └───────────────────────────┘
```

### Ablauf

1. **Planen (Claude, teuer, selten):** `/local-delegate <Aufgabe>` lässt Claude einen Plan in
   `.plans/<slug>.md` schreiben: Ziel, betroffene Dateien, Schritte, Akzeptanzkriterien,
   Befehl für die Tests. Je kleiner und präziser die Schritte, desto besser schafft es das lokale Modell.
2. **Umsetzen (lokal, billig, oft):** `scripts/local-llm/execute.sh` startet einen zweiten,
   headless Claude Code (`claude -p`) in einem eigenen Git-Worktree, der gegen den lokalen
   Server läuft. Gleiche Tools, gleiche Hooks — nur ein anderes Modell.
3. **Verifizieren (deterministisch):** Der Testbefehl aus dem Plan läuft. Rot = sofort zurück an den Executor.
4. **Kritik (lokal):** `scripts/local-llm/critic.sh` schickt Plan + Diff + Testausgabe an den
   Kritiker. Antwort ist JSON: `{"verdict":"PASS|FAIL","findings":[...]}`.
5. **Schleife:** Bei FAIL gehen die Findings als neuer Prompt an den Executor, maximal N Runden (Standard 3).
6. **Eskalation:** Nach N Runden oder bei PASS kommt Claude zurück ins Spiel:
   Endreview oder Übernahme der festgefahrenen Aufgabe.

Alles zusammen: `scripts/local-llm/pipeline.sh .plans/<slug>.md`.

### Drei Betriebsmodi

| Modus | Planer | Executor | Kritiker | Wann |
|---|---|---|---|---|
| **A – Lokal umsetzen** | Claude | lokal | lokal | Standardfall: klare, gut testbare Aufgaben |
| **B – Lokale Kritik** | Claude | Claude | lokal | Claude arbeitet, ein lokales Modell liefert eine zweite Meinung ohne Zusatzkosten |
| **C – Voll lokal** | lokal (Qwen3.8-27B) | lokal | lokal | offline, vertrauliche Kundendaten, Bulk-Jobs über Nacht |

Modus B geht auch ohne Pipeline: `scripts/local-llm/critic.sh <plan> main` gegen deinen Branch.

### Welche Aufgaben sich eignen

| Gut lokal | Besser bei Claude |
|---|---|
| Umsetzung nach präzisem Plan | Architektur, Planung, unklare Anforderungen |
| Tests schreiben zu bestehender Logik | Debugging über viele Dateien |
| Refactors nach Muster, Umbenennungen | Security-Review vor Release |
| Shopify-/SEO-Bulk-Texte, Meta-Descriptions | Kundenkommunikation mit Nuancen |
| Übersetzungen, Zusammenfassungen, Doku | Aufgaben ohne Testabdeckung |
| Datenextraktion aus PDFs/CSV | |

### Bekannte Stolpersteine

- **Langer System-Prompt:** Claude Code schickt ~20K+ Token Kontext. Gemessen: 3.654 t/s Prompt-Verarbeitung (Qwen3.6-35B-A3B, siehe `benchmarks.md`), also ~6 s. Bei größeren Modellen mit ~1.000–2.000 t/s
  sind das 10–20 s pro erster Runde. Prompt-Caching in LM Studio/Ollama aktiv lassen, Kontext ≥ 64K setzen.
- **Kontextfenster für Claude Code:** Claude Code kennt lokale Modelle nicht und muss die Fenstergröße gesagt bekommen
  (`CLAUDE_CODE_MAX_CONTEXT_TOKENS`). Von diesem Fenster zieht es die maximale Antwortlänge ab. Mit 64K und
  Standard-Antwortlänge blieb zu wenig Platz („Autocompact is thrashing“). Executor daher mit 128K Fenster,
  16K Antwortlänge und eigener, leerer Konfiguration (`CLAUDE_CONFIG_DIR=~/.claude-local`, `--strict-mcp-config`).
- **Zwei große Modelle in LM Studio:** LM Studios Lade-Schutz lehnt Qwen (37 GB) + gpt-oss-120b (67 GB) gemeinsam ab,
  obwohl 64 % Speicher frei sind. Der Kritiker läuft deshalb über `mlx_lm.server` (`scripts/local-llm/critic-server.sh`).
  gpt-oss liefert dort das rohe Harmony-Format (`<|channel|>analysis…final…`); `critic.sh` schneidet den Denkteil ab.
- **Tool-Calling:** Nicht jede Quantisierung hält das Tool-Format sauber. Mit 8-bit starten, erst bei Bedarf runter.
- **Thinking-Modus:** Qwen3.6/3.8 denken standardmäßig. Für den Executor gut; für schnelle Helfer `enable_thinking: false`.
- **Sampling:** Qwen3.8 Thinking: `temperature 1.0, top_p 0.95, top_k 20`. Instruct: `temperature 0.7, top_p 0.8, presence_penalty 1.5`.
- **Subagents:** Claude-Code-Agents (`agents/*.md`) kennen nur Anthropic-Modelle. Lokale Modelle deshalb über
  Skripte (Bash) einbinden, nicht über das `model:`-Feld.
- **Worktree statt Hauptbranch:** Der Executor arbeitet immer isoliert; übernommen wird nur, was Tests und Kritik bestanden hat.

---

## 5. Fahrplan

### Woche 1 – Basis
- [ ] LM Studio + Ollama installieren, Modellordner auf die SSD legen
- [ ] Qwen3.6-35B-A3B, Qwen3.8-27B, gpt-oss-120B, Qwen3.5-9B laden
- [x] Wired-Limit anheben, Token/s mit `mlx_lm.generate` selbst messen und in `docs/local-models/benchmarks.md` festhalten (Qwen3.6-35B-A3B 8-bit: 3.654 t/s Prompt, 93 t/s Generierung)
- [x] Claude Code einmal manuell gegen lokal testen (25.09.: `claude-local -p` legte Funktion + 6 Tests an, alle grün; `CLAUDE_CODE_MAX_CONTEXT_TOKENS` nötig, da Claude Code lokale Modelle nicht kennt):
      `ANTHROPIC_BASE_URL=http://localhost:1234 ANTHROPIC_AUTH_TOKEN=lmstudio claude --model qwen3.6-35b-a3b`

### Woche 2 – Harness
- [ ] `scripts/local-llm/models.conf` an die tatsächlichen Modellnamen anpassen
- [ ] `/local-delegate` an einer kleinen, echten Aufgabe mit Tests ausprobieren
- [ ] Modus B einbauen: Kritiker nach jedem größeren Claude-Commit laufen lassen

### Woche 3 – Messen statt raten
- [ ] 10–20 abgeschlossene eigene Aufgaben als Mini-Benchmark sammeln (Plan + Tests)
- [ ] Jede Aufgabe mit 2–3 Executor-Modellen laufen lassen; Erfolgsquote, Runden, Dauer notieren
- [ ] Standard-Executor und -Kritiker danach festlegen

### Danach – Erweitern
- **Eigenes Feintuning:** LoRA mit `mlx_lm.lora` auf eigene Codebasen/Texte (Shopify-Themes, Produkttexte).
  128 GB reichen für LoRA auf 27B–35B-Modellen.
- **Lokales RAG:** Embeddings (Qwen3-Embedding) über alle Repos und Kundendokumente, Suche als MCP-Server.
- **Nacht-Jobs:** Modus C per `launchd`: SEO-Texte, Übersetzungen, Test-Generierung über Nacht.
- **Prompt-Optimizer:** `po` optional über ein lokales Modell anreichern statt nur Keyword-Matching.
- **Weitere Medien:** Whisper (MLX) für Transkription, FLUX via `mflux` für Bilder.
- **Neue Modelle prüfen:** monatlich Hugging Face (`mlx-community`, `unsloth`, `Qwen`) sichten,
  neue Kandidaten durch den eigenen Mini-Benchmark schicken.

---

## Quellen

- [Qwen3.6-27B](https://huggingface.co/Qwen/Qwen3.6-27B) · [Qwen3.6-35B-A3B](https://huggingface.co/Qwen/Qwen3.6-35B-A3B) · [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) · [QwenLM/Qwen3.8](https://github.com/QwenLM/Qwen3.8)
- [Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next)
- [M5 Max Benchmarks (hardware-corner.net)](https://www.hardware-corner.net/m5-max-local-llm-benchmarks-20261233/)
- [Ollama: Claude Code Integration](https://docs.ollama.com/integrations/claude-code) · [LM Studio: Claude Code](https://lmstudio.ai/blog/claudecode)
- [Gemma 4 Überblick](https://codersera.com/blog/gemma-4-complete-guide-2026/) · [Best Ollama Models Aug. 2026](https://www.morphllm.com/best-ollama-models)
- [Open-Weight-Vergleich GLM/gpt-oss/DeepSeek](https://www.spheron.network/blog/open-weight-frontier-model-showdown-2026/)
