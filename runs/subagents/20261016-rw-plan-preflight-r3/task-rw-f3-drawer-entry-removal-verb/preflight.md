RESTATEMENT

1. Read `deskops/services/drawer.py`, `deskops/cli/parser.py`, `tests/test_inbox_promote_cli_gaps.py`, `PROVENANCE_FIELDS` in `deskops/graph/extract_edges.py:31`, and the two bound pills.
2. Confirm `DrawerService` exists with the API produced by `task-rw-f3-drawer-routing-service`; if not, stop (blocked dependency).
3. In `deskops/cli/parser.py` add a `drawer` subcommand group and a remove verb (`deskops drawer remove <selector>` — name unresolved) with a positional selector and dispatch to a CLI handler.
4. In `deskops/services/drawer.py` add a removal method on `DrawerService` that, inside one `DocTransaction`: resolves the drawer entry file from the selector, deletes the file, untracks it from the store if tracked, and rewrites `desk/drawer/tasks/Board.md` dropping every line starting with ``- `<entry-stem>` ``.
5. In that method, look up active tasks (`desk/tasks/`) whose `from_drawer` equals the entry stem and apply the owner-chosen behavior (refuse / warn / proceed) — behavior unresolved.
6. In `tests/test_inbox_promote_cli_gaps.py` add a CLI test copying the `_make_repo` / `_cli` helpers from `tests/test_lifecycle_end_to_end.py`: build repo in `tmp_path`, `git init` + seed commit, run `python -m deskops desk install <root>`, create/seed a drawer entry and Board bullets, run the verb via `subprocess.run([sys.executable, '-m', 'deskops', ...], cwd=root)`, assert the entry file is gone, its Board bullets are gone, and other bullets/headings remain.
7. Add a test case for the `from_drawer`-dangling scenario with whatever output/exit code the owner decision dictates.
8. Run `pytest tests/test_inbox_promote_cli_gaps.py`, then `pytest tests`.
9. Do not commit; report the diff for supervisor closeout.

AMBIGUITIES

1. Verb name and full CLI grammar (owner decision, listed as Open Ambiguity); cannot add the parser surface or write the test invocation without it.
2. Required behavior when an active task's `from_drawer` points at the entry — refuse, warn, or proceed silently (owner decision); determines implementation branch and test assertions.
3. Task `status: blocked` with `depends_on: task-rw-f3-drawer-routing-service`; no statement that the dependency is closed or that `DrawerService` has the needed API/signatures, so implementation may be unexecutable.
4. Selector semantics unspecified: task-id vs file stem vs path, and whether the drawer file is named `<task-id>.md`.
5. "Untracks it if tracked" has no concrete mechanism specified (which store command / SLDB API), and `DocTransaction`'s API is not given.
6. Bullet-match rule is literal ``- `<its stem>` `` — whether the stem includes `.md`, whether trailing text is required, whether indentation/heading placement matters, and what happens if `Board.md` has no matching bullet are all unspecified.
7. Whether removal should also clear or report the dangling `from_drawer` field in tasks is not stated; Done When and Validation only cover file + bullets.
8. No acceptance criteria for exit codes, stdout/stderr text, or idempotency/error behavior when the entry does not exist.
9. Only `desk/drawer/tasks/Board.md` is mentioned; whether other drawer/board files must stay untouched is not stated.
