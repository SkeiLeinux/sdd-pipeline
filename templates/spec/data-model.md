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

<!-- One document - the data model of one component. Storage - in Overview, a subsection per table.
     Columns: Name | Type | Comment | Constraint (types are logical - see data_model.types in sdd.config.json).
     Constraint: PK, FK <table.column>, NOT NULL, UNIQUE, max N, default, check. An empty Constraint cell means
     "optional". Indexes - a separate table. mode: change - add a Change column (new/chg/del). -->

## Overview

<Storage, schema, what the model holds and why. Source references. Relations between tables in one or two sentences.>

## Tables

### <table_name>

<What one row means.>

| Name | Type | Comment | Constraint |
|---|---|---|---|
| `id` | uuid | Identifier | PK |

## Enumerations

<!-- Every enum or reference value used in the tables: stored value, meaning, label shown to users (verbatim from the
     source). "Not applicable: no enumerations" if there are none. -->

| Column | Value | Meaning | Label |
|---|---|---|---|
| `<table.column>` | `<value>` | <meaning> | "<label from the source>" |

## Indexes

| Table | Index | Columns | Unique | Why |
|---|---|---|---|---|
| `<table>` | `<index>` | `<columns>` | no | <which query needs it> |

## Data lifecycle

<!-- Retention and deletion (how long rows live, who deletes them), archiving, personal or sensitive data and how
     it is protected (masking, encryption, access), expected volume and growth. -->

<...>

## Migration

<New tables only, or data migration steps and rollback; "Not applicable: new storage" when there is nothing to migrate.>

## Acceptance criteria

1. <...> (REQ-NNN)

## History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1 | YYYY-MM-DD | Created | <source version> |
