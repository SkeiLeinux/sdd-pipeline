---
type: manual
feature: LIB-1
updated: 2026-11-03
---

# Manual interventions LIB-1

Log of what a person changed in the agent's work. One block - one intervention, blocks are never edited.

### M-001 Domain map approved

- Type: approval
- What: approved the map of 5 domains and their Read lists after the edit in M-002
- Who and when: analyst, 2026-11-02
- Basis: review of analysis.md against the input
- Affects: analysis.md

### M-002 Two UI domains merged into one

- Type: edit
- What: the agent proposed ui-title-page and ui-my-reservations; merged them into ui-reservations
- Who and when: analyst, 2026-11-02
- Basis: both screens are small, belong to one application and use the same edge integration-portal-api; specs are still one per screen (SPEC-10, SPEC-11)
- Affects: analysis.md, requirements/ui-reservations.md
