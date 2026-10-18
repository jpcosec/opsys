# task-rw-f5-output-renderer — result summary

## What changed

- `deskops/cli/render.py` (new)
  - `normalize()` — dataclasses/Path/dict/list to JSON-safe values.
  - `serialize()` / `render()` — one text/json/yaml printer. JSON keeps `indent=2, default=str`; YAML uses `yaml.safe_dump(..., sort_keys=False, allow_unicode=True)`.
  - `error_envelope()` / `render_error()` — `{"ok": false, "error": {"code", "type", "message"}}` on stdout for `--format json`; text failures keep their prior text.
  - `requested_format()` — recovers `--format`/`--format=` for failures raised after argparse.
- `deskops/cli/main.py`
  - `main()` now uses `_error_parts()` and prints the JSON envelope for every post-argparse failure (DeskopsError, ValueError/ValidationError, FileNotFoundError, KeyError, SLDBStoreError, unexpected) while preserving text mode streams/prefixes.
  - Invalid `--root` uses the envelope only in json mode; argparse `SystemExit` still bypasses wrapping (stderr + exit 2).
- `deskops/cli/commands/operations.py`
  - Ported list tasks/artifacts/atoms and show task/artifact to `render()`; added `_format_task_list`, `_format_artifact_list`, `_format_task_detail`, `_format_artifact_detail`; replaced `_print_json`/`_normalize`.
  - Caught command errors now use `render_error()`.
- `deskops/cli/commands/atoms.py`
  - Ported `atoms list` and `atoms tree`; added `_format_atom_list` and `_format_tree`.
- `deskops/cli/commands/message.py`
  - Ported send/list/read/ack/inbox output to `render()`; added `_format_note_list`, `_format_note_detail`, delivery/ack text formatters. Removed the local `json` printing.
- `deskops/cli/commands/faq.py`
  - Ported FAQ index/entry to `render()`; added `_format_index`.
- `deskops/cli/commands/runtime.py`
  - Ported `runtime workers` to `render()`; added `_format_workers`.
- `tests/test_output_goldens.py`
  - Added `test_command_output_goldens`, fixture setup for a richer output repo and sender/target message repos, a fake herdr executable, output normalization, and `--update-golden` refresh.
  - Goldens cover every registered command with `--format`: all `list.*`, all `show.*`, `atoms list/show/tree`, `faq`, `inbox`, `message send/list/read/ack`, `runtime workers`, for every format each command accepts.
- `tests/fixtures/golden/output/` (new, 66 files)
  - Recorded from unmodified HEAD (a2a8c52) before porting.

## Validation

Commands run from `/tmp/rw/wt/renderer`:

```bash
PYTHONPATH=/tmp/rw/wt/renderer python -m pytest tests -q
# 418 passed, 3 skipped in 423.64s (0:07:03)

PYTHONPATH=/tmp/rw/wt/renderer python -m deskops list tasks --root . --format json
# exit=0, 276 lines of JSON

PYTHONPATH=/tmp/rw/wt/renderer python -m deskops list tasks --root .
# exit=0, 5 lines:
# task-rw-f3-single-closure-path | draft | ritual-execution
# task-rw-f5-output-renderer | draft | ritual-execution
# task-rw-f6-taskdoc-contract-cleanup | draft | ritual-execution
# task-tests-never-touch-the-real-global-store | draft | ritual-execution
# task-write-end-to-end-deskops-operator-manual | deferred | ritual-execution

PYTHONPATH=/tmp/rw/wt/renderer python -m deskops --help
# exit=0
```

Golden verification after porting:

```bash
PYTHONPATH=/tmp/rw/wt/renderer python -m pytest tests/test_output_goldens.py::test_command_output_goldens -q
# 1 passed in 51.78s
```

## Test against unfixed code

Goldens were generated from a detached worktree at HEAD (a2a8c52) with the new harness copied in:

```bash
PYTHONPATH=/tmp/rw/orig python -m pytest tests/test_output_goldens.py::test_command_output_goldens -q --update-golden
# 1 passed in 50.77s
```

The generated files were then copied to this worktree and the same test passed against the ported code.

## Task issues / ambiguities

- The cited line numbers are stale, as warned; code was located with grep.
- `Scope` says “every command that accepts `--format`”, but a command path can be invoked in several modes (e.g. `faq` index vs entry, `inbox` send vs `--list`). One golden per command path/format was recorded; `inbox` uses its default send mode, `faq` uses the index mode.
- Goldens for `message send`/`inbox` necessarily contain timestamps; the harness normalizes ISO timestamps and `YYYYMMDD-HHMMSS` note ids. It also isolates `HOME` and normalizes repo roots.
- `atoms show` is an alias that delegates to `OperationsCLI`; it is covered through `atoms_show` and `show_atom` goldens.
- No sldb bug was encountered; no sldb files were changed.
