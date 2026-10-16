RESTATEMENT:
1. Read, to confirm current behavior and stale line numbers: `deskops/cli/main.py` (~150, ~227, 370-392), `deskops/cli/parser.py` (`build_parser`, ~line 25), `deskops/cli/commands/desk.py` (149-171), `deskops/cli/commands/drift.py`, `deskops/operations.py` (345-375), `deskops/cli/commands` for existing `Unexpected:` prints, `tests/test_cli.py`, `tests/test_desk_sync.py`.
2. Create `deskops/errors.py`: `DeskopsError(Exception)` carrying `exit_code` (and message), subclasses `DomainError` (exit 1), `UsageError` (exit 2), `DeskopsEnvironmentError` (exit 3).
3. In `build_parser` (`cli/parser.py`), add a root-only `--debug` flag (`store_true`), threaded so `CLI.run` stores it on the CLI instance.
4. Rewrite the `main()` handler: replace `exc.__class__.__name__` string matching with `isinstance` checks; import pydantic `ValidationError` and SLDB `SLDBStoreError`.
5. `DeskopsError` branch: print the error message to stderr with no traceback (even under `--debug`), exit with `exc.exit_code`.
6. Keep `FileNotFoundError`, `KeyError`, `ValueError`, pydantic `ValidationError`, `SLDBStoreError` mapped to exit 1 with their current text/stream.
7. Unexpected-exception branch: print `Unexpected error: <type(exc).__name__>: <message> (rerun with --debug for the traceback)` to stderr, exit 3; under `--debug`, print full traceback to stderr first, then that same line, still exit 3.
8. In `main()`, read the `--debug` value from the CLI instance; with `--debug` also set logging to DEBUG.
9. Replace the hand-written `return 2` at `cli/main.py:153` and `:227` and `cli/commands/drift.py:14` with `raise UsageError(...)`, preserving the exact existing message text and stream (stdout).
10. In `cli/commands/desk.py`, make a failing `stores check` and unparseable JSON raise `DeskopsEnvironmentError` (exit 3) instead of printing "Desk is up to date." with exit 0.
11. In `operations.py`, delete the first `_setup_logging` definition (~line 350, dead/self-recursive) and keep the second (~362).
12. Add tests in `tests/test_cli.py`: injected unexpected exception → exit 3 + one-line message, no traceback without `--debug`; exit 3 + traceback with `--debug`; `desk update` with broken store → exit 3.
13. Run `pytest tests/test_cli.py tests/test_desk_sync.py`, then `pytest tests`.
14. Record every changed exit code for the closeout note; make no commit (supervisor commits).

AMBIGUITIES:
1. `--debug` "also sets logging to DEBUG" contradicts "Logging is unchanged (already DEBUG to a file)" — unclear what logging actually changes (file handler level, console handler, root level).
2. No mechanism is specified for injecting an unexpected exception in tests (no hook, no target given for monkeypatch).
3. `tests/test_desk_sync.py` is required by Validation but absent from `files:`; unclear whether it exists and whether the `desk update` test belongs there or in `test_cli.py`.
4. `deskops/cli/commands/drift.py` is in Scope but absent from `files:`.
5. Scope identifies the swallow only by line numbers (`desk.py:149-171`) and the command only as `desk update`; if line numbers are stale, the exact command/function is unknown.
6. If argparse fails (usage error) before a CLI instance exists, how `main()` obtains `--debug` and what stream/text is emitted is unspecified (only "argparse already uses 2").
7. Which exceptions currently map to exit 1 beyond the five named is not listed; the set of exit codes "that change" cannot be enumerated without reading `main.py`.
8. Constructor signature of the typed errors (message only vs. wrapping a cause) and exact messages for existing exit-1 mappings are unspecified.
9. It is unspecified whether all `Unexpected:` prints live in `main.py` or whether other modules must be swept for Done When's "no path prints `Unexpected:`".
10. Task `status: deferred` with `depends_on: task-rw-f2-selector-resolution-module`; whether that dependency is closed is not stated.
11. Pills are given as paths only; whether they must be read or impose exit-code/doctor-vs-desk-repair constraints is not stated.
12. Behavior when a typed error's message is empty/None is unspecified.
