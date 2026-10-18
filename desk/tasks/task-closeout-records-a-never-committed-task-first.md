---
id: task-closeout-records-a-never-committed-task-first
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

# Closing a task that never reached git first records it, so its content stays in history

## Rationale

_Explain why this task exists or the business driver behind it._

Reported by graph-ui-59 on 2026-10-18. When a task is created and closed between two commits (add task, advance three times, closeout commit), its why/goal/scope/validation/done_when never reach git. The closeout deletes the file, the closing commit carries only trailers, and runs/subagents/index.jsonl records {task_id, mode, commit: null}. Example: graph_ui 9566b01 (task-ci-de-graph-ui-en-github-actions); `git log --all -- desk/tasks/task-ci-*` is empty. AGENTS.md already asks for the task to be committed before implementation, but nothing enforces it.

## Goal

_Describe the concrete result this task must produce._

When `closeout commit`, `closeout supersede` or `closeout retire` closes a task whose file is not in HEAD, ClosureService first makes one commit that adds the task file as it is now, with subject `desk: registra <task stem>` and trailer `Task-Id: <id>`. Then it makes the usual closing commit that removes it. A task that is already committed keeps today's single closing commit.

## Scope

_State what is in scope and what is out of scope._

In scope: deskops/services/closure.py (the shared _close path), tests in tests/test_closeout.py, and one sentence in desk/rituals/closeout.md written with `deskops edit ritual ritual-closeout`. Out of scope: rewriting past history.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. In _close, before removing the task, check `git cat-file -e HEAD:<task path>`. 2. If it is absent, stage only the task file and commit it with the record subject and the Task-Id trailer. 3. Continue with the existing closing commit. 4. The amend-on-same-Task-Id logic must not fold the closing commit into the record commit, so the record commit needs a distinct trailer (for example `Closeout-Mode: record`) and the amend check must skip it. 5. Tests: a never-committed task leaves two commits, and the first one contains the task body (`git show HEAD~1:desk/tasks/<file>`). A committed task leaves one commit. Both routes leave a clean tree. The existing directory-paths test (4aada5f) must keep passing.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_closeout.py -q
- python -m pytest tests -q

## Done When

_Name the observable condition that makes the task complete._

The never-committed case leaves the task body readable in git history, the committed case is unchanged, and `pytest tests` is green.
