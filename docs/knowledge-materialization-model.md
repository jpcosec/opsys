# Knowledge Materialization Model

This model describes how an ideal generic project organizes durable knowledge. It is not specific to this repository.

## Core Idea

Atoms are the internal distilled knowledge units of a project. Main docs, specs, and diagrams are different materializations of selected atoms for humans, machines, and visual reasoning.

```text
Reality / Work / Decisions
        ↓
      Atoms
        ↓
Main Docs / Specs / Diagrams
        ↓
Implementation / Tests / UX / Operations
        ↓
Feedback / Drift / New Decisions
        ↺ back into atoms
```

## Roles

| Thing | Role |
|---|---|
| Atoms | Internal distilled knowledge. Small, stable, reusable claims extracted from work, docs, decisions, code, bugs, tests, incidents, operations, and conversations. |
| Main docs | Human-facing materializations of atoms. They explain a domain, system, workflow, or product from selected atoms. |
| Specs | Formal or semi-formal materializations of atoms. They define contracts, constraints, schemas, behaviors, and expected properties. |
| Diagrams | Visual materializations of atoms, specs, and docs. They project relationships, flows, boundaries, and structures for fast comprehension. |
| Code | Executable materialization. It implements or violates the relevant atoms and specs. |
| Tests | Verification materialization. They prove that selected atoms, specs, or behaviors still hold. |
| Issues/tasks | Operational materialization. They route work when atoms, specs, docs, diagrams, code, or tests are missing, stale, or inconsistent. |

## Atoms

Atoms are not public docs. They are the distilled substrate from which durable artifacts are made.

```text
Atom != README section
Atom != spec paragraph
Atom != diagram node
Atom != task
```

Instead:

```text
README section uses atoms
Spec clause uses atoms
Diagram node/edge uses atoms
Task references atoms
Test validates atoms/specs
Code implements atoms/specs
```

An atom should answer one internal knowledge question:

- What is this system?
- Why does this boundary exist?
- How should this workflow operate?
- How not to use this API?
- When should this process run?
- Where does this responsibility belong?
- For whom is this behavior designed?

Atoms should be small, stable, reusable, internal, source-like, and free from downstream use-site tracking.

## Main Docs

Main docs are composed narratives for humans. They select atoms and arrange them into useful explanations rather than dumping atom text verbatim.

Example:

```text
Project Overview Doc
    uses atom: what the system is
    uses atom: why the system exists
    uses atom: who uses it
    uses atom: how major parts interact
    uses atom: where to start
```

## Specs

Specs are contract materializations. They are stricter than docs and define what must be true.

Example:

```text
Atom:
Tasks must pass explicit phase gates.

Spec:
Task state machine has states:
draft -> initialized -> executing -> testing -> closeout -> closed

Transitions require:
validation evidence
pill coverage
closeout commit
```

## Diagrams

Diagrams are visual projections. They explain relationships that are harder to read linearly: dependency, flow, ownership, lifecycle, boundary, hierarchy, transformation, and feedback loops.

In the ideal model:

```text
atoms/specs/docs -> diagram spec -> rendered diagram
```

The diagram source should be structured where possible, and rendered diagram files should be treated as projections.

## Generic Project Layers

```text
1. Raw signals
   conversations, bugs, tasks, commits, code review, usage, incidents

2. Distillation layer
   atoms

3. Formalization layer
   specs, schemas, contracts, state machines, policies

4. Explanation layer
   main docs, guides, READMEs, architecture docs

5. Projection layer
   diagrams, generated views, indexes, dashboards

6. Execution layer
   code, tests, CI, deployment, operations

7. Feedback layer
   issues, tasks, drift reports, inbox, review notes
```

Atoms sit between raw signals and durable artifacts. They are not the final artifact; they are the internal knowledge that makes final artifacts coherent.

## Anti-Patterns

| Anti-pattern | Why it is bad |
|---|---|
| Atom copies doc prose | Atom becomes too large and not reusable. |
| Doc invents concepts not backed by atoms | Knowledge becomes hard to trace and maintain. |
| Spec encodes behavior nobody has distilled | Formal contract becomes detached from rationale. |
| Diagram is hand-edited without source | Visual explanation drifts from docs, specs, and code. |
| Task becomes the only place a decision exists | Decision disappears when task is closed. |
| Code is updated but atoms/specs/docs are not checked | Implementation and knowledge diverge. |
| Atom tracks every use site | Atom becomes an index instead of a knowledge unit. |

## Source Atoms

- `desk/atoms/knowledge-model/atom-atoms-distill-project-knowledge.md`
- `desk/atoms/knowledge-model/atom-docs-materialize-atoms-for-humans.md`
- `desk/atoms/knowledge-model/atom-specs-formalize-atoms-as-contracts.md`
- `desk/atoms/knowledge-model/atom-diagrams-project-knowledge-relations.md`
- `desk/atoms/knowledge-model/atom-implementation-feedback-refines-atoms.md`

## Diagram

- `docs/diagrams/workflow/knowledge-materialization-model.md`
