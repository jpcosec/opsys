# result-summary: task-rw-f0-closeout-amends-only-its-own-commit

## What changed

### `deskops/operations.py`
- `DeskopsOperations._auto_commit_task_closure` (function starts line 1086; decide block originally lines 1117-1123, cited accurately in the task).
- Replaced the HEAD subject check (`head_subject.startswith(f"closeout: {task_id}")`) with the `Task-Id` trailer:
  - runs `git log -1 --format=%(trailers:key=Task-Id,valueonly)`
  - strips the output and amends only when it equals `task_id`
  - no trailer (or another task's trailer) now produces a new commit.

### `tests/test_lifecycle_end_to_end.py`
- Added `test_closeout_amends_only_head_with_its_own_task_id`.
- Builds a throwaway repo via `_make_repo`, runs the real CLI (`init`, `add atom`, `add task` with explicit `id: task-foo`, two `advance` calls to `ritual-closeout`), sets references/files through `deskops edit task`, creates an empty HEAD commit `closeout: task-foo-bar` with `Task-Id: task-foo-bar`, then closes `task-foo` via `deskops advance task task-foo`.
- Asserts `HEAD~1` is the `task-foo-bar` commit (new commit, no amend) and that HEAD is `closeout: task-foo` / `Task-Id: task-foo`.

## Test against unfixed code

Command:
```
PYTHONPATH=/tmp/rw/wt/amends python -m pytest tests/test_lifecycle_end_to_end.py::test_closeout_amends_only_head_with_its_own_task_id -q
```
Result on unfixed code: `1 failed in 21.91s` — `AssertionError: closing task-foo must not amend another task's closeout commit` (`HEAD~1` was the seed commit, proving the foreign commit was amended).

After the fix:
```
PYTHONPATH=/tmp/rw/wt/amends python -m pytest tests/test_lifecycle_end_to_end.py -q
....                                                                     [100%]
4 passed in 30.54s
```

## Validation commands and final results

```
PYTHONPATH=/tmp/rw/wt/amends python -m pytest tests/test_lifecycle_end_to_end.py
============================== 4 passed in 29.02s ==============================

PYTHONPATH=/tmp/rw/wt/amends python -m pytest tests -q
336 passed, 3 skipped in 176.30s (0:02:56)
```

No desk/ mutations, no commits, no `git add`.

## Deviations / ambiguities

- The first full-suite run after the code change failed one unrelated test: `tests/test_skill_cli_drift.py::test_use_deskops_copies_document_the_from_drawer_authoring_path` (`missing use-deskops skill copy: .../.pi/skills/use-deskops/SKILL.md`). `.pi/` is gitignored by design and is not present in a fresh git worktree. Copied the main checkout's `.pi/` directory into this worktree (gitignored, appears in neither diff nor commit), after which the suite is green. This is an environment gap, not related to the change.
- No discrepancies in the task's cited line numbers or implementation path.
- No sldb bugs observed; `sldb` was not exercised beyond what `init`/CLI tests already run.
