---
id: task-rw-f0-closeout-commit-pathspec
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-rw-f0-merge-retarget-whole-tokens
pills:
- desk/contexts/pill-001-task-closure-commit.md
files:
- deskops/operations.py
- tests/test_lifecycle_end_to_end.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-rw-f0-closeout-commit-pathspec.md
---

# The advance closeout commit contains only the closing task's paths

## Rationale

_Explain why this task exists or the business driver behind it._

Inventory finding D3. The commit `_auto_commit_task_closure` makes when `deskops advance` closes a task (deskops/operations.py:1125-1128) runs `git commit -m` without a pathspec, so anything the operator had staged for other work is swept into `closeout: <task>`. Its `git rm --cached` calls (line 1113) use `check=False` and ignore failures.

Plan: phase F0 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

That commit includes exactly the removed task file, `desk/tasks/Board.md`, and those entries of the task's `files` list that have any change, new files included (`git status --porcelain -- <path>` prints something), with their working-tree content; unchanged listed paths are skipped; unrelated staged changes stay staged and out of the commit.

## Scope

_State what is in scope and what is out of scope._

In scope: the staging and commit calls in `_auto_commit_task_closure`, and one test. Out of scope: the amend rule (task-rw-f0-closeout-amends-only-its-own-commit) and `deskops closeout commit` (deskops/cli/commands/closeout.py).

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Build the path list: the removed task file, `desk/tasks/Board.md`, and each `files` entry for which `git status --porcelain -- <path>` prints something. Today the closeout `git add`s every listed file (operations.py:1104); keep that `git add -A -- <path>` for those paths only. The existing lifecycle test lists an untracked atom and test file and expects them in the commit; that must keep passing.
2. A pathspec commit records the working tree, so the task file must already be deleted when it runs: keep its bytes in memory, `git rm -- <task path>` (checked; this deletes it from disk and the index) instead of `git rm --cached`, then commit with `git commit -m <msg> -- <paths>` (or `git commit --amend --no-edit -- <paths>`). On any failure restore the task file from memory, the Board, and the index (`git restore --staged`), and raise `RuntimeError` with git's stderr. The later untrack/unlink step then only untracks.
3. Test in tests/test_lifecycle_end_to_end.py: stage an unrelated file, close a task through the CLI, assert the unrelated file is still staged (`git diff --cached --name-only`) and absent from `git show --name-only --format= HEAD`, and that HEAD's diff deletes the task file.

## Validation

_List the checks required before this task can close._

- pytest tests/test_lifecycle_end_to_end.py
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

The new test passes, the existing lifecycle test still commits the task's files, and `pytest tests` is green.

## Resolved Decisions

- CLI tests build a throwaway repo in pytest's `tmp_path` (git init, one empty seed commit), run `python -m deskops init <root>` (creates the store, the desk and the lifecycle graph that `advance` reads; the `lifecycle_desk` fixture in tests/conftest.py gives the same thing faster), and drive the real CLI, by default with `subprocess.run([sys.executable, '-m', 'deskops', ...], cwd=root)` (helpers `_make_repo` and `_cli` in tests/test_lifecycle_end_to_end.py); a task that says 'in-process' calls `deskops.cli.main.main([...])` with `capsys` instead. Files created in the sandbox are untracked until the test commits them. Never mutate the repo's own `desk/`.
- Create fixture tasks through the CLI so each is tracked and routed on the Board, e.g. `deskops add task --root <root> '{"id": "task-foo", "title": "Foo", "goal": "g", "scope": "s", "implementation_path": "i", "done_when": "d", "validation": ["pytest"]}'`; an explicit `id` overrides the title slug (deskops/specs/compiler.py:36). The task starts at the lifecycle node `ritual-execution`.
- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
