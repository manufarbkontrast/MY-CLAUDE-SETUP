---
name: aufgaben-import
description: Extract action items from documents (call summaries, meeting notes, emails — .docx/.pdf/.md/.txt or pasted text) and file them as tasks in the user's Obsidian vault at /Users/manuwolfram/Downloads/obsidian. Use when the user provides a document or text and asks to capture tasks — "trag die Aufgaben ein", "Call-Zusammenfassung", "Action Items übernehmen", "in meine Aufgaben eintragen", "was muss ich daraus tun".
---

# Aufgaben-Import (Dokument → Vault-Tasks)

Extract action items from a document and file them in the correct vault note, following the vault's single-source-of-truth rule for tasks.

## Vault conventions

- Vault: `/Users/manuwolfram/Downloads/obsidian`
- Tasks use the Tasks-plugin emoji format: `- [ ] Text 🔺|⏫|🔼 📅 YYYY-MM-DD` (priority and date only when known)
- All open tasks surface automatically in `00_Index/Cockpit.md` — never add tasks there directly
- One task lives in exactly ONE note. For the KI-Automatisierung project the task master is `30_Projekte/KI_Automatisierung/Rollout_Plan.md`
- Use the obsidian-markdown skill conventions: wikilinks, callouts, frontmatter

## Workflow

### 1. Read the document

Use the docx skill for .docx, the pdf skill for .pdf. Plain text/markdown: read directly.

### 2. Extract action items

Only real commitments and next steps — not discussion points or FYIs. Per item capture:
- Task text (concise, imperative, German)
- Owner — if not the user, prefix with the person's name: `Name klären: …` or note `(wartet auf X)`
- Due date only if explicit or clearly implied ("bis Freitag" → resolve to absolute date)
- Priority only if inferable: 🔺 blocker/critical, 🔼 important

If it is unclear whether something is a task, list it for the user in the final report as "unsicher" instead of silently filing it.

### 3. Determine the target note

Map by topic — check `30_Projekte/_Projekt_Index.md` and `MEMORY.md` (vault root) for current project mapping:
- ÆND / merchscene / Merch → `20_Brands/AEND/` project notes
- Shoes Please / SPZ → `20_Brands/Shoes_Please/Shoes_Please.md`
- Machu / MachuPicYou → `20_Brands/Machu/Machu.md`
- KI / Automatisierung / Agents / Dashboards → `30_Projekte/KI_Automatisierung/Rollout_Plan.md` (task master)
- Other existing project → its main note in `30_Projekte/<Projekt>/`
- No clear match → `00_Index/Task_Inbox.md` (create with frontmatter `tags: [inbox, tasks]` if missing)

### 4. Dedup before writing

Search the target note and the vault for semantically matching open tasks (`grep -rn "- \[ \]" --include="*.md"` on keywords). If a task already exists: do NOT duplicate — update the existing line (e.g. add a due date) if the document adds information, and report it as "bereits vorhanden".

### 5. Archive the source document

Save the summary as a note next to the target: `<Projektordner>/Calls/YYYY-MM-DD <Thema>.md` with frontmatter (`date`, `teilnehmer` if known, `quelle` = original filename) and the key content in Obsidian Markdown. Skip if the user only pasted a few lines of text.

### 6. File the tasks

Append under a `## Aufgaben` heading (reuse an existing suitable section — in phased notes like Rollout_Plan, add to the matching phase). Format:

```markdown
- [ ] Klaviyo-Winback-Flow für ÆND briefen 🔼 📅 2026-08-02 (aus [[2026-07-26 Call Klaviyo]])
```

Always link the source note in parentheses so provenance is clickable.

### 7. Report

Tell the user: how many tasks filed, in which note(s), which were duplicates/updated, and which items were ambiguous. Remind that everything shows up live in [[Cockpit]].
