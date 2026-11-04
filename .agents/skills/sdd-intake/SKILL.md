---
name: sdd-intake
description: "Accept a new requirements document into the pipeline: immutable numbered snapshot, feature passport, empty decisions files. Use when the user brings a new business requirements / functional specification document for a feature."
---

# sdd-intake: accept the input

Parameters: feature ID (matches `feature_id_pattern` in `sdd.config.json`), short title, path to the input. Missing - ask and stop.

## Before you start

The input must be Markdown. Anything else (Word, wiki page, PDF, Google Doc) - ask the user to convert it with a tool of their choice (pandoc, the wiki's export, copy-paste) and put the `.md` into `features/<ID>-<slug>/source/import/`. Do not convert or retell it yourself: the snapshot must be the document, not your reading of it.

## Do

1. Create the folder `features/<ID>-<slug>/` (slug - Latin kebab-case from the title) and put the input into `source/import/` if it is not there.
2. Call subagent `sdd-source`: feature folder, mode `snapshot`, the input path, origin as the user described it (name, link, version).
3. Create `README.md` from `templates/feature/passport.md`: frontmatter (`status: intake`, `source`, `owner` - ask if unknown, `updated` - today), Summary from the input's goals and scope sections with section numbers, constraints from the input. Leave "Spec plan" as in the template.
4. Create `decisions/questions.md`, `decisions/decisions.md`, `decisions/manual.md` from the templates, without blocks: questions.md - only frontmatter and title; decisions.md - the same; manual.md - with "No interventions yet."
5. History row: "Input accepted, version <N>; snapshot made".

## Never

Edit `source/source.md`, retell the input, invent the owner or version.

## Self-check

- [ ] `source/source.md`, `source/index.md` exist; the report of `sdd-source` has no errors.
- [ ] Call subagent `sdd-check`: scope - the feature folder, mode `fix`.

## Answer

Feature folder, number of sections, whether headings were numbered by the script, and the human check: section numbers match the original, tables and images survived conversion. Next step - `sdd-map`.
