# Customization

[Русская версия](customization.ru.md)

The pipeline is meant to be adopted, not used as is. Most adaptations are settings in `sdd.config.json`; the rest are templates and skills.

## Settings

| Key | Default | What it changes |
|---|---|---|
| `artifact_language` | `en` | language of the prose agents write; headings, keys, statuses and field labels stay English for the checker |
| `feature_id_pattern` | `^[A-Z][A-Z0-9]*-[0-9]+$` | feature IDs; match your tracker keys |
| `scope` | `{"in": "in", "out": "out"}` | labels of the Scope column, e.g. `{"in": "ours", "out": "external"}` |
| `requirement_types` | `FR`, `NFR`, `BR`, `IR` | allowed requirement types |
| `ui_domain_prefix` | `ui-` | domains with this prefix need a "Screen fields" table |
| `unit_types` | eight types | spec unit types in numbering order; each needs a template |
| `api_unit_type`, `data_model_unit_type` | `api-method`, `data-model` | which types get API and data model rules |
| `contract_kinds`, `contract_modes` | `api, message, file, other`; `new, change, reuse, external` | allowed values in contracts |
| `api_response_required_keys` | `[]` | keys every API response example must contain - your response envelope, e.g. `["data", "error"]` |
| `data_model` | `Name, Type, Comment, Constraint`, logical types | columns and types of data model tables |
| `style.forbidden_chars`, `style.forbidden_words` | empty | house style, reported as warnings |

Example of a strict house style:

```json
"style": {
  "forbidden_chars": {"—": "use '-'", "«": "use straight quotes", "»": "use straight quotes"},
  "forbidden_words": {"customer": "say 'user'"}
}
```

## Writing artifacts in another language

Set `artifact_language` (for example `ru`). Agents then write requirements, questions, cards and specs in that language. Keep in English: headings that come from templates, frontmatter keys, status values, field labels like `- Status:`, table headers, IDs. That is what makes the checker language-independent. If you want localized templates, translate the prose and the hints in `templates/`, but keep the `## ` headings in sync with what the skills and the checker expect - or change both.

## Adding a spec unit type

1. Add the type to `unit_types` (its position sets the numbering order).
2. Create `templates/spec/<type>.md`. Its `## ` headings become the required sections of every unit of that type.
3. Add a slicing rule to `.agents/skills/sdd-plan/SKILL.md` and, if the type has special rules, to `sdd-spec` and `sdd-review`.
4. Run `python tools/sync_agents.py`.

## House rules for APIs and data

- A standard response envelope: list its top-level keys in `api_response_required_keys`, describe it in the `api-method` template and in the rules of `sdd-spec`.
- Versioning, naming, error code registries: write them down in a `docs/` page of your own and add it to the "Read" list of `sdd-spec` and `sdd-review`.
- Data types: adjust `data_model.types` to your logical types and the template's hint.

## Approvals and roles

The pipeline only assumes that "approved" means "the people responsible agreed". A common setup: specs go to review as pull requests; approvals from the component's developers, consumers of its interfaces and QA; the owner sets `approved` after the merge. Write your approval matrix into `docs/pipeline.md` of your copy.

## Describing an existing system

For features that change an existing system, `sdd-impact` needs something to read: code, or documentation of the current state. A good practice is a `system/` folder with a card per component (purpose, interfaces, data, configuration) that is updated after each feature is delivered - so the next feature's specs are written as changes to a described system, not reverse-engineered from code.

## Extending past specs

The pipeline stops at approved specs on purpose. Natural extensions, each as a skill with a template:

- tasks per spec unit (one task - one merge request in one repository);
- test cases per spec unit, linked to requirements;
- a rollout plan per feature;
- updating the system description after delivery.

Add new ID types and checks to `tools/check.py` with tests, and new gates where they help.
