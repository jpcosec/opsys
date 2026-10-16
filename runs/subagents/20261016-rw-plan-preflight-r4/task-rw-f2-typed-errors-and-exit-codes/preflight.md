RESTATEMENT:
1. Create `deskops/errors.py`: `DeskopsError(Exception)` carrying an `exit_code`; subclasses `DomainError` (exit 1), `UsageError` (exit 2), `DeskopsEnvironmentError` (exit 3).
2. In `deskops/cli/parser.py` `build_parser` (~line 25), add a root-only `--debug` flag; when set, also set logging level to DEBUG.
3. In `deskops/cli/main.py` `CLI.run`, store the parsed `--debug` value on the CLI instance.
4. Rewrite the exception handler in `cli/main.py` (currently ~370-392): use `isinstance` checks instead of `exc.__class__.__name__` strings; import pydantic `ValidationError` and sldb `SLDBStoreError`; keep FileNotFoundError, KeyError, ValueError, pydantic ValidationError, SLDBStoreError mapped to exit 1.
5. Make typed `DeskopsError`s print their message with no traceback and exit with their `exit_code`, regardless of `--debug`.
6. Replace the hand-written `return 2` at `cli/main.py:153`, `cli/main.py:227`, and `cli/commands/drift.py:14` with `UsageError`; handler prints the same text to the same stream those sites use today (stdout).
7. For unexpected exceptions: print `Unexpected error: <type>: <message> (rerun with --debug for the traceback)` to stderr, exit 3; with `--debug` print full traceback to stderr and still exit 3. `main()` reads `--debug` from the CLI instance.
8. In `cli/commands/desk.py` (currently ~149-171), stop swallowing a failing `stores check`; raise `DeskopsEnvironmentError` when `stores check` fails or JSON is unparseable (removing the `Desk is up to date.` / exit 0 path).
9. In `deskops/operations.py`, delete the first `_setup_logging` definition (~350, dead/self-recursive) and keep the second (~362); no other logging behavior change.
10. Add tests in `tests/test_cli.py`: injected unexpected exception → exit 3 + one-line message without `--debug`; exit 3 + traceback with `--debug`; `desk update` against a broken store → exit 3.
11. Run `pytest tests/test_cli.py tests/test_desk_sync.py`, then `pytest tests`.
12. Ensure no code path prints `Unexpected:` without the `--debug` hint; record every changed exit code in the closeout.

AMBIGUITIES:
1. `--debug` "also sets logging to DEBUG" contradicts "Logging is unchanged (already DEBUG to a file)"; unclear what the flag actually changes or which logger/handler.
2. `main()` "reads `--debug` from that instance," but if the failure happens before/outside `CLI.run` (e.g., argparse error), no instance exists; no defined fallback.
3. `DeskopsEnvironmentError` name shadows the builtin `EnvironmentError`; intended or should it differ? Base class and where `exit_code` lives (class attr vs `__init__`) unspecified.
4. Whether existing exit-1 exceptions are re-wrapped as `DomainError` or kept as direct handler mappings is not stated.
5. Typed-error output stream is specified only for `UsageError` (stdout); unspecified for `DomainError` and `DeskopsEnvironmentError` (assumed stderr).
6. With `--debug`, unclear whether the one-line `Unexpected error:` summary is also printed alongside the traceback.
7. `<type>` in the message format is not defined (class `__name__` vs qualified name; wrapped vs original type).
8. Which command in `cli/commands/desk.py` contains the swallow is not stated; the test assumes `desk update`, but the doc never confirms `update` calls `stores check`.
9. Exact expected exit codes/assertions for the new tests are not enumerated.
10. Line-number references (`cli/main.py:153`, `:227`, `drift.py:14`, `operations.py:350/362`) may not match the current tree; no acceptance criterion handles drift.
11. "List every exit code that changes in the closeout" has no specified location, format, or file.
12. `depends_on: task-rw-f2-selector-resolution-module` is unresolved (task is `deferred`); no instruction on whether it must complete first or what happens if absent.
