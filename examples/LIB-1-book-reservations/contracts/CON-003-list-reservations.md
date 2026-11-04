---
type: contract
id: CON-003
title: List the member's reservations
feature: LIB-1
domain: integration-portal-api
kind: api
provider: Reservation service
consumers: [Member portal]
scope: in
mode: new
status: review
version: 1
requirements: [REQ-006, REQ-008, REQ-015]
updated: 2026-11-03
---

# CON-003 List the member's reservations

## Purpose

The "My reservations" page shows the member's own reservations (REQ-015, REQ-008).

## Expected input

No parameters; the member comes from the portal session.

## Expected result

All reservations of the member that are still visible (REQ-006): title, author, branch, date made, end date, status. Sorted newest first, or sorted by the page - to be fixed in the spec.

## Constraints and questions

Which expired and cancelled reservations are still returned [?Q-002]. Source of title and author [?Q-006].

## Sources

Designed from REQ-006, REQ-008, REQ-015.

## Detailed spec

SPEC-07 (not written yet).

## History

| Date | Version | Change | Basis |
|---|---|---|---|
| 2026-11-03 | 1 | Card created | requirements of integration-portal-api |
