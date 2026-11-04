---
type: contracts
feature: <ID>
status: draft
version: 1
owner: <Analyst>
updated: YYYY-MM-DD
---

# Contract registry <ID>

<!-- Short list of interfaces before the spec plan, grouped by edge domains of the map: one edge - one group.
     Cards are separate files (templates/feature/contract.md). Full request/response schemas belong in specs.
     Statuses: draft -> review (ready to plan, --gate contracts) -> approved. -->

## Registry

<!-- A group per edge: "### <edge> - <provider> -> <consumer>". An edge with no interface work - a line
     "No changes: <why>" instead of a table. Operations of the UI -> API edge come from the "Screen fields" tables. -->

### integration-<exchange> - <provider> -> <consumer>

| Contract | Kind | Provider | Consumers | Mode | Operation | Requirements | Status |
|---|---|---|---|---|---|---|---|
| [CON-001](CON-001-<slug>.md) | api | <component> | <components> | new | <operation, or a confirmed METHOD /path> | REQ-NNN | draft |

## Requirements without contracts

<!-- In-scope requirements that need no interface, and why (internal rule of a node, exposed through CON-NNN...).
     This does not drop them from the plan. -->

| Requirement | Why no contract |
|---|---|
| REQ-NNN | <reason> |

## History

| Date | Version | Contracts | Change | Basis |
|---|---|---|---|---|
| YYYY-MM-DD | 1 | CON-001 | First batch | <REQ / decision> |
