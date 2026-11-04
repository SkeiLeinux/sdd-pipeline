---
type: contract
id: CON-001
title: Get available copies of a title per branch
feature: LIB-1
domain: integration-catalog
kind: api
provider: Catalog system
consumers: [Reservation service]
scope: out
mode: external
status: draft
version: 1
requirements: [REQ-011, REQ-012]
updated: 2026-11-03
---

# CON-001 Get available copies of a title per branch

## Purpose

Before making a reservation the reservation service checks that the branch has at least one available copy of the title (REQ-011) and reacts to the catalog being unreachable (REQ-012).

## Expected input

Title ID and branch ID, the same IDs the title page gets from the catalog widget (Q-003).

## Expected result

Number of available copies of the title at the branch. If the operation also returns the title name and author, the "My reservations" list can use them (REQ-015).

## Constraints and questions

The operation, its address, identifiers and format are unknown [?Q-006]. The catalog is used as it is - no changes are requested from the Catalog team.

## Sources

Source 3 and 5.3; decision Q-003. Provider documentation is not available yet.

## Detailed spec

SPEC-03 (not written yet; waits for Q-006).

## History

| Date | Version | Change | Basis |
|---|---|---|---|
| 2026-11-03 | 1 | Card created | REQ-011, REQ-012 |
