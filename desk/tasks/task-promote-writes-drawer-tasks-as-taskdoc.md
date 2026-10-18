---
id: task-promote-writes-drawer-tasks-as-taskdoc
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
- deskops/services/drawer.py
- tests/test_promotion_nesting.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# `promote inbox-to-drawer-task` writes the drawer task as a TaskDoc

## Rationale

_Explain why this task exists or the business driver behind it._

Found on 2026-10-18 by the faqdoc worker: `deskops promote inbox-to-drawer-task` rendered drawer tasks in a legacy hand format (`ID:`/`Status:`/`Priority:` lines, `## Source`) with no frontmatter. TaskDoc cannot read it, so tests/test_taskdoc_read_without_overlay.py fails on the repo's own drawer, `add task --from-drawer` cannot extract it, and the store cannot track it. The release drawer task created that day turned main red.

## Goal

_Describe the concrete result this task must produce._

The promoted drawer task is rendered through TaskDoc (status deferred, fields from the note's sections, source note named in `why`), so every TaskDoc reader accepts it.

## Scope

_State what is in scope and what is out of scope._

In scope: DrawerService._render_drawer_task in deskops/services/drawer.py, tests/test_promotion_nesting.py (reads fields through TaskDoc), and replacing the malformed release drawer task through the CLI. Out of scope: the inbox note format.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Build a TaskDoc payload from the parsed note sections and render it with render_model_markdown. 2. The source note is deleted on promotion, so name it in `why`, not in `references` (graph missing would flag it). 3. Adapt the nesting test to read fields through TaskDoc. 4. Run drawer remove on the malformed release task, then message send and promote again.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_inbox_promote_cli_gaps.py tests/test_lifecycle_end_to_end.py tests/test_promotion_nesting.py tests/test_taskdoc_read_without_overlay.py -q
- python -m pytest tests -q

## Done When

_Name the observable condition that makes the task complete._

Every drawer task in the repo extracts as TaskDoc, and `pytest tests` is green.
