---
id: SPEC-02
type: data-model
title: Data model of Reservation service
feature: LIB-1
component: Reservation service
mode: new
status: draft
version: 1
requirements: [REQ-001, REQ-004, REQ-006, REQ-009]
contracts: []
depends: []
updated: 2026-11-04
---

# LIB-1 SPEC-02 Data model of Reservation service

## Overview

The reservation service has its own relational database `reservations` (decision Q-004). It stores reservations (REQ-001, REQ-004) and their audit trail (REQ-009). Title name and author are not stored until Q-006 shows whether the catalog returns them [?Q-006].

## Tables

### reservation

One row - one reservation of a title at a branch by a member.

| Name | Type | Comment | Constraint |
|---|---|---|---|
| `id` | uuid | Reservation ID | PK |
| `member_id` | string | Member ID from the portal session | NOT NULL, max 64 |
| `title_id` | string | Title ID from the catalog widget (Q-003) | NOT NULL, max 64 |
| `branch_id` | string | Branch ID from the catalog widget (Q-003) | NOT NULL, max 64 |
| `status` | enum | `active`, `expired`, `cancelled` | NOT NULL |
| `created_at` | date-time | When the reservation was made | NOT NULL |
| `valid_until` | date-time | End of the reservation: `created_at` + 3 days (REQ-004) | NOT NULL |
| `closed_at` | date-time | When it expired or was cancelled; the start of the 30 days of visibility (REQ-006) [?Q-002] | |

### reservation_audit

One row - one change of a reservation (REQ-009).

| Name | Type | Comment | Constraint |
|---|---|---|---|
| `id` | uuid | Record ID | PK |
| `reservation_id` | uuid | Changed reservation | NOT NULL, FK `reservation.id` |
| `action` | enum | `created`, `cancelled`, `expired` | NOT NULL |
| `actor` | string | Member ID, or `system` for expiry | NOT NULL, max 64 |
| `occurred_at` | date-time | When the change happened | NOT NULL |
| `details` | json | Previous and new status | |

## Indexes

| Table | Index | Columns | Unique | Why |
|---|---|---|---|---|
| `reservation` | `reservation_member_status_idx` | `member_id`, `status` | no | limit of 3 active and the duplicate check (SPEC-06), the member's list (SPEC-07) |
| `reservation` | `reservation_status_valid_until_idx` | `status`, `valid_until` | no | the expiry job (SPEC-05) |
| `reservation_audit` | `reservation_audit_reservation_idx` | `reservation_id` | no | audit trail of one reservation |

## Migration

Not applicable: new storage, no data to migrate.

## Acceptance criteria

1. A reservation saved by SPEC-06 has status `active` and `valid_until` exactly 3 days after `created_at` (REQ-001, REQ-004).
2. An expired or cancelled reservation keeps its row and gets `closed_at` (REQ-006).
3. Each created, cancelled or expired reservation has a `reservation_audit` row with actor and time (REQ-009).

## History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1 | 2026-11-04 | Created | source version 3 |
