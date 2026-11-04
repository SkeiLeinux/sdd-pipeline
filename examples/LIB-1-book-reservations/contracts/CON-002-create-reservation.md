---
type: contract
id: CON-002
title: Make a reservation
feature: LIB-1
domain: integration-portal-api
kind: api
provider: Reservation service
consumers: [Member portal]
scope: in
mode: new
status: review
version: 1
requirements: [REQ-001, REQ-002, REQ-003, REQ-004, REQ-010, REQ-014]
updated: 2026-11-03
---

# CON-002 Make a reservation

## Purpose

The "Reserve" button on the title page makes a reservation of a title at a branch for the logged-in member (REQ-014, REQ-001).

## Expected input

Title ID and branch ID from the catalog widget (Q-003). The member is identified by the portal session (REQ-014), never by a field of the request.

## Expected result

The created reservation with its end date for the success message (REQ-004, REQ-021). Distinct errors the page can tell apart: limit reached (REQ-002), title already reserved (REQ-003), no available copy (REQ-011), catalog unreachable (REQ-012).

## Constraints and questions

Responds within 2 seconds for 95% of requests, including the catalog call (REQ-010). Same title at another branch [?Q-005].

## Sources

Designed from REQ-001 - REQ-004, REQ-010, REQ-014; new interface of the reservation service.

## Detailed spec

[SPEC-06](../specs/SPEC-06-api-create-reservation.md).

## History

| Date | Version | Change | Basis |
|---|---|---|---|
| 2026-11-03 | 1 | Card created | requirements of integration-portal-api |
