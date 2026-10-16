RESTATEMENT:
1. Read `deskops/cli/commands/doctor.py` and locate the `if desk_dir.exists():` block, the `unreadable_docs` definition inside it, and the two `tracked_mds` assignments (the shadowed one and the one that shadows it).
2. Move `unreadable_docs: list[str] = []` (or equivalent initialization) above the `if desk_dir.exists():` block so it exists on every code path.
3. Delete the dead/shadowed `tracked_mds = set(inspection.tracked_surface_docs)` assignment.
4. Confirm no other code depends on the removed `tracked_mds` line and that findings section reads `unreadable_docs` safely.
5. Add a regression test in `tests/test_doctor_unmodeled_surfaces.py` that runs `python -m deskops doctor --root <empty tmp dir>`, asserts exit code in {0,1}, asserts the missing-desk-structure finding appears, and asserts `Unexpected:` is absent.
6. Run `pytest tests/test_doctor_unmodeled_surfaces.py`.
7. Run `pytest tests`.
8. Manually run `python -m deskops doctor --root <empty dir>` to confirm no `Unexpected:` and the finding prints.

AMBIGUITIES:
1. Cited line numbers (78, 80) cannot be trusted; must identify statements by content, not position.
2. Exact text/code/id of the "missing-desk-structure finding" to assert on is not given.
3. Exit code "0 or 1" is not tied to a condition; which code is correct for a desk-less root is unspecified.
4. Whether `tests/test_doctor_unmodeled_surfaces.py` already exists; if not, whether to create it or use another test file is unclear.
5. Test invocation method unspecified: subprocess (`python -m deskops`) vs in-process runner.
6. `--repair` scaffold behavior is called resolved but neither tested nor confirmed in scope; unclear if it must be verified.
7. Whether removing the line-78 `tracked_mds` leaves `tracked_mds`/`inspection` unused or broken elsewhere is unverifiable from the task text.
8. Rationale cites `task-doctor-proposes-missing-model-registration` as prerequisite but `depends_on` is empty; ordering requirement unknown.
9. Referenced pills and the plan inventory (`runs/planning/deskops-rewrite-inventory.md`) are not provided; their constraints cannot be checked.
10. Task status is `deferred`; whether implementation is expected now is unstated.
11. No acceptance criteria given for the removal of the shadowed `tracked_mds` beyond "no crash."
