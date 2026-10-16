---
id: task-rw-f4-single-snapshot-reader
status: deferred
references: []
depends_on:
- task-rw-f4-graph-on-sldb-edge-index
- task-rw-f1-output-golden-files
pills:
- desk/contexts/pill-011-self-reflection-noise-control.md
- desk/contexts/pill-010-graph-runtime-output-policy.md
files:
- deskops/graph/snapshot.py
- deskops/graph/checks.py
- deskops/graph/self_reflection.py
- tests/test_graph_snapshot.py
- deskops/cli/main.py
- tests/test_graph_checks.py
- tests/test_graph_self_reflection.py
task_type: implementation
tags:
- workspace:desk
- artifact:task
- source:drawer
- plan:deskops-rewrite
- phase:f4
- topic:graph
---

# One reader for the graph snapshot

## Rationale

_Explain why this task exists or the business driver behind it._

Inventory finding S5: snapshot.py, checks.py and self_reflection.py in deskops/graph/ each parse the snapshot JSON with different keys and different errors (`GraphSnapshotReadError`, defined at snapshot.py:29 and raised at 53 and 58; `GraphMissingCheckError`, defined at checks.py:13, raised at 42 and caught by the CLI at cli/main.py:292 and 329; raw `JSONDecodeError` elsewhere).

Plan: phase F4 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

`deskops.graph.snapshot.read_graph_snapshot(path: Path) -> GraphSnapshot` (dataclasses `GraphSnapshot(nodes, edges)`, `Node(id, kind=None, path=None, identity=None, label=None)` with `identity` kept raw (dict or str, as stored), `Edge(source, target, role='related', provenance_path=None, provenance_locator=None, extractor=None)`, no caching) is the only snapshot parser; it raises `GraphSnapshotReadError` for a missing file, invalid JSON or a missing key; checks.py and self_reflection.py use it. The snapshot `graph build` writes has top-level `version`, `nodes` and `metadata` and nests each node's outgoing edges in `nodes[].edges` (snapshot.py:85-101); the reader flattens those into `GraphSnapshot.edges`, and also accepts a top-level `edges` list if present. Required: the `nodes` list, each node's id (`id` or `identity.node_id`), and each edge's target (`target` or `target_id`; its source is the enclosing node when nested); every other field is optional with the defaults above. Any other malformed shape (a non-list, a non-dict item) also raises `GraphSnapshotReadError`. checks.py's own `read_graph_snapshot` (checks.py:40) is removed; checks.py catches `GraphSnapshotReadError` from the snapshot reader and re-raises `GraphMissingCheckError` with the same message (`raise ... from exc`), so `_graph_missing`'s `except GraphMissingCheckError` (cli/main.py:292) keeps working; `_graph_reflect` (cli/main.py:321-333) reads the snapshot itself, so its `except` must also catch `GraphSnapshotReadError` (tests/test_graph_cli.py:233-240). Callers of the removed function (cli/main.py:321, self_reflection.py:422) and tests that pass raw dicts (tests/test_graph_checks.py:23,47, tests/test_graph_self_reflection.py:53,165) are updated: the check functions accept a `GraphSnapshot`.

## Scope

_State what is in scope and what is out of scope._

In scope: the three modules and their tests. `read_graph_neighbors` keeps its signature and its output dicts byte-for-byte (keys node/incoming/outgoing/nodes and each node's `label`, which `deskops graph neighbors` prints, cli/main.py:341-364, tests/test_graph_cli.py:28,273); for that `Node` also carries `label: str | None` (semantics title, else label, else id, as snapshot.py:142 computes today). Out of scope: the snapshot format.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Add the dataclasses and reader to snapshot.py; add reader tests (missing file, bad JSON, missing key, malformed shape, a valid snapshot) to the existing tests/test_graph_snapshot.py.
2. Port checks.py and self_reflection.py.
3. The golden snapshot test stays green.

## Validation

_List the checks required before this task can close._

- pytest tests/test_graph_snapshot.py tests/test_graph_checks.py tests/test_graph_self_reflection.py tests/test_output_goldens.py
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

`def read_graph_snapshot` exists only in deskops/graph/snapshot.py, checks.py and self_reflection.py contain no `json.load`/`json.loads` of the snapshot file (self_reflection.py:152 reads the separate decisions file and stays), the new reader tests pass, and `pytest tests` is green.

## Resolved Decisions

- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
