RESTATEMENT:
1. Verify dependency `task-rw-f6-taskdoc-contract-cleanup` is closed and the F6 owner decision is resolved; otherwise stop (status is `blocked`).
2. Create `scripts/migrate_desk_stores.py` with argparse flags `--dry-run` (default), `--apply`, `--home` (default `~`).
3. Implement `discover(root)`: `os.walk(root, followlinks=False)`, skip dirs raising PermissionError; when a dir is named `.sldb`, check `<store>/core/models/TaskDoc.yaml` exists, no whole path segment of the `.sldb` path relative to `root` equals `.tmp`, `.venv`, `node_modules`, `tools`, or `tmp`, and `git -C <parent> rev-parse --is-inside-work-tree` prints `true`; record store and do not descend into it.
4. Implement a runner for external commands with a 300 s timeout; treat timeout as FAIL; capture stdout/stderr/return code.
5. `--dry-run`: print discovered stores and the command list per store; exit 0 iff at least one store found.
6. `--apply`, per store (`<store>` = `.sldb` dir, `<target>` = parent repo, `<deskops>` = this checkout): run `sldb stores check --store <store>` (before), run `sldb models update <Model> --store <store> --pythonpath <deskops>` for each changed deskops model (TaskDoc), run `deskops desk update --root <target> --apply`, run `sldb stores check --store <store>` (after); on any failure record FAIL and continue.
7. Exit 0 only if at least one store was found and all pass; ensure re-running is safe.
8. Write `runs/planning/store-migration-<YYYYMMDD>.md` starting with the full discovered list and its count, plus per-store before/after results.
9. Create `tests/test_migrate_desk_stores.py` building a fake tree under `tmp_path` with `.sldb` dirs, present/absent `core/models/TaskDoc.yaml`, git-initialized repos, and excluded-segment dirs; assert discovery and exclusion behavior.
10. Validate: `pytest tests/test_migrate_desk_stores.py`, `python scripts/migrate_desk_stores.py --dry-run`, `python scripts/migrate_desk_stores.py --apply`, `sldb stores check --store .sldb`, `pytest tests`.

AMBIGUITIES:
1. Task `status: blocked` and Open Ambiguity "does F6 enter this cycle?" make this unexecutable until the owner decision resolves; the Implementation Path/Validation sections contradict the blocked state.
2. No mechanism is specified to determine "whose contract hash changed"; only TaskDoc is named, and no hash source, comparison basis, or persisted prior hash is given.
3. `<deskops>` (the pythonpath value) derivation is unspecified: cwd, script location, or repo root.
4. `<Model>` argument form for `sldb models update` is unspecified: bare model name vs file path.
5. Whether `--dry-run` also writes `runs/planning/store-migration-<YYYYMMDD>.md` and whether it performs the git work-tree check is unspecified.
6. Log behavior on re-run is unspecified: overwrite, append, or new file; date is local vs UTC is unspecified.
7. Exit code value when zero stores are found is unspecified (only "not 0" can be inferred).
8. Definition of PASS/FAIL for `sldb stores check` is unspecified (exit code vs parsed text), so "before/after result" logging is undefined.
9. Whether a store failing the "before" check still runs the remaining steps, or is skipped to the next store, is unspecified ("continue" is ambiguous).
10. Whether the 300 s timeout also applies to the discovery `git rev-parse` call is unspecified.
11. Whether `deskops desk update` must run with cwd = target repo in addition to `--root <target>` is unspecified.
12. `runs/planning/` existence/creation is unspecified.
13. Test acceptance criteria are undefined beyond "covers discovery and exclusion": no required cases, assertions, or git-setup method for simulating work trees in `tmp_path`.
14. No spec for parsing/segment-matching case sensitivity of the exclusion names.
15. Pill `desk/contexts/pill-legacy-desk-formats-need-explicit-adaptation.md` contents are not provided, so its constraints cannot be applied or verified.
16. No acceptance criteria for idempotence beyond "re-running is safe", and no stated behavior for a store that was already PASS before migration.
