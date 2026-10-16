RESTATEMENT:

1. Confirm `task-rw-f6-taskdoc-contract-cleanup` is closed and this task has been promoted to `desk/tasks/`; do not start while `status: blocked`.
2. Read the pill `desk/contexts/pill-legacy-desk-formats-need-explicit-adaptation.md` and the plan `runs/planning/deskops-rewrite-inventory.md` (phase F6).
3. Write `scripts/migrate_desk_stores.py` with CLI flags `--dry-run` (default), `--apply`, `--home <dir>` (default `~`).
4. Implement discovery: `os.walk(root, followlinks=False)`, skip PermissionError dirs, do not descend into a matched store; match dirs named `.sldb` containing `core/models/TaskDoc.yaml`; exclude when any whole path segment of the `.sldb` path relative to the discovery root is `.tmp`, `.venv`, `node_modules`, `tools`, or `tmp`; keep only stores where `git -C <parent-of-.sldb> rev-parse --is-inside-work-tree` prints `true`.
5. Dry-run mode: print discovered stores and the commands that would run; exit 0 iff ≥1 store found.
6. Apply mode: per store run `sldb stores check --store <store>`, then `sldb models update TaskDoc --store <store> --pythonpath <deskops-repo-root>` (plus any other deskops model whose contract hash changed), then `deskops desk update --root <parent-of-.sldb> --apply`, then `sldb stores check --store <store>` again; 300 s timeout per command, timeout counts as FAIL; record FAIL and continue on failure.
7. Exit 0 only if ≥1 store found and every store passes; make reruns safe.
8. Write log `runs/planning/store-migration-<YYYYMMDD>.md` beginning with the full discovered list and its count, then per-store before/after check output and PASS/FAIL.
9. Write `tests/test_migrate_desk_stores.py` covering discovery and each exclusion rule on a fake tree under `tmp_path`, using `--home`.
10. Run `pytest tests/test_migrate_desk_stores.py`, `python scripts/migrate_desk_stores.py --dry-run`, `python scripts/migrate_desk_stores.py --apply`, `sldb stores check --store .sldb`, `pytest tests`.
11. Leave the commit to the supervisor; do not commit.
12. Done when the log shows every discovered store PASS after `--apply`.

AMBIGUITIES:

1. Status is `blocked` on `task-rw-f6-taskdoc-contract-cleanup`; no statement of what unblocks it beyond the Open Ambiguity about whether F6 enters this cycle.
2. No method given to determine "each deskops model whose contract hash changed" — no stored baseline hash, no defined comparison, no list of deskops models. Only TaskDoc is named.
3. "Passes" is undefined: exit code of `sldb stores check`, parsed output text, or both. The wording "logs per-store before/after `sldb stores check` results" suggests parsing output, but the parse target is unspecified.
4. Exit code value on failure/unfound is only specified as "not 0"; concrete codes unspecified.
5. `<deskops>` for `--pythonpath` is described as "this deskops checkout, so `deskops.models` imports" — whether that is the repo root, the `deskops/` package dir, or `sys.path`-style value is unstated.
6. Whether the 300 s timeout also applies to the `git rev-parse` probe and the discovery walk is not stated.
7. Whether `--apply` is required for the log to be written, or `--dry-run` also writes it, is unstated.
8. Whether `runs/planning/` must be created if absent, and whether the log file is overwritten or appended on rerun, is unstated.
9. Log filename is `store-migration-<YYYYMMDD>.md`; timezone/clock source and behavior when the file already exists today are unspecified.
10. Segment exclusion says "paths containing ... `/tools/` or `/tmp/`" but also ".tmp/, .venv/, node_modules/" (no slashes); exact segment strings (leading/trailing dots, case sensitivity) are only partly inferable.
11. Discovery root defaults to `~`, but validation runs `--apply` against the real `$HOME`, mutating ~24 real repositories; no confirmation gate or explicit exclusion of the deskops repo itself.
12. Tests must build a fake tree with git work-tree validity (`rev-parse --is-inside-work-tree` true) but the task does not say to init real git repos in `tmp_path` or to stub the git probe.
13. No acceptance criteria for the log's exact content/format beyond "starts with the full discovered list and its count".
14. Dependency on `task-rw-f6-taskdoc-contract-cleanup` means the "changed model" may be something other than TaskDoc; the task states TaskDoc but also says "for each ... whose contract hash changed", leaving the model set ambiguous.
