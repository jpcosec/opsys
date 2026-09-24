---
id: task-give-pilldoc-the-lifecycle-slots-its-commands-already-write
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
routine: routine-task-give-pilldoc-the-lifecycle-slots-its-commands-already-write
current_node: checklist-task-give-pilldoc-the-lifecycle-slots-its-commands-already-write-testing-ready
history:
- operator-task-give-pilldoc-the-lifecycle-slots-its-commands-already-write-activate
references: []
depends_on: []
pills: []
files: []
checklists:
- checklist-task-give-pilldoc-the-lifecycle-slots-its-commands-already-write-execution-ready
- checklist-task-give-pilldoc-the-lifecycle-slots-its-commands-already-write-testing-ready
- checklist-task-give-pilldoc-the-lifecycle-slots-its-commands-already-write-closeout-ready
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
closeout_evidence_verified: false
pill_graduation_verified: true
---

# Give PillDoc the lifecycle slots its commands already write

## Rationale

_Explain why this task exists or the business driver behind it._

desk/inbox/20260827-165024: 'deskops edit pill <id> status active' reports Updated and persists nothing, because PillDoc's template has no slot for status. The same gap hides summary, routine, current_node and history. edit pill also resolves selectors only under desk/contexts, so drawer pills are unreachable.

## Goal

_Describe the concrete result this task must produce._

PillDoc carries the lifecycle fields the pill commands read and write, so editing them persists and round-trips, and edit pill resolves pills in the drawer as well.

## Scope

_State what is in scope and what is out of scope._

deskops/models/pill.py template and fields; the pill selector path in deskops/operations.py or deskops/cli; tests. Does not change PillDoc's knowledge fields (what/why/when/where/how/how_not).

## Implementation Path

_Outline the expected implementation route or affected surface._

Add the optional lifecycle fields to PillDoc with optrev markers in the template (optional so existing documents stay valid), mirroring how TaskDoc declares status, and widen pill selector resolution to include desk/drawer/pills. Add a round-trip test and a CLI test that edit pill status persists.

## Validation

_List the checks required before this task can close._

- PYTHONPATH=$PWD python -m pytest tests/test_model_templates.py tests/test_cli.py -q

## Done When

_Name the observable condition that makes the task complete._

docs update and deskops edit pill status both persist a status on a pill under desk/contexts and under the drawer, and the store stays clean.
