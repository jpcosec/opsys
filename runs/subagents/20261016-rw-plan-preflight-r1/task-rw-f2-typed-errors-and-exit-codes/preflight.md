RESTATEMENT:
1. Create `deskops/errors.py` defining `DeskopsError` base carrying `exit_code`, plus subclasses `DomainError` (1), `UsageError` (2), `EnvironmentError_` (3).
2. Edit `deskops/cli/main.py`: replace the `exc.__class__.__name__` matching (≈lines 380-392) with `isinstance` dispatch on the typed errors; map SLDB `sldb`'s `SLDBStoreError` to domain (exit 1).
3. Add a global `--debug` flag in `cli/main.py`; when set, unexpected exceptions re-raise (traceback) instead of being converted to `SystemExit("Unexpected: ...")`.
4. Configure logging once in the entrypoint; delete the duplicated `_setup_logging` definition(s).
5. Edit `deskops/cli/commands/desk.py` (≈lines 149-171): a failing `stores check` or unreadable JSON must raise an environment error (exit 3), not print "Desk is up to date." with exit 0.
6. Touch `deskops/operations.py` as needed so domain failures raise typed errors rather than generic exceptions.
7. Update `tests/test_cli.py` only where an exit code intentionally changes; record each changed expectation.
8. Run: `pytest tests/test_cli.py tests/test_desk_sync.py`; then `pytest`; then `python -m deskops --debug doctor --root /tmp`.
9. Confirm no `Unexpected:` path lacks a traceback option; list each intentional exit-code change in the closeout.

AMBIGUITIES:
1. Dependency `task-rw-f2-selector-resolution-module` status unknown; not in `files`.
2. Location and number of duplicated `_setup_logging` definitions not specified.
3. Which "entrypoint" is meant (`cli/main.py` vs `__main__.py`); logging level/format/handlers unspecified.
4. Scoping of `SLDBStoreError` mapping: only `main.py` or also command modules.
5. Exit code for unexpected (non-typed) exceptions when `--debug` is not set is unspecified beyond "no `Unexpected:` without traceback option".
6. Whether `--debug` must also affect typed errors (traceback vs message), and whether it is global-only pre-subcommand.
7. `EnvironmentError_` naming/aliasing vs builtin `EnvironmentError` undefined.
8. Which F1 contract tests change, their current vs new expected exit codes, cannot be enumerated.
9. Scope says `desk update` swallow; validation references `test_desk_sync.py`/`desk sync` — exact command surface ambiguous.
10. "list each change" closeout artifact path/format unspecified.
11. Acceptance criteria for message text and for the doctor/Governance CI regressions not stated.
12. Priority when multiple typed errors could apply is unspecified.
13. Acceptance criteria for message text and for the doctor/Governance CI regressions not stated.
14. Priority when multiple typed errors could apply is unspecified.
15. `tests/test_desk_sync.py` existence not verified.
