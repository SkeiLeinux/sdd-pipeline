---
type: decisions
feature: LIB-1
updated: 2026-11-03
---

# Decisions LIB-1

### Q-003 Where the list of branches on the title page comes from

- Status: active
- Kind: external
- Question: The title page "already lists branches with available copies". Is that list available to the portal today, and with which identifiers?
- Decision: Yes. The portal shows it through the existing catalog widget, which gives the title ID and branch ID of every row. The "Reserve" button uses these IDs; no new interface is needed for the list.
- Why: confirmed by the portal team on the current title page.
- Decided: portal team lead, 2026-11-02; chat
- Affects: REQ-020, SPEC-10
- Where: source 6.1

### Q-004 Is the reservation service a separate component

- Status: active
- Kind: technical
- Question: Should reservations live in an existing component or in a new service with its own storage?
- Decision: A new reservation service with its own database. The portal calls it through its API.
- Why: the rules and the audit trail belong to reservations only; the portal stays a client.
- Decided: development lead, 2026-11-02; design meeting
- Affects: REQ-001, SPEC-01, SPEC-02
- Where: source 3
