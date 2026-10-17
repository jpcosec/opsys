---
id: task-rw-f0-closeout-amends-only-its-own-commit
status: deferred
references: []
depends_on: []
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
files:
- deskops/operations.py
- tests/test_lifecycle_end_to_end.py
task_type: implementation
tags:
- workspace:desk
- artifact:task
- source:drawer
- plan:deskops-rewrite
- phase:f0
- topic:closeout
- topic:git
---

# Closeout amends HEAD only when HEAD is the same task's closeout

## Rationale

_Explain why this task exists or the business driver behind it._

Inventory finding D2. `DeskopsOperations._auto_commit_task_closure` (deskops/operations.py:1086) decides whether to amend with `head_subject.startswith(f"closeout: {task_id}")` (line 1123), so if HEAD is `closeout: task-foo-bar`, closing `task-foo` amends the other task's commit. (Finding D1, the primitive glob that deleted another task's files, disappeared with the per-task primitives in afdec7f.)

Plan: phase F0 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

Closing a task amends HEAD only when HEAD's `Task-Id` trailer is exactly that task's id; otherwise it makes a new commit.

## Scope

_State what is in scope and what is out of scope._

In scope: the amend decision in `_auto_commit_task_closure` and one regression test. Out of scope: the commit pathspec (task-rw-f0-closeout-commit-pathspec) and untrack/rollback transactions (task-rw-f2-transactional-doc-io).

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Decide the amend from the trailer: amend only when `git log -1 --format=%(trailers:key=Task-Id,valueonly)` (stripped) equals `task_id`. The closeout commit message already carries `Task-Id: <id>` (operations.py:1115); a HEAD without that trailer never amends.
2. Test in tests/test_lifecycle_end_to_end.py: make HEAD a commit whose subject is `closeout: task-foo-bar` with trailer `Task-Id: task-foo-bar`, then close `task-foo` through the CLI and assert HEAD~1 is that commit (a new commit was created).

## Validation

_List the checks required before this task can close._

- pytest tests/test_lifecycle_end_to_end.py
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

The new test fails on the current code and passes after the fix, and `pytest tests` is green.

## Resolved Decisions

- CLI tests build a throwaway repo in pytest's `tmp_path` (git init, one empty seed commit), run `python -m deskops init <root>` (creates the store, the desk and the lifecycle graph that `advance` reads; the `lifecycle_desk` fixture in tests/conftest.py gives the same thing faster), and drive the real CLI, by default with `subprocess.run([sys.executable, '-m', 'deskops', ...], cwd=root)` (helpers `_make_repo` and `_cli` in tests/test_lifecycle_end_to_end.py); a task that says 'in-process' calls `deskops.cli.main.main([...])` with `capsys` instead. Files created in the sandbox are untracked until the test commits them. Never mutate the repo's own `desk/`.
- Create fixture tasks through the CLI so each is tracked and routed on the Board, e.g. `deskops add task --root <root> '{"id": "task-foo", "title": "Foo", "goal": "g", "scope": "s", "implementation_path": "i", "done_when": "d", "validation": ["pytest"]}'`; an explicit `id` overrides the title slug (deskops/specs/compiler.py:36). The task starts at the lifecycle node `ritual-execution`.
- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
