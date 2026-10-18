# Result Summary: task-next-guidance-without-active-task

## Changes

### `deskops/services/tasks.py` — `TasksService.next_action_report`
- When no `task_selector` is passed, reads the board task refs before `_next_task_path`.
- Zero refs returns `{"kind": "no_board_task", "board": "desk/tasks/Board.md", "suggested_commands": [...]}` with the three commands in the task-specified order.
- Multiple refs returns `{"kind": "multiple_board_tasks", "board": ..., "tasks": [{"id","status","title"}], "suggested_commands": ["deskops next <task-id> --root .", "deskops list tasks --root ."]}`.
- Single-ref and explicit-selector paths are unchanged.

### `deskops/cli/commands/operations.py` — `_print_next_action_report`
- Branches on `report["kind"]`, prints a `Next:` heading, a one-line explanation, routed task summaries for the multiple case, and one suggested command per line.
- Returns normally so the `next` command exits 0.
- Existing task report printing unchanged.

### `tests/test_cli.py`
- `test_next_without_selector_guides_when_board_routes_no_tasks`: init with empty board, asserts exit 0, guidance text/commands, and byte-identical board.
- `test_next_without_selector_lists_multiple_board_tasks`: adds two tasks, asserts exit 0, both ids listed, selector requested, suggested commands, and byte-identical board + both task files.

## Validation Commands And Results

All run with `PYTHONPATH=/tmp/rw/wt/nextguide`:

- `python -m pytest tests/test_cli.py -q` → `94 passed in 150.37s`
- `python -m pytest tests/test_closeout.py -q` → `23 passed in 6.56s`
- `python -m pytest -q` → `473 passed, 3 skipped in 849.97s`
- `python -m pytest tests -q` → `473 passed, 3 skipped in 761.30s`
- `python -m deskops next --root /tmp/rw/f0/sandbox-next` (fresh `init`) → printed `Next:`, zero-task explanation and commands, `exit=0`.

## Test Against Unfixed Code

- Temporarily restored `deskops/services/tasks.py` and `deskops/cli/commands/operations.py` from HEAD (tests kept):
  `python -m pytest tests/test_cli.py -q -k "next_without_selector"` → `2 failed, 92 deselected` (both returned exit 1 from `next`).
- Files restored afterward; `git status --short` showed only the three intended modified files.

## Task Errors / Ambiguities

- The task cites no line numbers (line-number verification not applicable).
- The task's Validation commands omit the required worktree `PYTHONPATH`; they were executed with it as instructed.
- No sldb bug encountered.
