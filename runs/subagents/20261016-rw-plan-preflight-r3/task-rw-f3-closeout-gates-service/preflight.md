RESTATEMENT:
1. Inspect `deskops/services/` and the sibling service from `task-rw-f3-drawer-routing-service` to copy its move+wrapper pattern.
2. Create `deskops/services/closeout_gates.py`; move `_closeout_reference_evidence`, `_reference_points_to_commit`, `_reference_points_to_test`, `_build_closeout_graph_context` there.
3. In `deskops/operations.py`, replace the moved bodies with thin wrappers that import and delegate to the service (keep existing call sites working).
4. Commit gate: require `re.fullmatch(r'[0-9a-f]{7,40}', ref)`; run `git rev-parse --verify <ref>^{commit}` to get the full sha (reject on nonzero exit / ambiguous abbreviation); run `git merge-base --is-ancestor <full sha> HEAD`; return True only if both succeed.
5. Tests gate: split ref on `::`, keep only the path part (node part ignored); resolve against `<root>`; require `.py` suffix, existence, and `resolved.is_relative_to(root / 'tests')`; reject absolute paths and `..` escapes.
6. Extend `tests/test_closeout.py`: assert rejection for `HEAD`, `main`, `deskops/x.py`, `/abs/tests/x.py`, `tests/../deskops/x.py`; assert acceptance for a real ancestor hash and `tests/test_x.py::test_y`.
7. Run `pytest tests/test_closeout.py tests/test_lifecycle_end_to_end.py`, then `pytest tests`.
8. Leave commits to the supervisor; do not commit.

AMBIGUITIES:
1. Signatures of the four moved functions and their exact call sites/params (e.g. where `root` comes from) are not given.
2. The `task-rw-f3-drawer-routing-service` pattern is referenced but not included, so wrapper/import conventions are unknown.
3. Whether `depends_on: task-rw-f3-primitives-service-and-dead-code` is already complete, and whether the executor must verify it.
4. `root` source unspecified (cwd, repo root, config).
5. Whether `HEAD` counts as an ancestor of itself for the `--is-ancestor` check (it exits 0), which affects the ancestor rule wording.
6. How to obtain a "real ancestor hash" in the test (HEAD~1, fixed sha) and whether it must differ from HEAD.
7. Whether the `::node` separator is allowed empty (`tests/test_x.py::`) and whether multiple `::` are handled.
8. Rejection mechanism for absolute paths is unspecified beyond "rejected" (resolve vs explicit check).
9. `_closeout_reference_evidence` behavior on mixed/invalid reference types after tightening is unspecified.
10. `_build_closeout_graph_context` dependencies (graph/kgdb modules) not described.
11. Test style (separate test functions vs parametrize) and file/fixture setup unspecified.
12. Repo AGENTS rule says capture substantive rules in `desk/atoms/` first; task does not mention atom updates, and scope only excludes the closure path.
13. `tests/test_lifecycle_end_to_end.py` existence/name is asserted but not verifiable from the task doc.
