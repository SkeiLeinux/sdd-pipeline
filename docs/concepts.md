# Concepts: what the pipeline believes and why

[Русская версия](concepts.ru.md)

The pipeline grew out of daily work of a systems analyst who had to turn long business requirement documents into specifications for several services, with AI agents writing drafts. Every rule below exists because something went wrong without it.

## The problem

A requirements document is written for reading: it follows processes and screens, mixes rules with UI texts, and refers to "the system" when three components and two other teams are involved. A delivery team needs something else: per component, what to build; per interface, what is exchanged; per change, who approves it.

Translating one into the other by hand is slow and loses things: a rule mentioned only in a screen description, an endpoint nobody listed, a question asked in chat and forgotten. Translating it with an LLM is fast and loses things differently: the model fills gaps with plausible inventions, retells the source in its own words, and is equally confident when it is wrong.

The pipeline keeps the speed of agents and adds what stops both kinds of loss.

## Principles

### 1. The spec is the main artifact

Code, tests and rollout are produced from approved specs and checked against them. Behaviour not in a spec is a process defect, not a developer's initiative. Specs are Markdown in git: diffable, reviewable in pull requests, readable by both people and agents.

### 2. The input is immutable

The document is taken in as a snapshot and never edited. Headings get stable section numbers, each section a checksum.

Why: once the source is "cleaned up" or retold, nobody can tell what the business actually said, and every later argument starts from the agent's version. A gap or contradiction becomes a question to its author, not a silent fix. The checksums show precisely which sections a new version changed, so the impact of a change is computed, not guessed.

### 3. Decompose by domains, not by sections

The snapshot is split into **domains**: nodes (a component or a large part of one, with its own data and logic) and edges (an exchange between two components). End-to-end scenarios run through several domains. Each requirement has exactly one home domain, chosen by simple rules: behaviour inside a component - its node; data and order of an exchange - the edge; the screen shows, the service decides.

Why: extracting requirements section by section duplicates them (the same rule appears in a process description and on a screen) and misses exchanges (no section is called "the API between the portal and the service"). Domains map onto what is actually built and owned. A section needed by several domains is read by each of them.

The agent does not choose what text a domain sees: a script builds each domain's **slice** - a verbatim copy of the sections listed for it in the map. The agent reads the source, not its own summary of it, and a new version of the source shows up as a diff of slices.

### 4. Contracts before the plan

After requirements and before planning, every interface is listed in a registry with a short card: purpose, provider, consumers, expected input and result, the requirements it serves. Full schemas come later, in specs.

Why: interfaces are where components and teams meet, and they are what is most often forgotten. A complete list before planning makes the plan complete (every new interface gets a spec) and lets both sides agree on meaning before anyone argues about field names. A gate checks that every edge of the map has its contracts and every requirement is linked to a contract or has a reason not to be.

### 5. One unit - one file

One API method, one data model per component, one integration per external system, one background job, one screen. Two methods are two specs, even if they are steps of one chain.

Why: small units have one owner and one set of approvers, are reviewed in one sitting, fit an agent's context whole, and can be written in parallel. A large document is approved once and then diverges from reality silently.

### 6. "I don't know" is a tracked question

Every unknown fact or rule becomes a question block (`Q-NNN`, to whom, what it blocks) and a marker `[?Q-NNN]` at the exact place. When answered, the decision is moved to an append-only log and applied where the marker was.

Why: language models are most dangerous where they don't know - they answer anyway, confidently. A marker makes the gap visible in the text; the "Blocks" field lets a gate refuse to approve anything that depends on an open question. The log keeps decisions out of chat history, where they are lost.

### 7. The machine checks form, people check meaning

`tools/check.py` is deterministic and cheap: broken references, missing sections, requirements without a source, uncovered requirements and contracts, stale slices, house style. It never claims the specs are right. A pass means "nothing is visibly missing or inconsistent".

Why: people are bad at noticing that requirement 47 of 300 is not covered by any spec; scripts are perfect at it. Scripts cannot judge whether a rule is correct; people can. Each does what it is good at.

### 8. Traceability is generated

Source section -> requirement -> contract -> spec is a chain of IDs inside the artifacts. The matrix (`traceability.md`) is built by the checker, never maintained by hand.

Why: a hand-made matrix is out of date the day after it is made.

### 9. One skill - one step - one session

Each step of the pipeline is a skill: explicit inputs, what to read and what not to, the template and an example, rules, a self-check. Each run handles one coherent portion (one domain, one spec) in a fresh session.

Why: the tail of a previous task in the context degrades any model. Templates fix the structure; examples fix the form better than any description, because models imitate examples more reliably than they follow instructions.

### 10. Scripts run in subagents; people's edits are recorded

Scripts are run by subagents that return a ten-line report, so long outputs never fill the main agent's context. When a person approves, edits or rejects a draft, it is recorded as `M-NNN` in `decisions/manual.md`.

Why: the first keeps the main agent sharp. The second shows, over time, where agents fail and which skills need fixing, and keeps decisions that were made "by just editing the file" visible.

## What the pipeline does not do

- It does not convert documents. Bring Markdown made by any tool; the snapshot freezes it.
- It does not replace the people who decide: architecture choices, contradictions in the source, approvals.
- It does not go past specs. Tasks, code, tests and rollout follow your own process; the IDs make it easy to link them back.

## When not to use it

A one-line change, a prototype whose requirements change daily, or a feature with no written requirements at all. The pipeline pays off when the input is long enough that things get lost, and when several people or teams need to agree on the result.
