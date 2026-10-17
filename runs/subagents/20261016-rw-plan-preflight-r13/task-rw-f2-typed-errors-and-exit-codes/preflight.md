RESTATEMENT:
1. Create `deskops/errors.py`: `DeskopsError(Exception)` with an `exit_code` attribute; subclasses `DomainError` (exit_code 1), `UsageError` (2), `DeskopsEnvironmentError` (3).
2. Delete the first `_setup_logging` definition in `deskops/operations.py` (line 322, dead/self-recursive); keep the second (line 334).
3. In `deskops/cli/parser.py`, `build_parser` (line 25), add a root-only `--debug` argparse flag and wire it to set logging to DEBUG.
4. Make `CLI.run` store the parsed `--debug` value on the CLI instance; make `main()` read it from that instance for exceptions raised outside `CLI.run`.
5. In `deskops/cli/main.py` main exception handler (lines ~373-394): replace `exc.__class__.__name__` string matching with `isinstance`; import pydantic `ValidationError` and sldb `SLDBStoreError`; keep exit 1 for `FileNotFoundError`, `KeyError`, `ValueError`, `ValidationError`, `SLDBStoreError`.
6. Map `DeskopsError` subclasses to their `exit_code`, printing the message to stderr with no traceback regardless of `--debug`.
7. Handle unexpected exceptions: print `Unexpected error: {type(exc).__name__}: {exc} (rerun with --debug for the traceback)` to stderr, exit 3; with `--debug`, print the traceback first, then that line, still exit 3.
8. Replace hand-written `return 2` at `deskops/cli/main.py:150-151` and `:228-229` and `deskops/cli/commands/drift.py:14` with `raise UsageError`, preserving their text and stream (stdout).
9. In `deskops/cli/commands/desk.py:149-171`, remove the swallow: raise `DeskopsEnvironmentError` when `stores check` fails or JSON is unparseable (instead of printing "Desk is up to date." and exiting 0).
10. Add tests in `tests/test_cli.py`: injected unexpected exception → exit 3, one-line message on stderr, no traceback without `--debug`; with `--debug` → traceback then the one-line message, still exit 3; `desk update` with broken store → exit 3.
11. Record every changed exit code for the closeout list.
12. Run `pytest tests/test_cli.py tests/test_desk_sync.py`, then `pytest tests`.
13. Do not commit; leave the diff for supervisor review.

AMBIGUITIES:
1. Contradiction: "typed errors print … on stderr" vs "UsageError … prints the same text to … (stdout)" — which stream applies to typed `UsageError`.
2. Not stated whether `FileNotFoundError`/`KeyError`/`ValueError`/`ValidationError`/`SLDBStoreError` become `DomainError` subclasses or stay separate `isinstance` branches; `errors.py` defines no linkage.
3. `deskops/cli/commands/drift.py` is required by Scope but missing from `files`; `tests/test_desk_sync.py` is run by Validation but also not listed — editable-file set unclear.
4. Contradiction: `--debug` "also sets logging to DEBUG" vs "Logging is unchanged (already DEBUG to a file)" — does `--debug` alter the level or not.
5. No mechanism given for how `main()` obtains the CLI instance holding `--debug` (construction site, attribute name).
6. No injection mechanism specified for the "injected unexpected exception" test (monkeypatch target, hook, env var).
7. "broken store" for the `desk update` test is undefined (failing `stores check` vs unparseable JSON).
8. Success-path output/exit for `desk update` after the change is unspecified; only the failure path is defined.
9. Exact text/stream of the sites at `main.py:150-151`, `:228-229`, `drift.py:14` is not quoted, so "same text to the same stream" is unverifiable zero-context.
10. Exit code 2 has two stream behaviors (argparse → stderr, `UsageError` → stdout); whether that split is intended is unstated.
11. "List every exit code that changes in the closeout" conflicts with Resolved Decisions (executor does not commit; supervisor does closeout) — who produces the list and where.
12. Whether `DeskopsEnvironmentError` should also subclass the builtin `EnvironmentError`/`OSError` is unstated; name collision.
13. Whether other `Unexpected:`/`SystemExit("Unexpected: ...")` sites exist outside `main.py:373-394` and must be removed for the Done When is unstated.
14. Dependency `task-rw-f2-selector-resolution-module` is `status: deferred` per sibling reference; its completion precondition cannot be verified from this document.
15. Unexpected exceptions and `DeskopsEnvironmentError` both exit 3; whether they must be distinguishable is unstated.
16. Validation omits the direct CLI run (`python -m deskops --help`, `deskops faq`) that project AGENTS.md requires for CLI changes.
