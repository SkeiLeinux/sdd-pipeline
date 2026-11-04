# Rules for the agent

This repository turns a structured requirements document (business requirements, functional specification, PRD) into a traceable set of small specifications. Process for people - `docs/pipeline.md`; why it is built this way - `docs/concepts.md`.

## Map

- `features/<ID>/` - one feature = one input document. `README.md` (passport and spec plan), `source/` (immutable snapshot, index, per-domain slices; raw input in `source/import/`), `analysis.md` (domain map and impact), `requirements/` (one file per domain), `decisions/` (`questions.md` open, `decisions.md` decided, `manual.md` human interventions), `contracts/` (registry and cards), `specs/` (spec units), `traceability.md` (generated).
- `examples/LIB-1-book-reservations/` - a complete example. When unsure about the form of an artifact, copy the form from here.
- `templates/` - templates of every artifact. Write by the template, do not invent structure.
- `sdd.config.json` - project settings: language of artifact prose, scope labels, requirement types, unit types, optional house rules.
- `.agents/skills/` - pipeline skills `sdd-*`; `.agents/subagents/` - instructions of the subagents.
- `tools/` - `new_feature.py`, `snapshot.py`, `slices.py`, `check.py`. Run by subagents.

## How to work

1. The user named a skill `sdd-*` - load it and follow it exactly. No skill named - clarify the task and suggest the fitting skill from the table below.
2. Read only what the step needs. The whole snapshot `source/source.md` - only for the domain map; for a domain - its slice `source/domains/<domain>.md`. Never edit the snapshot or the slices by hand.
3. One run - one coherent portion: one domain, one registry pass, one spec unit. Update the index files you touched.
4. Write artifact prose in `artifact_language` from `sdd.config.json`. Headings, frontmatter keys, statuses, field labels (`- Status:`), table headers and IDs stay exactly as in the templates - the checker reads them.
5. Scripts run inside subagents, because their output is long: checks - subagent `sdd-check`; new feature, snapshot and slices - subagent `sdd-source`. Pass parameters, get a short report, fix the meaningful remarks yourself. `python tools/check.py <feature> --next` (one line) is allowed directly.
6. Your tool cannot call subagents - read `.agents/subagents/<name>.md` and do its work yourself, including running its scripts; keep only its short report in your answer.
7. Answer briefly: what was done, which files, what a person should check.

## Hard rules

1. **Do not invent.** Sources are the snapshot, decisions in `decisions/decisions.md`, documentation and code the user pointed to. Unknown fact or rule - a question `Q-NNN` in `decisions/questions.md` and a marker `[?Q-NNN]` at the place. A new interface may be designed from requirements, stating that it is a design decision. Confidence is not a source.
2. **The source is immutable.** A gap or contradiction in the input is a question, never a silent fix. Never pick one side of a contradiction: put the marker on the contested value itself ("within 3 working days [?Q-025]"). `sdd-map` records contradictions under "Watch:"; `sdd-domain` turns them into questions.
3. **Only what is in scope.** Specs are written for components with scope `in`. Requirements to systems owned by others keep scope `out` and get no specs.
4. **One unit - one file.** One API method, one message we own, one data model per component, one integration per external system, one background job, one screen.
5. **Algorithms are numbered steps**, not tables. Each step names where its values come from. The last line - "Result: ...".
6. **Interface texts are verbatim** from the source.
7. **One home per requirement** - the domain chosen by the rules in `analysis.md`. A requirement for another domain goes to "Findings for domains" or straight into that domain's file if it is already analysed.
8. **Contracts before the plan.** After requirements: registry `contracts/README.md` and short cards CON-NNN. Full schemas are designed in specs.
9. **Approved artifacts** (`approved`) change only on the owner's explicit request: new `version`, status back to `review`, a row in "History". Exception - the working sections of an approved `analysis.md` that later steps maintain: the Questions column of "Domains", Read lists extended by `sdd-domain`, "Findings for domains", "Impact", "Plan coverage" of scenarios.
10. **IDs are Latin only:** `REQ-012`, `Q-007`, `M-001`, `CON-003`, `SPEC-05`. File names - Latin, kebab-case.
11. **Personal data** - synthetic only, in examples too.
12. **Record human interventions.** When a person approves, edits or rejects your draft (map, registry, plan, spec) - add a block `M-NNN` to `decisions/manual.md`. On approval also set the artifact's `status: approved` and add a passport history row "<artifact> approved (M-NNN)"; on edits apply them first. A conditional approval ("as a draft for planning") - keep `review`, record the condition in the M block.

## Skills

| Skill | What it does |
|---|---|
| `sdd-intake` | snapshot of the input, passport, empty `decisions/` |
| `sdd-map` | domain map of the whole input, slices |
| `sdd-domain` | requirements and questions of one domain |
| `sdd-impact` | impact on an existing system (optional) |
| `sdd-contracts` | contract registry and cards |
| `sdd-plan` | spec plan in the passport |
| `sdd-spec` | one spec unit |
| `sdd-review` | review of one spec unit, no edits |
| `sdd-decide` | apply answered questions to the artifacts |
| `sdd-update` | impact of a new version of the input |

## Subagents

| Subagent | Pass | When |
|---|---|---|
| `sdd-check` | scope (feature folder or files) and mode: `fix`, `report`, `trace`, `gate contracts`, `gate ready`, `regression` | self-check at the end of a skill; on request |
| `sdd-source` | mode: `new` (ID, slug, title, owner, origin, input), `snapshot` or `update` (feature and input path), `slices` (feature, optionally one domain) | intake, new input version, after the map changes |
