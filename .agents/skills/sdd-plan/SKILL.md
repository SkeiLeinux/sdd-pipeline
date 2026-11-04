---
name: sdd-plan
description: "Plan the spec set: distribute contracts and in-scope requirements into spec units (component, data-model, integration, job, api-method, scenario, ui, config) in the passport. Use after the contract registry passes its gate, before writing specs."
---

# sdd-plan: spec plan

Parameter: feature folder.

First call subagent `sdd-check`: mode `gate contracts`. Not passed - list what is missing and stop: the plan is not made over an incomplete registry.

## Read

1. `requirements/` - all files, `dispositions.md` if present.
2. `analysis.md`: domains, scenarios, impact.
3. `contracts/README.md` and the cards.
4. `decisions/questions.md` - field "Blocks".
5. `sdd.config.json` - `unit_types` (their order is the numbering order); `templates/spec/` - what each type describes.

## Slicing rules

- Only active in-scope requirements; out-of-scope, excluded and superseded ones are not planned.
- New component - one `component` unit; whether it is new is an open question - plan it with the marker in the title. Data model - one `data-model` per component. External system - one `integration` per system. Background job - one `job` per job. API method - one `api-method` per method, describing exactly one in-scope `api` contract. Message, event or queue we own - one `message` per message, describing exactly one in-scope `message` contract (mapping in `contract_unit_types`). Screen, tab, drawer or dialog - one `ui`. Configuration - one `config` per component that has settings: values the source calls configurable, or values the team decides to make settings (say "design decision" in the title or the history row); none - no unit.
- In-scope contracts of kind `file` or `other` (exports, reports, file exchanges) - described by the `integration` or `job` unit that produces or reads them.
- Every new or changed in-scope contract is described by a unit; external and reuse contracts are covered by the units of their consumers, never by a spec for the other team. A file or message format owned by another system that we produce (an import file of their system) is such an external contract: our `integration` or `job` unit lists it and describes how we produce it.
- A scenario of the map where a user action crosses several components and no unit shows the chain - a `scenario` unit; a scenario without a user is covered by a `job`. Fill "Plan coverage" in `analysis.md`.
- Tables by domains of the map: `### <domain> - <summary>`; a unit lives in the domain whose requirements it covers; a unit covering several edges of one external system - under the first edge, with "also covers <edge>" in its title; data model and configuration - with their component's node. Scenario units list in Contracts the contracts their chain crosses, or "-". Scenario units - group `### Scenarios`.

## Do

1. Section "Spec plan" of the passport: `Spec | Type | Title | Component | Requirements | Contracts | Status`, links `specs/SPEC-NN-<slug>.md`, status `draft`.
2. Every in-scope requirement in at least one unit; a requirement may be in several (method and screen).
3. Passport `status: plan`, history row.

## Never

Create spec files, put two methods in one unit, design endpoints here.

## Self-check

- [ ] No in-scope requirement left uncovered; every new/changed in-scope contract planned.
- [ ] Numbers consecutive, slugs unique.
- [ ] "Plan coverage" filled for every scenario.
- [ ] Call subagent `sdd-check`: scope - the passport, mode `fix`.

## Answer

Units per type, requirements covered by several units, units blocked by questions, the order to write them: component and data model -> integrations, jobs and messages -> API methods -> scenarios and screens -> configuration.
