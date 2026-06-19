---
id: task-add-desk-health-and-recovery-surface-deskops-slice
status: active
references:
- desk/drawer/tasks/task-add-desk-health-and-recovery-surface.md
depends_on: []
pills: []
files: []
routine: routine-task-add-desk-health-and-recovery-surface-deskops-slice
checklists:
- checklist-task-add-desk-health-and-recovery-surface-deskops-slice-execution-ready
- checklist-task-add-desk-health-and-recovery-surface-deskops-slice-testing-ready
- checklist-task-add-desk-health-and-recovery-surface-deskops-slice-closeout-ready
current_node: checklist-task-add-desk-health-and-recovery-surface-deskops-slice-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
- source:drawer
---

# Add desk health and recovery surface (deskops slice)

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Detect and repair common broken desk states safely (deskops-owned surfaces only).

## Scope

_State what is in scope and what is out of scope._

- missing or invalid `desk/` structure
- untracked modeled documents
- stale graph runtime files (`.sldb/runtime/`)
- invalid atom/task/pill documents

SLDB store health and model registration checks are routed to the sibling `sldb` repo's inbox (`20260614-000002`, `20260614-000003`). This task assumes those APIs exist and wraps them.

## Implementation Path

_Outline the expected implementation route or affected surface._

Promoted from desk/drawer/tasks/task-add-desk-health-and-recovery-surface.md.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
