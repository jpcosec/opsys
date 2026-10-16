RESTATEMENT:
1. Edit `deskops/graph/snapshot.py`: add dataclasses `GraphSnapshot(nodes, edges)`, `Node(id, kind=None, path=None, identity=None, label=None)`, `Edge(source, target, role='related', provenance_path=None, provenance_locator=None, extractor=None)`.
2. Implement `read_graph_snapshot(path: Path) -> GraphSnapshot`: parse JSON, require top-level `nodes` and `edges` lists, per-node id from `id` or `identity.node_id`, per-edge `source` and `target`, fill remaining fields from defaults, keep `identity` raw, no caching.
3. Raise `GraphSnapshotReadError` from the reader for missing file, invalid JSON, missing required key, non-list, non-dict item.
4. Keep `GraphSnapshotReadError` at `snapshot.py:29`; keep `read_graph_neighbors` signature and its dict output (`node`, `incoming`, `outgoing`, `nodes`; per-node `label`) byte-for-byte.
5. Edit `deskops/graph/checks.py`: make `GraphMissingCheckError` a subclass of `GraphSnapshotReadError`; replace direct JSON parsing with `read_graph_snapshot`.
6. Edit `deskops/graph/self_reflection.py`: read snapshot only via `read_graph_snapshot`; optionally keep `json.loads` of the separate decisions file at line 152.
7. Add reader tests to `tests/test_graph_snapshot.py`: missing file, bad JSON, missing key, malformed shape, valid snapshot.
8. Run `pytest tests/test_graph_snapshot.py tests/test_graph_checks.py tests/test_graph_self_reflection.py tests/test_output_goldens.py`.
9. Run `pytest tests`.
10. Do not commit; supervisor promotes the task and makes the closeout commit.

AMBIGUITIES:
1. Node id precedence when both `id` and `identity.node_id` are present is unspecified.
2. Deriving `identity.node_id` when `identity` is a str (task says identity may be dict or str) is undefined; unclear what the node `id` becomes.
3. Whether a missing `identity.node_id` (when `id` is absent) counts as the "missing key" error case is unspecified.
4. Where `Node.label` (title → label → id) is computed: dataclass default is `None`, but the semantics are stated "as snapshot.py:142 computes today"; unclear whether the reader or `read_graph_neighbors` populates it.
5. Message/attributes of `GraphSnapshotReadError` are unspecified.
6. Whether `GraphMissingCheckError` must preserve its existing constructor/message signature when re-parented is unspecified.
7. Whether `GraphSnapshotReadError` should also validate types of optional fields (e.g., `kind` is a str) is unspecified.
8. Behavior for valid JSON with a non-dict top level (e.g., a list) is not explicitly stated, though it may fall under "malformed shape".
9. "self_reflection.py:152 may keep its `json.loads`" is permissive; it is unclear whether keeping it is required or optional.
10. The current implementation of `read_graph_neighbors` and how `incoming`/`outgoing` are computed is not given, so "byte-for-byte" preservation can't be verified from the task text alone.
