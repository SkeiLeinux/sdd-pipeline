# Pipeline: stages, gates, changes

[Русская версия](pipeline.ru.md)

A **feature** is all the work on one input document, in the folder `features/<ID>-<slug>/`. Its status is the `status` field of the passport (`README.md`): `intake -> analysis -> contracts -> plan -> spec -> ready`, plus `hold` and `cancelled`. The checker becomes stricter as the status advances: a rule of a later stage is a warning before it and an error after.

## Stages

| Stage | Skill | Output | Gate |
|---|---|---|---|
| 0. Intake | `sdd-intake` | `source/` snapshot, passport | a person compares numbering with the original |
| 1. Domain map | `sdd-map` | `analysis.md`, slices | the owner approves the map (`M-NNN`) |
| 2. Requirements | `sdd-domain`, one run per domain | `requirements/<domain>.md`, questions | every domain analysed, every section assigned |
| 3. Impact (optional) | `sdd-impact` | "Impact" in `analysis.md` | a lead read it |
| 4. Contracts | `sdd-contracts` | `contracts/README.md`, `CON-NNN` | `check.py --gate contracts` |
| 5. Plan | `sdd-plan` | "Spec plan" in the passport | every in-scope requirement and new contract covered |
| 6. Specs | `sdd-spec`, one run per unit | `specs/SPEC-NN-*.md` | `check.py` without errors |
| 7. Review and approval | `sdd-review`, then people | specs `approved` | `check.py --gate ready` |

### 0. Intake

Convert the document to Markdown with any tool (for Word: `pandoc input.docx -t gfm --extract-media=. -o input.md`), then run `sdd-intake`. It creates the feature folder with `tools/new_feature.py` and makes the snapshot; without an agent:

```bash
python tools/new_feature.py PAY-42 refunds --title "Refunds" --owner "Analyst" --source "BRD v3" --input brd.md
```

```bash
python tools/snapshot.py features/PAY-42-refunds/source/import/brd.md features/PAY-42-refunds/source
```

Several documents for one feature (requirements plus an addendum) - join them into one Markdown file, each under its own top-level heading: one feature - one numbered source. Images and relative links keep working: the snapshot and the slices rewrite their paths. The script keeps the text and normalizes headings to numbered sections (`--number` numbers them if the document has no numbering). A person checks that the numbering matches the original and that tables and images survived the conversion.

### 1. Domain map

`sdd-map` reads the whole snapshot once and proposes nodes, edges, scenarios, cross-cutting rules, a Read list per domain and an index assigning every section to domains. The script builds slices from the Read lists. The owner approves or edits the map; the agent records it as `M-NNN`.

A good map: each domain fits one agent run; out-of-scope systems appear only at the ends of edges; no section is left unassigned.

### 2. Requirements per domain

`sdd-domain` takes one domain per run and reads only its slice. Every testable statement becomes a requirement with a source section, a type and a scope (`in` - we write specs for it; `out` - it is another system's job). Gaps become questions. A requirement for another domain goes to "Findings for domains" and is picked up when that domain is analysed. UI domains also get a "Screen fields" table: every field and action, the rule behind it and the operation feeding it.

Order: back-end nodes and edges first, UI domains last.

### 3. Impact

When the feature changes an existing system, `sdd-impact` records which components change, where in the code or docs, what is reused and what is risky. For green-field work - "Not applicable".

### 4. Contracts

`sdd-contracts` lists every interface per edge: new and changed ones we own, existing and external ones we only use. Each requirement in scope is linked to a contract or has a reason not to be. The registry goes to `review`, and `--gate contracts` must pass before planning. Owners of both sides of each interface read the cards.

### 5. Plan

`sdd-plan` distributes requirements and contracts into spec units by the slicing rules (one method - one unit, one data model per component, and so on) and fills the plan table in the passport, grouped by domains.

### 6. Specs

`sdd-spec` writes one unit per run, in the suggested order: component and data model -> integrations and jobs -> API methods -> scenarios and screens -> configuration. The full contract of an interface is designed here, with sources for every value. Units can go to review one by one; there is no need to wait for the whole set.

### 7. Review and approval

`sdd-review` in a fresh session produces remarks and a verdict. Approval itself belongs to people - typically approvals on a pull request by the component's developers, the consumers of its interfaces and QA. After the merge the owner sets `approved`. `--gate ready` checks that every planned spec and used contract is approved, no blocking question is open and no marker remains.

## Changes along the way

### Answers arrive

`sdd-decide` applies them: the decision is moved to `decisions/decisions.md` under the same ID, markers are removed, requirements, cards and specs are updated. An approved artifact is not edited - its owner decides on a new version.

### A new version of the input

Put it into `source/import/` and run `sdd-update`. The snapshot is replaced, `source/changes.md` lists changed, added, removed, renamed and moved sections, the slices are rebuilt. The skill traces changes to domains, requirements, contracts and specs and updates the drafts. Requirements are never deleted: they are excluded or superseded in `requirements/dispositions.md` with a reason.

### Someone finds a problem in a spec

Stop the affected work - never "just do it right". Register a question, fix the contract first if the interface changes, then the spec: `version + 1`, status `review`, a row in "History", approval again.

## Publishing specs for readers outside git

Approval often happens where the business reads documents. Specs are plain Markdown, so any converter works, for example:

```bash
pandoc features/PAY-42-refunds/specs/SPEC-06-api-create-refund.md -o SPEC-06.docx
```

The Markdown in git stays the source of truth: comments from a wiki or a Word file are brought back as changes to the spec, never the other way round.

## After the specs

The pipeline ends at approved specs. Tasks, code, tests and rollout follow your process. Useful conventions: reference `<feature ID>/SPEC-NN` and `REQ-NNN` in task titles, merge requests and test names, so the chain back to the source stays unbroken. The pipeline can be extended with your own stages - see [customization.md](customization.md).

## Gate summary

| Gate | When | How |
|---|---|---|
| Input accepted | end of stage 0 | human check of the snapshot |
| Map approved | end of stage 1 | owner, `M-NNN` in `decisions/manual.md` |
| Analysis complete | before contracts | `check.py` at status `contracts`: every domain has requirements, every section assigned, findings applied |
| Contracts described | before the plan | `check.py --gate contracts` |
| Plan complete | before specs | `check.py` at status `spec`: coverage of requirements and contracts |
| Ready | after approvals | `check.py --gate ready` |
