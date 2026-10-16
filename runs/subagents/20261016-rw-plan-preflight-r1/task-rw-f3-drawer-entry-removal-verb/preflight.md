RESTATEMENT:

1. Confirm the blocker is cleared: obtain the owner decision naming the verb and its behavior when an active task's `from_drawer` points at the target entry. If unresolved, stop; status is `blocked`.
2. Verify dependency `task-rw-f3-drawer-routing-service` is closed and its drawer service surface exists.
3. Read `deskops/services/drawer.py`, `deskops/cli/parser.py`, `tests/test_inbox_promote_cli_gaps.py`, and `deskops/graph/extract_edges.py` (PROVENANCE_FIELDS rule).
4. Add the new subcommand to `deskops/cli/parser.py`, matching existing drawer/CLI grammar (pill: operational-cli-grammar-follows-spoken-workflow).
5. Implement the removal function in `deskops/services/drawer.py` inside a `DocTransaction`: delete one drawer entry, untrack it if tracked, update `desk/drawer/tasks/Board.md`.
6. Apply the decided dangling-`from_drawer` policy (refuse/warn/proceed).
7. Add a CLI test in a sandbox desk (e.g. `.tmp/deskops-cli-test`).
8. Run `pytest tests/test_inbox_promote_cli_gaps.py` and `pytest`.
9. Close with the task's atomic commit.

AMBIGUITIES:

1. Verb name is undecided ("for example `deskops drawer remove <selector>`").
2. Behavior when an active task's `from_drawer` points at the entry is undecided: refuse, warn, or proceed.
3. Selector format unknown: entry id, path, slug, or index?
4. No instruction on who resolves the owner decision, when, or how to unblock the task.
5. Dependency `task-rw-f3-drawer-routing-service` status and API surface are not stated.
6. No named target function or existing API in `services/drawer.py` to extend.
7. "untracks it if tracked" — tracking mechanism (store, index, registry) unspecified.
8. Required `desk/drawer/tasks/Board.md` update format/rules unspecified.
9. No acceptance criteria for exit code, output text, or error messages.
10. No specified sandbox desk path or fixture pattern for the test.
11. Why a removal verb is tested in `tests/test_inbox_promote_cli_gaps.py` is unexplained; correct test home unstated.
12. No mention of flags (`--dry-run`, `--force`) or interactive confirmation.
13. Behavior for zero matches or multiple matches is unspecified.
14. Whether the verb must strip `from_drawer` from referencing tasks contradicts the provenance-may-dangle rule; unresolved.
15. No in-scope/out-of-scope detail for docs, atoms, or `desk/` updates.
