---
type: feature
id: LIB-1
title: Online book reservations
status: spec
source: book-reservations-brd.md, version 3
owner: Example analyst
updated: 2026-11-04
---

# LIB-1 Online book reservations

A complete, synthetic example of the pipeline: input, snapshot, domain map, requirements, questions and decisions, contracts, plan and three written specs. The library, its teams and all data are invented. Some specs are deliberately left unwritten and some questions open, so the checker shows what an in-progress feature looks like.

## Summary

| Item | Value |
|---|---|
| Input | [source/source.md](source/source.md), version 3 |
| Business goal | Members reserve books online instead of calling; reservation calls go down by half (source 2) |
| Scope | In: the new reservation service and member portal pages. Out: catalog system, notification gateway (source 3) |
| Components | Reservation service (new), Member portal |

## Constraints and assumptions

Constraints:

1. The catalog system and the notification gateway are used as they are (source 3).
2. Librarian tools are not part of this iteration (source 4, 9).

Assumptions:

1. The reservation service is a new component with its own database - decided by the lead, Q-004.

## Documents

| Document | Link |
|---|---|
| Domain map and impact | [analysis.md](analysis.md) |
| Requirements | [requirements/README.md](requirements/README.md) |
| Questions and decisions | [decisions/questions.md](decisions/questions.md), [decisions/decisions.md](decisions/decisions.md), [decisions/manual.md](decisions/manual.md) |
| Contracts | [contracts/README.md](contracts/README.md) |
| Traceability | [traceability.md](traceability.md) |

## Spec plan

### service-reservations - reservation rules and data

| Spec | Type | Title | Component | Requirements | Contracts | Status |
|---|---|---|---|---|---|---|
| [SPEC-01](specs/SPEC-01-reservation-service.md) | component | Component Reservation service | Reservation service | REQ-009, REQ-010 | - | draft |
| [SPEC-02](specs/SPEC-02-reservation-data-model.md) | data-model | Data model of Reservation service | Reservation service | REQ-001, REQ-004, REQ-006, REQ-009 | - | draft |
| [SPEC-05](specs/SPEC-05-expire-reservations-job.md) | job | Background job Expire reservations | Reservation service | REQ-005, REQ-006, REQ-018 | - | draft |

### integration-catalog - availability check

| Spec | Type | Title | Component | Requirements | Contracts | Status |
|---|---|---|---|---|---|---|
| [SPEC-03](specs/SPEC-03-catalog-integration.md) | integration | Integration with the catalog system | Reservation service | REQ-011, REQ-012 | CON-001 | draft |

### integration-notifications - emails to members

| Spec | Type | Title | Component | Requirements | Contracts | Status |
|---|---|---|---|---|---|---|
| [SPEC-04](specs/SPEC-04-notification-integration.md) | integration | Integration with the notification gateway | Reservation service | REQ-017, REQ-018 | CON-005 | draft |

### integration-portal-api - portal to reservation service

| Spec | Type | Title | Component | Requirements | Contracts | Status |
|---|---|---|---|---|---|---|
| [SPEC-06](specs/SPEC-06-api-create-reservation.md) | api-method | Add POST /reservations | Reservation service | REQ-001, REQ-002, REQ-003, REQ-004, REQ-010, REQ-011, REQ-012, REQ-014 | CON-002 | draft |
| [SPEC-07](specs/SPEC-07-api-list-reservations.md) | api-method | Add GET /reservations | Reservation service | REQ-006, REQ-008, REQ-015 | CON-003 | draft |
| [SPEC-08](specs/SPEC-08-api-cancel-reservation.md) | api-method | Add POST /reservations/{id}/cancel | Reservation service | REQ-007, REQ-016 | CON-004 | draft |

### Scenarios

| Spec | Type | Title | Component | Requirements | Contracts | Status |
|---|---|---|---|---|---|---|
| [SPEC-09](specs/SPEC-09-scenario-reserve-a-book.md) | scenario | Scenario Reserve a book | Reservation service | REQ-001, REQ-011, REQ-017, REQ-021 | - | draft |

### ui-reservations - member portal pages

| Spec | Type | Title | Component | Requirements | Contracts | Status |
|---|---|---|---|---|---|---|
| [SPEC-10](specs/SPEC-10-ui-reserve-button.md) | ui | Screen Reserve button on the title page | Member portal | REQ-020, REQ-021, REQ-022, REQ-023 | CON-002 | draft |
| [SPEC-11](specs/SPEC-11-ui-my-reservations.md) | ui | Screen My reservations | Member portal | REQ-024, REQ-025, REQ-026 | CON-003, CON-004 | draft |

## History

| Date | Event |
|---|---|
| 2026-11-01 | Input accepted, version 3; snapshot made |
| 2026-11-02 | Domain map approved (M-001); domains analysed |
| 2026-11-03 | Contract registry in review; spec plan made |
| 2026-11-04 | SPEC-02, SPEC-06, SPEC-11 written as drafts |
