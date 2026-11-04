---
id: SPEC-NN
type: integration
title: Integration with <system>
feature: <ID>
component: <our component>
mode: new
status: draft
version: 1
requirements: [REQ-NNN]
contracts: [CON-NNN]
depends: []
updated: YYYY-MM-DD
---

# <ID> SPEC-NN Integration with <system>

<!-- One document - one external system as seen by our component. The other system's interface is described as it is
     (cite its documentation and version); we do not specify changes to systems we do not own - those stay as
     out-of-scope requirements and questions to their owners. -->

## Overview

<Who talks to whom, why, which side starts the exchange.>

## Exchange

| Contract | Operation | Direction | Transport | Trigger |
|---|---|---|---|---|
| CON-NNN | <operation> | <us -> them> | <HTTP, queue, file> | <when> |

<For each operation: address or channel (by environment, or a configuration key), request and response as the provider
documents them, with an example.>

## Data mapping

| Their field | Our field | Rule |
|---|---|---|
| `<field>` | `<field>` | <conversion, default, what if empty> |

## Errors and retries

<!-- Per operation: timeouts, which errors are retried and how (count, interval, backoff), what happens when the
     other side is down for long, duplicates and idempotency, what the user or the caller sees. -->

<...>

## Security and access

<Authentication, network access, who issues credentials and where they are stored.>

## Operations

<!-- Expected volume and frequency, limits of the other side, monitoring and alerts, test environment or stub. -->

<...>

## Acceptance criteria

1. <...> (REQ-NNN)

## History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1 | YYYY-MM-DD | Created | <source version> |
