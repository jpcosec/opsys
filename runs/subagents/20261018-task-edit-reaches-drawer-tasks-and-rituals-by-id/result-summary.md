# Result: task-edit-reaches-drawer-tasks-and-rituals-by-id

## Changes

### `deskops/operations.py`

- `DeskopsOperations._editable_artifact`
  - `artifact.task`: still resolves `desk/tasks/` first; on `FileNotFoundError` it now resolves against `desk/drawer/tasks/`. An active match wins.
  - `artifact.ritual`: delegates to the new `_resolve_ritual_selector`.
- `DeskopsOperations._resolve_ritual_selector` (new)
  - Keeps the existing name/stem exact-then-prefix resolution.
  - Falls back to matching the document frontmatter `id` exactly.
  - Raises `ValueError` if multiple files share that id.
- `DeskopsOperations._frontmatter_id` (new, static)
  - Reads only the leading YAML frontmatter and returns `id` or `None`.

### `tests/test_cli.py`

- Added `_write_task_doc` helper.
- Added `test_edit_task_reaches_drawer_task`: edits a task that exists only in `desk/drawer/tasks/`.
- Added `test_edit_task_prefers_active_task_over_drawer_task`: active task wins over an identically named drawer task.
- Added `test_edit_ritual_accepts_frontmatter_id`: edits a ritual by frontmatter id when its file stem differs.

## Validation

Commands run with the required worktree import path:

```
PYTHONPATH=/tmp/rw/wt/editgap python -m pytest tests/test_cli.py -q
```

Final line: `97 passed in 122.68s (0:02:02)`

```
PYTHONPATH=/tmp/rw/wt/editgap python -m pytest tests -q
```

Final line: `496 passed, 3 skipped in 853.00s (0:14:13)`

Note: the first full-suite attempt hit the tool's 600s timeout before finishing (no failure reported); the rerun above completed green.

## Unfixed-code check

With `deskops/operations.py` reverted and the new tests present:

```
2 failed, 1 passed, 94 deselected
FAILED tests/test_cli.py::test_edit_task_reaches_drawer_task
FAILED tests/test_cli.py::test_edit_ritual_accepts_frontmatter_id
```

The active-shadow test passed on unfixed code, as expected (active tasks already resolved first).

## Task discrepancies / ambiguity

- The task says drawer tasks should use "the same exact-then-prefix rule"; the implementation reuses `_resolve_artifact_selector`, which additionally preserves its existing legacy tracked-task fallback. No behavior change versus the stated rule for normal `task-*` files.
- The task suggested matching `ritual-<stem>` as one option; the implementation instead matches the real frontmatter `id`, which covers that case and any other id/stem divergence.
- No sldb bug encountered.
