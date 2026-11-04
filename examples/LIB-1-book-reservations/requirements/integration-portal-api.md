---
type: requirements
feature: LIB-1
domain: integration-portal-api
status: draft
updated: 2026-11-03
---

# Requirements: integration-portal-api - portal to reservation service

Edge of the [domain map](../analysis.md): member portal -> reservation service.

Boundary. Here: operations the portal pages call and the data they need. Not here: the rules behind the operations (service-reservations), how the data is shown (ui-reservations).

## Operations

| ID | Requirement | Source | Scenario | Type | Scope | Note |
|---|---|---|---|---|---|---|
| REQ-014 | The portal shall ask the service to make a reservation, passing the title and the branch; the member is identified by the portal session, not by request data. | 6.1, 4 | Reserve a book | IR | in | - |
| REQ-015 | The portal shall get the member's reservations from the service with every column of the "My reservations" table. | 6.2 | - | IR | in | title and author come only from the catalog [?Q-006] |
| REQ-016 | The portal shall ask the service to cancel one reservation of the member. | 6.2 | - | IR | in | - |
