RESTATEMENT:
1. Confirm `task-rw-f3-drawer-routing-service` is closed and the blocked status is lifted by the owner decision; otherwise stop.
2. Read pills `desk/contexts/pill-cli-gaps-become-tracked-work.md` and `desk/contexts/pill-operational-cli-grammar-follows-spoken-workflow.md`; inspect `DrawerService` in `deskops/services/drawer.py` and the new subparser conventions in `deskops/cli/parser.py`.
3. Inspect `PROVENANCE_FIELDS` in `deskops/graph/extract_edges.py:31` to see how `from_drawer` is recorded/queried.
4. Add the approved verb to `deskops/cli/parser.py` (name from Open Ambiguities) with a selector argument.
5. Implement removal in `DrawerService` inside a `DocTransaction`: delete the drawer file, untrack it if tracked, and delete every `- \`<stem>\` ` bullet from `desk/drawer/tasks/Board.md`.
6. Apply the owner-chosen policy for entries still referenced by an active task's `from_drawer` (refuse / warn / proceed silently).
7. Add a CLI test in `tests/test_inbox_promote_cli_gaps.py` using the sandbox pattern (`_make_repo`, `_cli`) from `tests/test_lifecycle_end_to_end.py`: build throwaway repo in `tmp_path`, git init + seed commit, `python -m deskops desk install <root>`, create a drawer entry, run the verb, assert the file is gone, its Board bullets are gone, other bullets are intact.
8. Run `pytest tests/test_inbox_promote_cli_gaps.py`, then `pytest tests`.

AMBIGUITIES:
1. Task is `status: blocked`; no clear signal that it is unblocked or which owner decision resolved it.
2. Verb name is undefined (example `deskops drawer remove <selector>` only).
3. Refuse/warn/proceed-silently behavior on `from_drawer` references is undefined.
4. Selector semantics undefined (task id, file stem, or path).
5. "Untrack it if tracked" — tracking mechanism (`.sldb` store, sldb CLI, graph edges) unspecified.
6. `DocTransaction` import path/API not stated.
7. Board.md has "several headings"; which sections are searched and whether bullets in non-drawer sections are touched is unspecified.
8. Whether dangling `from_drawer` provenance in other tasks is fixed or left dangling is unspecified.
9. Expected CLI exit codes and output text are unspecified.
10. "Other bullets are intact" has no enumerated acceptance set.
11. Helpers `_make_repo`/`_cli` live in `tests/test_lifecycle_end_to_end.py` but the listed test file is `tests/test_inbox_promote_cli_gaps.py`; import/reuse approach unspecified.
12. Whether removal also updates `desk/` board pills, drawer Board index, or graph snapshots is unspecified.
13. No acceptance criterion for the case where the drawer file does not exist or the selector matches nothing.
14. Definition of "tracked" and whether untracking requires a separate sldb operation/commit is unspecified.
