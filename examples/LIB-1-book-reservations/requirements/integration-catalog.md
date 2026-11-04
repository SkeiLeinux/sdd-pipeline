---
type: requirements
feature: LIB-1
domain: integration-catalog
status: draft
updated: 2026-11-02
---

# Requirements: integration-catalog - availability check

Edge of the [domain map](../analysis.md): catalog system -> reservation service.

Boundary. Here: what the reservation service asks the catalog and how it reacts to failures. Not here: the reservation rules themselves (service-reservations).

## Availability

| ID | Requirement | Source | Scenario | Type | Scope | Note |
|---|---|---|---|---|---|---|
| REQ-011 | Before making a reservation, the service shall ask the catalog how many copies of the title are available at the branch and make the reservation only if there is at least one. | 5.3 | Reserve a book | IR | in | catalog interface [?Q-006] |
| REQ-012 | When the catalog cannot be reached, the service shall reject the reservation with a "temporarily unavailable" error. | 5.3 | Reserve a book | IR | in | - |
| REQ-013 | The catalog system provides the number of available copies of a title per branch. | 3, 5.3 | - | IR | out | owned by the Catalog team |
