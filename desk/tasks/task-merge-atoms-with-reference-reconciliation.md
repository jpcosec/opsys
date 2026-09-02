---
id: task-merge-atoms-with-reference-reconciliation
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
- source:drawer
routine: routine-task-merge-atoms-with-reference-reconciliation
current_node: checklist-task-merge-atoms-with-reference-reconciliation-execution-ready
history: []
references:
- desk/drawer/tasks/task-merge-atoms-with-reference-reconciliation.md
depends_on: []
pills: []
files: []
checklists:
- checklist-task-merge-atoms-with-reference-reconciliation-execution-ready
- checklist-task-merge-atoms-with-reference-reconciliation-testing-ready
- checklist-task-merge-atoms-with-reference-reconciliation-closeout-ready
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Merge atoms with reference reconciliation

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Define and implement a merge workflow for atoms that reconciles references, provenance, and downstream materializations.

## Scope

_State what is in scope and what is out of scope._

- define `deskops atoms merge ...` contract
- reconcile inbound references from old atom ids
- preserve provenance and traceability
- add sandbox CLI tests

## Implementation Path

_Outline the expected implementation route or affected surface._

Promoted from desk/drawer/tasks/task-merge-atoms-with-reference-reconciliation.md.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
