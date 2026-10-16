RESTATEMENT:
1. Read pill `desk/contexts/pill-legacy-desk-formats-need-explicit-adaptation.md`.
2. Create `scripts/migrate_desk_stores.py` with argparse exposing `--dry-run` (default) and `--apply`.
3. Implement discovery: `os.walk(os.path.expanduser("~"), followlinks=False)`; catch `PermissionError` and skip that dir; identify directories named `.sldb`.
4. For each candidate `.sldb`: form absolute normalized path; require `core/models/TaskDoc.yaml`; exclude when a whole path segment matches `.tmp`, `.venv`, `node_modules`, `tools`, `tmp`; require `git -C <parent-of-.sldb> rev-parse --is-inside-work-tree` → `true`; stop descending once matched.
5. Implement detection of deskops models whose contract hash changed (TaskDoc for the dependency task).
6. `--dry-run`: print discovered stores and the per-store command sequence; run no mutating commands.
7. `--apply`: per store run `sldb stores check --store <store>`; for each changed model run `sldb models update <Model> --store <store> --pythonpath <repo>`; run `deskops desk update --root <repo> --apply`; run `sldb stores check --store <store>` again; record PASS/FAIL and continue on failure.
8. Exit 0 only if ≥1 store discovered and all stores pass.
9. Write `runs/planning/store-migration-<YYYYMMDD>.md` headed by the full discovered list and its count, then per-store before/after check output.
10. Create `tests/test_migrate_desk_stores.py` using `tmp_path` fake tree asserting discovery and exclusion behavior.
11. Run `pytest tests/test_migrate_desk_stores.py`, `python scripts/migrate_desk_stores.py --dry-run`, `python scripts/migrate_desk_stores.py --apply`, `sldb stores check --store .sldb`, `pytest tests`.

AMBIGUITIES:
1. `status: blocked` and Open Ambiguities says F6's entry into this cycle is undecided; no signal the blocker is lifted.
2. Dependency `task-rw-f6-taskdoc-contract-cleanup` content is absent; cannot confirm it is done or which models' contracts changed.
3. No mechanism specified for detecting "contract hash changed".
4. `--dry-run` is default, but exit 0 requires "every store passes"; dry-run's required exit code is undefined.
5. Discovery root is hardcoded to `$HOME`; no parameter defined for `tmp_path` test injection.
6. Exclusion segments given as `/.tmp/`, `/.venv/`, `/node_modules/`, `/tools/`, `/tmp/` "matched on whole path segments"; exact segment tokens are ambiguous.
7. Whether exclusions apply to ancestor dirs of `.sldb` or only literal segments of the `.sldb` path is unstated.
8. "do not descend into a matched store" — "matched" is undefined (name match vs full discovery match).
9. Zero-stores behavior is undefined beyond exit 0 requiring ≥1.
10. `<repo>` in `--pythonpath <repo>` and `--root <repo>` is never defined; assumed parent of `.sldb`.
11. PASS/FAIL extraction from `sldb stores check` is unspecified (exit code vs output parsing).
12. "re-running is safe" has no test or acceptance criterion.
13. Log path `runs/planning/...` not resolved relative to CWD or repo root.
14. No spec of how the script enumerates deskops models for `sldb models update`.
15. Validation runs `--apply` against ~24 real `$HOME` repos, mutating them, conflicting with the AGENTS sandbox rule; conflict unreconciled.
16. Whether the "full discovered list" is pre- or post-exclusion/git filtering is unclear.
17. No spec of subprocess timeout or non-git/non-zero-case handling beyond "record FAIL and continue".
