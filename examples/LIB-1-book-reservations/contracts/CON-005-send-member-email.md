---
type: contract
id: CON-005
title: Send an email to a member
feature: LIB-1
domain: integration-notifications
kind: api
provider: Notification gateway
consumers: [Reservation service]
scope: out
mode: external
status: draft
version: 1
requirements: [REQ-017, REQ-018]
updated: 2026-11-03
---

# CON-005 Send an email to a member

## Purpose

The reservation service asks the gateway to email the member when a reservation is made (REQ-017) and before it expires (REQ-018).

## Expected input

Member, email kind, title, branch, end date.

## Expected result

The gateway accepts the request; delivery is the gateway's job (REQ-019, out of scope).

## Constraints and questions

Timing of the reminder [?Q-001]. The gateway's operation and templates are described in the Messaging team's documentation; it is used as it is.

## Sources

Source 3 and 7.

## Detailed spec

SPEC-04 (not written yet).

## History

| Date | Version | Change | Basis |
|---|---|---|---|
| 2026-11-03 | 1 | Card created | REQ-017, REQ-018 |
