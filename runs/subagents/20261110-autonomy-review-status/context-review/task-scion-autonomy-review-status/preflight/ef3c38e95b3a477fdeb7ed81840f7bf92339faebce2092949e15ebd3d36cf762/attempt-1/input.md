FILE:desk/tasks/task-scion-autonomy-review-status.md
---
sldb:
  by: agent
  at: '2026-11-10T15:02:34Z'
  authority: generated
  via: save_document_payload
id: task-scion-autonomy-review-status
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- ea42ea58
- tests/test_review_command.py
- desk/atoms/workflow-model/atom-review-status-preserves-current-dispositions.md
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

Read task and routed workflow; fresh task-only and cold review. Current input identity is the existing SHA256 of exact input_data bytes via review.py _sha; keep its normalization and builders unchanged. In _state_for_key first collect all records for this key; no records means missing. Then filter records by input_sha256 equal to _sha(input_data); records exist but none match means stale, regardless of old verdict. Among matching records use existential priority: accepted > rejected > pending (state reviewed) > incomplete (state technical_failure). This matches existing lifecycle any-current-accepted semantics and does not change gates. Preserve every receipt and provenance. Add all regression scenarios to tests/test_review_command.py using its existing real isolated-desk CLI fixtures. Record atom-review-status-preserves-current-dispositions via CLI before changing docs/operator-manual.md. Hypothetical lookup of existing helpers in the named sources is implementation work, not an unresolved policy decision.

## Validation

_List the checks required before this task can close._

- pytest tests/test_review_command.py
- actual isolated review status after accepted disposition
- pytest at integration

## Done When

_Name the observable condition that makes the task complete._

Current accepted disposition survives status and older rejected/stale receipts do not mask it; input changes report stale; existing pending and technical failure contracts remain; tests and closeout evidence pass.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-scion-autonomy-review-status: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

