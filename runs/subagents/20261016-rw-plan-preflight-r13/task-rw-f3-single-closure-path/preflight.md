RESTATEMENT:

1. Confirm dependency `task-rw-f3-atoms-service` is closed; task is `status: blocked`, so do not start implementation until that clears.
2. Read bound pills: `desk/contexts/pill-001-task-closure-commit.md`, `desk/contexts/pill-005-subagent-execution.md`, `desk/contexts/pill-closeout-knowledge-gates-require-traceable-evidence.md`; plus `desk/rituals/closeout.md` and `runs/planning/deskops-rewrite-inventory.md` (S1 finding, phase F3).
3. Inspect current closure paths: `_auto_commit_task_closure` (called from `deskops advance` at closeout node), `advance task <id> --to complete`, and `deskops/cli/commands/closeout.py`.
4. Create `deskops/services/closure.py` exposing one closure entry point that, in order: runs closeout gates (`closeout_gates`), updates `desk/tasks/Board.md` (removes task), removes the task bundle, makes exactly one commit carrying the route's trailers, and writes one index line.
5. Wire two routes into that service: `--run-dir <dir>` (run-based) and `--no-run --reason <text>` (manual; trailers `Closeout-Mode: manual`, `Closeout-Reason`, index entry `run_dir: null`, `mode: manual`). Do not change the `--run-dir`/`--no-run` CLI contract.
6. Repoint `deskops/cli/commands/closeout.py` `closeout commit` at `closure.py` without changing its CLI surface.
7. Rewire `deskops advance` at the closeout node and `advance --to complete` per the open decision (A/B/C) in `deskops/operations.py`.
8. Update `desk/rituals/closeout.md` to name `deskops closeout commit` as the one entry point.
9. Run `pytest tests/test_closeout.py tests/test_lifecycle_end_to_end.py`; keep `tests/test_closeout.py` unmodified; only change `tests/test_lifecycle_end_to_end.py` where the decision changes `advance` behavior.
10. Run `pytest tests` (must be green).
11. Verify closure result for each entry point: exit 0, task file gone, task removed from `desk/tasks/Board.md`, exactly one new commit with the route's trailers, exactly one new index line.
12. Do not commit; report the diff and run-dir/`--no-run --reason` evidence for the supervisor's closeout commit.

AMBIGUITIES:

1. Open decision A/B/C is unresolved (owner). Step 7 and step 8 cannot be executed, `tests/test_lifecycle_end_to_end.py` changes cannot be bounded, and Done When ("every closing entry point") conflicts with option A/C which remove entry points.
2. `closeout_gates` and `doc_io` are referenced with no module path or signature, and `deskops/services/` structure is not shown; whether they exist or must be created is unknown.
3. "Exactly one commit with the route's trailers": trailers for the `--run-dir` route are never specified (only the manual route's are given).
4. "One new index line": no file path, format, or schema is named for the index.
5. "Bundle removal": no definition of the bundle, its path convention, or behavior when absent.
6. Index/reason fields (`run_dir: null`, `mode: manual`) come from a prior shipped commit; whether to preserve or extend that schema is not stated.
7. `task-rw-f3-atoms-service` content is unknown; whether closure.py must reuse its service/atom patterns is unspecified.
8. Scope says out of scope is only the CLI contract, yet the decision may remove `--to complete` — a CLI-surface change; contradiction unresolved.
9. Resolved Decisions say the executor does not commit, while Done When/step 4 require "one new commit"; it is unstated how the executor demonstrates step 4 without committing.
10. No acceptance criteria detail for exit-0 verification of `advance` at the closeout node versus `closeout commit`.
11. "closeout commit (both routes)" and "CLI unchanged" assume current route behavior; current pre-819a8b8 tasks used a fabricated run dir — whether those remain valid inputs is unstated.
