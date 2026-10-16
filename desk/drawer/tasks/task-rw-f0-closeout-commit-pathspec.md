---
id: task-rw-f0-closeout-commit-pathspec
status: deferred
references: []
depends_on:
- task-rw-f0-merge-retarget-whole-tokens
pills:
- desk/contexts/pill-001-task-closure-commit.md
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

# The advance closeout commit contains only the closing task's paths

## Rationale

_Explain why this task exists or the business driver behind it._

Inventory finding D3. The commit `_auto_commit_task_closure` makes when `deskops advance` closes a task (deskops/operations.py:1549-1552) runs `git commit -m` without a pathspec, so anything the operator had staged for other work is swept into `closeout: <task>`. Its `git rm --cached` calls (line 1537) use `check=False` and ignore failures.

Plan: phase F0 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

That commit includes exactly the removed bundle paths, `desk/tasks/Board.md`, and those entries of the task's `files` list that have any change, new files included (`git status --porcelain -- <path>` prints something), with their working-tree content; unchanged listed paths are skipped; unrelated staged changes stay staged and out of the commit.

## Scope

_State what is in scope and what is out of scope._

In scope: the staging and commit calls in `_auto_commit_task_closure`, and one test. Out of scope: the amend rule (task-rw-f0-close-only-own-primitives) and `deskops closeout commit` (deskops/cli/commands/closeout.py).

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Build the path list: removed bundle paths, `desk/tasks/Board.md`, and each `files` entry for which `git status --porcelain -- <path>` prints something. Today the closeout `git add`s every listed file (operations.py:1518); keep that `git add -A -- <path>` for those paths only. The existing lifecycle test lists an untracked atom and test file and expects them in the commit; that must keep passing.
2. Commit with `git commit -m <msg> -- <paths>` (and `git commit --amend --no-edit -- <paths>` when amending). Run `git rm --cached` with a checked return code; on failure take the existing failure branch (restore the Board, unstage, raise `RuntimeError` with git's stderr).
3. Test in tests/test_lifecycle_end_to_end.py: stage an unrelated file, close a task through the CLI, assert the unrelated file is still staged (`git diff --cached --name-only`) and absent from `git show --name-only --format= HEAD`.

## Validation

_List the checks required before this task can close._

- pytest tests/test_lifecycle_end_to_end.py
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

The new test passes, the existing lifecycle test still commits the task's files, and `pytest tests` is green.

## Resolved Decisions

- CLI tests build a throwaway repo in pytest's `tmp_path` (git init, one seed commit), run `python -m deskops desk install <root>` to scaffold `desk/`, and drive the real CLI, by default with `subprocess.run([sys.executable, '-m', 'deskops', ...], cwd=root)` (helpers `_make_repo` and `_cli` in tests/test_lifecycle_end_to_end.py); a task that says 'in-process' calls `deskops.cli.main.main([...])` with `capsys` instead. Files created in the sandbox are untracked until the test commits them. Never mutate the repo's own `desk/`.
- Create fixture tasks through the CLI so each gets its routine and primitives, e.g. `deskops add task --root <root> '{"id": "task-foo", "title": "Foo", "goal": "g", "scope": "s", "implementation_path": "i", "done_when": "d", "validation": ["pytest"]}'`; an explicit `id` overrides the title slug (deskops/specs/compiler.py:37). A raw file write leaves the task without a routine, and `advance` then exits 1.
- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
