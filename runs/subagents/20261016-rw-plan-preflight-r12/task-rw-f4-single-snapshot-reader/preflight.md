RESTATEMENT:

1. Read `deskops/graph/snapshot.py`, `checks.py`, `self_reflection.py`, `deskops/cli/main.py`, and the four named test files to confirm the cited line numbers and current behavior.
2. In `deskops/graph/snapshot.py`: keep/define `GraphSnapshotReadError`; add dataclasses `GraphSnapshot(nodes, edges)`, `Node(id, kind=None, path=None, identity=None, label=None)`, `Edge(source, target, role='related', provenance_path=None, provenance_locator=None, extractor=None)`.
3. Implement `read_graph_snapshot(path: Path) -> GraphSnapshot`: read file, `json.load`; wrap `FileNotFoundError`/`JSONDecodeError`/OSError as `GraphSnapshotReadError`; require top-level `nodes` list; per node require `id` or `identity.node_id`; build `Node` with `identity` raw, `label = semantics.title else label else id`; flatten `nodes[].edges` with `source` = enclosing node id and `target` from `target` or `target_id`; also read top-level `edges` (own source) if present; require each edge target; raise `GraphSnapshotReadError` for non-list containers and non-dict items. No caching.
4. Keep `read_graph_neighbors` signature and output dicts byte-for-byte (keys `node`/`incoming`/`outgoing`/`nodes`; per-node `label`), now backed by `Node.label`.
5. Add reader tests to `tests/test_graph_snapshot.py`: missing file, bad JSON, missing key, malformed shape, valid snapshot.
6. Remove `read_graph_snapshot` from `checks.py`; import reader from `snapshot.py`; catch `GraphSnapshotReadError` and `raise GraphMissingCheckError(...) from exc`; change check functions to accept a `GraphSnapshot`.
7. Update `deskops/cli/main.py`: `_graph_missing` (except at 292) unchanged; point the read call (321) at `snapshot.read_graph_snapshot`; extend `_graph_reflect`'s except (321-333) to also catch `GraphSnapshotReadError`.
8. Update `self_reflection.py`: replace the removed-function call (422) with `snapshot.read_graph_snapshot`; keep the decisions-file `json.load` at 152.
9. Update tests passing raw dicts: `tests/test_graph_checks.py` (23, 47) and `tests/test_graph_self_reflection.py` (53, 165) to pass `GraphSnapshot`; verify `tests/test_graph_cli.py` (233-240) error-path expectations.
10. Run `pytest tests/test_graph_snapshot.py tests/test_graph_checks.py tests/test_graph_self_reflection.py tests/test_output_goldens.py`, then `pytest tests`.
11. Confirm Done When: `def read_graph_snapshot` exists only in `snapshot.py`; no `json.load`/`json.loads` of the snapshot in `checks.py`/`self_reflection.py`; new tests pass; `pytest tests` green.

AMBIGUITIES:

1. Precedence when both `id` and `identity.node_id` are present is unspecified.
2. Precedence when both `target` and `target_id` are present is unspecified.
3. Behavior when both top-level `edges` and nested `nodes[].edges` are present (merge, concat, dedupe, or precedence) is unspecified.
4. For top-level `edges`, the source key name is not given (only target is specified as required).
5. Which keys count as "a missing key": whether absent `version` or `metadata` raises, or only `nodes`/node-id/edge-target.
6. Exact `GraphSnapshotReadError` message text, and whether `GraphMissingCheckError` must reuse it verbatim.
7. Contradiction: check functions "accept a `GraphSnapshot`" yet `checks.py` "catches `GraphSnapshotReadError`" — who reads the file for checks is unclear.
8. New names/signatures of the check functions in `checks.py` after the reader is removed are not specified.
9. Location and parameter type of `read_graph_neighbors` (path vs `GraphSnapshot`) are not stated.
10. JSON keys mapping to `Edge.role`, `provenance_path`, `provenance_locator`, `extractor` are not stated.
11. Source of `semantics.title` for `label` (field name/structure) and confirmation that `kind`/`path` map from same-named keys are not stated.
12. Behavior when `identity` is a str and no `id` key is present (raise vs reuse str) is unspecified.
13. Handling of `identity` values that are neither dict nor str is unspecified.
14. Whether `id`/`target` may be empty strings or must be non-empty is unspecified.
15. Actual contents of pills `pill-011`/`pill-010` are not included, so required output shapes cannot be verified.
16. `depends_on` task completion cannot be verified; the reader format assumes their outputs.
17. Whether existing entries in `tests/test_output_goldens.py` must change is not stated beyond "stays green".
18. Whether `read_graph_snapshot` accepts only `Path` or also `str` is unspecified.
