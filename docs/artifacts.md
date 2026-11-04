# Artifacts: files, IDs, statuses, formats

[Русская версия](artifacts.ru.md)

## Feature folder

```
features/<ID>-<slug>/
  README.md                    passport and spec plan
  source/import/               raw input as received (not checked)
  source/source.md             immutable numbered snapshot
  source/index.md              sections with line ranges and checksums
  source/changes.md            what a new version changed (after an update)
  source/domains/<domain>.md   generated slices
  analysis.md                  domain map, scenarios, index of sections, impact, risks
  requirements/README.md       index of domain files
  requirements/<domain>.md     requirements of one domain
  requirements/dispositions.md excluded and superseded requirements
  decisions/questions.md       open, answered, deferred questions
  decisions/decisions.md       decisions (append-only)
  decisions/manual.md          human interventions (append-only)
  contracts/README.md          contract registry
  contracts/CON-NNN-<slug>.md  contract cards
  specs/SPEC-NN-<slug>.md      spec units
  traceability.md              generated matrix
```

The folder is `<ID>` or `<ID>-<slug>`; the ID matches `feature_id_pattern` in `sdd.config.json` (a tracker key works well: `PAY-42`). File names are Latin kebab-case.

## IDs

| Entity | Format | Unique within |
|---|---|---|
| Feature | by `feature_id_pattern`, e.g. `LIB-1` | repository |
| Domain | kebab-case, e.g. `service-reservations`, `ui-reservations`, `integration-catalog` | feature |
| Requirement | `REQ-NNN` | feature |
| Question / decision | `Q-NNN` (a decision keeps its question's ID) | feature |
| Manual intervention | `M-NNN` | feature |
| Contract | `CON-NNN` | feature |
| Spec unit | `SPEC-NN` | feature |

IDs are Latin only (the checker catches Cyrillic look-alikes such as `RЕQ` with a Cyrillic `Е`). IDs are never reused: an excluded requirement stays in its file and gets a row in `dispositions.md`. From outside the feature, use the full form `LIB-1/REQ-012`.

## Frontmatter

Every file starts with `--- ... ---`: `key: value` and lists `[a, b]` only.

| type | Required keys |
|---|---|
| `feature` (passport) | `id`, `title`, `status`, `source`, `owner`, `updated` |
| `analysis`, `requirements` | `feature`, `status`, `updated` (+ `domain` for requirements) |
| `questions`, `decisions`, `manual` | `feature`, `updated` |
| `contracts` (registry) | `feature`, `status`, `version`, `owner`, `updated` |
| `contract` (card) | `id`, `title`, `feature`, `domain`, `kind`, `provider`, `consumers`, `scope`, `mode`, `status`, `version`, `requirements`, `updated` |
| spec unit (`type` = unit type) | `id`, `type`, `title`, `feature`, `component`, `mode`, `status`, `version`, `requirements`, `contracts`, `depends`, `updated` |

## Statuses

| Artifact | Statuses |
|---|---|
| Feature | `intake`, `analysis`, `contracts`, `plan`, `spec`, `ready`; `hold`, `cancelled` |
| Contract registry and cards | `draft`, `review`, `approved` |
| Spec unit | `draft`, `review`, `approved`, `superseded` |
| Question | `open`, `answered` (not applied yet), `deferred` |
| Decision | `active`, `superseded by Q-NNN` |
| Manual intervention (Type) | `decision`, `edit`, `approval`, `rejection` |

An approved spec changes only through a new version: `version + 1`, status `review`, a row in "History".

## Requirements

Seven columns: `ID | Requirement | Source | Scenario | Type | Scope | Note`.

- Source - section numbers of the snapshot, comma-separated; always present.
- Type - from `requirement_types` (default `FR`, `NFR`, `BR`, `IR`).
- Scope - `scope.in` or `scope.out` labels from the config.
- Note - decision references `(Q-NNN)`, markers `[?Q-NNN]`, or `-`.

`dispositions.md`: `Requirement | State | Reason | Decision | Replacement`, state `excluded` or `superseded`.

## Domain map format

The headings of `analysis.md` are read by the scripts; keep them as in the template. The parts with a strict format:

- **Domains** - table `Domain | Kind | Component | Summary | Questions`, Kind `node` or `edge`.
- **Source slices** - a subsection `### <domain> - <summary>` per domain with a line `Read:` followed by bullets `- <refs> - <what to look for>.` References: `N` - section N with its subsections; `N-M` - from N through the end of M; `N (intro)` - only the text of N before its subsections; several separated by `, `.
- **Sections by domain** - table `Section | Domains | Notes`; first cell starts with the section number; domains comma-separated, `all`, or `-`.
- **Findings for domains** - subsections per domain with bullets; `- Applied <date> in <file>` marks them handled.

## Questions, decisions, interventions

Blocks `### Q-NNN <title>` with bullet fields. Question: `To`, `Where`, `Blocks`, `Status`, `Sent`, `Question`, `Proposal`, `Answer`. Decision: `Status`, `Kind` (`business`, `technical`, `external`), `Question`, `Decision`, `Why`, `Decided`, `Affects`, `Where`. Intervention `### M-NNN`: `Type`, `What`, `Who and when`, `Basis`, `Affects`.

## Markers

| Marker | Meaning |
|---|---|
| `[?Q-NNN]` | unknown here, see the open question; not allowed in approved specs |
| `(Q-NNN)` | this follows from a decision |
| `[new]`, `[chg]`, `[del]` | in `mode: change` specs - new, changed, removed step or row |

## Spec units

Default types (`unit_types` in `sdd.config.json`, numbering order):

| Type | One file describes |
|---|---|
| `component` | a new component or a significant change of one: boundaries, interfaces, operations |
| `data-model` | the data model of one component: tables, enumerations, indexes, lifecycle |
| `integration` | the exchange of our component with one external system |
| `job` | one background job |
| `message` | one message, event or queue we own: channel, payload, delivery |
| `api-method` | one API method: request, algorithm, response, every response code |
| `scenario` | an end-to-end chain through several components |
| `ui` | one screen, tab, drawer or dialog |
| `config` | the configuration a feature adds to one component |

`api-method` and `message` describe exactly one in-scope contract of kind `api` and `message` (`contract_unit_types`).

Required sections of a unit are the `## ` headings of its template `templates/spec/<type>.md`. A section that does not apply stays with "Not applicable: <why>". HTML comments copied from templates are hints and are reported until removed.

## Checker rule codes

Output lines look like `E path:line - [code] message`. Groups:

| Prefix | What |
|---|---|
| `fm-*` | frontmatter, file names, statuses |
| `id-cyrillic`, `style-*` | IDs and house style |
| `source-*`, `domain-*` | snapshot, domain map, slices, section index, findings, UI screen fields |
| `req-*` | requirements and dispositions |
| `q-*`, `m-*`, `marker-*` | questions, decisions, interventions, markers |
| `contract-*` | registry and cards, coverage |
| `plan-*`, `spec-*`, `scenario-coverage`, `section`, `placeholder`, `template-comment` | plan and spec units |
| `api-codes`, `api-success`, `api-envelope` | every code the algorithm uses is described with a body; the success code is stated; house envelope |
| `dm-*` | data model columns, logical types, primary keys |
| `link-*` | references to things that do not exist |
| `gate` | gate conditions |
