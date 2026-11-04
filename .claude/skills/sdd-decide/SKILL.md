---
name: sdd-decide
description: "Apply answers to open questions: update the requirements, contracts and specs that depend on them, remove [?Q-NNN] markers and move the question blocks to decisions/decisions.md. Use when the user brings answers to questions Q-NNN."
---

# sdd-decide: apply answers

Parameters: feature folder, the questions and their answers (from the user, or blocks with `Status: answered` in `decisions/questions.md`).

## Read

1. The question blocks; fields "Where" and "Blocks".
2. Every place that cites the question: search the feature for `Q-NNN` (requirements, analysis, contracts, specs).
3. `templates/feature/decisions.md`.

## Do

1. For each answer: decide its kind - `business` (answer of the business, interpretation of the source), `technical` (how we build it), `external` (fact or agreement about a system owned by others). Unsure - ask.
2. Apply the answer where the question was cited: change the requirement wording, the card, the spec text; remove the marker `[?Q-NNN]`, cite `(Q-NNN)` where it helps the reader. New requirements from the answer - next free IDs, source - the section the question was about.
3. An approved artifact is affected - do not edit it; list it in the answer: the owner decides on a new version.
4. Move the block to `decisions/decisions.md` under the same ID (ascending order): Status `active`, Kind, Question, Decision, Why, Decided (who, date, where), Affects. Delete it from `questions.md`.
5. An answer contradicts an earlier decision - a new question, not an edit of the decision. Revising a decision - a new block; the old one gets `Status: superseded by Q-NNN`.
6. The answer is partial - keep the question open with what is known in "Answer", apply only what is certain.

## Self-check

- [ ] No `[?Q-NNN]` left for moved questions.
- [ ] Call subagent `sdd-check`: scope - the feature folder, mode `fix`.

## Answer

Questions moved, artifacts changed, new requirements, approved artifacts that need a new version, questions still open.
