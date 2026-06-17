# ViMax — Integrationsplan für die Content-Pipeline

Bewertung und Adoptionsplan für [HKUDS/ViMax](https://github.com/HKUDS/ViMax) im Kontext
der bestehenden AI-Content-Repos.

## Warum ViMax

ViMax ist ein **end-to-end agentisches Video-Framework** (Idea/Novel/Script → Video) mit
Multi-Agent-Orchestrierung für Storytelling, Charakter-Design, Storyboarding, Asset-Erzeugung
und — entscheidend — **Konsistenz-Validierung über viele Shots**. Stack: Python (UV),
OpenAI/OpenRouter-kompatible LLMs, Bild via Google API/Nanobanana, Video via Veo, plus RAG
und eine Agent-TUI.

Das löst genau die Lücke der heutigen Repos: sie sind eher **Prompt-Generatoren + Scraper,
manuell zusammengeklebt** und haben keine durchgängige Konsistenz-/Orchestrierungsschicht.

## Bezug zu bestehenden Repos

| Repo | Heutiger Stand | Was ViMax beiträgt |
|------|----------------|--------------------|
| `shoesplease-ai-studio` | Shopify-Scraper → Gemini/Fal + Higgsfield → Meta Ads, Virality-Scoring | Ersetzt den ad-hoc Generierungs-Kern durch eine agentische Pipeline mit Shot-Konsistenz; Scraper + Meta-Ads-Launch + Virality bleiben als Layer davor/danach |
| `shoes-please-video-prompts` | Prompt-Generator für Schuh-Videos | Geht im Script2Video-Stage von ViMax auf; Prompts werden Input des Storyboard-Agents |
| `feldstation-wildlife-monitor` | YouTube-Transcript → Script-Produktion | Script2Video erzeugt daraus direkt episodisches Video |
| `bob-story-maker` | Story-Erzeugung | Novel2Video / Idea2Video als Backend |
| `Viral-Video-Scraper` | Scraping viraler Videos | Liefert Referenz-/Trainingsmaterial für Stil-Vorgaben |

**Killer-Feature für Commerce: AutoCameo** — eigene Fotos als konsistente Charaktere. Damit
lassen sich Produkt-/Merch-Videos mit wiederkehrenden „Models" oder Maskottchen erzeugen
(SHOES.PLEASE-Produkte, merchscene-Artists), statt bei jedem Shot neu zu würfeln.

## Empfohlene Architektur

ViMax **nicht** in ein bestehendes Repo mergen, sondern als eigenständigen Service forken
und die vorhandenen Repos als vor-/nachgelagerte Layer anbinden:

```
[Shopify/Scraper Layer]      → bestehende Repos (shoesplease-ai-studio Scraper)
        │  (Produktdaten, Briefing, Referenzbilder)
        ▼
[ViMax Core (Fork)]          → Idea/Script2Video, Storyboard, Asset-Gen, Konsistenz-Check
        │  (fertige Clips + Metadaten)
        ▼
[Distribution Layer]         → Meta-Ads-Launch + Virality-Scoring (shoesplease-ai-studio),
                               YouTube-Upload (feldstation), merchscene-Streaming
```

Schnittstelle dünn halten: ein Job-Contract (JSON) zwischen den Layern — `brief`,
`reference_images`, `dials`, danach `clips[]` + `scores`.

## Risiken / Prüfpunkte vor dem Commit

1. **Lizenz** von ViMax und der genutzten Modelle (Veo/Nanobanana) — kommerzielle Nutzung klären.
2. **Kosten**: Veo-Video-Gen ist teuer; Budget-Caps + Virality-Pre-Scoring *vor* der Voll-Generierung einbauen.
3. **Provider-Mapping**: ViMax ist OpenAI/OpenRouter-kompatibel → an bestehende Gemini/Fal-Keys via Router anbinden statt neuer Abhängigkeiten.
4. **Reproduzierbarkeit**: Seeds/Asset-IDs persistieren, damit Re-Runs konsistent bleiben.

## Nächste Schritte (konkret)

- [ ] ViMax forken, lokal mit UV aufsetzen, Idea2Video-Demo mit einem echten SHOES.PLEASE-Produkt durchspielen
- [ ] AutoCameo mit 3–5 Produktfotos testen (Konsistenz über 5+ Shots bewerten)
- [ ] Job-Contract (JSON) zwischen `shoesplease-ai-studio` Scraper und ViMax definieren
- [ ] Kosten-/Budget-Guardrails + Virality-Pre-Scoring als Gate einbauen
- [ ] Entscheidung: ersetzt ViMax den Generierungs-Kern von `shoesplease-ai-studio` oder läuft es parallel als A/B?

> Status: Bewertung. Noch kein Code adoptiert — dieser Plan ist die Entscheidungsgrundlage.
