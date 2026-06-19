---
id: task-make-list-behavior-data-integrity-safe
status: active
references:
- desk/drawer/tasks/task-make-list-behavior-data-integrity-safe.md
depends_on: []
pills: []
files: []
routine: routine-task-make-list-behavior-data-integrity-safe
checklists:
- checklist-task-make-list-behavior-data-integrity-safe-execution-ready
- checklist-task-make-list-behavior-data-integrity-safe-testing-ready
- checklist-task-make-list-behavior-data-integrity-safe-closeout-ready
current_node: checklist-task-make-list-behavior-data-integrity-safe-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
- source:drawer
---

# Make list behavior data-integrity-safe

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Ensure `deskops list` commands do not silently hide malformed workflow documents.

## Scope

_State what is in scope and what is out of scope._

- `deskops list tasks`
- `deskops list routines`
- `deskops list <artifacts>`
- `deskops list <primitives>`
- invalid frontmatter and malformed model payloads

## Implementation Path

_Outline the expected implementation route or affected surface._

Promoted from desk/drawer/tasks/task-make-list-behavior-data-integrity-safe.md.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
