---
id: task-prevent-promotion-from-nesting-structured-source-sections-into-active-task-fields
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
- source:drawer
routine: routine-task-prevent-promotion-from-nesting-structured-source-sections-into-active-task-fields
current_node: checklist-task-prevent-promotion-from-nesting-structured-source-sections-into-active-task-fields-execution-ready
history: []
references:
- desk/drawer/tasks/task-prevent-promotion-from-nesting-structured-source-sections-into-active-task-fields.md
depends_on: []
pills: []
files: []
checklists:
- checklist-task-prevent-promotion-from-nesting-structured-source-sections-into-active-task-fields-execution-ready
- checklist-task-prevent-promotion-from-nesting-structured-source-sections-into-active-task-fields-testing-ready
- checklist-task-prevent-promotion-from-nesting-structured-source-sections-into-active-task-fields-closeout-ready
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Prevent promotion from nesting structured source sections into active task fields

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Keep inbox-to-drawer-to-active promotion robust when the source note already uses structured headings.

## Scope

_State what is in scope and what is out of scope._

- reproduce the nested-heading promotion case from intake notes
- decide whether normalization belongs in inbox-to-drawer rendering or drawer-to-active extraction
- preserve operator-authored active-task sections after promotion
- add focused regression coverage

## Implementation Path

_Outline the expected implementation route or affected surface._

Promoted from desk/drawer/tasks/task-prevent-promotion-from-nesting-structured-source-sections-into-active-task-fields.md.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
