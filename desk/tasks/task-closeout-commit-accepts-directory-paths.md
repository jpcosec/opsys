---
id: task-closeout-commit-accepts-directory-paths
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills:
- desk/contexts/pill-001-task-closure-commit.md
files:
- deskops/services/closure.py
- tests/test_closeout.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# `closeout commit` accepts a directory in --paths that contains the closing task

## Rationale

_Explain why this task exists or the business driver behind it._

Reported by sldb-04 on 2026-10-18. With `--paths desk/tasks`, `git add -A -- desk/tasks` stages the task created in this cycle. `git ls-files --error-unmatch` then reports it as tracked, so the closure runs `git rm -f` on it and adds it to the commit pathspec. `git commit -- <task>` fails with "pathspec did not match any file(s) known to git". The rollback works. Workaround: do not pass desk/tasks.

## Goal

_Describe the concrete result this task must produce._

`closeout commit --paths desk/tasks ...` closes a task that was never committed, and a task that was, with one commit and a clean tree.

## Scope

_State what is in scope and what is out of scope._

In scope: deskops/services/closure.py (decide whether the task file is tracked against HEAD with `git cat-file -e HEAD:<path>`, not against the index) and a regression test. Out of scope: other closure behavior.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Reproduce in a test with add task, advance to ritual-closeout, and `closeout commit --task T --no-run --reason x --paths desk/tasks`. 2. Replace the index-based tracked check with a HEAD-based one, and only add the task path to the commit pathspec when HEAD has it. 3. Cover both cases, a never-committed task and a committed one.

## Validation

_List the checks required before this task can close._

- PYTHONPATH=<worktree> python -m pytest tests/test_closeout.py -q
- PYTHONPATH=<worktree> python -m pytest tests -q

## Done When

_Name the observable condition that makes the task complete._

The regression test fails on the unfixed code and passes, and `pytest tests` is green.
