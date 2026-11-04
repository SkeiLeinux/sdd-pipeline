---
type: requirements
feature: LIB-1
domain: integration-notifications
status: draft
updated: 2026-11-02
---

# Requirements: integration-notifications - emails to members

Edge of the [domain map](../analysis.md): reservation service -> notification gateway.

Boundary. Here: which emails the service requests and with what data. Not here: delivery (the gateway, out of scope).

## Emails

| ID | Requirement | Source | Scenario | Type | Scope | Note |
|---|---|---|---|---|---|---|
| REQ-017 | After a reservation is made, the service shall ask the gateway to email the member the title, the branch and the end date. | 7 | Reserve a book | IR | in | - |
| REQ-018 | Before a reservation expires, the service shall ask the gateway to remind the member. | 7 | Reservation expires | IR | in | when and how [?Q-001] |
| REQ-019 | The notification gateway delivers emails to members. | 3, 7 | - | IR | out | owned by the Messaging team |
