---
id: task-taskdoc-tags-optional-for-legacy-tasks
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
- deskops/models/task.py
- tests/test_model_templates.py
- tests/fixtures/model_contract_hashes.json
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Tasks without a `tags:` key validate again after the f6 TaskDoc contract

## Rationale

_Explain why this task exists or the business driver behind it._

Reported by graph-ui-59 on 2026-10-18. task-rw-f6-taskdoc-contract-cleanup (b4517c0) moved TaskDoc frontmatter from a free dict to explicit markers and declared `tags: ⸢rev,list•tags⸥` as required. Tasks written before that have no `tags:` key, extract as tags=None and fail validation: graph_ui desk/tasks/001..006 make `sldb stores check` and `deskops desk update` fail with "TaskDoc / tags / Input should be a valid list". Every other optional frontmatter key is already `optrev` and listed in `_ABSENT_FRONTMATTER_DEFAULTS`; `tags` was missed.

## Goal

_Describe the concrete result this task must produce._

A task file with no `tags:` key validates as tags=[], and `desk update --apply` repairs stores whose tasks predate f6.

## Scope

_State what is in scope and what is out of scope._

In scope: deskops/models/task.py (`tags` marker to `optrev,list`, add it to `_ABSENT_FRONTMATTER_DEFAULTS`), the TaskDoc hash in tests/fixtures/model_contract_hashes.json, a regression test, and re-registering TaskDoc in this repo's .sldb. Out of scope: editing other repos' stores (their owners run `desk update --apply`).

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Change the marker and the defaults set. 2. Regression test in tests/test_model_templates.py with a legacy task that has no `tags:` key. 3. Refresh the TaskDoc contract hash. 4. `sldb stores update` here. 5. Verify on a copy of UIs/graph_ui: `desk update --apply`, then `sldb stores check` PASS and `sldb edges check` OK.

## Validation

_List the checks required before this task can close._

- pytest tests/test_model_templates.py tests/test_model_contract_snapshot.py
- pytest tests
- sldb stores check --store .sldb

## Done When

_Name the observable condition that makes the task complete._

The legacy-task regression test fails on b4517c0 and passes here, a copy of graph_ui passes `stores check` after `desk update --apply`, and `pytest tests` is green.
