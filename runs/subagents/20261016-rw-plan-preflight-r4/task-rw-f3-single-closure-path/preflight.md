RESTATEMENT:

1. Follow startup route: `README.md`, `docs/faq.md`, `desk/tasks/Board.md`, board-routed pills, `desk/rituals/{phase,execution,testing,closeout}.md`, atoms via `sldb find`.
2. Bind pills `pill-001-task-closure-commit`, `pill-005-subagent-execution`, `pill-closeout-knowledge-gates-require-traceable-evidence` (check `when`/`where`/`how_not`).
3. Confirm `task-rw-f3-atoms-service` is closed before starting (dependency).
4. Run execution-ritual fresh-context subagent review of this task bundle.
5. Read current closeout code: `deskops/services/` (closeout gates module), `deskops/operations.py` `_auto_commit_task_closure`, `deskops/cli/commands/closeout.py`, doc IO layer.
6. Create `deskops/services/closure.py`: single closure routine over closeout_gates + doc_io that runs gates, updates `desk/tasks/Board.md`, removes the task bundle, makes exactly one commit with route-specific trailers, writes the index entry (`run_dir: null`, `mode: manual` for the manual route), and returns exit 0.
7. Rewire `closeout commit` (`--run-dir` and `--no-run --reason`) to call `closure.py`; keep its CLI unchanged.
8. Rewire `advance` at closeout node and `advance task <id> --to complete` per the owner's decision on the Open Ambiguity.
9. Update `desk/rituals/closeout.md` to name `deskops closeout commit` as the single entry point.
10. Run `pytest tests/test_closeout.py tests/test_lifecycle_end_to_end.py`, then `pytest tests`; adjust `test_lifecycle_end_to_end.py` only where the decision changes `advance`.
11. Verify step-4 criteria per route: exit 0, task file + primitives gone, task absent from Board, one new commit with trailers, one new index line.
12. Do not commit; hand diff to supervisor for `deskops closeout commit`.

AMBIGUITIES:

1. Open Ambiguity A/B/C is undecided; step 8 (rewire `advance`) cannot be implemented without the owner's choice.
2. `depends_on: task-rw-f3-atoms-service` status unknown; whether its outputs (gates/doc_io interfaces) exist is unverifiable from the task.
3. `closeout_gates` and `doc_io` are referenced by name only; module paths, function signatures, and whether they already exist are unspecified.
4. Auto/advance route trailers are unspecified; only the manual route's `Closeout-Mode: manual` and `Closeout-Reason` are given.
5. Index file path, schema, and line format are not given.
6. "Bundle removal" does not enumerate which files/artifacts constitute the bundle (task file only, or primitives, pills, atoms too).
7. `deskops/operations.py` is listed in `files` but no step says what changes there; unclear whether `_auto_commit_task_closure` is deleted, kept as a wrapper, or replaced.
8. "Both routes" for `closeout commit` is not explicitly enumerated (`--run-dir` vs `--no-run --reason` stated elsewhere).
9. "one new commit" is ambiguous when the worktree is dirty or when multiple tasks close; no policy given for multiple commits or pre-existing uncommitted changes.
10. Gate-failure behavior (exit code, rollback of partial Board/bundle mutations, message) is unspecified.
11. Done When requires `advance` to produce the closure result while also requiring a single entry point; under decision A these are contradictory.
12. No acceptance criteria for the `desk/rituals/closeout.md` wording beyond "names one entry point".
