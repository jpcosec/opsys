---
id: task-make-task-lifecycle-runnable-from-intake-to-closeout
status: active
references: []
depends_on: []
pills:
- desk/contexts/pill-closeout-knowledge-gates-require-traceable-evidence.md
- desk/contexts/pill-durable-pill-knowledge-graduates-to-atoms-at-closeout.md
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
- desk/contexts/pill-cli-gaps-become-tracked-work.md
files: []
routine: routine-task-make-task-lifecycle-runnable-from-intake-to-closeout
checklists:
- checklist-task-make-task-lifecycle-runnable-from-intake-to-closeout-execution-ready
- checklist-task-make-task-lifecycle-runnable-from-intake-to-closeout-testing-ready
- checklist-task-make-task-lifecycle-runnable-from-intake-to-closeout-closeout-ready
current_node: checklist-task-make-task-lifecycle-runnable-from-intake-to-closeout-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
- source:drawer
---

# Make task lifecycle runnable from intake to closeout

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Turn the documented task lifecycle into an executable deskops path.

## Scope

_State what is in scope and what is out of scope._

- promote drawer or inbox item into task candidate
- create routed task bundle
- bind pills
- advance through execution, testing, and closeout gates
- delete closed active task artifacts
- preserve durable evidence in atoms, docs, graph relations, tests, and git

## Resolved Decisions

Supervisor rulings (the machinery mostly exists; this is dogfood + gap-fix + regression-lock):

- Deliverable: (a) an end-to-end regression test driving promote -> promote -> advance(xN) through the REAL CLI on a temp git repo + scaffolded desk, asserting final status=closed, task/routine/primitive files removed, Board unlinked, closing commit present; PLUS (b) the minimal fix so the gated path is actually traversable.
- Known blocker to fix: create_task_bundle defaults `references` to the deleted drawer source, so `closeout_evidence_verified` is False by default and closeout cannot pass without manual evidence. Decision: this is intended (operator must supply real atom/test/commit evidence) — the E2E test supplies real evidence rather than changing the default. Only touch promote.py/operations.py if a stage is genuinely broken (not merely requiring evidence).
- The E2E test MUST exercise the gated path (no `--to` bypass) to prove the contract.
- Standardize the closing mechanism on the auto-commit path (_auto_commit_task_closure); `deskops closeout commit` remains the run-evidence trailer surface.
- All mutating exploration uses a disposable desk (tmp_path / .tmp), never the real desk/.
- Route non-blocking gaps to desk/drawer/tasks/. Capture the durable 'lifecycle is CLI-runnable end-to-end' ruling as an atom.

## Implementation Path

_Outline the expected implementation route or affected surface._

New tests/test_lifecycle_end_to_end.py (real-CLI, temp git repo); minimal fixes in operations.py/promote.py only if a stage is broken; atom capture.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
