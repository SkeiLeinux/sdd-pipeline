---
type: feature
id: <ID>
title: <Short feature title>
status: intake
source: <Where the input came from: document name, link, version>
owner: <Analyst>
updated: YYYY-MM-DD
---

# <ID> <Short feature title>

<!-- Feature passport: features/<ID>/README.md. Filled stage by stage: summary at intake, plan after contracts.
     Statuses: intake -> analysis -> contracts -> plan -> spec -> ready; also hold, cancelled. -->

## Summary

| Item | Value |
|---|---|
| Input | [source/source.md](source/source.md), <version of the input> |
| Business goal | <1-2 sentences from the input> |
| Scope | <what is in, what is explicitly out> |
| Components | <components we write specs for; a new one - working name> |

## Constraints and assumptions

<!-- Constraints - from the input, with a section reference. Assumptions - team decisions taken without an answer: who, when, which question. -->

Constraints:

1. <constraint> (source 2.3)

Assumptions:

1. <assumption> - taken by <who>, <date>, question Q-NNN.

## Documents

| Document | Link |
|---|---|
| Domain map and impact | [analysis.md](analysis.md) |
| Requirements | [requirements/README.md](requirements/README.md) |
| Questions and decisions | [decisions/questions.md](decisions/questions.md), [decisions/decisions.md](decisions/decisions.md), [decisions/manual.md](decisions/manual.md) |
| Contracts | [contracts/README.md](contracts/README.md) |
| Traceability | [traceability.md](traceability.md) |

## Spec plan

<!-- Filled by sdd-plan after the contract registry. One row - one spec unit. Tables grouped by domains of the map:
     "### <domain> - <summary>"; scenario units - group "### Scenarios".
     Numbering follows unit_types order in sdd.config.json. Contracts - CON IDs or "-". -->

### <domain> - <summary>

| Spec | Type | Title | Component | Requirements | Contracts | Status |
|---|---|---|---|---|---|---|
| [SPEC-01](specs/SPEC-01-<slug>.md) | component | <title> | <component> | REQ-001 | - | draft |

## History

| Date | Event |
|---|---|
| YYYY-MM-DD | Input accepted, version <N> |
