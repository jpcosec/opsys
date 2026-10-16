RESTATEMENT:
1. Create `deskops/errors.py` with `DeskopsError(Exception)` carrying an `exit_code` attribute; subclasses `DomainError` (1), `UsageError` (2), `DeskopsEnvironmentError` (3).
2. Add a global `--debug` flag to the root parser in `build_parser` (`deskops/cli/parser.py:25`).
3. In `main()` (`deskops/cli/main.py`), read the flag via `'--debug' in argv` before parsing (exceptions are handled outside `CLI.run`); the flag also sets logging to DEBUG.
4. In `deskops/operations.py`: delete the first `_setup_logging` (line 350, dead/self-recursive); keep the second (line 362); do not move where logging is configured.
5. In `deskops/cli/main.py:370-392`: replace class-name string classification with `isinstance` checks; import pydantic `ValidationError` and sldb `SLDBStoreError`. Keep exit 1 for FileNotFoundError, KeyError, ValueError, pydantic ValidationError, SLDBStoreError.
6. Unexpected exception: print `Unexpected error: <type>: <message> (rerun with --debug for the traceback)` to stderr, exit 3; with `--debug`, print full traceback to stderr, still exit 3. Remove the `SystemExit("Unexpected: ...")` path.
7. Raise `UsageError` where the CLI currently returns 2 by hand: `deskops/cli/main.py:153`, `deskops/cli/main.py:227`, `deskops/cli/commands/drift.py:14`.
8. In `deskops/cli/commands/desk.py:149-171`: stop ignoring a failing `stores check`; a failing `stores check` or unparseable JSON raises `DeskopsEnvironmentError` instead of printing `Desk is up to date.` with exit 0.
9. Add tests in `tests/test_cli.py`: injected unexpected exception exits 3 without `--debug` and re-raises with `--debug`; `desk update` against a broken store exits 3.
10. Run `pytest tests/test_cli.py tests/test_desk_sync.py`, then `pytest tests`.
11. Record every exit code that changes in the closeout.

AMBIGUITIES:
1. Contradiction: Implementation Path says the injected exception "re-raises with `--debug`", but Goal/Done When say `--debug` prints a traceback and "still exits 3". Unknown which the test must assert.
2. "List every exit code that changes in the closeout" names no artifact, file, or format for that list.
3. `--debug` "also sets logging to DEBUG" while "where logging is configured does not move" — no file/function for that wiring is given, nor how it relates to the retained `_setup_logging` (operations.py:362).
4. `'--debug' in argv` is a raw string check: behavior when `--debug` is a value of another option, after `--`, or passed to a subcommand is unspecified.
5. Only unexpected exceptions define `--debug` behavior; whether typed `DomainError`/`UsageError`/`DeskopsEnvironmentError` also print tracebacks under `--debug` is unspecified.
6. The document does not enumerate all built-in exceptions currently mapped at `cli/main.py:370-392`; unknown which mappings besides the five kept at exit 1 exist and need `isinstance` conversion.
7. "Raised where the CLI returns 2 by hand today" at `cli/main.py:153` and `:227` gives no description of that existing code, so it is unknown how replacing a return-2 with a raise changes control flow.
8. Command naming: scope and tests say `desk update`, files list `deskops/cli/commands/desk.py`; the exact CLI invocation to test is not stated.
9. No acceptance criteria for `deskops/operations.py` beyond "delete the first `_setup_logging`, keep the second"; how to verify nothing references the deleted one is unspecified.
10. Unknown which existing tests assert the old `Unexpected:`/`SystemExit` messages and therefore must change.
11. `pytest tests/test_desk_sync.py` is required but the document does not state how the `desk.py` change affects it or whether it exists.
12. `depends_on: task-rw-f2-selector-resolution-module` — no information here on whether it is complete or what interface it provides.
13. The two listed pills are referenced but no binding/application criteria for them is given.
