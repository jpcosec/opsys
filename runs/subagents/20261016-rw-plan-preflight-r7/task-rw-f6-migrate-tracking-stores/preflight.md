RESTATEMENT:

1. Create `scripts/migrate_desk_stores.py` (and `tests/test_migrate_desk_stores.py`) implementing a CLI with `--dry-run` (default), `--apply`, `--home <dir>` (default `~`).
2. Implement discovery: `os.walk(home, followlinks=False)`, catch/skip `PermissionError` dirs, find directories named `.sldb` whose `core/models/TaskDoc.yaml` exists.
3. For each candidate, compute the absolute normalized path and drop it if any whole path segment is `.tmp`, `.venv`, `node_modules`, `tools`, or `tmp`.
4. Run `git -C <parent-of-.sldb> rev-parse --is-inside-work-tree`; keep only stores where stdout is `true`. Do not descend into a matched store directory.
5. For each discovered store, define repo = parent directory of the `.sldb` path, and build the command sequence: `sldb stores check --store <store>` → `sldb models update <Model> --store <store> --pythonpath <repo>` for each deskops model whose contract hash changed → `deskops desk update --root <repo> --apply` → `sldb stores check --store <store>`.
6. In `--dry-run`: print/emit the store list and the exact commands that would run; exit 0 iff ≥1 store found.
7. In `--apply`: execute each command with a 300 s timeout; treat timeout as FAIL; record per-store before/after `sldb stores check` results; on failure record FAIL and continue to the next store.
8. Exit 0 only if ≥1 store found and every store PASSes; make reruns safe (idempotent).
9. Write log to `runs/planning/store-migration-<YYYYMMDD>.md`, beginning with the full discovered store list and its count.
10. Write tests in `tests/test_migrate_desk_stores.py` covering discovery and exclusion against a fake tree under `tmp_path`.
11. Run validation: `pytest tests/test_migrate_desk_stores.py`, `python scripts/migrate_desk_stores.py --dry-run`, `python scripts/migrate_desk_stores.py --apply`, `sldb stores check --store .sldb`, `pytest tests`.
12. Confirm the log shows every discovered store PASS after `--apply`.
13. Do not commit; hand the diff to the supervisor for closeout.

AMBIGUITIES:

1. Task is `status: blocked` and Open Ambiguities leaves F6 cycle entry undecided; no execution is possible until that owner decision lands.
2. `depends_on: task-rw-f6-taskdoc-contract-cleanup` is unresolved, so the actual changed-model set and its contract hashes are unknown.
3. No mechanism is specified for detecting "each deskops model whose contract hash changed". Whether this is a hardcoded `TaskDoc` list, a hash comparison against the store's recorded model state, or parsed `sldb models update` output is unspecified.
4. `--pythonpath <repo>` value is undefined: repo root, package dir, or path containing the deskops Python package.
5. Whether `--root <repo>` in `deskops desk update` is the same value as `--pythonpath <repo>` is not stated.
6. "PASS" for a store is not defined: exit code zero, specific stdout text, or absence of FAIL lines.
7. Exit code for `--dry-run`/`--apply` when zero stores are found is unspecified (only "exit 0 iff at least one store was found").
8. Log behavior is unspecified: whether it is written during `--dry-run`, whether it overwrites or appends on a same-date rerun.
9. Exclusion rule lists `/tmp/` while tests must use `tmp_path` (typically under `/tmp`), which the exclusion would filter out; this is a contradiction between Scope and Implementation Path step 5.
10. Whether the exclusion test applies to the `.sldb` segment itself or the whole path including symlink resolution before normalization is unstated.
11. Behavior when `git` is missing, errors, or exceeds a timeout is unstated (only command timeouts of 300 s are defined).
12. `--home` handling of `~`, relative paths, and non-existent roots is unstated.
13. Order/determinism of store processing is unstated.
14. Whether `scripts/migrate_desk_stores.py` and `tests/test_migrate_desk_stores.py` already exist (modify vs create) is unstated.
15. Contradiction: Scope says record FAIL and continue, while Done When and Goal require every discovered store to PASS; no acceptance criterion is given for legitimately unmigratable stores.
16. Done When depends on machine-specific state (the actual ~24 stores on this machine) that the repo test suite cannot verify.
17. Whether the script must be exposed as a `deskops` subcommand or packaging entry point is unstated.
