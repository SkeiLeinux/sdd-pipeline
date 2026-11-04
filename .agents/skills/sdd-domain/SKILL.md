---
name: sdd-domain
description: "Extract the requirements of one domain of the map from its source slice into requirements/<domain>.md, register questions, record findings for other domains; for a UI domain also the 'Screen fields' table. Use after the domain map is approved, one domain per run."
---

# sdd-domain: requirements of one domain

Parameters: feature folder and domain name. No map or no such domain - stop and suggest `sdd-map`. One run - one domain.

## Step 0. Slice

Call subagent `sdd-source`: mode `slices`, the domain. An error - stop and show it: the domain's Read list in `analysis.md` must be fixed first.

## Read

1. `analysis.md`: "How to read the map", the domain's row in "Domains", its subsection in "Source slices", "Cross-cutting rules", "Glossary", its subsection in "Findings for domains".
2. The slice `source/domains/<domain>.md` - whole. Do not read the snapshot section by section.
3. `requirements/README.md` and files of neighbouring domains - only to avoid duplicates. `requirements/dispositions.md`, if present.
4. `decisions/questions.md` and `decisions/decisions.md` - questions and decisions about this domain.
5. `templates/feature/requirements.md`, the example `examples/LIB-1-book-reservations/requirements/` for the form.
6. Next free IDs: `python tools/check.py <feature> --next`.

## Do

1. Every testable statement of the slice whose home is this domain (rules of one home in `analysis.md`) - a requirement. Every row of a logic table in the source whose rule lives in this domain - a separate requirement; compare the counts. Rows whose rule lives elsewhere (field rules in a UI or edge domain) - only what this domain adds: the label for a screen, the field in an operation for an edge. An operation or field the edge needs but the source does not state ("get one claim") - a requirement with Note "design: <why it is needed>", not a fact of the source.
2. `requirements/<domain>.md` by the template: "Boundary", subsections by topic, the seven columns. Source - section numbers as in the snapshot, always. Scope - `in` for components we spec, `out` for what other systems must do. Type - from `requirement_types`. Wording close to the source, entity names from the Glossary; interface texts verbatim, in quotes.
3. A requirement whose home is another domain: that domain not analysed yet - a bullet under its name in "Findings for domains" (only when it adds something that domain's Read list will not show: a question, a REQ to link, a decision); already analysed - a row in its file. Never the same requirement in two files. Events: the trigger of a notification or message lives in the domain whose action causes it; its delivery and text - in the edge.
4. UI domain: section "Screen fields" - every field and action of the screens in the slice, the rule behind it (node REQ) and the operation that feeds it (edge REQ now; `sdd-contracts` may replace it with the CON ID). The screen is not a source of data.
5. Gaps, contradictions, vague words ("if needed", "several times"), two names for one thing, every "Watch:" item of this domain - a block in `decisions/questions.md` and a marker `[?Q-NNN]` in the Note column. A contradiction: never choose a side - the contested value in the requirement text carries the marker ("3 working days [?Q-025]"), both values are in the Note. An existing open question now also blocks your requirements - add them to its `Blocks`. A new question also blocks a requirement of an already analysed domain - add it to `Blocks` and the marker to that row's Note (the checker reports `q-blocks-marker` otherwise). A decision already exists - apply it and cite `(Q-NNN)`. Check the domain as a whole: who acts, what triggers it, the result, edge cases and errors, access rights, audit.
6. Findings of this domain in "Findings for domains" - applied; add "- Applied <date> in requirements/<domain>.md". No findings for the domain - nothing to do.
7. Update `requirements/README.md` (row of the file, counts) and the domain's Questions column in the "Domains" table of `analysis.md`. Passport history: "Domain <domain> analysed: REQ-NNN - REQ-NNN, questions Q-NNN - Q-NNN" (one question - "question Q-NNN", none - "no new questions").
8. The slice misses a section the domain needs (a reference "see 7.2" in the text, a section named in the domain's "Watch:", or the section of a cross-cutting rule that applies to the domain) - add it to this domain's Read list and to "Sections by domain", rebuild the slice, read the addition. Do not change other domains' lists.

## Never

Fix the source by meaning, edit slices by hand, merge different behaviours into one requirement, analyse another domain whole, change decided questions.

## Self-check

- [ ] The slice was read whole; table rows counted.
- [ ] Seven columns, a source section in every row, IDs unique in the feature.
- [ ] Own findings applied, findings for others recorded.
- [ ] UI domain: "Screen fields" covers every field and action.
- [ ] Call subagent `sdd-check`: scope - the domain file, `requirements/README.md`, `analysis.md`, `decisions`; mode `fix`. Fix the remaining remarks yourself, at most two more rounds.

## Answer

Domain, number of requirements (in / out of scope), ID range, new questions, findings for other domains, uncertainties for the owner.
