# Make deskops easy to use

## Kind

feature

## Status

open

## Problem

The model is becoming powerful but concept-heavy: SLDB, primitives, atoms, specs, materializations, rituals, drawer/inbox, diagrams, and validation all compete for first-use attention.

## Desired Outcome

Create a progressive onboarding and UX path that lets a user start, inspect available work, add knowledge, route issues, validate, and close out without understanding the entire architecture up front.

## Questions

- What is the smallest happy path command sequence?
- Which commands need `--why`, `doctor`, `next`, or guided mode support?
- What should the CLI recommend when no active board-routed task exists?

## Related Atoms

- atom-ease-of-use-requires-progressive-disclosure
- atom-available-tasks-are-board-routed-work
- atom-upstream-routing-needs-convenient-command

---

## Merged item: `make-extensibility-first-class`

#### Kind

feature

#### Status

open

#### Problem

Extensibility currently appears as scattered capabilities: tag namespaces, spec artifacts, generated CLI surfaces, diagram extension rules, and sibling tool routing. It is not yet a named contract with explicit extension points and tests.

#### Desired Outcome

Define the first-class extension points for models, fields, artifacts, primitives, materializers, CLI commands, diagrams, atom roles, and tag namespaces.

#### Questions

- Which extension points are stable public contracts?
- Which extension points are internal and allowed to change?
- What validation proves an extension does not break existing workflows?

#### Related Atoms

- atom-extensibility-is-a-contract
- atom-spec-driven-artifact-architecture
- atom-self-generating-spec-derived-cli

---

## Merged item: `deskops-cli-grammar-from-workflow-nouns`

#### Issue

The old `046-052` task set proposed a fixed noun-verb CLI over many document models, but the model has shifted: CLI nouns should come from actual workflow operations, not from every available model.

#### Core Need

Define a `deskops` CLI grammar where nouns are user-facing operational surfaces and verbs are meaningful actions over those surfaces.

#### Constraints

- Do not expose every model just because it exists.
- Preserve existing working commands until replacements are real.
- Prefer workflow-derived nouns such as task, atom, board, routine, hook, namespace, and inbox when they have clear user value.
- Avoid deprecated assumptions from the old task set: `materializes_into`, atom lifecycle `status`, atoms in drawer, and atom-to-task/pill/feature generation.

#### Follow-Up Shape

- Review current CLI commands and classify them as operational, model CRUD, or transitional.
- Define priority nouns from current workflow diagrams and atoms.
- Add parser tests for only the nouns/verbs that are intentionally exposed.

#### Tags

- system:deskops
- topic:cli
- topic:workflow-model

---

## Merged item: `add-sldb-primitives-docs-cli-component-diagram`

#### Kind

feature

#### Status

open

#### Problem

The repository had diagrams for documents/primitives and workflow surfaces, but no end-to-end component diagram showing how SLDB, models, docs, fields, primitives, materializers, specs, and CLI interact.

#### Desired Outcome

Review and stabilize `docs/diagrams/codebase/sldb-primitives-docs-cli-components.md`, then migrate it to structured spec2viz source when that workflow is ready.

#### Questions

- Are materializers correctly placed between desk surfaces and modeled SLDB docs?
- Should primitives belong only to deskops, or should some primitive abstractions move to SLDB or another reusable tool?
- Which arrows represent implemented behavior today versus target architecture?

#### Related Atoms

- atom-cli-is-thin-over-primitives-and-sldb
- atom-primitives-encode-operational-rules
- atom-deskops-owns-workflow-not-document-infrastructure
