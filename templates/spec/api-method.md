---
id: SPEC-NN
type: api-method
title: <Add|Change> <METHOD> <path>
feature: <ID>
component: <component that provides the method>
mode: new
status: draft
version: 1
requirements: [REQ-NNN]
contracts: [CON-NNN]
depends: []
updated: YYYY-MM-DD
---

# <ID> SPEC-NN <Add|Change> <METHOD> <path>

<!-- One document - one API method. Purpose and expected data come from the contract card; here the full contract
     is designed: method, path, request, response, errors, access. Every field, code and path has a source
     (requirement, decision, source document, code, provider docs) or is an explicit design decision for a new interface.
     Unknown - [?Q-NNN], never an invented value. mode: change - mark steps [new]/[chg]/[del] and add a Change column. -->

## Description

<What the method does and why, with source references. For mode: change - how it works now and what changes.>

## Method

Contract: CON-NNN, version <N>.

| Item | Value |
|---|---|
| Purpose | <...> |
| Method | <GET / POST / PUT / PATCH / DELETE> |
| Path | `/<path>` |
| Caller | <screen or component> |
| Access | <who may call it and what is checked> |

## Request

<!-- Parameters: path, query, header, body. Full example: the path with sample values; for a body - complete JSON. -->

| Parameter | In | Type | Required | Description |
|---|---|---|---|---|
| `<name>` | path | uuid | yes | <description> |

Example: `GET /<path>/<sample value>`

## Algorithm

<!-- Plain numbered steps, not a table. Each step says what to do and where every value comes from.
     Error branches inside the steps: "If ... - stop with error 404". Last line - "Result: ...". -->

1. <Check access. If ... - stop with error 403.>
2. <...>

Result: <what the caller gets>.

## Response

<!-- Every field: type, description, source. Complete, working example - no "..." except for long values. -->

| Field | Type | Description | Example |
|---|---|---|---|
| `<field>` | <type> | <description, source> | <example> |

```json
{
  "<field>": "<value>"
}
```

## Response codes

<!-- A subsection per code: when it happens (which step) and the full response body. -->

### 404 <Message>

When: <condition, step>.

```json
{
  "<field>": "<value>"
}
```

## Acceptance criteria

<!-- 3-10 testable statements: condition and observable result, each ending with the requirement it checks. -->

1. <When ..., the method returns ...> (REQ-NNN)

## History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1 | YYYY-MM-DD | Created | <source version> |
