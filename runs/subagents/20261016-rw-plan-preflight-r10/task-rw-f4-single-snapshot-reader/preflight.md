RESTATEMENT:
1. In `deskops/graph/snapshot.py`, add dataclasses `GraphSnapshot(nodes, edges)`, `Node(id, kind=None, path=None, identity=None, label=None)`, `Edge(source, target, role='related', provenance_path=None, provenance_locator=None, extractor=None)`.
2. Add `read_graph_snapshot(path: Path) -> GraphSnapshot` in `snapshot.py`, no caching, raising the existing `GraphSnapshotReadError` (defined line 29) for: missing file, invalid JSON, missing required key, or malformed shape (non-list `nodes`/`edges`, non-dict item). Required: top-level `nodes`/`edges` lists; node id from `id` or `identity.node_id`; edge `source` and `target`.
3. Compute `Node.label` as title, else label, else id, matching the current logic at `snapshot.py:142`; keep `identity` raw.
4. Add reader tests to `tests/test_graph_snapshot.py`: missing file, bad JSON, missing key, malformed shape, valid snapshot.
5. In `deskops/graph/checks.py`: delete `read_graph_snapshot` (checks.py:40); catch `GraphSnapshotReadError` and re-raise `GraphMissingCheckError` with the same message via `raise ... from exc`; change check functions to accept a `GraphSnapshot`.
6. In `deskops/graph/self_reflection.py`: use `read_graph_snapshot`; update caller at line 422; leave the decisions-file read at line 152.
7. In `deskops/cli/main.py`: update the removed-function caller at line 321; keep `except GraphMissingCheckError` at 292/329; keep `read_graph_neighbors` signature and output dicts byte-for-byte (341-364).
8. Update tests that pass raw dicts: `tests/test_graph_checks.py:23,47`, `tests/test_graph_self_reflection.py:53,165`.
9. Run `pytest tests/test_graph_snapshot.py tests/test_graph_checks.py tests/test_graph_self_reflection.py tests/test_output_goldens.py`, then `pytest tests`.

AMBIGUITIES:
1. `depends_on` tasks are listed as `status: deferred`; no evidence they are complete, so prerequisite state (edge index, golden files) is unverified.
2. `Node` has no `title` field, yet `label` derives from "title, else label, else id"; the source key for `title` and its interaction with the explicit `label` field is unspecified.
3. "with the same message" — the exact `GraphMissingCheckError` message text to mirror from `GraphSnapshotReadError` is not given, nor whether message equality is tested.
4. Mapping from stored dict keys to `provenance_path`, `provenance_locator`, `extractor` (naming/nesting) is not specified.
5. Precedence when both `id` and `identity.node_id` are present (or when `identity` is a dict lacking `node_id`) is not stated.
6. Wiring after removing `checks.py:read_graph_snapshot` is unclear: which `checks.py` functions change signature, and whether callers read the snapshot themselves or pass a `GraphSnapshot` into an existing path-based entry point.
7. Whether `GraphSnapshotReadError` from `cli/main.py:321` propagates uncaught or is wrapped is not specified.
8. `tests/test_graph_cli.py` (lines 28,240,273) is required to keep working but is not in the `files` list; whether it may be edited is unstated.
