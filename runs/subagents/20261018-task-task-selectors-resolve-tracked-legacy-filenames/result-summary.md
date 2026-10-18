# result summary: task-task-selectors-resolve-tracked-legacy-filenames

Done by the supervisor directly (small fix; no worker dispatched).

## What changed

- `deskops/desk_paths.py`: `resolve_selector` takes an optional `keep` predicate that filters candidates before the exact and prefix tiers.
- `deskops/operations.py`: `_resolve_artifact_selector` for `artifact.task` retries with `*.md` when `task-*.md` finds nothing, keeping only the files that `.sldb/core/documents/TaskDoc/*.yaml` tracks (`_tracked_task_paths`). Untracked markdown in desk/tasks is still ignored.
- `tests/test_cli.py`: `test_edit_task_resolves_tracked_task_with_legacy_file_name`.

## Validation

- Regression test on the unfixed code: 1 failed (`edit` exits 1). With the fix: 1 passed.
- Full suite: see validation.log.

## Reported by

graph-ui-59 (graph_ui tasks 001..006 could not be edited).
