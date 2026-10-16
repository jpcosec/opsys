RESTATEMENT:
1. Read `deskops/graph/snapshot.py`, `deskops/graph/checks.py`, `deskops/graph/self_reflection.py`, `tests/test_graph_snapshot.py`; grep repo for importers of the old parse helpers, `read_graph_neighbors`, and the two error classes.
2. In `snapshot.py` add dataclasses `GraphSnapshot(nodes, edges)`, `Node(id, kind=None, path=None, identity=None)`, `Edge(source, target, role='related', provenance_path=None, provenance_locator=None, extractor=None)`; keep `GraphSnapshotReadError` (currently line 29).
3. In `snapshot.py` implement `read_graph_snapshot(path: Path) -> GraphSnapshot`: `json.load` the file; raise `GraphSnapshotReadError` on missing file, invalid JSON, missing required key, non-list top-level `nodes`/`edges`, non-dict items; require node `id` or `identity.node_id` and edge `source`/`target`; store `identity` raw; no caching.
4. Keep `read_graph_neighbors` in `snapshot.py`, rebuilt on `read_graph_snapshot`.
5. Port `checks.py` to parse only via `read_graph_snapshot`; make `GraphMissingCheckError` a subclass of `GraphSnapshotReadError` (imported from `snapshot.py`) so `cli/main.py:292,329` `except` clauses keep working.
6. Port `self_reflection.py` to use `read_graph_snapshot`, leaving its line-~152 `json.loads` of the separate decisions file.
7. Add tests to `tests/test_graph_snapshot.py`: missing file, bad JSON, missing key, malformed shape, valid snapshot.
8. Run `pytest tests/test_graph_snapshot.py tests/test_graph_checks.py tests/test_graph_self_reflection.py tests/test_output_goldens.py`, then `pytest tests`; confirm golden snapshot test passes; do not commit (supervisor commits).

AMBIGUITIES:
1. Whether `GraphSnapshotReadError` stays in `snapshot.py` or moves; moving to a shared module affects the import cycle with `checks.py`.
2. `Node.id` resolution when both top-level `id` and `identity.node_id` are present — precedence unspecified.
3. `identity` present as a str (no `node_id`) and no top-level `id`: error vs fallback unspecified.
4. `Node.identity` value when only top-level `id` exists (None vs raw) unspecified.
5. Edge provenance mapping: source JSON key layout for `provenance_path`/`provenance_locator`/`extractor` (flat vs nested `provenance` object) unknown.
6. Type validation for `source`/`target`/`id` (must be str?) unspecified.
7. Error message/attribute contract for `GraphSnapshotReadError` unspecified, so tests cannot assert message content.
8. Whether `tests/test_graph_checks.py` and `tests/test_graph_self_reflection.py` already exist; `files:` lists only `tests/test_graph_snapshot.py`.
9. Existing expectations in `tests/test_graph_snapshot.py` and `tests/test_output_goldens.py` unknown; goldens may assert parse output that the refactor changes.
10. Non-listed importers of the old helpers/errors besides `checks.py` and `self_reflection.py` unknown; scope limits to three modules.
11. Whether `read_graph_neighbors`'s signature and behavior must remain byte-for-byte identical.
12. Dataclass options (frozen, slots, equality, ordering) unspecified though likely asserted by tests.
13. Ordering/duplicate handling for nodes and edges unspecified.
14. Whether every current `GraphMissingCheckError` raise site (conditions) must be preserved exactly after porting.
15. Top-level JSON that is valid but not an object (e.g., a list) — text covers "non-dict item" but not this case explicitly.
16. Whether "missing key" applies uniformly to top-level `nodes`/`edges` and to per-node/per-edge required keys, and whether absent optional top-level keys are tolerated.
