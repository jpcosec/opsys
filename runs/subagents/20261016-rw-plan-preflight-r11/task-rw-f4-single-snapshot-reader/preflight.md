RESTATEMENT:
1. Read `deskops/graph/snapshot.py` (esp. 29, 53, 58, 142), `checks.py` (13, 40, 42), `self_reflection.py` (152, 422), `cli/main.py` (292, 321, 329, 341-364), and the four named test files.
2. In `deskops/graph/snapshot.py` add dataclasses `GraphSnapshot(nodes, edges)`, `Node(id, kind=None, path=None, identity=None, label=None)` (identity stored raw), `Edge(source, target, role='related', provenance_path=None, provenance_locator=None, extractor=None)`; keep `GraphSnapshotReadError`.
3. Implement `read_graph_snapshot(path: Path) -> GraphSnapshot`: read + `json.load`; raise `GraphSnapshotReadError` for missing file, `JSONDecodeError`, missing required key, or malformed shape (non-list top-level `nodes`/`edges`, non-dict item). Required: node `id` or `identity.node_id`; edge `source` and `target`. No caching.
4. Delete `read_graph_snapshot` at `checks.py:40`; import the snapshot reader; wrap it in `try/except GraphSnapshotReadError` and `raise GraphMissingCheckError(<same message>) from exc`.
5. Update `cli/main.py:321` and `self_reflection.py:422` to use the new reader/GraphSnapshot; leave `except GraphMissingCheckError` at `cli/main.py:292,329` untouched.
6. Change the check functions in `checks.py` to accept a `GraphSnapshot` instead of raw dicts.
7. Keep `read_graph_neighbors` signature and output dicts byte-for-byte (`node`/`incoming`/`outgoing`/`nodes`, node `label`); compute `Node.label` as title→label→id per current `snapshot.py:142`.
8. Tests: add reader tests to `tests/test_graph_snapshot.py` (missing file, bad JSON, missing key, malformed shape, valid snapshot); update `tests/test_graph_checks.py:23,47` and `tests/test_graph_self_reflection.py:53,165` to pass a `GraphSnapshot`.
9. Run `pytest tests/test_graph_snapshot.py tests/test_graph_checks.py tests/test_graph_self_reflection.py tests/test_output_goldens.py`, then `pytest tests`.
10. Verify Done When: `def read_graph_snapshot` only in `snapshot.py`; no `json.load`/`json.loads` of the snapshot in `checks.py`/`self_reflection.py` (except `self_reflection.py:152` decisions file); new tests pass; full suite green.
11. Do not commit; hand the diff to the supervisor for closeout.

AMBIGUITIES:
1. `Node` has no `title` field, but `label` semantics are "title, else label, else id" — unclear where `title` is read (in the reader vs in `read_graph_neighbors`) and whether `Node` must also carry `title`.
2. Node `id` resolution when both `id` and `identity.node_id` exist: no stated precedence.
3. When `identity` is a raw str (no `node_id`), whether `id` becomes mandatory (missing-key error) is unstated.
4. `Node.identity` "kept raw" vs. `id` derived from `identity.node_id` — whether `identity` is stored unmodified in both cases.
5. Which source keys map to `Edge.provenance_path`, `provenance_locator`, `extractor` is not stated.
6. Item-level type rules beyond "non-dict item": whether non-str `id`/`source`/`target` (e.g. int, null) is a missing-key error, a malformed-shape error, or accepted, is unstated.
7. "with the same message" for `GraphMissingCheckError`: whether it is exactly `str(exc)` and whether the pre-change message text/CLI output must remain byte-identical is unverified.
8. Check-function signatures after the change (names, parameter type/order, return types) are not enumerated.
9. Whether checks/self_reflection/CLI callers may still accept a path for backward compatibility, or strictly `GraphSnapshot`.
10. The specific code at `cli/main.py:321` and `self_reflection.py:422` is not described, so the required edit is unknown from the doc alone.
11. Whether tests must construct `GraphSnapshot` via a helper, literal dataclasses, or `read_graph_snapshot` on a temp file is unspecified.
12. No instruction to grep for other callers/importers of `checks.read_graph_snapshot` outside the two named call sites; completeness is unverified.
13. Whether `GraphSnapshot`/`Node`/`Edge` must be re-exported (e.g. `deskops/graph/__init__.py`) or documented is unstated.
14. Dataclass options (frozen, slots, eq, types of `id`/`source`/`target`) are unspecified.
15. Ordering/deduplication guarantees for `nodes`/`edges` in the returned `GraphSnapshot` are unspecified.
16. Scope line says out of scope is "the snapshot format", but implementation adds required-key/malformed-shape validation — whether validation strictness may reject snapshots currently accepted (golden/self-store data) is unstated.
