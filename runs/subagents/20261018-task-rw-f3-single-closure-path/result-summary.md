# result summary: task-rw-f3-single-closure-path

## What changed

- `deskops/services/closure.py` (new): `ClosureService` is the one closure implementation.
  - `close_manual` and `close_with_run` implement the two fixed CLI routes.
  - `_close` runs closeout gates for a board-routed task, removes the task from `desk/tasks/Board.md`, untracks it from `.sldb`, stages the task deletion, makes exactly one commit with the route trailers (or amends HEAD only when its `Task-Id` matches), and appends the index entry.
  - `close_auto` is the legacy `_auto_commit_task_closure` compatibility hook; it delegates to the same `_close`.
  - `_gate_outcome` calls `DeskopsOperations.verify_task_closeout`.
- `deskops/cli/commands/closeout.py`: `_commit_manual` and `_commit_with_run` now delegate to `ClosureService`; argument validation and printed messages are unchanged.
- `deskops/services/tasks.py`:
  - `advance_task` refuses `--to complete` and the terminal closeout transition without writing anything; returns a blocked result whose message names both `deskops closeout commit` routes.
  - `_closure_required` builds that message.
  - `_auto_commit_task_closure` delegates to `ClosureService.close_auto`.
- `deskops/operations.py`: added the `closure` property (and `ClosureService` type import).
- `desk/rituals/closeout.md`: names `deskops closeout commit` as the one closure entry point and states `advance` does not close.
- Tests updated to close through `closeout commit`: `tests/test_lifecycle_end_to_end.py`, `tests/test_cli.py`, `tests/test_doc_io.py`, `tests/test_inbox_promote_cli_gaps.py`, `tests/e2e_agent/scenarios/first-task-to-closeout.yaml`.
- `tests/test_closeout.py` was not modified.

## Validation commands and final lines

- `PYTHONPATH=/tmp/rw/wt/closure python -m pytest tests/test_closeout.py tests/test_lifecycle_end_to_end.py -q` -> `24 passed in 40.07s`
- `PYTHONPATH=/tmp/rw/wt/closure python -m pytest tests -q` -> `404 passed, 3 skipped in 336.49s`
- Additional targeted runs while fixing: `test_closeout.py` 19 passed; `test_output_goldens.py` 6 passed; `test_cli.py` 85 passed; `test_doc_io.py` 8 passed; `test_inbox_promote_cli_gaps.py` 23 passed.

## Tests run against the unfixed code

Extracted `HEAD` into `/tmp/rw/unfixed`, copied in the modified test files, and ran with `PYTHONPATH=/tmp/rw/unfixed`:

- `test_inbox_promote_cli_gaps.py::test_forced_advance_to_complete_refuses_and_points_at_closeout` -> FAILED (old `advance --to complete` set `current_node: complete` / `status: closed`).
- `test_lifecycle_end_to_end.py::test_task_lifecycle_runs_from_intake_to_closeout_via_real_cli` -> FAILED (old `closeout commit` left `desk/tasks/task-lifecycle-e2e.md` in place).
- Result line: `2 failed in 9.07s`.

## Task issues / ambiguities found

- The task's line references are stale. `_auto_commit_task_closure` is no longer in `operations.py`; it lives in `deskops/services/tasks.py` with a delegating hook in `operations.py`.
- Gate scope is an interpretation. `closeout commit` runs `closeout verify` only when the task file exists and is routed on `desk/tasks/Board.md`. This keeps `tests/test_closeout.py` unmodified (those cases have no task file) and keeps the golden fixture tasks, which are not board-routed, working. Without this condition those existing tests would fail.
- In `tests/test_lifecycle_end_to_end.py`, the task's `files` list now names only the atom. The test file is still committed through `closeout commit --paths`; keeping the test file in `files` made the existing changed-file link gate fail because test files have no atom/materialization edge.
- No sldb bug observed. No `desk/` mutation command was run in this worktree, and nothing was staged or committed.

## Supervisor note (closeout)

- The coordinator approved the change to tests/e2e_agent/scenarios/first-task-to-closeout.yaml (consequence of decision A on `advance`).
- With this change, closing a board-routed task through `closeout commit` runs the full `closeout verify`: tests, a link for every changed file (atom/materialization or a routed follow-up), and a commit that is an ancestor of HEAD. The old `advance` close accepted any one of the three. Under "one atomic commit per task" the commit gate can only point at an earlier commit; this closeout cites the promotion commit b046c83 and covers the changed files with the routed follow-up task-docs-teach-closeout-commit-as-the-only-close. That follow-up should decide whether the commit gate keeps requiring a prior commit.
- Validation: `pytest tests` on main with the patch applied: 443 passed, 3 skipped.
