RESTATEMENT:

1. Read `deskops/graph/snapshot.py`, `deskops/graph/checks.py`, `deskops/graph/self_reflection.py`, `tests/test_graph_snapshot.py`, `tests/test_graph_checks.py`, `tests/test_graph_self_reflection.py`, and the `except` sites in `deskops/cli/main.py` (~292, ~329) to inventory current JSON parse keys, error types, and constructor/attribute usage.
2. In `deskops/graph/snapshot.py`, add dataclasses: `Node(id, kind=None, path=None, identity=None)`, `Edge(source, target, role='related', provenance_path=None, provenance_locator=None, extractor=None)`, `GraphSnapshot(nodes, edges)`.
3. Keep/extend `GraphSnapshotReadError` (currently defined at snapshot.py:29) as the single read error type.
4. Implement `read_graph_snapshot(path: Path) -> GraphSnapshot`: `json.load` the file; raise `GraphSnapshotReadError` on missing file, invalid JSON, non-dict top level, missing/non-list `nodes` or `edges`, non-dict node/edge items, missing node id (`id` or `identity.node_id`), missing edge `source`/`target`. Apply defaults for all other fields. No caching.
5. Rebuild `read_graph_neighbors` on top of `read_graph_snapshot` in the same module.
6. In `deskops/graph/checks.py`, replace local parsing with `read_graph_snapshot`; make `GraphMissingCheckError` subclass `GraphSnapshotReadError` while preserving constructor/attribute behavior used by `cli/main.py`.
7. In `deskops/graph/self_reflection.py`, replace snapshot JSON parsing with `read_graph_snapshot`; keep the `json.loads` at self_reflection.py:152 for the separate decisions file.
8. Add tests to `tests/test_graph_snapshot.py`: missing file, bad JSON, missing top-level key, non-list `nodes`/`edges`, non-dict node/edge, missing node id, missing edge endpoints, valid snapshot.
9. Run `pytest tests/test_graph_snapshot.py tests/test_graph_checks.py tests/test_graph_self_reflection.py tests/test_output_goldens.py`, then `pytest tests`.
10. Do not commit; report diff for supervisor closeout.

AMBIGUITIES:

1. Task `status: deferred` with two `depends_on` tasks whose completion state is not shown; readiness to execute is unknown.
2. `runs/planning/deskops-rewrite-inventory.md` (phase F4 plan) is referenced but not provided.
3. Node id precedence is unspecified when both `id` and `identity.node_id` are present and differ.
4. Whether `identity` may be a non-dict (string) while `id` is absent — behavior unspecified (id resolution would fail; error vs. fallback unclear).
5. Optional-field semantics for explicit `null` values (e.g. `"role": null`) — keep null vs. apply default is unspecified.
6. Container types for `GraphSnapshot.nodes`/`edges` (list vs. tuple) and whether ordering is preserved are unspecified.
7. Whether `read_graph_snapshot` accepts `str`/`os.PathLike` or only `Path` is unspecified.
8. Behavior for other I/O errors (permission denied, directory path, encoding) beyond "missing file" is unspecified.
9. Error message/attribute contract of `GraphSnapshotReadError` is unspecified; needed to confirm CLI `except` sites and any message consumption.
10. `GraphMissingCheckError`'s current constructor signature/payload (used at cli/main.py:292 and 329) is not shown; subclassing may conflict with `GraphSnapshotReadError`'s signature.
11. `read_graph_neighbors` signature and module location are not given; whether it keeps its current signature is unspecified.
12. Current JSON field names in checks.py/self_reflection.py are not shown; whether they match `provenance_path`/`provenance_locator`/`extractor` exactly is unverified.
13. Whether existing `tests/test_graph_snapshot.py`, `tests/test_graph_checks.py`, `tests/test_graph_self_reflection.py` exist and how much they assert is unverified.
14. Whether goldens in `tests_output_goldens` may change if reader behavior differs is not addressed.
15. The two pills (`pill-011`, `pill-010`) are referenced but their content is not provided.
