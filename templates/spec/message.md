---
id: SPEC-NN
type: message
title: <Publish|Consume> <event or message name>
feature: <ID>
component: <component that owns the message>
mode: new
status: draft
version: 1
requirements: [REQ-NNN]
contracts: [CON-NNN]
depends: []
updated: YYYY-MM-DD
---

# <ID> SPEC-NN <Publish|Consume> <event or message name>

<!-- One document - one asynchronous message, event or queue we own (we publish it, or we define what we accept).
     A message of another system we only consume is described in its integration spec instead.
     Every field has a source or is an explicit design decision. Unknown - [?Q-NNN]. -->

## Description

<What happened or what is requested, who needs to know and why. Source references.>

## Channel

Contract: CON-NNN, version <N>.

| Item | Value |
|---|---|
| Transport | <broker, queue, topic, webhook> |
| Channel | `<topic or queue name, or configuration key>` |
| Producer | <component> |
| Consumers | <components> |
| Key | <partition or routing key, if ordering matters> |
| Access | <who may publish and subscribe> |

## Payload

<!-- Every field: type, required, description with its source. Headers or metadata (message ID, type, time,
     correlation ID). Complete example. -->

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `<field>` | <type> | yes | <description, source> | <example> |

```json
{
  "<field>": "<value>"
}
```

## Trigger and processing

<!-- Producer: in which step of which spec the message is sent, inside or after the transaction.
     Consumer: numbered steps of processing; last line "Result: ...". -->

1. <...>

Result: <...>.

## Delivery and errors

<!-- Delivery guarantee (at least once / at most once), ordering, duplicates and idempotency on the consumer side,
     retries, dead-letter handling, what happens with an invalid message, retention of the channel. -->

<...>

## Compatibility

<!-- mode: new - "Not applicable: new message". mode: change - backward compatible or not; versioning of the payload;
     which consumers must change and when. -->

<...>

## Acceptance criteria

1. <...> (REQ-NNN)

## History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1 | YYYY-MM-DD | Created | <source version> |
