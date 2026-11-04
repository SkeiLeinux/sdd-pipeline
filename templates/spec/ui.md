---
id: SPEC-NN
type: ui
title: Screen <name>
feature: <ID>
component: <front-end application>
mode: new
status: draft
version: 1
requirements: [REQ-NNN]
contracts: [CON-NNN]
depends: []
updated: YYYY-MM-DD
---

# <ID> SPEC-NN Screen <name>

<!-- One document - one screen, tab, drawer or dialog. Every field and action comes from the "Screen fields" table of
     the UI domain: the rule that drives it and the operation that feeds it. Interface texts - verbatim from the source. -->

## Purpose

<What the user does here.>

## Entry points and access

<How the user gets here; who may see it; what happens without access; what a user without some rights sees.>

## Layout

<Blocks of the screen in order; a link to a mock-up if the source has one; behaviour on small screens if required.>

## Fields and actions

<!-- Every field and action. Behaviour: format, empty value, sorting, when enabled or hidden. Input fields -
     validation and its message (verbatim). Actions - which operation, what happens after success. -->

| Field or action | Source rule | Operation | Behaviour |
|---|---|---|---|
| <label> | REQ-NNN | CON-NNN | <format, empty value, validation, enabled when ...> |

## Navigation and dialogs

<!-- Where each action leads, confirmations before destructive actions (texts verbatim), what is kept when the user
     leaves and comes back (filters, page). "Not applicable: <why>" if the screen has none. -->

<...>

## States and messages

<Loading, empty, error, partial data states and the exact texts from the source; what the user sees for each error
code of the operations.>

## Acceptance criteria

1. <...> (REQ-NNN)

## History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1 | YYYY-MM-DD | Created | <source version> |
