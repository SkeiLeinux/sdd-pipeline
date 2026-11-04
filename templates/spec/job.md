---
id: SPEC-NN
type: job
title: Background job <name>
feature: <ID>
component: <component>
mode: new
status: draft
version: 1
requirements: [REQ-NNN]
contracts: []
depends: []
updated: YYYY-MM-DD
---

# <ID> SPEC-NN Background job <name>

<!-- One document - one background job: what starts it, what it does step by step, how it fails. -->

## Purpose

<What the job achieves and for whom.>

## Trigger and schedule

<Schedule or event, overlap rule (may two runs overlap?), manual start.>

## Algorithm

<!-- Plain numbered steps; the source of every value; error branches inside steps; last line "Result: ...". -->

1. <...>

Result: <...>.

## Configuration

| Key | Type | Default | Description |
|---|---|---|---|
| `<key>` | <type> | <value> | <...> |

## Errors and retries

<What happens on failure of each step; retries; partial results.>

## Observability

<Logs, metrics, alerts an operator needs.>

## Acceptance criteria

1. <...> (REQ-NNN)

## History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1 | YYYY-MM-DD | Created | <source version> |
