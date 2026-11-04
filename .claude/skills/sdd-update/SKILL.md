---
name: sdd-update
description: "Take a new version of the input document: new snapshot, list of changed sections, affected domains, requirements, contracts and specs, and update them. Use when the business sends a new version of the requirements."
---

# sdd-update: new version of the input

Parameters: feature folder, path to the new Markdown version (in `source/import/`), its origin and version.

## Do

1. Call subagent `sdd-source`: mode `update`. It makes the new snapshot (`source/changes.md`) and rebuilds the slices.
2. Read `source/changes.md`. For every changed, added, removed, renamed or moved section find, through "Sections by domain" of `analysis.md`, the affected domains; through the Source column - the requirements citing it; through the requirements - contracts and specs.
3. Write the impact list into `analysis.md`, section "Next steps": section -> domains -> requirements -> contracts -> specs, and what to do with each.
4. Moved or renumbered sections - fix the Source column of requirements and the Read lists; rebuild slices.
5. Added sections - put them into "Sections by domain" and the Read lists of their domains; analyse the new text with the rules of `sdd-domain` (in this run for small changes, otherwise suggest a run per domain).
6. Changed text - re-read the changed sections in the slices and update requirements; a requirement that loses its basis - `dispositions.md` (excluded or superseded, with the reason and the decision), never deletion.
7. Contracts and specs affected - drafts: update them; approved: list them, the owner decides on a new version.
8. Passport: `source` - the new version, history row.

## Never

Edit the snapshot, delete requirements, change approved artifacts without the owner.

## Self-check

- [ ] Every row of `source/changes.md` is handled in the impact list.
- [ ] Call subagent `sdd-check`: scope - the feature folder, mode `fix`.

## Answer

The changes table, affected domains, requirements changed, added, excluded; contracts and specs to update; approved artifacts waiting for the owner.
