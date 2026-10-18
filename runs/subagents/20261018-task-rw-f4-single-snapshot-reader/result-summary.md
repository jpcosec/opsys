# task-rw-f4-single-snapshot-reader — result summary

## Changes

- `deskops/graph/snapshot.py`
  - Added `Node(id, kind=None, path=None, identity=None, label=None)`, `Edge(source, target, role="related", provenance_path=None, provenance_locator=None, extractor=None)`, `GraphSnapshot(nodes, edges)` dataclasses (frozen; list defaults).
  - Added `read_graph_snapshot(path) -> GraphSnapshot`: validates file/JSON/object/`nodes` list; raises `GraphSnapshotReadError` for missing file, invalid JSON, missing `nodes`, missing node id, missing edge target/source, non-object node/edge, non-list `nodes`/`edges`/`nodes[].edges`.
  - Added helpers `_read_node`, `_read_nested_edges`, `_read_top_level_edge`, `_edge_provenance`, `_neighbor_nodes`.
  - `read_graph_neighbors` now uses `read_graph_snapshot`; same signature and top-level output keys (`node`, `incoming`, `outgoing`, `nodes`); node dicts keep `id`/`kind`/`label` plus `identity`/`path` when present.
  - Removed `_snapshot_nodes_by_id` and `_snapshot_edges`.
- `deskops/graph/checks.py`
  - Removed local `read_graph_snapshot`, `_snapshot_node_ids`, `_snapshot_edges`, `_simple_snapshot_edge`, `_edge_metadata`, and the `json` import.
  - `find_missing_graph_references` reads via `deskops.graph.snapshot.read_graph_snapshot` and re-raises `GraphMissingCheckError(str(exc)) from exc`.
  - `find_missing_snapshot_targets(snapshot: GraphSnapshot)` iterates `snapshot.nodes` / `snapshot.edges`.
- `deskops/graph/self_reflection.py`
  - `build_self_reflection_report` and helpers take `GraphSnapshot`; removed dict-parsing `_snapshot_nodes`/`_snapshot_edges`; added `_node_path(Node)`; edge walking uses `edge.source/target/role`.
  - `drift_check_knowledge_surfaces` imports the reader from `snapshot`, falls back to `GraphSnapshot()`, and walks `snapshot.edges`.
  - `json.loads` remains only in `_read_existing_decisions` (decisions file, per task).
- `deskops/cli/main.py`
  - `_graph_reflect` imports `GraphSnapshotReadError`/`read_graph_snapshot` from `deskops.graph.snapshot`; except is `(GraphSnapshotReadError, GraphMissingCheckError)`.
  - `_graph_missing` unchanged.
- Tests
  - `tests/test_graph_snapshot.py`: 6 new reader tests (nested flattening on the golden KGDB fixture, top-level edges + `identity.node_id`, missing file, invalid JSON, missing key, malformed shapes).
  - `tests/test_graph_checks.py`: passes `GraphSnapshot`/`Node`/`Edge` instead of raw dicts.
  - `tests/test_graph_self_reflection.py`: writes payloads to a temp file and reads them with `read_graph_snapshot`.

## Validation

- `PYTHONPATH=/tmp/rw/wt/snapreader python -m pytest tests/test_graph_snapshot.py tests/test_graph_checks.py tests/test_graph_self_reflection.py tests/test_output_goldens.py -q`
  - `21 passed in 99.17s (0:01:39)`
- `PYTHONPATH=/tmp/rw/wt/snapreader python -m pytest tests -q`
  - `410 passed, 3 skipped in 354.93s (0:05:54)`
- Goldens were not updated; all green unchanged.

## Tests against unfixed code

- None run.

## Task issues / ambiguities

- Cited line numbers were stale as warned: e.g. `_graph_missing` except is `deskops/cli/main.py:303` (not 292), `_graph_reflect` begins ~336 (not 321-333), `_graph_neighbors` printing runs 365-381 (not 341-364), checks' old reader was at 41 (not 40), `drift_check_knowledge_surfaces` starts ~423 (not 422), `test_graph_reflect_reports_missing_graph` is 231-239 (not 233-240).
- "`read_graph_neighbors` keeps its output dicts byte-for-byte" cannot hold literally for KGDB-style nodes: the old code spread every `semantics` key into the node dict, but the mandated `Node` has only 5 fields. Preserved the keys the CLI consumes (`id`, `kind`, `label`, plus `identity`/`path` when present); fixture output and all existing assertions are unchanged.
- `Node.label` precedence was not fully explicit; implemented `semantics.title` → node `label` → `semantics.label` → `id`.

## sldb

- No sldb bug observed. No sldb files changed.
