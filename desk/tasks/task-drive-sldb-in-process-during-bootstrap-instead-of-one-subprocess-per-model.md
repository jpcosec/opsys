---
id: task-drive-sldb-in-process-during-bootstrap-instead-of-one-subprocess-per-model
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
routine: routine-task-drive-sldb-in-process-during-bootstrap-instead-of-one-subprocess-per-model
current_node: checklist-task-drive-sldb-in-process-during-bootstrap-instead-of-one-subprocess-per-model-testing-ready
history:
- operator-task-drive-sldb-in-process-during-bootstrap-instead-of-one-subprocess-per-model-activate
references: []
depends_on: []
pills: []
files: []
checklists:
- checklist-task-drive-sldb-in-process-during-bootstrap-instead-of-one-subprocess-per-model-execution-ready
- checklist-task-drive-sldb-in-process-during-bootstrap-instead-of-one-subprocess-per-model-testing-ready
- checklist-task-drive-sldb-in-process-during-bootstrap-instead-of-one-subprocess-per-model-closeout-ready
task_type: performance
inherits_from: []
inherit_acceptance_context: false
atoms: []
closeout_evidence_verified: false
pill_graduation_verified: true
---

# Drive sldb in process during bootstrap instead of one subprocess per model

## Rationale

_Explain why this task exists or the business driver behind it._

desk/drawer/issues/issue-deskops-init-spawns-one-process-per-model.md: deskops init spends ~8.5s almost entirely on interpreter start-up, one subprocess per model, and six tests pay that same cost each, together ~67s of a 114s suite.

## Goal

_Describe the concrete result this task must produce._

Bootstrap drives sldb in process when it is importable and keeps the subprocess path only as a fallback, so init and the suite drop to roughly a second.

## Scope

_State what is in scope and what is out of scope._

deskops/bootstrap.py and the tests that go through init. Keeps the existing subprocess fallback for a bootstrap environment where sldb is not yet importable.

## Implementation Path

_Outline the expected implementation route or affected surface._

Replace run_sldb calls with sldb's in-process equivalents: store creation for 'stores init', load_store_index(...).models for 'models list', and ModelCLI().add(SimpleNamespace(...)) for 'models add', the way PromoteCLI._untrack_note already calls DocCLI().untrack. Keep run_sldb as the fallback guarded by _sldb_importable. The drawer issue lists the exact call sites and the measured timings.

## Validation

_List the checks required before this task can close._

- PYTHONPATH=$PWD python -m pytest -q --durations=10

## Done When

_Name the observable condition that makes the task complete._

deskops init on a fresh directory leaves a store where sldb stores check passes, and the six tests named in the drawer issue drop below 2s each.
