# Create atoms from pill, graph, and diagram sources

ID: task-create-atoms-from-pill-graph-and-diagram-sources
Status: deferred
Priority: medium

## Rationale

Create-from-source atom workflows were explicitly deferred from `task-define-atom-lifecycle-operations` so the current task ships only validate/delete.

## Goal

Define and implement atom creation flows sourced from pills, graph findings, and diagrams.

## Scope

- define create-from-pill workflow
- define create-from-graph workflow
- define create-from-diagram workflow
- preserve provenance links back to each source
- add sandbox CLI tests

## Non-goals

- split operations
- merge operations

## Validation

- `pytest`
- focused CLI tests for create-from-source behavior
