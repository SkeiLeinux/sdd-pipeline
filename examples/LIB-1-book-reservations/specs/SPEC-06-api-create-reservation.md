---
id: SPEC-06
type: api-method
title: Add POST /reservations
feature: LIB-1
component: Reservation service
mode: new
status: draft
version: 1
requirements: [REQ-001, REQ-002, REQ-003, REQ-004, REQ-010, REQ-011, REQ-012, REQ-014]
contracts: [CON-002]
depends: [SPEC-02, SPEC-03, SPEC-04]
updated: 2026-11-04
---

# LIB-1 SPEC-06 Add POST /reservations

## Description

Make a reservation of a title at a branch for the logged-in member. The member presses "Reserve" on the title page (source 6.1); the service checks the limits (source 5.1), asks the catalog for availability (source 5.3), saves the reservation for 3 days (source 5.2) and asks the gateway to email the member (source 7).

Paths, field names and error codes of this new interface are design decisions taken in this spec from REQ-001 - REQ-004 and REQ-014; there is no earlier interface to follow.

## Method

Contract: CON-002, version 1.

| Item | Value |
|---|---|
| Purpose | Make a reservation |
| Method | POST |
| Path | `/reservations` |
| Caller | Member portal, "Reserve" button (SPEC-10) |
| Authentication | Session token of the member portal in the `Authorization` header |
| Authorization | Any logged-in member; the reservation is always created for the member of the session (REQ-014, source 4) |

## Request

| Parameter | In | Type | Required | Constraints | Description |
|---|---|---|---|---|---|
| `Authorization` | header | string | yes | `Bearer <token>` | Session token of the member portal |
| `titleId` | body | string | yes | 1-64 characters | Title ID from the catalog widget (Q-003) |
| `branchId` | body | string | yes | 1-64 characters | Branch ID from the catalog widget (Q-003) |

Example: `POST /reservations`

```json
{
  "titleId": "T-000417",
  "branchId": "B-07"
}
```

## Algorithm

1. Take the member ID from the session token. If there is no valid session - stop with error 401.
2. Check `titleId` and `branchId`: both present, at most 64 characters. Otherwise - stop with error 400.
3. Count rows of `reservation` (SPEC-02) with this `member_id` and `status` = `active`. If there are 3 or more - stop with error 409 `LIMIT_REACHED` (REQ-002).
4. Look for a row of `reservation` with this `member_id`, `title_id` and `status` = `active`. If found - stop with error 409 `ALREADY_RESERVED` (REQ-003). Whether the branch is part of this check - [?Q-005].
5. Ask the catalog for available copies of the title at the branch through CON-001 (SPEC-03). If the catalog does not answer within the timeout of SPEC-03 or answers with an error - stop with error 503 `CATALOG_UNAVAILABLE` (REQ-012). If the number of available copies is 0 - stop with error 409 `NOT_AVAILABLE` (REQ-011).
6. Save a row of `reservation`: new `id`, `member_id`, `title_id`, `branch_id`, `status` = `active`, `created_at` = now, `valid_until` = now + 3 days (REQ-001, REQ-004). In the same transaction save a `reservation_audit` row with `action` = `created` and `actor` = member ID.
7. Ask the gateway to send the "reservation made" email through CON-005 (SPEC-04). A failure of this call does not cancel the reservation; it is retried as described in SPEC-04.

Result: the member has an active reservation until `valid_until`, the response carries it.

The whole algorithm completes within 2 seconds for 95% of requests, including step 5 (REQ-010).

## Response

Status: 201.

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `id` | uuid | yes | Reservation ID, `reservation.id` | `"0b6f6d1e-5c1a-4d7e-9a43-2f0d3c9b8a10"` |
| `titleId` | string | yes | `reservation.title_id` | `"T-000417"` |
| `branchId` | string | yes | `reservation.branch_id` | `"B-07"` |
| `status` | string | yes | `reservation.status`, always `active` here | `"active"` |
| `createdAt` | string (date-time) | yes | `reservation.created_at` | `"2026-11-04T10:15:00Z"` |
| `validUntil` | string (date-time) | yes | `reservation.valid_until`; the page shows it in the success message (REQ-021) | `"2026-11-07T10:15:00Z"` |

```json
{
  "id": "0b6f6d1e-5c1a-4d7e-9a43-2f0d3c9b8a10",
  "titleId": "T-000417",
  "branchId": "B-07",
  "status": "active",
  "createdAt": "2026-11-04T10:15:00Z",
  "validUntil": "2026-11-07T10:15:00Z"
}
```

## Response codes

All errors have the body `{"error": {"code", "message"}}`; `code` lets the page choose its message (SPEC-10).

### 400 Invalid request

When: step 2.

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "titleId and branchId are required"
  }
}
```

### 401 Not logged in

When: step 1.

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Session is missing or expired"
  }
}
```

### 409 Limit reached

When: step 3.

```json
{
  "error": {
    "code": "LIMIT_REACHED",
    "message": "The member already has 3 active reservations"
  }
}
```

### 409 Already reserved

When: step 4.

```json
{
  "error": {
    "code": "ALREADY_RESERVED",
    "message": "The member already has an active reservation of this title"
  }
}
```

### 409 Not available

When: step 5, no available copy.

```json
{
  "error": {
    "code": "NOT_AVAILABLE",
    "message": "No available copy of the title at this branch"
  }
}
```

### 503 Catalog unavailable

When: step 5, the catalog does not answer.

```json
{
  "error": {
    "code": "CATALOG_UNAVAILABLE",
    "message": "Reservations are temporarily unavailable"
  }
}
```

## Non-functional requirements

- Performance: 95% of requests within 2 seconds, including the catalog call (REQ-010); the catalog call timeout is set in SPEC-03.
- Idempotency: the method is not idempotent; a repeated request after success is answered with 409 `ALREADY_RESERVED` by step 4, so a retry by the portal cannot create a second reservation of the same title.
- Concurrency: steps 3-6 run in one transaction with a lock on the member's active reservations, so two parallel requests cannot exceed the limit of 3.
- Audit: step 6 writes the audit record (REQ-009). Logs carry the reservation ID and member ID, no other personal data.

## Compatibility

Not applicable: new method.

## Acceptance criteria

1. A member with fewer than 3 active reservations and an available copy gets 201 and an `active` reservation whose `validUntil` is 3 days after `createdAt` (REQ-001, REQ-004).
2. The member ID is taken from the session; a `memberId` in the body is ignored (REQ-014).
3. A member with 3 active reservations gets 409 `LIMIT_REACHED`, nothing is saved (REQ-002).
4. A member with an active reservation of the same title gets 409 `ALREADY_RESERVED` (REQ-003).
5. With 0 available copies the response is 409 `NOT_AVAILABLE`; the catalog is asked before anything is saved (REQ-011).
6. When the catalog does not answer the response is 503 `CATALOG_UNAVAILABLE` (REQ-012).
7. Under the expected load 95% of requests complete within 2 seconds (REQ-010).

## History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1 | 2026-11-04 | Created | source version 3 |
