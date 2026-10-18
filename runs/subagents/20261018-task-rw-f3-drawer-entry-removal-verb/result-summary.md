# Result: task-rw-f3-drawer-entry-removal-verb

## Changed

- `deskops/services/drawer.py`
  - Added `DrawerRemoval` result dataclass.
  - Added `DrawerService.remove_entry(selector, *, force=False)`: resolves the entry with `resolve_drawer_source`, refuses when a `desk/tasks/task-*.md` doc has a matching `from_drawer`, then inside `doc_io.DocTransaction` removes matching `- \`<stem>\` ` bullet lines from `desk/drawer/tasks/Board.md` and `transaction.delete(source)` (untracks when tracked, then unlinks).
  - Added `_tasks_recording(relative)` (reads task docs with `sldb.runtime.validation.extract_model_data(TaskDoc, ...)`) and `_without_entry_bullets(text, stem)`.
- `deskops/cli/parser.py`
  - Added the `drawer` command group with `drawer remove <selector> [--root] [--force]`.
- `deskops/cli/main.py`
  - Dispatches `drawer` to `DrawerCLI`.
- `deskops/cli/commands/drawer.py` (new)
  - `DrawerCLI.run` calls `DrawerService.remove_entry` and prints its messages.
- `tests/test_inbox_promote_cli_gaps.py`
  - Added 4 CLI tests: remove file + its bullets while keeping others; refusal when a task records the entry in `from_drawer` (message names the task); `--force` bypass; untracking a tracked entry from `.sldb`.
- `tests/test_cli.py`
  - Added `drawer` to the hardcoded top-level command list assertion.
- `tests/fixtures/golden/help/deskops.txt`, `deskops_drawer.txt` (new), `deskops_drawer_remove.txt` (new)
  - Regenerated/added help goldens.

## Validation (final, all green)

Run from `/tmp/rw/wt/drawerrm` with `PYTHONPATH=/tmp/rw/wt/drawerrm`.

- `python -m deskops drawer --help` / `python -m deskops drawer remove --help` - both printed usage and exited 0.
- `PYTHONPATH=/tmp/rw/wt/drawerrm python -m pytest tests/test_inbox_promote_cli_gaps.py -q` - `23 passed in 3.88s`
- `PYTHONPATH=/tmp/rw/wt/drawerrm python -m pytest tests -q` - `399 passed, 3 skipped in 334.39s (0:05:34)`
- Intermediate: `PYTHONPATH=/tmp/rw/wt/drawerrm python -m pytest tests/test_cli.py tests/test_output_goldens.py -q` - `91 passed in 148.27s (0:02:28)`

## Test against unfixed code

Before implementation:
`PYTHONPATH=/tmp/rw/wt/drawerrm python -m pytest tests/test_inbox_promote_cli_gaps.py -q -k drawer_remove`
=> `4 failed, 19 deselected in 1.25s`. All four failed because argparse rejected `drawer` (`invalid choice: 'drawer'`, exit 2).

After implementation but before refreshing goldens, full `pytest tests -q` showed 2 expected failures (`tests/test_cli.py::test_cli_help_uses_deskops_name`, `tests/test_output_goldens.py::test_help_goldens`) from the new top-level command; both were fixed by updating the command-list assertion and help goldens, then the full suite was green.

## Task issues / ambiguities

- The task's cited line numbers are stale after F2 (as expected); located code via grep.
- The task's `files` list omits `deskops/cli/commands/drawer.py` and the help goldens, which were needed for dispatch and `pytest tests` green.
- "Active task in desk/tasks/" was implemented as any `desk/tasks/task-*.md` doc, matching existing deskops usage of "active tasks" for that directory (`operations.py:2109`), not as `status == "active"` only.
- Bullet removal targets the canonical `desk/drawer/tasks/Board.md`; that file carries entries for all drawer subfolders.
- No sldb bug observed.
