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
     (cite its documentation); we do not specify changes to systems we do not own. -->

## Overview

<Who talks to whom, why, how often.>

## Exchange

| Contract | Operation | Direction | Transport | Trigger |
|---|---|---|---|---|
| CON-NNN | <operation> | <us -> them> | <HTTP, queue, file> | <when> |

## Data mapping

| Their field | Our field | Rule |
|---|---|---|
| `<field>` | `<field>` | <conversion, default> |

## Errors and retries

<Timeouts, retry policy, what happens when the other side is down, alerts.>

## Security and access

<Authentication, network access, who issues credentials.>

## Acceptance criteria

1. <...> (REQ-NNN)

## History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1 | YYYY-MM-DD | Created | <source version> |
