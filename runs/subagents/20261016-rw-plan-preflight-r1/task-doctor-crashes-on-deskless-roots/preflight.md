RESTATEMENT:
1. Read `deskops/cli/commands/doctor.py`; locate the `if desk_dir.exists():` block, the `unreadable_docs` assignment inside it, and the `tracked_mds = set(inspection.tracked_surface_docs)` at line 78 that line 80 shadows.
2. Move `unreadable_docs: list[str] = []` to before the `if desk_dir.exists():` block so it is defined on all paths.
3. Delete the shadowed `tracked_mds` assignment at line 78.
4. Read `tests/test_doctor_unmodeled_surfaces.py` to match existing fixture/assertion conventions.
5. Add one regression test: create an empty tmp dir, run `python -m deskops doctor --root <tmp>`, assert exit code in {0,1}, assert the missing-desk-structure finding text appears in stdout/stderr, assert `Unexpected:` does not appear.
6. Run `pytest tests/test_doctor_unmodeled_surfaces.py`.
7. Run `pytest`.
8. Manually run `python -m deskops doctor --root <empty tmp dir>` and confirm the finding prints with no `Unexpected:`.

AMBIGUITIES:
1. Exact literal output text of the "missing-desk-structure finding" is not given; cannot assert it without guessing the substring.
2. Which exit code (0 vs 1) desk-less roots should return is not specified; task allows either, weakening the assertion.
3. Whether the current `unreadable_docs` definition inside the block is typed (`list[str]`) or untyped is not shown.
4. Which of the two `tracked_mds` lines is truly dead cannot be confirmed from the doc; only line numbers 78/80 are given and may have drifted.
5. Exact command form is inconsistent: `python -m deskops doctor` vs `deskops doctor`; which the test should invoke is unspecified.
6. Whether `--repair` behavior on desk-less roots must also be tested is unclear (Resolved Decisions mention it; Scope/Implementation Path do not require a test).
7. Existing test conventions in `tests/test_doctor_unmodeled_surfaces.py` (tmp_path vs tmpdir, subprocess vs in-process runner, capsys usage) are unknown.
8. Repo-root/working-directory and package-install assumptions for running the test are unstated.
9. The three bound pills are not provided; whether they impose extra gates (e.g., closure commit, real-surface proof) cannot be verified.
10. Whether a commit is required by this task (no closure-commit pill is listed) is unspecified.
11. Chained dependency: task `task-rw-f2-typed-errors-and-exit-codes` is referenced as related but is out of scope; whether the `Unexpected:` handler will still mask the crash in the test's environment is unclear.
