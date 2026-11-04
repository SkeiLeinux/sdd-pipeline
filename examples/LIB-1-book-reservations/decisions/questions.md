---
type: questions
feature: LIB-1
updated: 2026-11-03
---

# Open questions LIB-1

### Q-001 When and how is the member reminded before expiry

- To: business analyst
- Where: source 7; REQ-018
- Blocks: REQ-018, CON-005, SPEC-04, SPEC-05
- Status: open
- Sent: 2026-11-02
- Question: "The member should be reminded before the reservation expires" gives no timing. How long before the end is the reminder sent, and is it one email or more?
- Proposal: one email 24 hours before the end; none if the reservation is shorter than that.
- Answer: -

### Q-002 From when are the 30 days of visibility counted

- To: business analyst
- Where: source 5.2; REQ-006
- Blocks: REQ-006, SPEC-02, SPEC-05, SPEC-07
- Status: open
- Sent: 2026-11-02
- Question: "Expired reservations stay visible to the member for 30 days" - from the end of the reservation or from the moment it was made? Do cancelled reservations follow the same rule?
- Proposal: 30 days from the end (expiry or cancellation), the same for cancelled.
- Answer: -

### Q-005 Is a second reservation of the same title at another branch allowed

- To: business analyst
- Where: source 5.1; REQ-003
- Blocks: REQ-003, SPEC-06
- Status: open
- Sent: 2026-11-02
- Question: "Cannot reserve the same title again while they have an active reservation for it" - does it also forbid the same title at a different branch?
- Proposal: forbid at any branch.
- Answer: -

### Q-006 Catalog interface for availability, title and author

- To: Catalog team
- Where: source 3, 5.3, 6.2; REQ-011, REQ-015
- Blocks: CON-001, SPEC-03
- Status: open
- Sent: 2026-11-03
- Question: Which catalog operation returns the number of available copies of a title per branch, with what identifiers and format? Does it also return the title name and author, which the "My reservations" table needs?
- Proposal: -
- Answer: -
