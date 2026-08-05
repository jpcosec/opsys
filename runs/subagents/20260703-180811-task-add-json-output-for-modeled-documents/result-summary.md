# Result summary

## Scope executed
- Added `--format json` support to modeled `deskops list ...` and `deskops show ...` surfaces for tasks, routines, primitives, and generated artifact subjects.
- Kept existing text output unchanged.
- Added CLI tests that parse real command output and assert stable JSON fields.

## Changed files
- `deskops/cli/parser.py`
- `deskops/cli/commands/operations.py`
- `tests/test_cli.py`

## Validation run
- `pytest tests/test_cli.py -k 'support_json_output' -q`
- `pytest tests/test_cli.py -q`
- `python -m deskops list tasks --root . --format json`
- `python -m deskops show task task-add-json-output-for-modeled-documents --root . --format json`
- `pytest -q`

See `validation.log` for command output.

## Notes
- `deskops graph missing --root .` still reports pre-existing missing references outside this task.
- `.deskops.log` was updated by CLI execution and remains untracked.
- No files are staged.
