---
name: sdd-intake
description: "Accept a new requirements document into the pipeline: immutable numbered snapshot, feature passport, empty decisions files. Use when the user brings a new business requirements / functional specification document for a feature."
---

# sdd-intake: accept the input

Parameters: feature ID (matches `feature_id_pattern` in `sdd.config.json`), short title, path to the input (any Markdown file; the script copies it into `source/import/`), owner, origin (name, version, link if there is one). Missing ID, title, input or owner - ask and stop. No link - write the origin without it.

## Before you start

Several documents for one feature (requirements plus an addendum, a separate document of screens) - ask the user to join them into one Markdown file, each document under its own top-level heading, and make one snapshot: one feature - one numbered source.

The input must be Markdown. Anything else (Word, wiki page, PDF, Google Doc) - ask the user to convert it with a tool of their choice (pandoc, the wiki's export, copy-paste) and put the `.md` into `features/<ID>-<slug>/source/import/`. Do not convert or retell it yourself: the snapshot must be the document, not your reading of it.

## Do

1. Call subagent `sdd-source`: mode `new` with the ID, slug (Latin kebab-case from the title), title, owner (ask if unknown), origin as the user described it (name, link, version) and the input path. It creates `features/<ID>-<slug>/` with the passport, empty `decisions/` and the input in `source/import/`.
2. Call subagent `sdd-source`: feature folder, mode `snapshot`, the input path in `source/import/`, the same origin.
3. Fill the passport `README.md`: Summary from the input's goals and scope sections with section numbers; Components - only what the input names, new or existing as the input says (not said - write "new or existing - not stated" and register a question in `decisions/questions.md`); constraints from the input with section numbers; Assumptions - "None yet.". Keep the template's HTML comments, `status: intake` and "Spec plan" as they are.
4. History row: "Input accepted, version <N>; snapshot made".

## Never

Edit `source/source.md`, retell the input, invent the owner or version.

## Self-check

- [ ] `source/source.md`, `source/index.md` exist; the report of `sdd-source` has no errors.
- [ ] Call subagent `sdd-check`: scope - the feature folder, mode `fix`.

## Answer

Feature folder, number of sections, whether headings were numbered by the script, and the human check: section numbers match the original (the snapshot writes `1. Goals` as `1 Goals`; text before the first heading becomes section 0 Preamble), tables and images survived conversion. The original input file outside the feature may be deleted by the user. Next step - `sdd-map`.
