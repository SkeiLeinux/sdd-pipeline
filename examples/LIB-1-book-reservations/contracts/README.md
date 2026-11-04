---
type: contracts
feature: LIB-1
status: review
version: 1
owner: Example analyst
updated: 2026-11-03
---

# Contract registry LIB-1

Interfaces of the feature, grouped by edge domains of the [domain map](../analysis.md). Full schemas are in the specs.

## Registry

### integration-catalog - Catalog system -> Reservation service

| Contract | Kind | Provider | Consumers | Mode | Operation | Requirements | Status |
|---|---|---|---|---|---|---|---|
| [CON-001](CON-001-catalog-availability.md) | api | Catalog system | Reservation service | external | Get available copies of a title per branch | REQ-011, REQ-012 | draft |

### integration-portal-api - Reservation service -> Member portal

| Contract | Kind | Provider | Consumers | Mode | Operation | Requirements | Status |
|---|---|---|---|---|---|---|---|
| [CON-002](CON-002-create-reservation.md) | api | Reservation service | Member portal | new | Make a reservation | REQ-001, REQ-002, REQ-003, REQ-004, REQ-010, REQ-014 | review |
| [CON-003](CON-003-list-reservations.md) | api | Reservation service | Member portal | new | List the member's reservations | REQ-006, REQ-008, REQ-015 | review |
| [CON-004](CON-004-cancel-reservation.md) | api | Reservation service | Member portal | new | Cancel a reservation | REQ-007, REQ-016 | review |

### integration-notifications - Notification gateway -> Reservation service

| Contract | Kind | Provider | Consumers | Mode | Operation | Requirements | Status |
|---|---|---|---|---|---|---|---|
| [CON-005](CON-005-send-member-email.md) | api | Notification gateway | Reservation service | external | Send an email to a member | REQ-017, REQ-018 | draft |

## Requirements without contracts

| Requirement | Why no contract |
|---|---|
| REQ-005 | internal rule of the reservation service (background job); the result is visible through CON-003 |
| REQ-009 | internal audit log of the reservation service; no consumer in this feature |
| REQ-020 | the branch list and its IDs come from the existing catalog widget (Q-003); the button calls CON-002 |
| REQ-021 | screen text; data from CON-002 |
| REQ-022 | screen text; error from CON-002 |
| REQ-023 | screen text; error from CON-002 |
| REQ-024 | screen layout; data from CON-003 |
| REQ-025 | screen action; calls CON-004 |
| REQ-026 | screen text; empty list from CON-003 |

## History

| Date | Version | Contracts | Change | Basis |
|---|---|---|---|---|
| 2026-11-03 | 1 | CON-001 - CON-005 | First batch, all edges | requirements of the edges |
