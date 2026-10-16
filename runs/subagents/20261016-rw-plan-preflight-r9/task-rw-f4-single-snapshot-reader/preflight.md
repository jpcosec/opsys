RESTATEMENT:
1. Read, before editing: `deskops/graph/snapshot.py`, `checks.py`, `self_reflection.py`, `cli/main.py:280-370`, `tests/test_graph_snapshot.py`, `tests/test_graph_checks.py`, `tests/test_graph_self_reflection.py`, `tests/test_output_goldens.py`, `tests/test_graph_cli.py`, and pills `desk/contexts/pill-010-graph-runtime-output-policy.md`, `desk/contexts/pill-011-self-reflection-noise-control.md`.
2. In `deskops/graph/snapshot.py`: keep `GraphSnapshotReadError` (line 29); add dataclasses `GraphSnapshot(nodes, edges)`, `Node(id, kind=None, path=None, identity=None, label=None)`, `Edge(source, target, role='related', provenance_path=None, provenance_locator=None, extractor=None)`.
3. Implement `read_graph_snapshot(path: Path) -> GraphSnapshot`, no caching: open file (file-missing → `GraphSnapshotReadError`), `json.loads` (decode error → `GraphSnapshotReadError`), require top-level `nodes` and `edges` lists, require each node's `id` (from `id` or `identity.node_id`), require each edge's `source` and `target`, keep `identity` raw, compute `label` as title → label → id; raise `GraphSnapshotReadError` on non-list containers and non-dict items.
4. Rewrite `read_graph_neighbors` to consume `read_graph_snapshot`, preserving its signature and its exact output dict keys (`node`, `incoming`, `outgoing`, `nodes`) and each node's `label` value, using the snapshot.py:142 label semantics.
5. In `checks.py`: change `GraphMissingCheckError(GraphSnapshotReadError)`, replace its own JSON parsing with `read_graph_snapshot`, keep raise sites/behavior at line 42 and the `deskops graph missing` output.
6. In `self_reflection.py`: replace snapshot parsing with `read_graph_snapshot`; keep `json.loads` at line 152 for the decisions file.
7. Add tests to `tests/test_graph_snapshot.py`: missing file, invalid JSON, missing required key (nodes, edges, node id, edge source/target), malformed shape (nodes non-list, item non-dict), valid snapshot, and subclass check `issubclass(GraphMissingCheckError, GraphSnapshotReadError)`.
8. Run `pytest tests/test_graph_snapshot.py tests/test_graph_checks.py tests/test_graph_self_reflection.py tests/test_output_goldens.py`, then `pytest tests`; manually run `python -m deskops graph neighbors ...` and `deskops graph missing` to confirm unchanged output.
9. Do not commit; hand the diff to the supervisor.

AMBIGUITIES:
1. `read_graph_neighbors` signature is not written (only "keeps its signature"); parameter list/types must be read from code.
2. `label` computation is stated only by reference to snapshot.py:142; not executable from the doc alone.
3. Whether `read_graph_snapshot` itself populates `label` (always, since `id` exists), or a directly-constructed `Node` has `label=None`, is unspecified; `label: str | None` implies both.
4. Falsy-but-present `title`/`label` (e.g. empty string) fallback behavior is unspecified.
5. `identity.node_id` access assumes a dict; whether a non-dict `identity` with a nested lookup, or a str identity lacking top-level `id`, is an error is implied but not stated.
6. Whether `id`/`source`/`target` must be strings (vs any JSON scalar) is unspecified.
7. Unknown extra keys on `nodes`/`edges`/top-level items: stated "every other field is optional", but whether unknown keys are ignored or rejected is not explicit.
8. Duplicate node ids / duplicate edges: not addressed.
9. Whether edges must reference existing nodes (referential integrity) inside the reader or only in checks is unspecified.
10. No required exception message/args for `GraphSnapshotReadError`; whether messages must match current ones is unspecified.
11. Encoding/OS errors (non-UTF-8 file, path is a directory, permission error) are not mapped to `GraphSnapshotReadError` in the doc.
12. If `checks.py` lets a plain `GraphSnapshotReadError` propagate, the CLI `except GraphMissingCheckError` at main.py:292/329 will not catch it; doc says CLI excepts "keep working" but does not say CLI must be extended or that readers must re-wrap as `GraphMissingCheckError`.
13. Whether `checks.py` and `self_reflection.py` must reproduce byte-identical output to today (goldens) beyond the neighbor dict is only implied by "golden snapshot test stays green".
14. `read_graph_snapshot`/`Node`/`Edge` mutability, equality, `frozen`, `slots` are unspecified.
15. Whether removed parsing code should leave any backward-compatible alias/export is unspecified.
16. Other importers of the old parse paths or error types outside the three modules and listed tests are not enumerated; scope says only those three modules, so breaking them would be silent.
17. "no caching" — whether an existing cache exists to delete, or this is only a constraint on new code, is unspecified.
18. Exact "malformed shape" test cases to cover are undefined beyond examples.
19. How "reads the snapshot only through `read_graph_snapshot`" is verified (grep vs review) is unspecified.
20. Whether `read_graph_snapshot` should accept `str | Path` (CLI may pass strings) is unspecified.
21. The doc gives resolved decisions about promotion/commit but no run-dir or task-promotion path value, so the executor cannot complete those steps if any fall to it.
