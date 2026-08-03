---
name: podcast
description: Create a NotebookLM audio overview (podcast) from a document or from the current session context using the notebooklm CLI. Use when the user says "Podcast", "mach einen Podcast", "erstell einen Podcast", or asks for an audio summary / Audio Overview of a file, document, meeting notes, URL, or the current conversation.
---

# Podcast (NotebookLM Audio Overview)

Turn a document, URL, or the current session context into a podcast MP3 via the `notebooklm` CLI.

## Prerequisites

`notebooklm` CLI must be installed and authenticated. If any command fails with an auth error, run `notebooklm doctor` and ask the user to type `! notebooklm login` in the prompt (interactive Google login).

## Workflow

### 1. Determine the source

- **User names a document or URL** → use that as the source. Local files (.docx, .pdf, .md, .txt) and URLs upload directly; no conversion needed.
- **No document named** ("mach einen Podcast" mid-session) → distill the current session into a markdown file in the scratchpad directory. Structure it as: Thema, Kontext, wichtigste Erkenntnisse/Entscheidungen, offene Punkte, nächste Schritte. Write full prose, not terse bullets — this text is the only thing the podcast hosts will see.

### 2. Create (or reuse) a notebook

Check `notebooklm list` first — if a notebook for the same document/topic already exists, add the new source to it instead of creating a duplicate. Otherwise:

```bash
notebooklm create "<kurzer Titel>" --json   # capture the returned notebook id
```

### 3. Add the source and wait for processing

```bash
notebooklm source add "<file-or-url>" -n <notebook-id> --timeout 120
# prints "Added source: <source-id>"
notebooklm source wait <source-id> -n <notebook-id>
```

Pitfall: `source wait` requires the SOURCE_ID as a positional argument.

### 4. Generate the audio

Generation takes 3–10 minutes — always run it as a background task (`run_in_background`), then tell the user generation has started.

```bash
notebooklm generate audio "<Fokus-Prompt>" -n <notebook-id> --language de --wait --timeout 1200
```

- Default language is **German** (`--language de`) unless the user asks otherwise.
- Default style is deep-dive. If the user wants it short: `--length short` and/or `--format brief`. Other formats: `critique`, `debate`.
- Write the focus prompt in German, tailored to the request, e.g. "Fasse den aktuellen Stand zusammen: wichtigste Entscheidungen, offene Punkte und nächste Schritte".

### 5. Download the MP3

```bash
notebooklm download audio "/Users/manuwolfram/Downloads/<Titel> Podcast.mp3" -n <notebook-id>
```

Pitfall: the output path is a **positional argument** — there is no `-o`/`--output` flag.

Default output location: `~/Downloads/`. The command prints the NotebookLM-generated episode title ("Artifact: ...") — include it in the final report.

### 6. Report

Tell the user: file path, episode title, and the notebook id so they can add more sources later (`notebooklm source add <datei> -n <id>`).
