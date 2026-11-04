---
id: task-advance-to-closed-no-cierra-la-tarea
status: ready_for_testing
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-closeout
history:
- task_activates
- task_hands_to_closeout
references:
- tests/test_inbox_promote_cli_gaps.py
- 33fe54d7
- atom-closing-commits-are-tool-made-and-run-linked
depends_on: []
pills: []
files:
- deskops/services/tasks.py
- tests/test_inbox_promote_cli_gaps.py
task_type: code
inherits_from: []
inherit_acceptance_context: false
atoms: []
closeout_evidence:
- tests
- commit
- atom
- materialization
---

# advance --to closed no cierra la tarea

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Que deskops advance task --to closed rechace cerrar igual que --to complete y apunte a deskops closeout commit, como ya promete el help de --to.

## Scope

_State what is in scope and what is out of scope._

deskops/services/tasks.py (rama --to) y tests/test_inbox_promote_cli_gaps.py. No cambia otros valores de --to (draft, open, in_progress, blocked siguen fijando status).

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- pytest tests/test_inbox_promote_cli_gaps.py -q

## Done When

_Name the observable condition that makes the task complete._
