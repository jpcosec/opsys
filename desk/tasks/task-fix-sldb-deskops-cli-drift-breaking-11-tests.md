---
id: task-fix-sldb-deskops-cli-drift-breaking-11-tests
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
routine: routine-task-fix-sldb-deskops-cli-drift-breaking-11-tests
current_node: complete
history: []
references: []
depends_on: []
pills: []
files: []
checklists:
- checklist-task-fix-sldb-deskops-cli-drift-breaking-11-tests-execution-ready
- checklist-task-fix-sldb-deskops-cli-drift-breaking-11-tests-testing-ready
- checklist-task-fix-sldb-deskops-cli-drift-breaking-11-tests-closeout-ready
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Fix sldb<->deskops CLI drift breaking 11 tests

## Rationale

_Explain why this task exists or the business driver behind it._

sldb moved CLI helpers to new modules; deskops still imports from sldb.cli.utils, breaking repo/inbox commands and 11 tests. This is drift between the data layer (sldb) and the workflow harness (deskops).

## Goal

_Describe the concrete result this task must produce._

Restore green deskops CLI test suite by realigning deskops to the current sldb CLI API and fixing the TaskDoc render expectation drift.

## Scope

_State what is in scope and what is out of scope._

IN: deskops/cli/commands/repo.py, deskops/cli/commands/inbox.py imports; the advance-task runtime path returning exit 2; the TaskDoc frontmatter render mismatch; add/adjust tests. OUT: changing sldb source, KGDB graph/coverage code, unrelated tasks.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Repoint imports: get_store_context now lives in sldb.cli.store_context; registered_model + resolve_model_ref now live in sldb.cli.model_utils (verify exact symbols). 2) Investigate why `advance task` returns 2 in test_cli.py (1260/1510/1620/1670) and fix root cause. 3) Fix test_composition.py TaskDoc render expectation drift (rendered no longer starts with the commented frontmatter header). 4) Fix test_add_atom_tracks_local_sldb_store (sldb resolve.py 'Unknown document target'). Run smallest scope first then full suite.

## Validation

_List the checks required before this task can close._

- cd /home/jp/proyectos/hum-ecosystem/tools/deskops && python -m pytest tests/test_cli.py -q
- cd /home/jp/proyectos/hum-ecosystem/tools/deskops && python -m pytest tests/test_composition.py -q
- cd /home/jp/proyectos/hum-ecosystem/tools/deskops && python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

cd /home/jp/proyectos/hum-ecosystem/tools/deskops && pytest is fully green (0 failed), and no sldb source files were modified.
