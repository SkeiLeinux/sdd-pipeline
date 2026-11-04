---
id: SPEC-NN
type: data-model
title: Data model of <component>
feature: <ID>
component: <component>
mode: new
status: draft
version: 1
requirements: [REQ-NNN]
contracts: []
depends: []
updated: YYYY-MM-DD
---

# <ID> SPEC-NN Data model of <component>

<!-- One document - the data model of one component. Database - in Overview, a subsection per table.
     Columns: Name | Type | Comment | Constraint (types are logical - see data_model.types in sdd.config.json).
     An empty Constraint cell means "optional". Indexes - a separate table. mode: change - add a Change column (new/chg/del). -->

## Overview

<Storage, schema, what the model holds and why. Source references.>

## Tables

### <table_name>

<What one row means.>

| Name | Type | Comment | Constraint |
|---|---|---|---|
| `id` | uuid | Identifier | PK |

## Indexes

| Table | Index | Columns | Unique | Why |
|---|---|---|---|---|
| `<table>` | `<index>` | `<columns>` | no | <which query needs it> |

## Migration

<New tables only, or data migration steps; "Not applicable: new storage" when there is nothing to migrate.>

## Acceptance criteria

1. <...> (REQ-NNN)

## History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1 | YYYY-MM-DD | Created | <source version> |
