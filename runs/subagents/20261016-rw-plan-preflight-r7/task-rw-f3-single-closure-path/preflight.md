RESTATEMENT:

1. Confirm `task-rw-f3-atoms-service` (depends_on) is closed and that `status: blocked` can be lifted; do not start until the blocker clears.
2. Read `deskops/operations.py` `_auto_commit_task_closure`, `closeout_gates`, and `doc_io` to enumerate existing closure behavior: gate execution, Board update, bundle removal, commit + trailers, index append.
3. Read `deskops/cli/commands/closeout.py` to capture the fixed CLI surface: `--task`, `--run-dir`, `--no-run`, `--reason`, and current trailers/index writes.
4. Read `tests/test_closeout.py` and `tests/test_lifecycle_end_to_end.py` to capture current asserted behaviors for both routes.
5. Create `deskops/services/closure.py` exposing a single closure entry function built on `closeout_gates` and `doc_io` that, in order: runs closeout gates, removes the task bundle (task file + its primitives), removes the task from `desk/tasks/Board.md`, stages, creates exactly one commit with the route's trailers, and appends exactly one index line.
6. Give closure.py both routes: automated (`run_dir` set, mode `run`) and manual (`run_dir: null`, `mode: manual`, trailers `Closeout-Mode: manual`, `Closeout-Reason: <text>`).
7. Rewire `closeout commit` (both `--run-dir` and `--no-run --reason` paths) in `deskops/cli/commands/closeout.py` to call closure.py, leaving the CLI flags unchanged.
8. Rewire `advance` at the closeout node and `advance task <id> --to complete` per the owner's A/B/C decision (A: stop closing, print instruction to run `closeout commit`; B: call closure.py requiring `--run-dir`/`--no-run --reason`; C: delete `--to complete`, keep `advance` closing via closure.py).
9. Update `desk/rituals/closeout.md` to name `deskops closeout commit` as the single closing entry point.
10. Run `pytest tests/test_closeout.py tests/test_lifecycle_end_to_end.py`, allowing changes to `test_lifecycle_end_to_end.py` only where the decision changes `advance` behavior.
11. Run `pytest tests` and confirm green.
12. Verify Done When: for each remaining closing entry point, exit 0, task file and primitives gone, task absent from `desk/tasks/Board.md`, exactly one new commit with the route's trailers, exactly one new index line.
13. Do not commit; hand the diff to the supervisor for the closeout commit.

AMBIGUITIES:

1. Open Ambiguity A/B/C is unresolved. Steps 8, 9, and the meaning of "Every closing entry point" cannot be executed without the owner's choice.
2. `status: blocked` with `depends_on: task-rw-f3-atoms-service`; nothing states whether that dependency is complete or who/unblocks the status.
3. Step 2 "with both routes" is undefined: could mean `--run-dir` vs `--no-run`, or `advance` vs `closeout commit`.
4. "The route's trailers" for the automated route are never named; only the manual route's `Closeout-Mode: manual` / `Closeout-Reason` are given.
5. Index file path and line schema are not given; only `run_dir: null` and `mode: manual` are specified, and the automated route's `mode` value is unstated.
6. "Bundle removal" is undefined: what files/dirs constitute a bundle, and whether the run dir is removed.
7. `closeout_gates` and `doc_io` are referenced without module paths or function signatures.
8. Goal says closure.py performs the Board update and one commit, but Resolved Decisions say the executor does not commit and the supervisor does; which actor invokes closure.py per route is unstated.
9. `closeout commit` "with its CLI unchanged" vs Goal requiring it to now perform Board update and bundle removal — whether its observable behavior beyond flags may change is unstated.
10. No acceptance criterion for what `advance` prints/errors under option A, or exit codes for the new behavior under B.
11. "Done When ... names one entry point" conflicts with `advance` still existing as a closing path unless option A or C is chosen.
12. No instruction on where/how to run end-to-end commit tests without mutating the real `desk/` (AGENTS.md requires a sandbox desk); the task does not address this.
13. Whether `deskops advance` non-closeout phases/nodes are also to be routed through closure.py or left untouched is unstated.
14. No criterion states how "one new index line" and "one new commit" are counted or asserted in tests.
