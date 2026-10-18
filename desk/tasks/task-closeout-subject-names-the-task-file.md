---
id: task-closeout-subject-names-the-task-file
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- deskops/services/closure.py
- tests/test_closeout.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# The default closeout commit subject names the task file, not a bare id

## Rationale

_Explain why this task exists or the business driver behind it._

Reported by graph-ui-59 on 2026-10-18. Retiring the legacy task 001 produced the commit `closeout: 001`, so git log does not say what was closed. Tasks named task-<slug> only get a readable subject because their id is the slug.

## Goal

_Describe the concrete result this task must produce._

Without -m, every closure route (commit, supersede, retire) uses `closeout: <task file stem>`, for example `closeout: 001-define-graph-ui-data-contract`. When the stem equals the id, the subject stays as it is today. The Task-Id trailer always carries the id.

## Scope

_State what is in scope and what is out of scope._

In scope: the default subject in deskops/services/closure.py (or wherever the CLI builds it), and tests. Out of scope: the trailers.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Find where the default subject `closeout: <id>` is built. 2. Use the stem of the resolved task path. 3. Tests: a legacy task with id 001 in file 001-some-title.md is retired; assert the subject is `closeout: 001-some-title` and the trailer is `Task-Id: 001`. Add one case where the subject is unchanged.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_closeout.py -q
- python -m pytest tests -q

## Done When

_Name the observable condition that makes the task complete._

The new tests pass and `pytest tests` is green.
