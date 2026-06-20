---
id: task-add-json-output-for-modeled-documents
status: active
references:
- desk/drawer/tasks/task-add-json-output-for-modeled-documents.md
depends_on: []
pills:
- desk/contexts/pill-machine-readable-cli-output-needs-stable-contract.md
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
files: []
routine: routine-task-add-json-output-for-modeled-documents
checklists:
- checklist-task-add-json-output-for-modeled-documents-execution-ready
- checklist-task-add-json-output-for-modeled-documents-testing-ready
- checklist-task-add-json-output-for-modeled-documents-closeout-ready
current_node: checklist-task-add-json-output-for-modeled-documents-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
- source:drawer
---

# Add JSON output for modeled documents

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Make modeled document `list` and `show` commands scriptable with JSON output.

## Scope

_State what is in scope and what is out of scope._

- `deskops list ... --format json`
- `deskops show ... --format json`
- modeled artifacts, tasks, routines, and primitives

## Implementation Path

_Outline the expected implementation route or affected surface._

Promoted from desk/drawer/tasks/task-add-json-output-for-modeled-documents.md.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
