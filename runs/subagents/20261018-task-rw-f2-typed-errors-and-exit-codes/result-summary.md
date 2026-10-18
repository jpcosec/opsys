# task-rw-f2-typed-errors-and-exit-codes — executor result

## Changed files and functions

- `deskops/errors.py` (new): `DeskopsError` (exit 1), `DomainError` (1), `UsageError` (2), `DeskopsEnvironmentError` (3), each with class-level `exit_code`.
- `deskops/cli/main.py`
  - `CLI.debug = False` class attribute; `CLI.run` sets it from parsed `args.debug` right after `parse_args`.
  - Replaced `return 2` unknown-command paths (`run`, `_graph`) with `raise UsageError(...)`.
  - `main`: creates one `CLI`, catches `DeskopsError` first, prints to stdout for `UsageError` and stderr otherwise, returns `exc.exit_code`.
  - `ValidationError` now an `isinstance` check placed before `ValueError` (pydantic v2 `ValidationError` subclasses `ValueError`, so the old class-name branch was dead).
  - `SLDBStoreError` now an `isinstance` check.
  - Unexpected exceptions: optional `traceback.print_exc()` when `cli.debug`, then `Unexpected error: <type>: <message> (rerun with --debug for the traceback)` on stderr, exit 3.
- `deskops/cli/parser.py`: `build_parser` adds root-only `--debug` (`store_true`).
- `deskops/cli/commands/desk.py` (`DeskCLI.update`)
  - Imports `DeskopsEnvironmentError`.
  - `missing_store = not store_dir.exists()`. When the store is missing, `sldb stores check` is not run; the missing store is reported as `- Missing store: .sldb` and counts as divergence, so `--apply` creates it as before.
  - When the store exists, `stores check` JSON is parsed explicitly: unparseable non-empty stdout raises, empty stdout raises (including the subprocess exit code when non-zero). A parseable payload is used regardless of return code, so a non-zero exit with JSON remains a normal divergence report.
- `deskops/cli/commands/drift.py`: unknown drift subcommand raises `UsageError` instead of `print` + `return 2`.
- `deskops/operations.py`: deleted the first, dead, self-recursive `_setup_logging`; kept the second (now the only) definition.
- `tests/test_cli.py`: added
  - `test_unexpected_error_exits_three_with_type_and_hint`
  - `test_unexpected_error_with_debug_prints_traceback_then_the_line`
  - `test_desk_update_exits_three_when_stores_check_has_no_json` (existing store; empty stdout/127 and non-JSON stdout/1)
  - `test_desk_update_without_store_reports_divergence_and_apply_repairs` (no `.sldb`: exit 1, divergence report without "failed", then `--apply` exits 0 and `sldb stores check` returns 0).
- `tests/test_graph_cli.py`: updated `test_graph_missing_surfaces_an_import_failure_instead_of_masking_it` to the new contract (return 3, message on stderr) instead of expecting `SystemExit`.
- `tests/fixtures/golden/help/deskops.txt`: regenerated for the new `--debug` help line.

## Exit codes that changed

- Unexpected exceptions: previously uncaught `SystemExit("Unexpected: ...")` (process code 1) => now exit 3, with hint and optional traceback.
- `desk update` with an existing store that emits no parseable JSON from `sldb stores check`: previously swallowed, returned 0 or 1 => now exit 3.
- `desk update` with no `.sldb` store: unchanged from the old behavior (divergence report, exit 1; `--apply` exits 0), and it no longer runs `stores check` at all.
- Unknown command / graph subcommand / drift subcommand: still exit 2, now routed through `UsageError`; text still on stdout.
- `FileNotFoundError`, `KeyError`, `ValueError`, pydantic `ValidationError`, `SLDBStoreError`: still exit 1.

## Validation commands and final results

```bash
PYTHONPATH=/tmp/rw/wt/typederr python -m pytest tests/test_cli.py tests/test_desk_sync.py -q
# 87 passed in 51.40s

PYTHONPATH=/tmp/rw/wt/typederr python -m pytest tests -q
# 384 passed, 3 skipped in 289.76s

PYTHONPATH=/tmp/rw/wt/typederr python -m pytest tests/test_cli.py -k "desk_update" -q
# 3 passed, 82 deselected in 1.58s
```

Manual smoke checks:

```bash
rm -rf /tmp/dsk-f2-empty && mkdir -p /tmp/dsk-f2-empty
PYTHONPATH=/tmp/rw/wt/typederr python -m deskops desk update --root /tmp/dsk-f2-empty
# Desk divergence report:
# - Missing store: .sldb
# - Missing desk structure: desk/
# - Unregistered models: ...
# Run with --apply to repair these issues.
# exit=1

PYTHONPATH=/tmp/rw/wt/typederr python -m deskops desk update --root /tmp/dsk-f2-empty --apply
# apply_exit=0

PYTHONPATH=/tmp/rw/wt/typederr python -m sldb stores check --store /tmp/dsk-f2-empty/.sldb
# PASS: store integrity — 0 documents in 12 models
# check_exit=0
```

```bash
PYTHONPATH=/tmp/rw/wt/typederr python -m deskops --help
# exits 0; usage shows [--debug]
```

## Tests run against unfixed code

`/tmp/rw/f2-unfixed` created from `git archive HEAD`, with the new `tests/test_cli.py` copied in:

```bash
cd /tmp/rw/f2-unfixed && PYTHONPATH=/tmp/rw/f2-unfixed python -m pytest tests/test_cli.py \
  -k "unexpected_error_exits_three or unexpected_error_with_debug or desk_update_exits_three" -q
# 4 failed, 80 deselected in 0.82s
```

Failures: both unexpected-error tests (old code raised `SystemExit` / old parser rejected `--debug`) and both existing-store `desk update` cases (`assert 1 == 3`; old code printed the divergence report).

```bash
cd /tmp/rw/f2-unfixed && PYTHONPATH=/tmp/rw/f2-unfixed python -m pytest tests/test_cli.py \
  -k "desk_update_without_store" -q
# 1 failed, 84 deselected in 0.97s
```

Failure: old code produced the divergence report and exit 1, but had no `- Missing store: .sldb` line.

## Task notes / ambiguities / sldb

- Line numbers cited in the task had drifted: `main()` is around lines 385-427 (not 373-394), the `desk update` `stores check` block is around lines 172-199 (not 149-171), and `drift.py:14` matches.
- Scope said `--debug` "also sets logging to DEBUG" but also "Logging is unchanged (already DEBUG to a file)". Implemented the flag and traceback behavior only; logging is still DEBUG to `.deskops.log`, and no new logging setup was added.
- Full-suite greenness also required touching two files outside the task's `files` list: `tests/test_graph_cli.py` (encoded the old uncaught-`SystemExit` contract) and `tests/fixtures/golden/help/deskops.txt` (root help golden). No production scope widened.
- Supervisor review fix: a missing `.sldb` is treated as divergence, not as an environment error; exit 3 is reserved for an existing store whose `stores check` output is unusable.
- No sldb bug encountered; `sldb stores check` behaved as expected (exit 1 with empty stdout when the store is absent).
