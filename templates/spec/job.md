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

<!-- One document - one background job: what starts it, what it does step by step, how it fails and recovers. -->

## Purpose

<What the job achieves and for whom.>

## Trigger and schedule

<Schedule (with time zone) or event; manual start; what happens to a run missed during downtime.>

## Algorithm

<!-- Plain numbered steps; the source of every value; error branches inside steps; batching for large volumes;
     last line "Result: ...". -->

1. <...>

Result: <...>.

## Concurrency and restart

<!-- May two runs overlap, and how it is prevented with several instances (lock, single leader). Is a rerun safe
     (idempotent)? What happens to a run interrupted halfway. -->

<...>

## Configuration

| Key | Type | Default | Description |
|---|---|---|---|
| `<key>` | <type> | <value> | <...> |

## Errors and retries

<What happens on failure of each step; retries; partial results; who is told.>

## Observability

<Logs, metrics (processed, failed, duration), alerts an operator needs.>

## Acceptance criteria

1. <...> (REQ-NNN)

## History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1 | YYYY-MM-DD | Created | <source version> |
