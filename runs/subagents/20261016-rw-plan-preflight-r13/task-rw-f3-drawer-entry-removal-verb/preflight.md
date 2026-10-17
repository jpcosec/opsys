RESTATEMENT:
1. Read `deskops/services/drawer.py`, `deskops/cli/parser.py`, the CLI entrypoint (`deskops/cli/main.py`), `tests/test_inbox_promote_cli_gaps.py`, `tests/test_lifecycle_end_to_end.py` (`_make_repo`, `_cli`), and `tests/conftest.py` (`lifecycle_desk`) to find `DrawerService`, `DocTransaction`, and the existing drawer-verb pattern.
2. Obtain the owner-approved verb name and dangling-provenance policy (blocked; see AMBIGUITIES 1–2); confirm dependency task `task-rw-f3-drawer-routing-service` is closed.
3. Add the subcommand to `deskops/cli/parser.py` (argument: selector), wired to the new service method.
4. Implement removal in `DrawerService` (`deskops/services/drawer.py`) inside one `DocTransaction`: resolve selector → drawer entry file; delete the file; untrack it if tracked; edit `desk/drawer/tasks/Board.md` removing every bullet line matching ``- `<stem>` — …`` and leaving all other lines byte-identical.
5. Handle the resolved dangling-provenance policy (refuse/warn/silent) when an active task's `from_drawer` equals the stem.
6. Add a CLI test in `tests/test_inbox_promote_cli_gaps.py` using `_make_repo` + subprocess `_cli` (or `lifecycle_desk`) in `tmp_path`: seed a drawer entry file, seed `desk/drawer/tasks/Board.md` with the target bullets under ≥2 headings plus an unrelated bullet, run the verb, assert file gone, target bullets gone, unrelated bullet intact.
7. Run `pytest tests/test_inbox_promote_cli_gaps.py`, then `pytest tests`; report diff to supervisor (no commit by executor).

AMBIGUITIES:
1. Verb name and full CLI grammar are undecided (owner decision), so parser wiring cannot be written.
2. Undecided: does the verb refuse, warn, or proceed silently when an active task's `from_drawer` points at the entry (and does it edit that task's `from_drawer` / the provenance edge)?
3. Task status is `blocked` on an open owner decision; no execution path is authorized yet.
4. "untracks it if tracked" — undefined: SLDB store untracking vs `git rm --cached` vs nothing.
5. "deletes every Board.md bullet" — which Board(s): only `desk/drawer/tasks/Board.md`, or also any board under `desk/drawer/`? Also unclear whether bullets in all headings (e.g. deferred/completed) are removed.
6. Selector semantics undefined: stem only, path, or any unique DrawerService selector; behavior on zero matches or multiple matches (exit code, message) unspecified.
7. Identity of `DocTransaction` module/API is not stated.
8. Undefined: whether the verb also rebuilds/validates the lifecycle graph or runs `deskops graph missing` after removing lines that may be referenced by `PROVENANCE_FIELDS`.
9. Acceptance criteria lack: exit/error behavior, output text, dry-run/confirm flag for a destructive op.
10. Test location is odd (`tests/test_inbox_promote_cli_gaps.py` covers inbox promote); unclear whether a new test file is acceptable.
11. Dependency `task-rw-f3-drawer-routing-service` state and the API it exposes are unknown.
