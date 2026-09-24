# Formalize epistemic knowledge flow (Pills to Atoms)

## Kind

feature

## Status

open

## Problem

There is ambiguity about where knowledge should live and how it graduates. Agents and operators often duplicate stable knowledge between transitionary "pills", "atoms", specific task files, and documentation. This causes knowledge drift and makes it hard for subagents to rely on a stable source of truth.

## Desired Outcome

Formalize and document the epistemic knowledge flow:
`Pills -> Atoms -> Specs/Docs -> Code -> Testing`

- **Pills**: Transient, transitionary operational context for specific task phases or subagents. Should not duplicate stable knowledge.
- **Atoms**: The stabilized, baseline truth (business rules, domain theory, patterns).
- **Specs/Docs**: Human-facing materializations derived from atoms.
- **Code/Testing**: The implementation of the specs.

Tasks must bind enough atoms and pills to enable autonomous execution with minimal hidden chat context.

## Questions

- How do we automate the "graduation" of durable knowledge from pills to atoms during task closeout?
- Should `deskops` provide a specific command to promote a pill to an atom?
- How do we audit pills to ensure they are remaining transient and not hoarding stable domain logic?

## Follow-Up Shape

- Define the epistemic model explicitly in `docs/workflow-policy-reference.md`.
- Add a closeout checklist item to review pills for atom-graduation.
- Create atoms defining this specific knowledge hierarchy.

## Related Atoms

- atom-pills-are-transient
- atom-pills-carry-transitional-task-knowledge
- atom-pills-end-as-atoms-docs-or-deletion

---

## Merged item: `define-knowledge-promotion-criteria`

#### Kind

feature

#### Status

open

#### Problem

The workflow distinguishes raw signals, inbox notes, drawer items, atoms, docs, specs, diagrams, and tasks, but it does not define criteria for promoting a signal from one layer to another.

#### Desired Outcome

Define a small promotion policy for common moves: inbox to drawer, inbox to task, drawer to atom, atom to doc/spec/diagram, and issue to active board task.

#### Questions

- What evidence is required before a conversation insight becomes an atom?
- When should an unclear item stay as an issue instead of becoming an atom?
- Who or what is allowed to promote drawer items into active board work?

#### Related Atoms

- atom-raw-signals-need-distillation-before-formalization
- atom-promotion-needs-explicit-criteria
- atom-available-tasks-are-board-routed-work
