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
     is designed: method, path, request, validation, response, every response code, access, non-functional needs.
     Every field, code and path has a source (requirement, decision, source document, code, provider docs) or is an
     explicit design decision for a new interface. Unknown - [?Q-NNN], never an invented value.
     mode: change - mark steps [new]/[chg]/[del] and add a Change column (new/chg/del) to the tables. -->

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
| Authentication | <how the caller is identified> |
| Authorization | <who may call it; which objects they may touch (ownership, organization, role)> |

## Request

<!-- Every parameter: where it goes (path, query, header, body), type, required, constraints (length, format, range,
     allowed values, default). Nested objects - a Block column with the parent name.
     Full example: the path with sample values; for a body - complete JSON with every field. -->

| Parameter | In | Type | Required | Constraints | Description |
|---|---|---|---|---|---|
| `<name>` | path | uuid | yes | - | <description> |

Example: `GET /<path>/<sample value>`

## Algorithm

<!-- Plain numbered steps, not a table. Each step says what to do and where every value comes from (table and
     column, contract, configuration key). Validation of the request goes first. Error branches inside the steps:
     "If ... - stop with error 404". Every code used here needs a subsection in "Response codes".
     Last line - "Result: ...". -->

1. <Check authentication. If ... - stop with error 401.>
2. <Validate the request by "Request". If invalid - stop with error 400.>
3. <...>

Result: <what the caller gets>.

## Response

<!-- Success status code, then every field: type, required, description with its source. Lists - sorting and
     pagination. Complete, working example - no "..." except for long values. -->

Status: <200 / 201 / 204>.

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `<field>` | <type> | yes | <description, source> | <example> |

```json
{
  "<field>": "<value>"
}
```

## Response codes

<!-- A subsection "### <code> <message>" for every code the method returns: each error the algorithm stops with,
     and the shared ones (400, 401, 403, 404, 409, 422, 429, 500, 503 - only those that can happen; 500 can always happen;
     when the house rules describe shared codes elsewhere - link them). Each: when it happens (step) and the full body. -->

### 400 <Message>

When: step <N>, <condition>.

```json
{
  "<field>": "<value>"
}
```

## Non-functional requirements

<!-- Whatever applies, with sources; otherwise "Not applicable: <why>".
     Performance (latency, throughput), idempotency and retries of the caller, pagination limits, rate limits,
     timeouts of calls to other systems, caching, audit and logging (what is logged, personal data masked). -->

<...>

## Compatibility

<!-- mode: new - "Not applicable: new method". mode: change - is the change backward compatible; if not: new version
     of the path, which consumers must migrate, how long the old version lives. -->

<...>

## Acceptance criteria

<!-- Testable statements, at least one per header requirement and per error code (group related checks in one statement): condition and observable result, each ending with the requirement it checks.
     Cover the success path and every error code. -->

1. <When ..., the method returns ...> (REQ-NNN)

## History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1 | YYYY-MM-DD | Created | <source version> |
