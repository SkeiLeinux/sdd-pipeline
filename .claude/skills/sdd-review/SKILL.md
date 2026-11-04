---
name: sdd-review
description: "Review one spec unit against its requirements, contract, source and template without editing it: table of remarks and a verdict whether it can go to approval. Use when the user asks to review or check SPEC-NN. Best run in a fresh session, not the one that wrote the spec."
---

# sdd-review: review of one spec unit

Parameters: feature folder and `SPEC-NN`.

You are a strict reviewer: find defects, do not praise. Do not edit the spec.

## Read

The spec; its template; the rows of its requirements; their source sections in the domain slices; the contract cards from its header; `decisions/`; specs from `depends`; for `ui` - the "Screen fields" table of its domain; for `scenario` - its path in `analysis.md`.

## Check

Form:

0. Call subagent `sdd-check`: scope - the spec, mode `report`. Every line about this file is a remark: E - important, W - minor. Check by eye only what the script cannot see.
1. Every template section present; header complete.
2. Algorithm in numbered steps ending with "Result"; examples complete and consistent with the tables.

Content:

3. Every header requirement is implemented in the text; every behaviour in the text rests on a requirement, a decision or a source. Extra behaviour - a remark.
4. All rows of source logic tables related to this unit are reflected.
5. Interface texts match the source.
6. Every check in the algorithm has its error branch; every code used has its subsection with condition and full body; the success code is stated; shared codes that can happen (401, 403, 404, 409, 422, 429, 500, 503) are not forgotten; every error has an acceptance criterion. For `ui` - the user-visible reaction to each error.
7. Non-functional needs considered: performance, idempotency and retries, concurrency, pagination and limits, audit and personal data, compatibility for `mode: change`. "Not applicable" must have a real reason.
8. `data-model`: primary keys, foreign keys, enum values with labels, indexes for the queries the other units make, retention. `message`: delivery guarantee, duplicates, ordering, versioning.
9. Names and types agree with the data model and related units.
10. Acceptance criteria are testable: a condition and an observable result.
11. `[?Q-NNN]` only for open questions; decided ones applied.
12. The contract part agrees with the card (purpose, expected data, version); the card links back to the spec.
13. `ui`: every field and action of "Screen fields" is described with the same rule and operation. `scenario`: steps follow the path of the scenario.

## Answer

Table `# | Where (section, step) | Remark | Severity (blocker, important, minor) | Suggestion`, then the verdict: ready for approval or not. No remarks - say what you checked, items 0-13. Mechanical remarks can be fixed by `sdd-check` in mode `fix` - say so in one line.
