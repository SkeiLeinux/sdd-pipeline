---
name: sdd-impact
description: "Analyse the impact of the feature's requirements on an existing system: which components change, where in code or docs, new components, integrations, risks. Optional - use when the feature changes an existing system and the user gave access to its code or documentation."
---

# sdd-impact: impact on the existing system

Parameters: feature folder and where the existing system is described (code paths, documentation folders). A green-field feature - write "Not applicable: <why>" in "Impact" of `analysis.md` and stop.

## Read

1. `analysis.md` - domains and scenarios; `requirements/` - all domain files.
2. Only the parts of the code or documentation that the requirements point to. Search by names of entities, endpoints, tables; do not read whole repositories. If a code-search subagent is available, use it.
3. `decisions/` - existing decisions.

## Do

1. "Impact" table in `analysis.md`: one row - one component or its part: what changes (new endpoint, field, table, rule), path in code or docs, related contracts if already known. Every statement about code - with a path; not found - say "not found".
2. Note what is reused unchanged and what is not touched.
3. New components - working name, purpose, who calls it and whom it calls. Name and technology - questions to the lead, not your decision.
4. "Risks": data migration, dependencies on other teams, order of rollout.
5. Requirements whose real state in the code contradicts the source - questions.

## Never

Decide architecture, change requirements to match the code, invent paths.

## Self-check

- [ ] Every component in the map's nodes has a row or "no changes".
- [ ] Every path exists.
- [ ] Call subagent `sdd-check`: scope - `analysis.md`, mode `fix`.

## Answer

Components and the size of change, new components, risks, questions for the lead.
