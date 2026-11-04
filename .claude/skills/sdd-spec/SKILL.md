---
name: sdd-spec
description: "Write one spec unit SPEC-NN by its template: API method, data model, integration, background job, screen, scenario, configuration or component. Use when the user asks to write or rewrite a planned spec."
---

# sdd-spec: one spec unit

Parameters: feature folder and `SPEC-NN`. Not in the plan - stop and suggest `sdd-plan`.

## Read (only this)

1. The passport - the plan row of `SPEC-NN`: type, title, component, requirements, contracts.
2. The rows of those requirements in `requirements/`. For `ui` - the "Screen fields" table of its UI domain; for `scenario` - its row in "Scenarios" of `analysis.md`.
3. The source sections cited by those requirements - in the slice of the requirement's domain `source/domains/<domain>.md`; only those sections.
4. `decisions/` - decisions and open questions about these requirements and contracts.
5. The contract cards from the plan row.
6. `templates/spec/<type>.md`; the example of the same type in `examples/LIB-1-book-reservations/specs/` if there is one.
7. Specs from `depends` and written specs of the same component - only headers and the tables you must agree with (names and types of fields).
8. For `mode: change` - the current description of what changes (code or docs the user pointed to).

## Do

1. Create `specs/SPEC-NN-<slug>.md` exactly as named in the plan. Frontmatter: values from the plan row, `mode`, `status: draft`, `version: 1`, `depends`, `updated` - today.
2. Fill every section of the template. Not applicable - "Not applicable: <why>".
3. Design the full contract here: method and path, parameters, schemas, errors, access, with sources; respect the purpose and data of the card and give its version. A new interface - explicit design decisions from requirements; an existing one - only from its documentation or code.
4. `api-method`: complete working examples - path with sample values, full request body for methods with a body, full response, the full body of every error code. No "..." except for long values. `api_response_required_keys` in `sdd.config.json` - every response example contains them.
5. `data-model`: columns and logical types from `sdd.config.json`; constraints in the Constraint column; indexes - separate table.
6. Algorithms - numbered steps; every value with its source (table and column, contract, configuration key); error branches inside steps; last line "Result: ...".
7. Acceptance criteria - at least one testable statement per header requirement, ending with `(REQ-NNN)`.
8. Unknowns - `[?Q-NNN]` and a question block; never an invented value. Add a link to this spec in the card's "Detailed spec".
9. Status of the plan row, if it changed.

## Self-check

- [ ] Every header requirement is in the text and in acceptance criteria.
- [ ] No field, code, status or path without a source or an explicit design decision.
- [ ] Names and types agree with the data model and related specs; interface texts match the source character for character.
- [ ] No template placeholders left except under `[?Q-NNN]`.
- [ ] Call subagent `sdd-check`: scope - the spec and `decisions`, mode `fix`. Fix what is left, at most two more rounds. `link-spec` for other planned but unwritten units is normal.

## Answer

Path, covered requirements, new questions, applied decisions, and 3-5 places a person should check first.
