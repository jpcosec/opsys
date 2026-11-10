---
id: task-scion-autonomy-review-status
status: deferred
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ''
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Scion autonomy: review status preserves current dispositions

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Owner authorization 2026-11-10: iterate with bots and fix DeskOps/Scion to operate
without manual prompting between normal workflow steps.

First leaf: ReviewService._state_for_key currently ignores disposed accepted and
rejected receipts, reporting technical failure/stale and provoking review loops.
Filter by current exact input hash first. Report accepted if any current accepted
receipt exists (same existential condition as lifecycle); else rejected if any
current rejected, reviewed for current pending, technical_failure for current
incomplete. With records but no current hash report stale; with no records missing.
Preserve all receipts and run provenance; change no gate, model or CLI grammar.
Capture this durable contract in an atom and reflect it in operator-manual.md.
Regression tests must use real modeled receipts/status CLI with isolated desks.

Files: deskops/services/review.py, tests/test_review_command.py, a relevant new
atom under desk/atoms/workflow-model/, docs/operator-manual.md, CHANGELOG.md.
Validation: affected pytest, actual review status before/after accepted disposition,
full pytest at integration, declared exact closeout evidence and atomic commit.

## Scope

_State what is in scope and what is out of scope._

Historical drawer source; the separately authored active task owns implementation and closeout.

## Implementation Path

_Outline the expected implementation route or affected surface._

Use the authored task implementation contract.

## Validation

_List the checks required before this task can close._

-

## Done When

_Name the observable condition that makes the task complete._

Preserve the source candidate; the authored task owns execution and closeout.
