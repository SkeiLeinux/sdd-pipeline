---
type: requirements
feature: LIB-1
domain: ui-reservations
status: draft
updated: 2026-11-03
---

# Requirements: ui-reservations - member portal pages

Node of the [domain map](../analysis.md): member portal.

Boundary. Here: the button, the page, texts, sorting, states. Not here: the rules (service-reservations) and the operations (integration-portal-api).

## Title page

| ID | Requirement | Source | Scenario | Type | Scope | Note |
|---|---|---|---|---|---|---|
| REQ-020 | The title page shall show a "Reserve" button next to each branch with at least one available copy. | 6.1 | Reserve a book | FR | in | the branch list already exists (Q-003) |
| REQ-021 | After a successful reservation the page shall show "The book is reserved for you until {date}." | 6.1 | Reserve a book | FR | in | - |
| REQ-022 | When the limit is reached the page shall show "You already have 3 active reservations." | 6.1 | Reserve a book | FR | in | - |
| REQ-023 | When the catalog cannot be reached the page shall show "Reservations are temporarily unavailable. Please try again later." | 5.3 | Reserve a book | FR | in | - |

## My reservations page

| ID | Requirement | Source | Scenario | Type | Scope | Note |
|---|---|---|---|---|---|---|
| REQ-024 | The portal menu shall have a "My reservations" page with a table: Title, Author, Branch, Reserved on, Valid until, Status (Active, Expired, Cancelled), sorted by "Reserved on", newest first. | 6.2 | - | FR | in | - |
| REQ-025 | The page shall offer the "Cancel" action for active reservations. | 6.2 | - | FR | in | - |
| REQ-026 | When there are no reservations the page shall show "You have no reservations yet." | 6.2 | - | FR | in | - |

## Screen fields

| Field or action | Source rule | Operation |
|---|---|---|
| "Reserve" button | REQ-020, REQ-001 | CON-002 |
| Success message with the end date | REQ-021, REQ-004 | CON-002 |
| Limit message | REQ-022, REQ-002 | CON-002 |
| Catalog unavailable message | REQ-023, REQ-012 | CON-002 |
| Table columns and statuses | REQ-024, REQ-008 | CON-003 |
| Sorting by "Reserved on" | REQ-024 | CON-003 |
| "Cancel" action | REQ-025, REQ-007 | CON-004 |
| Empty state | REQ-026 | CON-003 |
