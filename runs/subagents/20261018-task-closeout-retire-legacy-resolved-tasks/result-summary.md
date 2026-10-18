# task-closeout-retire-legacy-resolved-tasks — execution summary

## Changes

- `deskops/services/closure.py`
  - Added `ClosureService.close_retired(task_id, *, reason, refs, paths=None, message=None)`.
    - Normalizes and requires `--reason` and at least one `--ref`.
    - Resolves every ref only through `CloseoutGatesService.reference_points_to_commit` (HEAD or ancestor commit); existing paths are rejected.
    - Reads the task with `TaskDoc`, accepts status `resolved`, `closed`, `done`, `complete` (case-insensitive, stripped), and refuses everything else. It does not rewrite status or history.
    - Calls the shared `_close` with `route="legacy-resolved"`, `run_gates=False`, trailers `Task-Id`, `Closeout-Mode: legacy-resolved`, `Closeout-Reason`, one `Closeout-Ref` per ref, and index entry `mode: "legacy-resolved"`. `_close` removes the Board route, deletes the bundle, commits, and folds the index line into the same commit (same path as `close_superseded`).
  - Updated the module docstring to list the retire route.
- `deskops/cli/commands/closeout.py`
  - Dispatch for `closeout_command == "retire"`, new `CloseoutCLI._retire`, usage text updated.
- `deskops/cli/registry.py`
  - Registered `(closeout, retire)` with `--root`, required `--task`, required `--reason`, repeatable required `--ref`, help epilog/example, `mutates=True`.
- `tests/test_closeout.py`
  - `_make_repo` now writes/commits a `.gitignore` containing `.deskops.log` (mirrors the real repo; `DeskopsOperations` opens that log file eagerly).
  - Added `_write_legacy_task`, `_commit_legacy_task_on_board`, `_retire_main`.
  - Tests: happy path for each resolved-family status (trailers, Board removal, task removal, clean tree, index `mode: legacy-resolved`, one commit), refusal of an active task with unchanged HEAD/clean tree/Board intact, refusal of unresolvable refs (`missing path`, `deadbeef`, 40 zeros, an existing non-commit path) with unchanged tree, blank reason, and missing `--ref`.
- `tests/test_command_registry.py`
  - Added `("closeout", "retire")` to `MUTATING_COMMANDS`.
- `tests/fixtures/golden/help/deskops_closeout.txt` updated and `tests/fixtures/golden/help/deskops_closeout_retire.txt` added via `--update-golden`.

No commits, no `git add`, and no desk-mutating deskops command were run. Only `deskops closeout retire --help` (read-only) was executed.

## Validation

- `PYTHONPATH=/tmp/rw/wt/retire python -m pytest tests/test_closeout.py tests/test_command_registry.py -q`
  - Final: `46 passed in 8.41s`
- `PYTHONPATH=/tmp/rw/wt/retire python -m pytest tests -q`
  - Final: `510 passed, 3 skipped in 851.57s (0:14:11)`
- `PYTHONPATH=/tmp/rw/wt/retire python -m deskops closeout retire --help`
  - Exit 0.

## Against the unfixed code

Extracted `HEAD` with `git archive` into `/tmp/rw/f0/unfixed`, copied the updated `tests/test_closeout.py`, and ran:

`PYTHONPATH=/tmp/rw/f0/unfixed python -m pytest /tmp/rw/f0/unfixed/tests/test_closeout.py -q -k retire`

Result: `11 failed, 32 deselected in 1.57s` — all retire tests fail because `closeout retire` is not a valid choice.

## Task gaps / ambiguities

- The Goal says "refuses any task whose status is not resolved", while Scope and Implementation Path define the "resolved family" as `resolved`, `closed`, `done`, `complete`. I implemented the four-value family; a task with any other status is refused.
- The Implementation Path says "do not rewrite the status"; implemented literally (no `_write_doc`, no history append, unlike `close_superseded`). The shared `_close` then deletes the task bundle, so the status survives only in the commit (the task file is removed in the same commit), as with supersede.
- The `files` frontmatter does not list `tests/fixtures/golden/help/*` or `tests/test_command_registry.py`, but Scope requires the help goldens and registry test; they were changed.
- Clean-tree assertions in the new retire tests exposed a pre-existing test-isolation defect shared by the supersede tests: `DeskopsOperations.__init__` opens `.deskops.log` in the repo, so running a single closeout test in a fresh process leaves `?? .deskops.log`. Fixed only in the test helper by committing a `.gitignore` with `.deskops.log`, matching the real repo. Running the supersede happy-path test alone now also passes.
- No sldb bug encountered.

## Desk change for the supervisor (do NOT apply from the worker)

- Field: `purpose`
- Action: append this exact sentence to the existing `purpose` text (after the supersede sentence):

`\`deskops closeout retire\` removes a task whose status is already resolved, closed, done or complete, as pre-lifecycle tasks are, without rewriting its status.`

## Supervisor note
The worker gave no ritual sentence. The supervisor added one to the closeout ritual's purpose with `deskops edit ritual ritual-closeout purpose ...`, which also exercised edit-by-id from b970352.
