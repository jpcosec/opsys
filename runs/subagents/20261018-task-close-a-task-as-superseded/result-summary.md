# task-close-a-task-as-superseded — execution summary

## Changes

- `deskops/services/closure.py`
  - Added `ClosureService.close_superseded(task_id, *, reason, refs, paths=None, message=None)`.
    - Requires a non-empty normalized reason and at least one non-empty `--ref`.
    - Resolves every ref through `CloseoutGatesService.reference_points_to_commit` (ancestor commit) or root-relative path existence.
    - Loads `TaskDoc`, sets `status: superseded`, appends `"superseded"` to `history`, and writes it via `DeskopsOperations._write_doc` before closing. Restores the original bytes if that write or the closure fails.
    - Calls the shared `_close` with `route="superseded"`, `run_gates=False`, trailers `Task-Id`, `Closeout-Mode: superseded`, `Closeout-Reason`, one `Closeout-Ref` per ref, and index entry `mode: "superseded"`.
  - Added `ClosureService._ref_resolves`.
  - Updated the module docstring to list the supersede route.
- `deskops/cli/commands/closeout.py`
  - Dispatch for `closeout_command == "supersede"`, new `CloseoutCLI._supersede`, usage text updated.
- `deskops/cli/registry.py`
  - Registered `(closeout, supersede)` with `--root`, required `--task`, required `--reason`, repeatable required `--ref`, help epilog/example, `mutates=True`.
- `desk/rituals/closeout.md`
  - Added the supersede step, purpose sentence, precondition, two validation bullets, and two failure-mode bullets.
- `tests/test_closeout.py`
  - Added `_write_board`, `_write_lifecycle_task`, `_commit_task_on_board`, `_supersede_main`.
  - Tests: commit-ref happy path (trailers, board removal, task removal, clean tree, index `mode: superseded`, one commit), existing-path ref, blank/missing reason, unresolvable refs (`missing path`, `deadbeef`, 40 zeros) with unchanged HEAD/clean tree/task intact/no index, and missing `--ref`.
- `tests/test_command_registry.py`
  - Added `("closeout", "supersede")` to `MUTATING_COMMANDS`.
- `tests/fixtures/golden/help/deskops_closeout.txt` updated and `tests/fixtures/golden/help/deskops_closeout_supersede.txt` added (required by `test_help_goldens` and `test_registry_paths_match_help_goldens`).

No commits, no `git add`, no desk-mutating deskops commands were run.

## Validation

- `PYTHONPATH=/tmp/rw/wt/supersede python -m pytest tests/test_closeout.py -q`
  - Final: `32 passed in 4.81s`
- `PYTHONPATH=/tmp/rw/wt/supersede python -m pytest tests -q`
  - Final: `480 passed, 3 skipped in 740.99s`
- Also run: `pytest tests/test_closeout.py tests/test_command_registry.py tests/test_output_goldens.py::test_help_goldens -q`
  - Final: `36 passed in 191.39s`

## Against the unfixed code

Extracted `HEAD` with `git archive` into `/tmp/rw/f0/unfixed`, copied the new `tests/test_closeout.py`, and ran:

`PYTHONPATH=/tmp/rw/f0/unfixed python -m pytest tests/test_closeout.py -q -k supersede`

Result: `9 failed, 23 deselected in 2.30s` — every supersede test failed because `closeout supersede` was not a valid choice.

## Task gaps / ambiguities

- The task says the task's `status` and `history` record `superseded`, but the shared `_close` deletes the task bundle in the same closing commit. The write happens as specified, then the file is removed, so `status`/`history` are not observable in the resulting commit or tree. I followed the Implementation Path literally (write, then shared `_close`); if the intent was to keep a superseded task file in `desk/tasks/`, `_close` needs a keep-task option, which the task did not ask for.
- Green `pytest tests` required touching files outside the task's `files` list: `deskops/cli/registry.py`, `tests/fixtures/golden/help/deskops_closeout*.txt`, and `tests/test_command_registry.py`. Without them the CLI registry/golden tests fail.
- `--reason` is declared required in argparse, so omitting the flag exits 2 (argparse) rather than 1; an empty/blank value reaches the service and exits 1 with the domain message. Tests cover both.
- No sldb bug encountered.

## Supervisor note
The worker's desk/rituals/closeout.md changes were applied in main with `deskops edit ritual closeout <field>` (purpose, preconditions, steps, validation, failure_modes) rather than from its hand edit. The task file is removed in the same commit by the shared closure, so status/history superseded show up in the commit's trailers and the index entry (mode: superseded), not in the tree.
