---
type: contract
id: CON-004
title: Cancel a reservation
feature: LIB-1
domain: integration-portal-api
kind: api
provider: Reservation service
consumers: [Member portal]
scope: in
mode: new
status: review
version: 1
requirements: [REQ-007, REQ-016]
updated: 2026-11-03
---

# CON-004 Cancel a reservation

## Purpose

The "Cancel" action on the "My reservations" page cancels one active reservation of the member (REQ-016, REQ-007).

## Expected input

Reservation ID; the member comes from the portal session.

## Expected result

The reservation with status "Cancelled", or an error when it is not the member's, not found or not active.

## Constraints and questions

A member changes only their own reservations (source 4).

## Sources

Designed from REQ-007, REQ-016.

## Detailed spec

SPEC-08 (not written yet).

## History

| Date | Version | Change | Basis |
|---|---|---|---|
| 2026-11-03 | 1 | Card created | requirements of integration-portal-api |
