---
type: requirements
feature: LIB-1
domain: service-reservations
status: draft
updated: 2026-11-02
---

# Requirements: service-reservations - reservation rules and data

Node of the [domain map](../analysis.md): the new reservation service.

Boundary. Here: limits, lifetime, cancellation, retention, audit, performance. Not here: how availability is asked (integration-catalog), what the pages show (ui-reservations).

## Making a reservation

| ID | Requirement | Source | Scenario | Type | Scope | Note |
|---|---|---|---|---|---|---|
| REQ-001 | The service shall create a reservation of a title at one branch for the logged-in member, with status "Active". | 5.1, 4 | Reserve a book | FR | in | - |
| REQ-002 | The service shall reject a new reservation when the member already has 3 active reservations. | 5.1 | Reserve a book | BR | in | - |
| REQ-003 | The service shall reject a new reservation of a title for which the member has an active reservation. | 5.1 | Reserve a book | BR | in | same title at another branch [?Q-005] |
| REQ-004 | The service shall set the end of a reservation to 3 days after the moment it was made. | 5.2 | Reserve a book | BR | in | - |

## Lifetime

| ID | Requirement | Source | Scenario | Type | Scope | Note |
|---|---|---|---|---|---|---|
| REQ-005 | The service shall change an active reservation to "Expired" automatically when its end has passed. | 5.2 | Reservation expires | FR | in | - |
| REQ-006 | The service shall keep expired reservations visible to the member for 30 days. | 5.2 | - | BR | in | counted from what, and does it apply to cancelled [?Q-002] |
| REQ-007 | The service shall let the member cancel their own active reservation; its status becomes "Cancelled". | 5.2, 4 | - | FR | in | - |
| REQ-008 | The service shall return the member's own reservations with title, author, branch, date made, end date and status. | 6.2, 4 | - | FR | in | - |

## Audit and performance

| ID | Requirement | Source | Scenario | Type | Scope | Note |
|---|---|---|---|---|---|---|
| REQ-009 | The service shall log every change of a reservation for audit: who, when and what changed. | 8 | - | NFR | in | system changes (expiry) - actor "system" |
| REQ-010 | The service shall make a reservation within 2 seconds for 95% of requests. | 8 | Reserve a book | NFR | in | includes the catalog call |
