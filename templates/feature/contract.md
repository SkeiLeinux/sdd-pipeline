---
type: contract
id: CON-001
title: <Operation name>
feature: <ID>
domain: <edge domain>
kind: api
provider: <component>
consumers: [<component>]
scope: in
mode: new
status: draft
version: 1
requirements: [REQ-NNN]
updated: YYYY-MM-DD
---

# CON-001 <Operation name>

<!-- One card - one operation or kind of exchange. kind: api, message, file, other. mode: new, change (our interface),
     reuse (existing interface used as is), external (owned by another system). scope: in when we own the provider.
     Do not invent the address or schema of an existing or external interface - cite its source or ask. -->

## Purpose

<Which behaviour needs this operation.>

## Expected input

<Data, identifiers and context the operation needs - or "no input".>

## Expected result

<What the consumer gets. Full schemas are not required before the spec.>

## Constraints and questions

<Rules, dependencies, [?Q-NNN] markers.>

## Sources

<Source sections, decisions, code paths or the provider's documentation. For a new interface - "designed from REQ-NNN".>

## Detailed spec

<Link to the spec that describes the full contract, or "Not written yet".>

## History

| Date | Version | Change | Basis |
|---|---|---|---|
| YYYY-MM-DD | 1 | Card created | <REQ / decision> |
