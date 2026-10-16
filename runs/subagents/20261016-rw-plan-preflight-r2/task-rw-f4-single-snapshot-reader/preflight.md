RESTATEMENT:
1. Read `deskops/graph/snapshot.py`, `deskops/graph/checks.py`, `deskops/graph/self_reflection.py` to locate current parse sites and required keys.
2. In `snapshot.py`, add dataclasses: `GraphSnapshot(nodes, edges)`, `Node(id, kind, path=None, identity=None)`, `Edge(source, target, role, provenance_path=None, provenance_locator=None, extractor=None)`.
3. Add `read_graph_snapshot(path: Path) -> GraphSnapshot`; parse with no caching; raise `GraphSnapshotReadError` on missing file, invalid JSON, missing key.
4. Keep `read_graph_neighbors`, reimplemented on top of `read_graph_snapshot`.
5. In `checks.py`, replace direct JSON parsing with `read_graph_snapshot`; remove `json.load` usage and reconcile `GraphMissingCheckError` at line 41.
6. In `self_reflection.py`, replace direct JSON parsing with `read_graph_snapshot`; remove raw `JSONDecodeError` handling.
7. Run `pytest tests/test_graph_snapshot.py tests/test_graph_checks.py tests/test_graph_self_reflection.py tests/test_output_goldens.py`.
8. Run `pytest tests`.
9. Verify `grep -n 'json.load' deskops/graph/checks.py deskops/graph/self_reflection.py` returns empty.
10. Do not commit; leave the diff for supervisor closeout.

AMBIGUITIES:
1. No snapshot JSON schema given: which keys map to `nodes`/`edges` and to each `Node`/`Edge` field, and at what nesting.
2. "Missing key" undefined: which keys are required vs optional per `Node`/`Edge`.
3. `GraphSnapshotReadError` location/definition not stated: existing in `snapshot.py:52,57`? move, rename, or keep?
4. `GraphMissingCheckError` (`checks.py:41`) disposition unspecified: keep, remove, or subclass/replace with `GraphSnapshotReadError`.
5. Whether type errors and non-list shapes should also raise `GraphSnapshotReadError`, or only file/JSON/key errors.
6. Error message format, exception chaining (`from`), and whether `JSONDecodeError`/`KeyError` should be wrapped.
7. Dataclass field ordering, types, defaults, frozenness, and whether `Edge.source/target/role` are required.
8. Whether existing caching in these modules must be removed (doc only says the new reader has "no caching").
9. `read_graph_neighbors` signature and error behavior after the port not specified.
10. Whether `tests/test_graph_snapshot.py` exists today or must be created/extended; no new-test acceptance criteria beyond green tests.
11. Whether golden files in `test_output_goldens.py` may need regeneration; out-of-scope snapshot format leaves this unclear.
12. Contradiction risk: "Out of scope: the snapshot format" while implementation requires knowing the format to map keys.
13. No acceptance criteria on error-type identity for callers of `checks.py`/`self_reflection.py`.
