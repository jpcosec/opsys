RESTATEMENT:
1. Create `deskops/errors.py`: `DeskopsError(Exception)` with an `exit_code` attribute; subclasses `DomainError` (1), `UsageError` (2), `DeskopsEnvironmentError` (3).
2. Edit `deskops/cli/main.py` handler (~370-392): import `pydantic`'s `ValidationError` and sldb's `SLDBStoreError`; replace `exc.__class__.__name__` string checks with `isinstance`; keep exit 1 for `FileNotFoundError`, `KeyError`, `ValueError`, `ValidationError`, `SLDBStoreError`; return `exc.exit_code` for `DeskopsError`; for anything else print `Unexpected error: <type>: <message> (rerun with --debug for the traceback)` to stderr and exit 3, and if `--debug` is set, re-raise.
3. Add a global `--debug` flag in `deskops/cli/parser.py` and thread the boolean into the main handler.
4. In `deskops/operations.py`, delete one of the two `_setup_logging` definitions and invoke logging setup exactly once from the CLI entrypoint.
5. In `deskops/cli/commands/desk.py` `desk update` (lines 149-171), stop ignoring a failing `stores check`; raise `DeskopsEnvironmentError` on a failing `stores check` or unparseable JSON instead of printing `Desk is up to date.` and exiting 0.
6. Add to `tests/test_cli.py`: injected unexpected exception → exit 3 with the stderr message; same with `--debug` → re-raise/traceback; `desk update` against a broken store → exit 3.
7. Run `pytest tests/test_cli.py tests/test_desk_sync.py`, then `pytest tests`.
8. List every changed exit code for closeout; do not commit (supervisor commits).

AMBIGUITIES:
1. `UsageError` (2) has no specified raise sites; unclear if any command/argparse path must raise it or it is define-only.
2. Unclear whether the existing exit-1 exceptions are wrapped as `DomainError` or only mapped via `isinstance` in main.py (leaving `DomainError` define-only).
3. Exit code under `--debug` is unspecified: "re-raises" yields interpreter exit 1, which contradicts environment-error 3.
4. `operations.py` defines `_setup_logging` twice; which definition to keep, and whether the "entrypoint" is `main.py` or `operations.py`, is not stated.
5. `--debug` details unspecified: whether it is strictly a global pre-subcommand flag, whether it changes logging verbosity, and how the value reaches the handler.
6. `<type>` in the unexpected-error message: unqualified class name vs fully-qualified path is unspecified.
7. How to inject the unexpected exception in the test is unspecified.
8. The exact failing call and JSON-parse location in `desk.py` `desk update` are not identified.
9. `tests/test_desk_sync.py` appears in Validation but not in `files`; unclear whether the broken-store `desk update` test belongs there or in `tests/test_cli.py`.
10. Handler scope is unclear: only command execution, or also parser/entrypoint setup errors.
11. `DeskopsEnvironmentError` collides conceptually with the builtin `EnvironmentError` (alias of `OSError`); intentional or not is unstated.
12. Done When says no path prints `Unexpected:` without the `--debug` hint, but the new message is `Unexpected error:` and `--debug` prints nothing; matching prefix/condition is ambiguous.
