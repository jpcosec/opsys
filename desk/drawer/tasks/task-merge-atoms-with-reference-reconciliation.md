# Merge atoms with reference reconciliation

ID: task-merge-atoms-with-reference-reconciliation
Status: deferred
Priority: medium

## Rationale

Atom merge operations were explicitly deferred from `task-define-atom-lifecycle-operations` to avoid widening the safe CLI slice.

## Goal

Define and implement a merge workflow for atoms that reconciles references, provenance, and downstream materializations.

## Scope

- define `deskops atoms merge ...` contract
- reconcile inbound references from old atom ids
- preserve provenance and traceability
- add sandbox CLI tests

## Non-goals

- split operations
- create-from-source flows

## Validation

- `pytest`
- focused CLI tests for merge behavior
