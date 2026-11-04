---
name: sdd-contracts
description: "Contract First: build the contract registry contracts/README.md and short cards CON-NNN from the requirements, grouped by edge domains, before the spec plan. Use after all domains are analysed."
---

# sdd-contracts: contract registry

Parameter: feature folder. Some domains of the map have no requirements file - stop and list them.

Why before the plan: interfaces are where components and teams meet. Listing them first makes the plan complete (no forgotten endpoint) and lets owners of both sides agree on purpose and data before anyone designs details.

## Read

1. `analysis.md`: domains (edges), scenarios, impact.
2. `requirements/` - edge files whole; node and UI files - the rows the edges serve, and the "Screen fields" tables.
3. `decisions/`.
4. `templates/feature/contracts.md`, `templates/feature/contract.md`, the example `examples/LIB-1-book-reservations/contracts/`.

## Do

1. A group per edge domain: `### <edge> - <provider> -> <consumer>`. An edge with no interface work - "No changes: <why>".
2. One card per operation or kind of exchange: `contracts/CON-NNN-<slug>.md`. Frontmatter: kind (`contract_kinds`), provider, consumers, scope (`in` when we own the provider), mode (`new`, `change`, `reuse`, `external`), status `draft` (it becomes `review` when the owners of both sides get it to read), requirements - the in-scope requirements the operation serves (edge requirements and the node requirements exposed through it; a rule for every operation of the edge, such as identity and access, goes on each card). Out-of-scope requirements of the other side are named in the card text, not in `requirements`. Kind - what the source or the other side's documentation implies (`api` for a call, `file`, `message`); nothing to go on - `other` with a marker. The registry `owner` - the passport owner unless the user names another.
3. Card body: purpose, expected input, expected result, constraints and questions, sources. An existing or external interface - cite its documentation or code; unknown address or schema - a question, never a guess. A new interface - "designed from REQ-NNN"; method, path and full schemas are left to the spec.
4. Operations of the UI -> API edge - from the "Screen fields" tables: every operation there has a card.
5. "Requirements without contracts" - every in-scope requirement not linked to a card, with a concrete reason (internal rule, exposed through CON-NNN; screen text, data from CON-NNN).
6. Open questions that now block a card - add the CON IDs to their `Blocks`.
7. When the registry is complete: status `review`, passport `status: contracts`, history row.

## Never

Design full request/response schemas here, create specs, invent existing interfaces.

## Self-check

- [ ] Every edge has a group; every card is in the registry and agrees with it (kind, mode, status, requirements).
- [ ] Every in-scope requirement is in a card or in "Requirements without contracts".
- [ ] Call subagent `sdd-check`: scope - the feature folder, mode `gate contracts`. Not passed - fix and repeat, at most two more rounds.

## Answer

Contracts per edge (new / change / reuse / external), requirements without contracts, questions that block contracts. Ask owners of both sides of each interface to read the cards.
