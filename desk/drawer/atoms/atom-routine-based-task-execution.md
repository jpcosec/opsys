# Routine-based task execution

ID: atom-routine-based-task-execution
Status: stable
Category: architecture

## What

Tasks are executed through a routine: a directed graph of conditions, checklists, operators, and edges. The advance command walks the routine graph, checking preconditions (conditions), verifying completion (checklists), and applying state transitions (operators) along the edges.

## Why

Ad-hoc task advancement without phase gates leads to skipped validation, incomplete closeout, and loss of audit trail. A routine encodes the expected lifecycle as code that can be validated, visualized, and enforced.

## How

When a task is created via the spec compiler, it generates a RoutineDoc with decomposition nodes and edges. Each node is a checklist or operator. Each edge has an optional condition_ref. Advancing evaluates the current node's checklists, checks edge conditions, and if all pass, transitions to the next node via the matching operator.

## When

Use routine-based execution for any task that has defined phases, validation gates, or multi-step closeout criteria. For simple single-step tasks, a trivial routine with one node suffices.

## Where

deskops/operations.py (advance_task), deskops/runtime/primitives.py (Routine), spec/artifacts/task.yaml (routine template)

## For Whom

Operators executing tasks and developers designing task workflows.

## Related Atoms

- atom-spec-driven-artifact-architecture, atom-field-oriented-document-composition

## Materializes Into

- deskops/runtime/primitives.py, deskops/operations.py

## Stabilized In

- deskops/runtime/primitives.py, tests/test_operational.py

## Distinct From

A pill advises how to work during a session. A routine is a machine-enforceable state machine that gates task progress.

## Tags

- workspace:drawer
- artifact:atom
