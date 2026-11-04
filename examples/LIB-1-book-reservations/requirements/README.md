---
type: requirements-index
feature: LIB-1
status: draft
updated: 2026-11-03
---

# Requirements LIB-1

One file - one domain of the [domain map](../analysis.md). Requirement texts live in domain files, not here.

| File | Domain | Requirements | Out of scope |
|---|---|---|---|
| [service-reservations.md](service-reservations.md) | service-reservations - reservation rules and data | 10 (REQ-001 - REQ-010) | 0 |
| [integration-catalog.md](integration-catalog.md) | integration-catalog - availability check | 3 (REQ-011 - REQ-013) | 1 |
| [integration-portal-api.md](integration-portal-api.md) | integration-portal-api - portal to reservation service | 3 (REQ-014 - REQ-016) | 0 |
| [integration-notifications.md](integration-notifications.md) | integration-notifications - emails to members | 3 (REQ-017 - REQ-019) | 1 |
| [ui-reservations.md](ui-reservations.md) | ui-reservations - member portal pages | 7 (REQ-020 - REQ-026) | 0 |

Total 26. Next free ID: `python tools/check.py examples/LIB-1-book-reservations --next`.
