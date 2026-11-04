---
name: sdd-map
description: "Build the domain map of a whole input document: nodes (components), edges (exchanges), scenarios, Read lists per domain and the index of sections by domain; then build the per-domain slices. Use after sdd-intake, before requirements are extracted."
---

# sdd-map: domain map

Parameter: feature folder. No snapshot - stop and suggest `sdd-intake`.

Why: input documents describe processes, screens and rules mixed together, while specs, contracts and code live in components and in the exchanges between them. Requirements are therefore extracted per domain, not per section; the section number stays as a reference in every requirement.

## Read

1. `source/source.md` - whole. This is the only skill that reads the whole snapshot.
2. `templates/feature/analysis.md` and `examples/LIB-1-book-reservations/analysis.md` (the form to follow).
3. The passport (scope, components) and `decisions/`.

## Do

1. Create `analysis.md` from the template. Keep the headings: the scripts read them.
2. **Domains.** Nodes - a component or a large part of one with its own data and logic (a new service, an existing service's part, a front-end application). Edges - an exchange between two components, including systems out of scope (they appear as providers or consumers of edges, not as nodes we analyse). Names: lowercase kebab-case; UI nodes start with `ui_domain_prefix` from `sdd.config.json`; edges conventionally `integration-<exchange>`. Size: a domain is something one agent run can analyse completely - roughly up to 40 requirements; split a node whose behaviour falls into clearly separate parts (approval rules, export processing). A core node reading many sections partly is normal. Edge direction: `<provider> -> <consumer>`, where the provider owns the interface (exposes the API, defines the file or message format, sends the notification on request) and the consumer uses it; data may flow either way - say which in the summary.
3. **Source slices.** A subsection `### <domain> - <summary>` per domain: what is inside and what is not, links (which edges), a `Read:` list in the strict format of the template, and "Watch:" for contradictions, different names of one thing, text only on images. A section several domains need goes into each Read list.
4. **Sections by domain.** Every section of `source/index.md`: its domains, "all" for overview or constraints sections, or "-" with the reason (history, glossary, motivation).
5. **Scenarios.** Chains of user or system actions through several domains, with source sections and the path.
6. **Cross-cutting rules** (access, limits of the feature) with the domains they apply to.
7. **Glossary.** Every entity and term of the feature with one name to use in specs, and the synonyms the source uses. Two names for one thing, or one name for two things - a question.
8. Questions that decide domain boundaries (who owns the data, which component does it, name of a new component) - blocks in `decisions/questions.md`, markers in the domains table; `Blocks: -` and the domains in `Where` (no requirements exist yet; `sdd-domain` fills Blocks). Other gaps and contradictions - only under "Watch:"; `sdd-domain` turns them into questions. A Watch item names the sections it needs; they must be in that domain's Read list. Next free ID: `python tools/check.py <feature> --next`.
8a. "Impact": keep the heading with the line "Not analysed yet - `sdd-impact`."; for a green-field feature write "Green field - no existing system." instead.
9. Call subagent `sdd-source`: mode `slices`. Errors in Read lists - fix the lists and rebuild.
10. "Next steps": the order to analyse domains - back-end nodes and edges first, UI domains last.
11. Passport: `status: analysis`, history row "Domain map drafted".

## Never

Retell or edit the source, skip a section in the index, name a domain after a section of the document ("section-5"), create domain requirement files (that is `sdd-domain`).

## Self-check

- [ ] Every section of `source/index.md` is in "Sections by domain".
- [ ] Every domain has a Read list; slices are built without errors.
- [ ] Every edge has a provider and a consumer; out-of-scope systems are only at the ends of edges.
- [ ] Call subagent `sdd-check`: scope - `analysis.md`, mode `fix`.

## Answer

Domains (nodes, edges), scenarios, questions about boundaries, the suggested order. Ask the owner to approve the map. Their answer (any later session): apply edits, rebuild slices, record `M-NNN` in `decisions/manual.md`, set `analysis.md` to `status: approved`, passport history "Domain map approved (M-NNN)".
