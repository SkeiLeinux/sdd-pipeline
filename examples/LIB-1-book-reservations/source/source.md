---
type: source
feature: LIB-1
title: Online book reservations - business requirements
origin: book-reservations-brd.md, version 3
snapshot: 2026-11-04
---

# Online book reservations - business requirements

<!-- Snapshot of the input document. Do not edit: a new version of the input is a new snapshot (tools/snapshot.py --force). -->

## 0 Preamble

Version 3, prepared by the Member Services team of a fictional city library network. All names and data are invented.

## 1 Background

Members of the library can reserve a book only by phone today. Staff spend about two hours a day on reservation calls, and members cannot see which reservations they already have.

## 2 Goals

- Members reserve a book online for pickup at a chosen branch.
- Members see their reservations and can cancel them.
- Phone calls about reservations go down by half within three months.

## 3 Scope

In scope: a new reservation service and the member portal pages described below.

Out of scope: the catalog system (owned by the Catalog team) - it already knows how many copies of a title each branch has; the notification gateway (owned by the Messaging team) - it sends emails to members. We use both as they are.

## 4 Users and access

Only members logged in to the member portal can reserve books and see reservations. A member sees and changes only their own reservations. Librarian tools are not part of this iteration.

## 5 Business rules

### 5.1 Reservation limits

- A reservation is made for a title at one branch.
- A member may have at most 3 active reservations at a time.
- A member cannot reserve the same title again while they have an active reservation for it.

### 5.2 Reservation lifetime

- A reservation is active for 3 days from the moment it is made. After that it expires automatically.
- A member can cancel an active reservation at any time.
- Expired reservations stay visible to the member for 30 days.

### 5.3 Availability

- A book can be reserved only if the catalog reports at least one available copy at the chosen branch at the moment of the request.
- If the catalog cannot be reached, the member sees the message "Reservations are temporarily unavailable. Please try again later."

## 6 Screens

### 6.1 Title page: Reserve button

- The title page already lists branches with available copies. A "Reserve" button is shown next to each branch with at least one available copy.
- After a successful reservation the member sees: "The book is reserved for you until {date}."
- If the member already has 3 active reservations: "You already have 3 active reservations."

### 6.2 My reservations page

- A new page "My reservations" in the member portal menu.
- Table columns: Title, Author, Branch, Reserved on, Valid until, Status.
- Statuses: Active, Expired, Cancelled.
- Action "Cancel" is available for active reservations.
- Rows are sorted by "Reserved on", newest first.
- When there are no reservations: "You have no reservations yet."

## 7 Notifications

- When a reservation is made, the member gets an email with the title, the branch and the date until which the book is held.
- The member should be reminded before the reservation expires.

## 8 Non-functional requirements

- Making a reservation takes no longer than 2 seconds for 95% of requests.
- Every change of a reservation is logged for audit: who, when and what changed.

## 9 Open points

- Whether librarians may override the limit of 3 reservations will be decided in the next iteration.
