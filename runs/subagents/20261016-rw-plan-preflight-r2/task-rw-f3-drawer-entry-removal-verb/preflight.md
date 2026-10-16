RESTATEMENT:

1. Load the pills `desk/contexts/pill-cli-gaps-become-tracked-work.md` and `desk/contexts/pill-operational-cli-grammar-follows-spoken-workflow.md`, plus `desk/rituals/execution.md` / `testing.md` / `closeout.md`.
2. Confirm `depends_on: task-rw-f3-drawer-routing-service` is closed, and obtain the owner decision on the verb name before writing code (task is `status: blocked`).
3. Read `deskops/services/drawer.py` (`DrawerService`), `deskops/cli/parser.py` (verb registration/grammar), `deskops/graph/extract_edges.py:31` (`PROVENANCE_FIELDS`), locate `DocTransaction`, and inspect the bullet format in `desk/drawer/tasks/Board.md`.
4. Register the approved verb in `deskops/cli/parser.py` with selector + root/desk-root options consistent with sibling commands.
5. Implement a `DrawerService` removal method: inside a `DocTransaction`, delete the drawer file, untrack it from the store if tracked, and rewrite `Board.md` deleting every bullet line whose prefix is ``- `<stem>` ``.
6. Add a CLI test in `tests/test_inbox_promote_cli_gaps.py` using the `_make_repo` / `_cli` pattern from `tests/test_lifecycle_end_to_end.py`: build a throwaway repo in `tmp_path` (git init + seed commit), `python -m deskops desk install <root>`, then `subprocess.run([sys.executable, '-m', 'deskops', ...], cwd=root)`.
7. Assert: target file gone, its Board.md bullets gone, unrelated bullets intact.
8. Run `pytest tests/test_inbox_promote_cli_gaps.py` and `pytest`.
9. Do not commit; leave the diff for the supervisor's closeout commit.

AMBIGUITIES:

1. Verb name/grammar is undecided (`deskops drawer remove <selector>` is only an example) — blocks parser registration and the test's command line.
2. Selector semantics undecided: stem, path, id, or slug; how it resolves to one file.
3. Behavior when an active task's `from_drawer` points at the entry (refuse / warn / silent) is undecided.
4. Whether the verb must also clear or repair the dangling `from_drawer` provenance on tasks is unspecified; the Goal lists only file + untrack + bullets.
5. "untracks it if tracked" — which store/API call and what "tracked" means is not stated.
6. Bullet match "starts with ``- `<stem>` ``" is unspecified for exact whitespace/backtick/separator, duplicate bullets, and multiple headings.
7. If the drawer file does not exist, or Board.md has no matching bullets, expected behavior/exit code is unspecified.
8. Whether removal is idempotent or errors on second run is unspecified.
9. Task is `status: blocked` and depends on an unfinished task; no instruction on proceeding.
10. `files:` lists `tests/test_inbox_promote_cli_gaps.py` as the only test artifact, but it is unclear whether to extend that file (its name references inbox-promote CLI gaps) or add a new test file.
11. No specified CLI help text, exit codes, or `--dry-run`.
12. No acceptance criteria for the CLI test beyond prose ("the file is gone, its Board bullets are gone, other bullets are intact"); no exact assertions/expected stdout defined.
