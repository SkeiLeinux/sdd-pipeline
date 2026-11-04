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

1. Every testable statement of the slice whose home is this domain (rules of one home in `analysis.md`) - a requirement. Every row of a logic table in the source - a separate requirement; compare the counts.
2. `requirements/<domain>.md` by the template: "Boundary", subsections by topic, the seven columns. Source - section numbers as in the snapshot, always. Scope - `in` for components we spec, `out` for what other systems must do. Type - from `requirement_types`. Wording close to the source, entity names from the Glossary; interface texts verbatim, in quotes.
3. A requirement whose home is another domain: that domain not analysed yet - a bullet under its name in "Findings for domains"; already analysed - a row in its file. Never the same requirement in two files.
4. UI domain: section "Screen fields" - every field and action of the screens in the slice, the rule behind it (node REQ) and the operation that feeds it (edge REQ or CON). The screen is not a source of data.
5. Gaps, contradictions, vague words ("if needed", "several times"), two names for one thing - a block in `decisions/questions.md` and a marker `[?Q-NNN]` in the Note column. A decision already exists - apply it and cite `(Q-NNN)`. Check the domain as a whole: who acts, what triggers it, the result, edge cases and errors, access rights, audit.
6. Findings of this domain in "Findings for domains" - applied; add "- Applied <date> in requirements/<domain>.md".
7. Update `requirements/README.md` (row of the file, counts). Passport history: "Domain <domain> analysed: REQ-NNN - REQ-NNN, questions Q-NNN - Q-NNN".
8. The slice misses a section the domain needs (a reference "see 7.2" in the text) - add it to this domain's Read list and to "Sections by domain", rebuild the slice, read the addition. Do not change other domains' lists.

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
