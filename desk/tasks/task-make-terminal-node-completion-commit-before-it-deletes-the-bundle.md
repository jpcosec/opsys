---
id: task-make-terminal-node-completion-commit-before-it-deletes-the-bundle
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
routine: routine-task-make-terminal-node-completion-commit-before-it-deletes-the-bundle
current_node: checklist-task-make-terminal-node-completion-commit-before-it-deletes-the-bundle-testing-ready
history:
- operator-task-make-terminal-node-completion-commit-before-it-deletes-the-bundle-activate
references: []
depends_on: []
pills: []
files: []
checklists:
- checklist-task-make-terminal-node-completion-commit-before-it-deletes-the-bundle-execution-ready
- checklist-task-make-terminal-node-completion-commit-before-it-deletes-the-bundle-testing-ready
- checklist-task-make-terminal-node-completion-commit-before-it-deletes-the-bundle-closeout-ready
task_type: bugfix
inherits_from: []
inherit_acceptance_context: false
atoms: []
closeout_evidence_verified: false
pill_graduation_verified: true
---

# Make terminal-node completion commit before it deletes the bundle

## Rationale

_Explain why this task exists or the business driver behind it._

desk/inbox/20260907-125920: reaching the terminal node 'complete' deletes the task bundle with no atomic commit and no store cleanup first, so the work and its record can be lost in one step.

## Goal

_Describe the concrete result this task must produce._

Completing a task through the terminal node commits the closing change and untracks what it deletes from the store, and refuses to delete while the change is uncommitted.

## Scope

_State what is in scope and what is out of scope._

deskops/operations.py completion path around current_node == complete and the closeout CLI; tests. Does not redesign the closeout ritual.

## Implementation Path

_Outline the expected implementation route or affected surface._

deskops/operations.py:1038 is where completion triggers auto-commit and cleanup; make deletion of the bundle follow a recorded commit, and untrack every removed document through sldb's untrack API instead of leaving entries behind.

## Validation

_List the checks required before this task can close._

- PYTHONPATH=$PWD python -m pytest tests/test_lifecycle_end_to_end.py tests/test_cli.py -q

## Done When

_Name the observable condition that makes the task complete._

Completing a task leaves a commit that contains the closing change and a store with no dangling entries, and a failing commit leaves the bundle in place.
