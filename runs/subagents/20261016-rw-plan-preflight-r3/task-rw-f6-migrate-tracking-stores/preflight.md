RESTATEMENT:

1. Confirm `task-rw-f6-taskdoc-contract-cleanup` is closed and the F6-cycle blocker is resolved; if not, stop.
2. Create `scripts/migrate_desk_stores.py` with an argparse CLI: `--dry-run` (default) and `--apply`, mutually exclusive.
3. Implement discovery: `os.walk(os.path.expanduser("~"), followlinks=False)`; for each directory named `.sldb` whose path has `core/models/TaskDoc.yaml`, compute absolute normalized path; exclude if any whole path segment equals `.tmp`, `.venv`, `node_modules`, `tools`, or `tmp`; require `git -C <parent-of-.sldb> rev-parse --is-inside-work-tree` to print `true`; catch `PermissionError` per-directory and skip; do not descend into a matched `.sldb`.
4. For each discovered store: run `sldb stores check` (before), then `sldb models update`, then `deskops desk update --apply`, then `sldb stores check` (after); capture both check outputs.
5. On any per-store failure, record FAIL for that store and continue to the next store.
6. In `--dry-run`, print the discovered stores and the exact commands that would run; make no mutations.
7. Exit 0 only if every store's after-check passes; nonzero otherwise. Ensure re-run safety (idempotent).
8. Write `runs/planning/store-migration-<YYYYMMDD>.md` beginning with the full discovered list and its count, then per-store before/after check results and final status.
9. Write `tests/test_migrate_desk_stores.py` using `tmp_path` fake trees covering discovery and exclusion rules; use mocked/stubbed git and `sldb` invocations as needed.
10. Run `pytest tests/test_migrate_desk_stores.py`, then `python scripts/migrate_desk_stores.py --dry-run`, then `--apply`, then `sldb stores check --store .sldb`, then `pytest tests`.
11. Verify log file shows every discovered store PASS after `--apply`. Do not commit; report diff to supervisor.

AMBIGUITIES:

1. Task `status: blocked` and Open Ambiguity states the F6-cycle owner decision is unresolved — no instruction on whether to execute now, wait, or treat blocker as resolved.
2. `depends_on: task-rw-f6-taskdoc-contract-cleanup` has no stated code artifact that this script consumes; unclear what interface/behavior it provides.
3. Rationale says stores need `sldb models update` **and** `deskops desk update --apply`; Implementation Path step 2 says "check, update" without naming commands — unclear which update command(s) to run and in what order relative to each store's cwd.
4. Ambiguity whether per-store commands run with cwd set to the store's parent repo, and whether `--store <path>` must be passed to `sldb stores check` per store.
5. Exclusion rules say "matched on whole path segments" but list `/tools/` and `/tmp/` with slashes — unclear whether `tools`/`tmp` anywhere in home (e.g. `~/projects/tmp/x/.sldb`) are excluded.
6. No definition of "passes" for `sldb stores check` — exit code, output substring, or specific status token unspecified.
7. Whether the script should commit anything in each store's repo is unresolved; scope says "Each store's repo commit is its owner's" but it is unclear if that means the script must not commit, or must leave the tree clean.
8. Behavior for stores with dirty/uncommitted worktrees, missing `sldb`/`deskops` on PATH, or non-git parents of `.sldb` is unspecified.
9. Log format is underspecified: no schema for before/after check capture, timestamp format beyond `<YYYYMMDD>` (timezone unspecified), or overwrite-vs-append on re-run same day.
10. `--dry-run` output format is not specified (human text, table, machine-readable); no acceptance criterion for its content.
11. Acceptance criterion "log shows every discovered store PASS" does not define required store count, so a run with zero or one discovered store could trivially pass.
12. `pytest tests` must be green (Resolved Decisions) but no baseline is stated; unclear how to distinguish pre-existing failures from this task's.
13. Validation lists `sldb stores check --store .sldb` only for the deskops repo, not for the ~24 target stores, so end-state verification of the goal is not actually specified as a check.
14. Directory `scripts/` and `runs/planning/` existence is not stated; unclear whether to create them.
15. Test coverage is limited to "discovery and exclusion"; no test requirement for check/update/run-apply/logging behavior, so regression risk in those paths is unguarded.
16. `git rev-parse --is-inside-work-tree` output parsing ("prints `true`") does not say how to handle nonzero exit, stderr, or trailing whitespace.
17. No timeout, parallelism, or ordering requirement for ~24 stores; runtime expectation unstated.
18. No owner/decision record defining when F6 enters the cycle, so "done" cannot be confirmed independent of that decision.
