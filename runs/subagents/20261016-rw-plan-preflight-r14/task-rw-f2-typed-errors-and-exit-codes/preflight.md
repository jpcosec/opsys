RESTATEMENT:

1. Read `deskops/cli/main.py` (handler at ~373-394, `return 2` sites at ~150-151, ~228-229), `deskops/cli/parser.py` (`build_parser` at ~25), `deskops/cli/commands/desk.py` (~149-171), `deskops/cli/commands/drift.py` (~14), `deskops/operations.py` (`_setup_logging` at 322 and 334), `tests/test_cli.py`, `tests/test_desk_sync.py` to confirm current behavior and line anchors.
2. Create `deskops/errors.py`: `DeskopsError(Exception)` carrying `exit_code`; `DomainError` (1); `UsageError` (2); `DeskopsEnvironmentError` (3). Messages carried as the exception text.
3. In `deskops/cli/parser.py` `build_parser`: add root-only `--debug` (argparse), and have it set logging to DEBUG.
4. In `deskops/cli/main.py`: replace `exc.__class__.__name__` string classification with `isinstance` checks; import pydantic `ValidationError` and sldb `SLDBStoreError`. Keep `FileNotFoundError`, `KeyError`, `ValueError`, pydantic `ValidationError`, `SLDBStoreError` at exit 1.
5. In `deskops/cli/main.py` handler: for `DeskopsError` subclasses print the message with no traceback (even with `--debug`) and exit with `exit_code`; for `UsageError` print to stdout (same text/stream as the replaced `return 2` sites).
6. In `deskops/cli/main.py` handler: unexpected exceptions print `Unexpected error: <type(exc).__name__>: <message> (rerun with --debug for the traceback)` to stderr, exit 3; with `--debug`, print the full traceback to stderr first, then that same line, still exit 3.
7. In `CLI.run`: store the parsed `--debug` value on the CLI instance so `main()` (which handles exceptions outside `CLI.run`) can read it.
8. Replace the three hand-written usage exits with `raise UsageError(...)`: `deskops/cli/main.py:150-151`, `deskops/cli/main.py:228-229`, `deskops/cli/commands/drift.py:14`.
9. In `deskops/cli/commands/desk.py:149-171` (`desk update`): stop ignoring the failing `stores check`; raise `DeskopsEnvironmentError` when sldb is missing or the output is not parseable JSON (a non-zero exit with JSON stays a normal divergence report, exit 0).
10. In `deskops/operations.py`: delete the first `_setup_logging` definition (~322, dead and self-recursive); keep the second (~334). Change nothing else about logging.
11. Add tests to `tests/test_cli.py`: injected unexpected exception → exit 3 + one-line stderr message, no traceback, no `--debug`; same injection with `--debug` → exit 3, traceback then the line; `desk update` with `stores check` producing no parseable JSON → exit 3.
12. Run `pytest tests/test_cli.py tests/test_desk_sync.py`, then `pytest tests`.
13. Record in the closeout the full list of exit codes that changed for every affected path.
14. Do not commit; supervisor promotes the task, reviews the diff, and runs `deskops closeout commit --task <id> --run-dir <dir>` (or `--no-run --reason <why>`) with `pytest tests` green.

AMBIGUITIES:

1. `deskops/cli/commands/drift.py` is required by Scope step "UsageError replaces … cli/commands/drift.py:14" but is absent from `files:` — which list governs edits?
2. `tests/test_desk_sync.py` appears in Validation but not in `files:`; unclear whether it may be modified or is only run.
3. "`--debug` also sets logging to DEBUG" conflicts with "Logging is unchanged (already DEBUG to a file)"; what concretely changes (console handler, root level, file level) is unspecified.
4. Mechanism for `main()` to read `--debug` "from that instance" is unspecified: whether `CLI.run` sets the attribute before dispatch, catches-then-reraises, or shares it another way.
5. If argparse itself errors (including before `--debug` is parsed), behavior is unspecified; argparse's own exit 2 path is not addressed.
6. Built-in exceptions (`FileNotFoundError`, `KeyError`, `ValueError`, `SLDBStoreError`, pydantic `ValidationError`) must exit 1, but it is unspecified whether they are wrapped into typed errors or caught directly in the handler, and what message format they print.
7. Typed-error output stream is specified only by reference to existing exit-1 mappings and by `UsageError`→stdout; which stream `DomainError`/`DeskopsEnvironmentError` use is not stated explicitly.
8. `DeskopsEnvironmentError` and unexpected exceptions both exit 3; no rule distinguishes them for tests or users.
9. In `desk update`, behavior for a non-zero exit without JSON is unstated (only "non-zero exit with JSON" and "not parseable JSON" are covered).
10. Exact wording/format of the `UsageError` message replacing each `return 2` site is not given.
11. "List every exit code that changes in the closeout" does not specify the artifact (commit message, closeout doc, or run record).
12. No acceptance criteria for the `_setup_logging` deletion beyond "dead and self-recursive"; no test or check verifies it.
13. Test naming/structure beyond "injected unexpected exception" and the `stores check` case is unspecified; whether `drift.py` and the two `main.py` usage sites need tests is not stated.
14. `depends_on: task-rw-f2-selector-resolution-module` and `status: deferred`; whether the dependency must be closed before this work starts is not stated in the task.
