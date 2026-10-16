RESTATEMENT:
1. Confirm dependency `task-rw-f3-primitives-service-and-dead-code` is closed and that `deskops/services/` exists; read the "pattern from task-rw-f3-drawer-routing-service" to copy the move+wrapper structure.
2. Read `deskops/operations.py` around 2221–2260 for `_closeout_reference_evidence`, `_reference_points_to_commit`, `_reference_points_to_test`, `_build_closeout_graph_context`; read `tests/test_closeout.py` (~335) and `tests/test_lifecycle_end_to_end.py` (~126).
3. Create `deskops/services/closeout_gates.py`; move the four function bodies there unchanged except the two gate tightenings.
4. In `deskops/operations.py` replace the moved bodies with thin wrappers of the same names delegating to the service; keep existing call sites unchanged.
5. Commit gate in the service: reject unless `re.fullmatch(r'[0-9a-f]{7,40}', ref)`; run `git rev-parse --verify <ref>^{commit}` (reject on failure/ambiguous abbreviation); run `git merge-base --is-ancestor <full sha> HEAD` (reject on non-zero).
6. Tests gate in the service: strip `::...` suffix (node not validated); reject if `Path(ref).is_absolute()`; else resolve against root, require `.py` suffix, existence, and `resolved.is_relative_to((root / 'tests').resolve())`.
7. Extend `tests/test_closeout.py`: assert rejection of `HEAD`, `main`, `deskops/x.py`, `/abs/tests/x.py`, `tests/../deskops/x.py`; assert acceptance of a real ancestor hash and `tests/test_x.py::test_y`.
8. Run `pytest tests/test_closeout.py tests/test_lifecycle_end_to_end.py`, then `pytest tests`.
9. Report diff to supervisor; do not commit.

AMBIGUITIES:
1. `_closeout_reference_evidence` has no specified signature, return type, or contract (bool vs (ok, reason)), nor how a reference is classified as commit-gate vs tests-gate input.
2. `_build_closeout_graph_context` behavior, inputs, and dependencies are unspecified; unclear what "closeout graph context" must contain after the move.
3. Implementation Path cites pattern from `task-rw-f3-drawer-routing-service`, but `depends_on` names `task-rw-f3-primitives-service-and-dead-code`; which pattern/file to follow is unclear.
4. "wrappers" is undefined: same private names, renamed public names, re-exports, or service entrypoint module API.
5. `root` is undefined: repo root, cwd, desk root, or CLI `--root`; `.resolve()` symlink behavior for the `tests/` containment check unspecified.
6. Git cwd/target repo for `rev-parse`/`merge-base` is unspecified; behavior on exit code 128 vs 1 and on missing `git` is unspecified.
7. Whether the commit gate checks ancestry against `HEAD` of the repo root or the run dir is unspecified.
8. Tests gate: whether an empty `::` node part or a `::` with no path is rejected, and whether the `<root>/tests` directory must exist, is unspecified.
9. Unspecified how references that are neither a hex id nor a `tests/` `.py` path are handled (rejected by both gates, or new error).
10. Required Python version for `Path.is_relative_to` is unspecified.
11. Whether the cited existing tests (test_closeout.py:335, lifecycle:126) may be edited, or must pass unchanged, is unspecified.
12. Exact expected return values / error messages / exception types asserted by the new tests are unspecified ("rejected"/"accepted" only).
13. Whether `deskops/services/__init__.py` needs changes is unspecified.
