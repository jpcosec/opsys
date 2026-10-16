RESTATEMENT:
1. Confirm prerequisite: dependency task-rw-f6-taskdoc-contract-cleanup is closed and the new TaskDoc contract is final; otherwise stop (task status is `blocked`).
2. Read `desk/contexts/pill-legacy-desk-formats-need-explicit-adaptation.md` and `runs/planning/deskops-rewrite-inventory.md` (phase F6) for the adaptation format.
3. Create `scripts/migrate_desk_stores.py` with argparse: `--dry-run` (default) and `--apply`.
4. Implement discovery: walk `$HOME` for directories named `.sldb`, keep only those containing `core/models/TaskDoc.yaml`, exclude any path containing `/.tmp/`, `/.venv/`, `/node_modules/`, `/tools/`, or `/tmp/`, and keep only those inside a git work tree.
5. For `--dry-run`: print each discovered store path and the per-store commands that would run (`sldb models update`, `deskops desk update --apply`); make no changes.
6. For `--apply`, per store run in order: `sldb stores check` (before), `sldb models update`, `deskops desk update --apply`, `sldb stores check` (after); on any failure record `FAIL` and continue to the next store.
7. Exit 0 only if every discovered store passes; otherwise exit nonzero; ensure re-running is safe.
8. Write the per-store before/after results to `runs/planning/store-migration-<YYYYMMDD>.md`.
9. Run `python scripts/migrate_desk_stores.py --dry-run`, then `--apply`, then `sldb stores check --store .sldb`.
10. Do not commit; hand the diff to the supervisor for `deskops closeout commit --task <id> --run-dir <dir>` (or `--no-run --reason <why>`).

AMBIGUITIES:
1. Task status is `blocked` and the Open Ambiguity ("does F6 enter this cycle?") is unresolved — cannot start.
2. Dependency task-rw-f6-taskdoc-contract-cleanup status/final contract not shown; no evidence the new contract exists.
3. Discovery traversal depth, symlink handling, and permission-error handling under `$HOME` unspecified.
4. "inside a git work tree" is undefined: which directory is tested (the `.sldb` dir, its parent, or repo root) and via what command.
5. Exclusion matching is ambiguous: applied to the `.sldb` path or the repo path; `/.tmp/` vs `/tmp/` overlap; case/relative vs absolute paths unspecified.
6. Exact CLI invocation for `sldb models update` and `deskops desk update --apply` unspecified (no `--store`/path argument given; unclear if they accept one).
7. Precedence when both `--dry-run` and `--apply` are passed is unspecified.
8. Log file format unspecified (columns, how FAIL details are captured, timestamps, whether commands are echoed); exact filename when run date vs UTC differs unspecified.
9. Exit-code semantics for `--dry-run` (0 vs nonzero when a store would fail) unspecified.
10. Re-run behavior unspecified: whether already-passing stores are skipped or re-updated.
11. "every discovered store passes" has no expected store list/count; the "about 24" figure is approximate, so completeness cannot be verified.
12. Writing into other repos' working trees is required, but no rule on whether those repos may be left dirty, and no per-repo commit (task says each store's repo commit is its owner's).
13. Validation omits `pytest` and any test for the new script; no automated test or acceptance check for the script itself.
14. Validation `sldb stores check --store .sldb` does not identify which store (cwd-relative); no validation that all other stores pass except the script's own log.
15. `runs/planning/` is not listed in `files`, and its base location relative to the deskops repo is unstated.
