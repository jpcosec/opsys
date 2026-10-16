RESTATEMENT:
1. Read `runs/planning/deskops-rewrite-inventory.md` (finding X6), the drawer-routing-service precedent task, and the two bound pills to learn the move-to-service + wrapper pattern.
2. Read current `_closeout_reference_evidence`, `_reference_points_to_commit`, `_reference_points_to_test`, `_build_closeout_graph_context` in `deskops/operations.py` (~2221-2260) and all their callers.
3. Create `deskops/services/closeout_gates.py` containing the moved `_closeout_reference_evidence`, `_reference_points_to_commit`, `_reference_points_to_test`, `_build_closeout_graph_context`.
4. Tighten commit gate: `re.fullmatch(r'[0-9a-f]{7,40}', ref)`; reject on no match; run `git rev-parse --verify <ref>^{commit}`; reject on failure; run `git merge-base --is-ancestor <full_sha> HEAD`; accept only on exit 0.
5. Tighten tests gate: strip `::node` suffix, resolve path against `<root>`, require suffix `.py`, existence, and `resolved.is_relative_to(root / 'tests')`; reject absolute paths and `..` escapes.
6. Rewrite `_closeout_reference_evidence` to call the two gates; keep `_build_closeout_graph_context` behavior unchanged.
7. Add thin wrappers in `deskops/operations.py` delegating to the service so existing call sites keep working.
8. Update `tests/test_closeout.py`: assert rejection of `HEAD`, `main`, `deskops/x.py`, `/abs/tests/x.py`, `tests/../deskops/x.py`; assert acceptance of a real ancestor hex hash and `tests/test_x.py::test_y`.
9. Run `pytest tests/test_closeout.py tests/test_lifecycle_end_to_end.py`, then `pytest tests`.
10. Do not commit; leave the diff for supervisor closeout.

AMBIGUITIES:
1. Precedent "task-rw-f3-drawer-routing-service" is named in Implementation Path but appears in neither `depends_on` nor `references`; its file pattern is unknown.
2. `status: deferred` and `depends_on: task-rw-f3-primitives-service-and-dead-code` are not marked resolved, so whether the dependency is complete or whether work may start is unknown.
3. `runs/planning/deskops-rewrite-inventory.md` is cited but absent from `references`; existence/content unknown.
4. Contents of both bound pills are not included.
5. Wrapper convention is unspecified: names, signatures, return types, and whether old private names must remain importable.
6. Unknown whether gates return bool/raise; the doc says "rejected/accepted" without a return contract, exception type, or message.
7. `_closeout_reference_evidence` behavior after the move is never described.
8. `_build_closeout_graph_context` inputs/outputs are never described; moving it safely is unspecified.
9. Where `<root>` comes from (repo root, store root, injected param) is unspecified.
10. Path resolution order is unspecified (resolve before/after join, symlink handling, `os.path.realpath` vs `Path.resolve`).
11. Behavior for empty path before `::`, multiple `::`, or trailing `::` is unspecified.
12. Python version assumption for `is_relative_to` (3.9+) is not stated.
13. `git merge-base --is-ancestor` behavior on a repository without a parent commit (root HEAD) is unspecified; test using a "real ancestor hash" may be unrunnable.
14. How the test obtains a real ancestor hash (fixture repo vs this repo) is unspecified.
15. Whether `tests/test_lifecycle_end_to_end.py` exists and depends on the free/renamed function names is unknown.
16. Full-sha extraction from `git rev-parse` output (stdout parsing, stripping) is unspecified.
17. Out-of-scope boundary with task-rw-f3-single-closure-path is ambiguous because callers of the moved functions live on the closure path.
18. Done When requires "green" but no coverage threshold or new-case list beyond the four reject/two accept examples is given.
