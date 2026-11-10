FILE:desk/tasks/task-scion-autonomy-review-status.md
---
sldb:
  by: agent
  at: '2026-11-10T14:29:08Z'
  authority: generated
  via: create_document
id: task-scion-autonomy-review-status
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- e58ee061
- tests/test_review_command.py
depends_on: []
pills: []
files:
- deskops/services/review.py
- tests/test_review_command.py
- desk/atoms/workflow-model/atom-review-status-preserves-current-dispositions.md
- docs/operator-manual.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-scion-autonomy-review-status.md
---

# Scion autonomy: preserve current accepted review status

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Current accepted/rejected reviews are reported truthfully for the current exact input, preventing false technical failures and review loops.

## Scope

_State what is in scope and what is out of scope._

Only review status classification, its tests and atom-backed documentation; no lifecycle gates, model or CLI grammar changes. Independent runtime-readiness leaf of the autonomy repair phase.

## Implementation Path

_Outline the expected implementation route or affected surface._

Read task and routed workflow; fresh task-only and cold review; classify matching hash accepted > rejected > pending(reviewed) > incomplete(technical_failure), stale when only other inputs, missing when none. Keep all receipts. Add real isolated-desk status CLI regressions, source atom then docs.

## Validation

_List the checks required before this task can close._

- pytest tests/test_review_command.py
- actual isolated review status after accepted disposition
- pytest at integration

## Done When

_Name the observable condition that makes the task complete._

Current accepted disposition survives status and older rejected/stale receipts do not mask it; input changes report stale; existing pending and technical failure contracts remain; tests and closeout evidence pass.
