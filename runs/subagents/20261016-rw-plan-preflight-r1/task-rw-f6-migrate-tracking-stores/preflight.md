RESTATEMENT:
1. Confirm the blocker `task-rw-f6-taskdoc-contract-cleanup` is closed and the owner decision to enter F6 is recorded; do not start implementation while `status: blocked` holds.
2. Read `desk/contexts/pill-legacy-desk-formats-need-explicit-adaptation.md` and follow its adaptation rules for legacy store formats.
3. Read `runs/planning/deskops-rewrite-inventory.md` phase F6 to get the authoritative store list and the exact meaning of "tracked by deskops models".
4. Create `scripts/migrate_desk_stores.py`:
   - discover stores via `find ~ -path '*/.sldb/core/models/TaskDoc*'` (or the inventory list if provided).
   - default to dry-run; require an explicit `--apply` flag for mutation.
   - for each store, record `sldb stores check --store <store>` output before and after.
   - on apply, run the per-store update steps (`sldb models update`, `deskops desk update --apply`) against that store root.
   - write a log to `runs/planning/store-migration-<date>.md` with a per-store PASS/FAIL table.
5. Run `python scripts/migrate_desk_stores.py --dry-run`; inspect the log for correct discovery and no mutations.
6. Run with `--apply`; re-run `sldb stores check --store .sldb` and confirm the log shows every store PASS.
7. Do not commit to any target store repo; only commit the script, the log, and the task doc change in this repo.

AMBIGUITIES:
1. `status: blocked` and the listed blocker/owner decision — the doc never states the decision outcome, so I cannot tell whether I am allowed to start.
2. "24 stores on this machine" and "every listed store" — no store list, no paths, no count source in the doc; the inventory file referenced is not included.
3. "each runs `sldb models update` and `deskops desk update --apply`" vs Implementation Path step 2 ("Dry run, then `--apply`") — unclear whether the script must invoke those two commands, or only the script's own `--apply`.
4. Whether "passes afterwards" means the working tree check passes only, or requires the store owners to commit; Scope says their commits are out of scope but Done When says every store PASS.
5. Validation lists only `--dry-run` and `.sldb` check — no validation entry for the apply run or for the other stores.
6. Log filename `runs/planning/store-migration-<date>.md` — date format unspecified.
7. "TaskDoc" contract change — the actual changed contract/fields are not described, so I cannot verify migration correctness.
8. `sldb stores check` invocation form per store (cwd vs `--store` path, absolute vs relative) unspecified.
9. Whether `.sldb` in this repo is one of the 24 stores or a separate case.
10. Discovery via `find ~` may hit sandbox/untracked stores; inclusion/exclusion rules absent.
11. No acceptance criteria beyond the log; no exit-code, idempotency, or partial-failure behavior defined.
12. Pill content is not included, so its constraints on adaptation are unknown.
