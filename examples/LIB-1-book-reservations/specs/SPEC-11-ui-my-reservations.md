---
id: SPEC-11
type: ui
title: Screen My reservations
feature: LIB-1
component: Member portal
mode: new
status: draft
version: 1
requirements: [REQ-024, REQ-025, REQ-026]
contracts: [CON-003, CON-004]
depends: [SPEC-07, SPEC-08]
updated: 2026-11-04
---

# LIB-1 SPEC-11 Screen My reservations

## Purpose

The member sees their reservations and cancels the ones they no longer need (source 2, 6.2).

## Entry points and access

A new item "My reservations" in the member portal menu (REQ-024). Only a logged-in member sees the item and the page; without a session the portal sends the member to its login page, as for other member pages.

## Layout

1. Page title "My reservations".
2. Table of reservations, or the empty state.

## Fields and actions

| Field or action | Source rule | Operation | Behaviour |
|---|---|---|---|
| Title | REQ-024, REQ-008 | CON-003 | text; source of the value [?Q-006] |
| Author | REQ-024, REQ-008 | CON-003 | text; source of the value [?Q-006] |
| Branch | REQ-024 | CON-003 | branch name as the portal shows it elsewhere |
| Reserved on | REQ-024 | CON-003 | date of `createdAt` in the member's time zone |
| Valid until | REQ-024 | CON-003 | date of `validUntil` in the member's time zone |
| Status | REQ-024 | CON-003 | "Active", "Expired" or "Cancelled" for `active`, `expired`, `cancelled` |
| Sorting | REQ-024 | CON-003 | by "Reserved on", newest first; the member cannot change it |
| "Cancel" | REQ-025, REQ-007 | CON-004 | shown only in rows with status "Active"; after success the row shows "Cancelled" |
| Empty state | REQ-026 | CON-003 | shown instead of the table when the list is empty |

## States and messages

- Loading: the table area shows the portal's standard loader.
- Empty: "You have no reservations yet." (REQ-026)
- Error loading the list or cancelling: the portal's standard error notice; the source gives no text for it.

## Acceptance criteria

1. The menu has "My reservations"; the page shows the columns Title, Author, Branch, Reserved on, Valid until, Status in this order (REQ-024).
2. Rows are sorted by "Reserved on", newest first (REQ-024).
3. "Cancel" is shown only for active reservations and, after success, the row status becomes "Cancelled" (REQ-025).
4. A member without reservations sees "You have no reservations yet." (REQ-026)

## History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1 | 2026-11-04 | Created | source version 3 |
