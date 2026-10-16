RESTATEMENT:

1. Read task doc, its pills, `desk/rituals/closeout.md`, `runs/planning/deskops-rewrite-inventory.md`, and dependency `task-rw-f3-atoms-service` for closure/atoms interfaces.
2. Create `deskops/services/closure.py`: single closure routine composed over `closeout_gates` and `doc_io`; per invocation it runs gates, updates `desk/tasks/Board.md`, removes the task bundle, makes exactly one commit carrying the route's trailers, and writes one index entry.
3. Support both routes inside that service: `--run-dir <dir>` (existing trailers/index shape) and `--no-run --reason <text>` (`Closeout-Mode: manual`, `Closeout-Reason`, `run_dir: null`, `mode: manual`).
4. Rewire `deskops/cli/commands/closeout.py` so `closeout commit` calls the service; leave the `--run-dir`/`--no-run`/`--reason` CLI contract unchanged.
5. Rewire `deskops/operations.py` `advance` at the closeout node and `advance task <id> --to complete` to the chosen option (A, B, or C).
6. Update `desk/rituals/closeout.md` to name `deskops closeout commit` as the single closing entry point.
7. Run `pytest tests/test_closeout.py tests/test_lifecycle_end_to_end.py`; keep `tests/test_closeout.py` unmodified and touch `tests/test_lifecycle_end_to_end.py` only where the decision changes `advance` behavior.
8. Verify the step-4 result for each entry point: exit 0, task file and its primitives gone, task absent from `desk/tasks/Board.md`, one new commit with the route trailers, one new index line.
9. Run `pytest tests`.
10. Do not commit; hand the diff to the supervisor for the closeout commit.

AMBIGUITIES:

1. The Open Ambiguities decision (A/B/C) for what `advance` and `advance --to complete` do is unresolved, while Implementation Path step 3 and Scope require rewiring them "per the decision" — step 5 above cannot be executed.
2. `closure.py` API unspecified: function names, signatures, return type, and whether a single entry function or one per route.
3. "index entry"/"one new index line" has no stated file path or line format; only trailer/mode fields are given.
4. "Bundle removal" undefined: which artifacts (task file, primitives, linked pills?) are removed.
5. What "Board update" concretely changes in `desk/tasks/Board.md` (line shape, pills column, phase section) is not stated.
6. How "exactly one commit" is produced and verified given Resolved Decisions says the executor does not commit and the supervisor makes the closeout commit — no verification command or sandbox root is given, and AGENTS.md forbids mutating the real `desk/`.
7. Under option A or B, the required `advance` behavior on invocation is unspecified: exit code, error message text, and whether the task stays untouched.
8. Dependency `task-rw-f3-atoms-service` is not described; whether `status: blocked` must be lifted and whether its atoms surface is a prerequisite is unknown.
9. No acceptance check is given for "one entry point" beyond the prose in Done When; the doc-naming change has no test.
10. Contradiction: Resolved Decisions forbids executor commits while the task's Done When requires every entry point to produce a commit, leaving unclear whether the executor may run closing commands locally at all.
