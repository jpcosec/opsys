RESTATEMENT:
1. In `deskops/graph/snapshot.py`, add dataclasses `GraphSnapshot(nodes, edges)`, `Node(id, kind=None, path=None, identity=None, label=None)` (identity kept raw), `Edge(source, target, role='related', provenance_path=None, provenance_locator=None, extractor=None)`; no caching.
2. Add `read_graph_snapshot(path: Path) -> GraphSnapshot` in the same module: open/load JSON; raise existing `GraphSnapshotReadError` on missing file, invalid JSON, missing required key, or malformed shape (non-list `nodes`, non-dict node/edge item).
3. Flatten nested `nodes[].edges` into `GraphSnapshot.edges`, setting each nested edge's `source` to the enclosing node's resolved id; also accept a top-level `edges` list.
4. Resolve node id from `id`, else `identity.node_id`; resolve edge target from `target`, else `target_id`; treat all other fields as optional with the defaults above.
5. Compute `Node.label` as title, else label, else id, matching current snapshot.py:142 semantics.
6. In `deskops/graph/checks.py`, delete the local `read_graph_snapshot` (checks.py:40); have checks call the snapshot reader and catch `GraphSnapshotReadError`, re-raising `GraphMissingCheckError` with the same message via `raise ... from exc`.
7. Change checks.py check functions to accept a `GraphSnapshot` instead of a raw dict.
8. In `deskops/graph/self_reflection.py`, port to the new reader; keep the separate decisions-file `json.load` at self_reflection.py:152.
9. In `deskops/cli/main.py`, update the call at :321 to the new reader; add `GraphSnapshotReadError` to `_graph_reflect`'s except (currently :321-333); keep `_graph_missing`'s `except GraphMissingCheckError` at :292 working.
10. Keep `read_graph_neighbors` signature and output dicts byte-for-byte (keys node/incoming/outgoing/nodes, plus each node's label).
11. Update tests passing raw dicts: tests/test_graph_checks.py:23,47 and tests/test_graph_self_reflection.py:53,165 (pass `GraphSnapshot` now); update tests/test_graph_cli.py:233-240 and :28,273 as needed.
12. Add reader tests to tests/test_graph_snapshot.py: missing file, bad JSON, missing key, malformed shape, valid snapshot (nested edges flattened, top-level edges accepted, defaults, identity fallback).
13. Run: `pytest tests/test_graph_snapshot.py tests/test_graph_checks.py tests/test_graph_self_reflection.py tests/test_output_goldens.py`, then `pytest tests`.
14. Verify guardrails: only snapshot.py defines `read_graph_snapshot`; checks.py/self_reflection.py contain no snapshot `json.load`/`json.loads` (self_reflection.py:152 excepted); all tests green.

AMBIGUITIES:
1. Which keys are "missing key" errors vs. skipped nodes/edges: is a node lacking both `id` and `identity.node_id` an error, and an edge lacking both `target`/`target_id` an error? Not explicitly stated.
2. `identity` fallback when `identity` is a string (no `.node_id`) — whether to stringify/index it or require `id`. Unspecified.
3. JSON field-name mapping to optional dataclass fields (`kind` vs `type`, `role` vs `type`, `provenance_path`/`provenance_locator`/`extractor` nesting) is not given.
4. Top-level edge `source` field name (`source` vs `source_id`) and whether it is required for top-level edges is unspecified.
5. `GraphSnapshot.edges` ordering/dedup rules (nested-then-top-level? input order?) unspecified.
6. Exact `GraphSnapshotReadError` message text per failure kind not specified.
7. Whether `GraphSnapshotReadError` keeps its current definition (snapshot.py:29) or gains new constructor args for the added cases.
8. `GraphMissingCheckError` re-raise "same message" — which message (the reader's) and whether attributes are preserved.
9. Whether `read_graph_snapshot` must be re-exported from checks.py/self_reflection.py for other importers, or imports repointed — not stated.
10. tests/test_graph_cli.py is referenced but absent from the task's `files` list; whether edits to it are in scope is unclear.
11. "label = title, else label, else id" — the source JSON keys for "title" and "label" are not stated.
12. Whether `_graph_reflect` should use the new reader directly or a shared helper, and whether its error surface/message changes.
13. tests/test_output_goldens.py is in Validation but not in `files`; unclear if it may need edits.
14. No acceptance criterion defines expected `Node.identity` shape when source JSON stores a string vs dict beyond "kept raw".
