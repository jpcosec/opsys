RESTATEMENT:
1. Do not start implementation: task is `status: blocked` on `task-rw-f6-taskdoc-contract-cleanup`; confirm that dependency is closed before proceeding.
2. Create `scripts/migrate_desk_stores.py` with an argparse CLI: `--dry-run` (default mode), `--apply`, `--home <dir>` (default `~`).
3. Implement discovery over the `--home` root: `os.walk(root, followlinks=False)`; skip dirs raising `PermissionError`; do not descend into a matched store.
4. Match a store when the directory is named `.sldb`, contains `core/models/TaskDoc.yaml`, and its parent passes `git -C <parent of .sldb> rev-parse --is-inside-work-tree` printing `true`.
5. Exclusion rule: take the `.sldb` path relative to the discovery root, split into path segments, and exclude when any segment is `.tmp`, `.venv`, `node_modules`, `tools`, or `tmp`.
6. Dry-run: print each discovered store and the commands that would run; exit 0 iff at least one store was found.
7. Apply, per store, each command with a 300 s timeout (timeout = FAIL): `sldb stores check --store <store>` → `sldb models update TaskDoc --store <store> --pythonpath <repo>` (models whose contract hash changed) → `deskops desk update --root <repo> --apply` → `sldb stores check --store <store>`.
8. On any per-store failure record FAIL and continue to the next store.
9. Exit codes: dry-run 0 iff ≥1 store found; apply 0 iff ≥1 store found and every store passes.
10. Write `runs/planning/store-migration-<YYYYMMDD>.md`, opening with the full discovered list and its count, then per-store before/after `sldb stores check` results.
11. Create `tests/test_migrate_desk_stores.py` using a fake tree under pytest `tmp_path` to cover discovery and exclusion.
12. Run: `pytest tests/test_migrate_desk_stores.py`; `python scripts/migrate_desk_stores.py --dry-run`; `python scripts/migrate_desk_stores.py --apply`; `sldb stores check --store .sldb`; `pytest tests`.
13. Do not commit; supervisor promotes, reviews diff, and runs closeout commit with `pytest tests` green.

AMBIGUITIES:
1. Inputs to "the models whose contract hash changed" are undefined: no source of truth for a model's prior hash, no list of "deskops models", and no specified hash-comparison method.
2. Success criterion for "PASS/FAIL" is undefined: whether `sldb stores check` exit code, stdout token, or per-model status determines pass.
3. Exact wiring of the hash change detection vs `--apply` idempotency ("re-running is safe") is unspecified.
4. `sldb models update <Model> --store <store> --pythonpath <repo>` and `deskops desk update --root <repo> --apply` flag names/signatures are unverified.
5. Meaning of `<repo>` (parent of `.sldb`?) is only implied.
6. Non-zero exit code value(s) for apply failure are unspecified (only "exit 0" is pinned).
7. No-store-found behaviour under `--apply` is unspecified (only dry-run rule is given).
8. Log file collision on a same-day re-run is unspecified: overwrite vs append, and which timezone/date to use for `<YYYYMMDD>`.
9. Log path base (cwd vs repo root) and required log schema/format are unspecified.
10. Discovered-list ordering is unspecified (unsorted `os.walk` output vs sorted).
11. Whether the 300 s timeout is fixed or configurable is unspecified.
12. Test acceptance criteria cover only discovery and exclusion; no tests specified for apply flow, exit codes, logging, or timeout.
13. Git setup for fake `tmp_path` trees is unspecified, though discovery requires `rev-parse --is-inside-work-tree` to print `true`.
14. Interpretation of "matched on whole path segments" for exclusion (relative path, leading/trailing slash, and `tmp` vs `/tmp/`) is under-specified.
15. Whether validation steps `--dry-run`/`--apply` must run against the real `$HOME` (default) or a sandbox is unspecified, given the sandbox rule in AGENTS.md.
16. "Each store's repo commit is its owner's" states a constraint but specifies no action for the script.
17. `core/models/TaskDoc.yaml` is assumed relative to `<store>/.sldb`; not stated.
