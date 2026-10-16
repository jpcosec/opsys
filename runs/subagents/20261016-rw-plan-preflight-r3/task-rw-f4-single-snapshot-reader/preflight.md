RESTATEMENT:

1. Read `deskops/graph/snapshot.py`, `deskops/graph/checks.py`, `deskops/graph/self_reflection.py`, `cli/main.py` (~lines 292, 329), and `tests/test_graph_snapshot.py`, `tests/test_graph_checks.py`, `tests/test_graph_self_reflection.py`, `tests/test_output_goldens.py` to see current parsing/keys/errors.
2. In `snapshot.py`: keep/define `GraphSnapshotReadError`; add frozen-free dataclasses `GraphSnapshot(nodes, edges)`, `Node(id, kind, path=None, identity=None)`, `Edge(source, target, role, provenance_path=None, provenance_locator=None, extractor=None)`.
3. In `snapshot.py`: add `read_graph_snapshot(path: Path) -> GraphSnapshot` (no caching): open file; wrap `OSError`/missing file, `json.JSONDecodeError`, and top-level-not-dict into `GraphSnapshotReadError`; require `nodes` and `edges` top-level lists; require each item be a dict; else raise `GraphSnapshotReadError`.
4. Node id resolution: use `id`, else `identity.node_id`; raise `GraphSnapshotReadError` if neither; build `Node(id, kind, path, identity)` from optional fields defaulting to None.
5. Edge: require `source` and `target`; build `Edge(source, target, role, provenance_path, provenance_locator, extractor)` from optional fields defaulting to None.
6. Rebuild `read_graph_neighbors` on top of `read_graph_snapshot`; keep its public signature.
7. In `checks.py`: make `GraphMissingCheckError` subclass `GraphSnapshotReadError`; replace its JSON parsing with `read_graph_snapshot` and keep its raise sites (line ~42) working.
8. In `self_reflection.py`: replace snapshot JSON parsing with `read_graph_snapshot`; keep the separate `json.loads` of the decisions file (~line 152).
9. Append tests to `tests/test_graph_snapshot.py`: missing file, invalid JSON, missing required key, malformed shape (non-list `nodes`/`edges`, non-dict item), a valid snapshot (plus `identity.node_id` fallback), each asserting `GraphSnapshotReadError`.
10. Run `pytest tests/test_graph_snapshot.py tests/test_graph_checks.py tests/test_graph_self_reflection.py tests/test_output_goldens.py`.
11. Run `pytest tests`.
12. Do not commit; hand diff to supervisor.

AMBIGUITIES:

1. `Node.kind` and `Edge.role` have no default in the stated dataclass signatures, but "every other field is optional and defaults to None" implies they should. Contradiction: are `kind`/`role` required or optional?
2. Precedence when a node has both top-level `id` and `identity.node_id` is unspecified.
3. Whether `identity` is kept as a raw dict/object or normalized is unspecified.
4. Whether a missing edge `role`, node `kind`, or missing `path` are errors or silently None is unresolved (see #1).
5. Error for missing key does not specify which key or the error message/attributes; no `GraphSnapshotReadError` fields/constructor contract stated.
6. Dataclass mutability/equality/`frozen` not specified.
7. Whether `path` is stored as `str` or `Path` is unspecified.
8. `read_graph_neighbors` behavior (direction, dedup, return shape) after the port is unspecified beyond "stays".
9. Whether extra/unexpected JSON keys are ignored or rejected is unspecified.
10. No fixture format or golden file details are given; "the golden snapshot test stays green" has no named test/fixture.
11. No acceptance threshold beyond tests passing; no explicit check that `checks.py`/`self_reflection.py` contain no other JSON snapshot parsing (e.g., other keys) besides the reader.
