# result summary: task-migration-never-touches-kimun

Done by the supervisor directly, after the coordinator reported the incident on 2026-10-19.

- kimun reverted, only `docs/archive/architecture/spec2viz`: `git restore`; the 5 untracked paths removed; the git-ignored `.sldb/` restored from the pass-1 backup and checked identical with `diff -rq`. `git -C kimun status` then showed only the owner's `docs/research/` and `runs/research/2026-10-13/`.
- `scripts/migrate_desk_stores.py`: new `PROTECTED_RELATIVE_ROOTS` (`proyectos/kimun`) and `PROTECTED_ABSOLUTE_ROOTS` (`/home/jp/proyectos/kimun`), and `is_protected()`. Discovery prunes protected directories during the walk and also refuses a matched store under them.
- `tests/test_migrate_desk_stores.py`: a TaskDoc store under `<home>/proyectos/kimun/...` in a git repo is not discovered, while a sibling repo is; the real kimun path is protected by absolute path. Both tests fail without the fix and pass with it. A dry-run of the script lists no kimun store.
- spec2viz was told. The only inbox note in the archive was deskops' own pass-1 notice, and it went with the revert.
- `runs/planning/store-migration-20261018-pass2.md`: incident recorded.

The full suite ran with a private `--basetemp`: see validation.log. The first run was lost when the machine rebooted at 09:36 and wiped /tmp, so this is a rerun.
