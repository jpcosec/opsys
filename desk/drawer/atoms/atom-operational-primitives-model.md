# Operational primitives model

ID: atom-operational-primitives-model
Status: stable
Category: architecture

## What

Five primitive types (Condition, Operator, Checklist, Edge, Hook) serve as composable building blocks for artifact behaviors. Defined in spec/primitives/, they template into Concrete instances at compilation time.

## Why

Hardcoded task logic prevents reuse across artifact types. Separating conditions (predicate evaluation), checklists (completion tracking), operators (state transitions), edges (routing + gating), and hooks (side effects) allows any artifact to declare operational behavior.

## How

Each primitive spec has a template with {context} variables. The compiler resolves templates with the artifact's title, slug, task_id, and other context. Runtime classes evaluate primitives: Condition checks a predicate, Checklist verifies items, Operator applies a transition, Edge routes between nodes if a condition passes, Hook fires a side effect.

## When

When adding new operational behavior to an artifact: compose existing primitives first. If no existing primitive covers the needed behavior, write a new primitive spec.

## Where

spec/primitives/, deskops/runtime/primitives.py, deskops/specs/compiler.py

## For Whom

Developers designing artifact operational behaviors.

## Related Atoms

- atom-spec-driven-artifact-architecture, atom-routine-based-task-execution

## Materializes Into

- spec/primitives/, deskops/runtime/primitives.py

## Stabilized In

- spec/primitives/, deskops/runtime/primitives.py, tests/test_operational.py

## Distinct From

Pills provide contextual guidance. Primitives are reusable executable components that can be assembled into routines.

## Tags

- workspace:drawer
- artifact:atom
