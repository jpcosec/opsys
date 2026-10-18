# result-summary: task-next-why-explanation

## Changed files and functions

- `deskops/cli/registry.py` — `("next",)` command: added `--why` (`action="store_true"`, help "Explain why this task and these actions were selected.").
- `deskops/services/tasks.py` — `TasksService.next_action_report`:
  - builds `sources` once (task, board, workflow);
  - adds a `"why"` list with: selection route (`explicit selector` vs `single board route`), `current_node <node> matched workflow state <state id> in deskops/spec/workflows/task_lifecycle.yaml`, pill merge sources, and the three source paths.
- `deskops/cli/commands/operations.py`:
  - `next` handler passes `why=getattr(args, "why", False)`;
  - `_print_next_action_report(report, *, why=False)` prints the `Why:` heading and `- ` lines after pills and before `Next actions:`.
- `tests/fixtures/golden/help/deskops_next.txt` — regenerated from actual `python -m deskops next --help` (usage line now includes `[--why]`, option entry added).
- `tests/test_cli.py` — added `test_next_task_why_explains_selection_without_mutating`; asserts `Why:`, explicit-selector line, workflow spec path, `desk/tasks/Board.md`, and unchanged task file.

No commit, no `git add`, no desk mutations.

## Validation commands and results

Run with `PYTHONPATH=/tmp/rw/wt/nextwhy` as required.

- `python -m pytest tests/test_cli.py -q` → `95 passed in 104.35s (0:01:44)`
- `python -m pytest tests/test_command_registry.py -q` → `3 passed in 0.44s`
- `python -m pytest tests -q` → `485 passed, 3 skipped in 755.81s (0:12:35)`
- Extra: `python -m pytest tests/test_output_goldens.py::test_help_goldens -q` → `1 passed in 113.11s (0:01:53)`
- Extra after restoring source files: `python -m pytest tests/test_cli.py::test_next_task_why_explains_selection_without_mutating tests/test_command_registry.py -q` → `4 passed in 0.82s`

## Test against unfixed code

Procedure: reverted only the four implementation/golden files to `HEAD`, kept the new test, ran it, then restored the working files from backup.

- `python -m pytest tests/test_cli.py::test_next_task_why_explains_selection_without_mutating -q`
- Result: `FAILED ... 1 failed in 0.62s`, `assert result == 0` / `assert 2 == 0` (argparse rejected unknown `--why`, exit code 2).

## Task discrepancies / ambiguity

- `deskops/services/tasks.py` is the real `next_action_report` implementation; `deskops/operations.py` only delegates. The task listed `services/tasks.py` correctly. No cited line numbers were present in the Implementation Path.
- `deskops next --why` output was verified in a sandbox desk (`.tmp/why-check`) for both explicit-selector and single-board-route paths; both show the expected six `Why:` lines.
- Full `pytest tests` took ~12m35s in this environment, not ~3 min.
- The `Why:` source line uses state id (`execution_gate`) plus the current node; `match_workflow_state` returns the state dict, so `state["id"]` was used.

## sldb observation (not fixed)

During sandbox `init`, sldb emitted:

```
Warning: /home/jp/.sldb already links 'deskops' to /home/jp/proyectos/SLDB_1/deskops/.sldb, not to /tmp/rw/wt/nextwhy/.sldb.
Skipping model registration in /home/jp/.sldb: 'deskops' is linked elsewhere.
Global deskops model registry is ready.
Initializing local store at /tmp/rw/wt/nextwhy/.tmp/why-check/.sldb...
Linked /tmp/rw/wt/nextwhy/.sldb as deskops in /tmp/rw/wt/nextwhy/.tmp/why-check/.sldb.
```

The global registry points at the main checkout. This is an environment/global-store state issue, not a deskops code bug; no sldb change made.
