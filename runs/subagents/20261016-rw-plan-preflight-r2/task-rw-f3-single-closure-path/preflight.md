RESTATEMENT:
1. Confirm prerequisite: verify `task-rw-f3-atoms-service` is closed and that its atoms service exists in the tree before touching closure code.
2. Read the surfaces: `deskops/services/closure.py`, `deskops/operations.py`, `deskops/cli/commands/closeout.py`, the closeout-gates module (`closeout_gates`), `doc_io`, `desk/rituals/closeout.md`, `tests/test_closeout.py`, `tests/test_lifecycle_end_to_end.py`, and the shipped `advance`/`_auto_commit_task_closure` path in `deskops/operations.py`.
3. Locate the current three closure paths: `advance` at closeout node (`_auto_commit_task_closure`), `advance task <id> --to complete`, and `closeout commit`.
4. Implement `deskops/services/closure.py` on top of `closeout_gates` and `doc_io`, exposing one closure routine that: runs closeout gates, updates `desk/tasks/Board.md`, removes the task bundle, makes exactly one commit with the route's trailers, and writes one index entry.
5. Support both routes in the service: run-dir route (commit trailer/index `run_dir` set, `mode` non-manual) and manual route (`--no-run --reason <text>`, trailers `Closeout-Mode: manual` and `Closeout-Reason`, index `run_dir: null`, `mode: manual`), matching 819a8b8.
6. Point `closeout commit` (both routes) at the service without changing its CLI contract (`--task`, `--run-dir`, `--no-run`, `--reason`); run `pytest tests/test_closeout.py` unchanged.
7. Rewire `advance` (closeout node) and `advance task <id> --to complete` per the Open Ambiguity decision A/B/C.
8. Update `desk/rituals/closeout.md` so it names `deskops closeout commit` as the one entry point.
9. Run `pytest tests/test_closeout.py tests/test_lifecycle_end_to_end.py`, then `pytest`.
10. Verify step-4 acceptance per entry point: exit 0, task file and primitives gone, task removed from `desk/tasks/Board.md`, one new commit with the route trailers, one new index line.
11. Do not commit; leave the diff for supervisor closeout via `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`.

AMBIGUITIES:
1. Open Ambiguity A/B/C is undecided, so step 7 and "every closing entry point" in Done When cannot be executed or verified.
2. Task `status: blocked`; no acceptance criteria for when/if the block clears, or who clears it.
3. `depends_on: task-rw-f3-atoms-service` — no statement of whether it is closed, or what atoms-service API closure.py must consume.
4. "Index entry" — index location, format, and writer are unspecified.
5. "Bundle removal" — "bundle" is undefined; only "task file and its primitives gone" is stated.
6. "Removed from Board" — no Board.md entry format or removal mechanism specified.
7. "Exactly one commit" — no commit message format, author, signing, or scope rule when unrelated dirty worktree changes exist.
8. "Same closure result" is defined only in the task; no test-level assertion of commit count or trailer content is specified for `advance` paths.
9. Which module/name provides `closeout_gates` and `doc_io` is not given; reuse vs new code is unspecified.
10. Resolved Decision ("Do not commit") conflicts with Done When observables ("one new commit", "one new index line") for an executor who cannot commit.
11. Docs change to `desk/rituals/closeout.md` implies an atom capture per AGENTS.md, but the task neither requires nor forbids it.
12. Whether "`advance` at the closeout node" and "`advance --to complete`" are the same code path is unstated.
13. No sandbox-desk path or concrete CLI invocation is given for mutating end-to-end validation.
14. Validation lists `test_lifecycle_end_to_end.py` but does not say whether it must pass unmodified or may be edited.
