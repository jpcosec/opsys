---
id: task-define-materialization-contract-slice-deskops-surface
status: active
references:
- desk/drawer/tasks/task-define-materialization-contract-slice.md
depends_on: []
pills:
- desk/contexts/pill-materialization-contracts-declare-source-intent-and-target.md
- desk/contexts/pill-atom-lifecycle-preserves-provenance-and-materialization-links.md
files: []
routine: routine-task-define-materialization-contract-slice-deskops-surface
checklists:
- checklist-task-define-materialization-contract-slice-deskops-surface-execution-ready
- checklist-task-define-materialization-contract-slice-deskops-surface-testing-ready
- checklist-task-define-materialization-contract-slice-deskops-surface-closeout-ready
current_node: checklist-task-define-materialization-contract-slice-deskops-surface-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
- source:drawer
---

# Define materialization contract slice (deskops surface)

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Implement the deskops CLI and contract definition surface for materialization.

## Scope

_State what is in scope and what is out of scope._

- source atom references
- target artifact identity/path
- materialization intent model
- validation checks
- generated/projection metadata

KGDB relation extraction for materialization is routed to the sibling `kgdb` repo's inbox. This task assumes the extraction API exists.

## Implementation Path

_Outline the expected implementation route or affected surface._

Promoted from desk/drawer/tasks/task-define-materialization-contract-slice.md.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
