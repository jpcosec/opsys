RESTATEMENT:

1. Confirm the blocker is cleared: `task-rw-f6-taskdoc-contract-cleanup` closed and the F6 owner decision resolved; do not start otherwise.
2. Create `scripts/migrate_desk_stores.py` with argparse flags `--dry-run` (default), `--apply`, `--home <dir>` (default `~`).
3. Implement discovery: `os.walk(home, followlinks=False)`; locate dirs named `.sldb` containing `core/models/TaskDoc.yaml`; skip `PermissionError` dirs; do not descend into a matched store; compute the `.sldb` path relative to the discovery root and exclude if any path segment is `.tmp`, `.venv`, `node_modules`, `tools`, or `tmp`; keep only stores where `git -C <parent of .sldb> rev-parse --is-inside-work-tree` prints `true`.
4. For each discovered store run, with 300 s timeout per command: `sldb stores check --store <store>` (before) → `sldb models update TaskDoc --store <store> --pythonpath <repo>` → `deskops desk update --root <repo> --apply` → `sldb stores check --store <store>` (after).
5. `--dry-run`: print discovered stores and the commands that would run; exit 0 iff at least one store was found. `--apply`: execute commands, mark each store PASS/FAIL, continue on failure.
6. Exit 0 only if at least one store found and every store passes; ensure re-run safety.
7. Write `runs/planning/store-migration-<YYYYMMDD>.md` starting with the full discovered list and its count, plus per-store before/after `sldb stores check` results.
8. Create `tests/test_migrate_desk_stores.py` covering discovery and exclusion rules on a fake tree under `tmp_path`.
9. Run: `pytest tests/test_migrate_desk_stores.py`; `python scripts/migrate_desk_stores.py --dry-run`; `python scripts/migrate_desk_stores.py --apply`; `sldb stores check --store .sldb`; `pytest tests`.

AMBIGUITIES:

1. Status is `blocked` on an open owner decision and an unclosed `depends_on`; the doc gives no signal whether the executor should start, wait, or only plan.
2. No mechanism is specified to determine "each deskops model whose contract hash changed" or where that hash lives; the only concrete model named is TaskDoc.
3. `<repo>` is undefined: parent of `.sldb`, the git work-tree root reported by `git rev-parse`, or the deskops repo.
4. Log path `runs/planning/store-migration-<YYYYMMDD>.md` has no anchor (cwd, deskops repo root, `--home`, or each target repo).
5. How to classify a store as PASS/FAIL from `sldb stores check` is unspecified (exit code vs parsing stdout) — needed for both the log and the exit rule.
6. Whether `--dry-run` runs the `sldb stores check` commands (and is subject to the 300 s timeout) is not stated.
7. Exclusion list both `/.tmp/` and `/tmp/` and is described as segment-matched; overlap and intended semantics are unclear.
8. Whether the script must avoid committing in discovered repos ("repo commit is its owner's") or merely avoid owning their commits is ambiguous.
9. Done When requires every store PASS after `--apply`, but Implementation Path says to record FAIL and continue; no rule for handling a permanently failing store while satisfying exit criteria.
10. Zero stores discovered under `--apply` yields nonzero exit but "Done When" is unsatisfiable; not addressed.
11. Tests must satisfy the git-work-tree discovery condition; the doc does not state tests must create git repos under `tmp_path`.
12. Requirement "re-running is safe" has no acceptance check or definition of idempotent behavior.
13. No acceptance criteria for the log's format beyond "starts with the full discovered list and its count".
14. Whether other files may be added/changed (e.g., `.sldb` in deskops itself, docs) is unstated.
