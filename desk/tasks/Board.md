---
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-write-end-to-end-deskops-operator-manual
- desk/tasks/task-rw-f3-single-closure-path.md
- desk/tasks/task-rw-f4-single-snapshot-reader.md
# List of pill-xxx paths
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-007-phase-gated-task-flow.md
- desk/contexts/pill-durable-pill-knowledge-graduates-to-atoms-at-closeout.md
- desk/contexts/pill-phase-closeout-reconciles-pills-and-surfaces-next-work.md
- desk/contexts/pill-ready-phases-prove-dependencies-and-non-overlap.md
- desk/contexts/pill-board-routed-pills-stay-minimal-and-reusable.md
# List of ritual-xxx paths
rituals:
- desk/rituals/phase.md
- desk/rituals/execution.md
- desk/rituals/closeout.md
- desk/rituals/testing.md
# e.g., system:sldb, workspace:desk
tags:
- system:sldb
- workspace:desk
- topic:routing
---

# Desk Board

## Purpose

_Explain what this board routes and why it exists._



## Notes

_Add short operational notes about the current routed set._

- Make role prompts sldb-tracked RoleDocs with pi-agent materialization [active] - Roles become canonical sldb-tracked documents; installed pi agents become regenerated artifacts; drift is detectable via `deskops drift check`.

## Task Details

_Generated from the task references above._

- One closure service behind every way of closing a task [draft] - `deskops/services/closure.py` performs every closure: gates (closeout_gates), Board update, bundle removal, exactly one commit with the route's trailers, and the index entry. `closeout commit` (both routes) uses it with its CLI unchanged.
- One reader for the graph snapshot [draft] - `deskops.graph.snapshot.read_graph_snapshot(path: Path) -> GraphSnapshot` (dataclasses `GraphSnapshot(nodes, edges)`, `Node(id, kind=None, path=None, identity=None, label=None)` with `identity` kept raw (dict or str, as stored), `Edge(source, target, role='related', provenance_path=None, provenance_locator=None, extractor=None)`, no caching) is the only snapshot parser; it raises `GraphSnapshotReadError` for a missing file, invalid JSON or a missing key; checks.py and self_reflection.py use it. The snapshot `graph build` writes has top-level `version`, `nodes` and `metadata` and nests each node's outgoing edges in `nodes[].edges` (snapshot.py:85-101); the reader flattens those into `GraphSnapshot.edges`, and also accepts a top-level `edges` list if present. Required: the `nodes` list, each node's id (`id` or `identity.node_id`), and each edge's target (`target` or `target_id`; its source is the enclosing node when nested); every other field is optional with the defaults above. Any other malformed shape (a non-list, a non-dict item) also raises `GraphSnapshotReadError`. checks.py's own `read_graph_snapshot` (checks.py:40) is removed; checks.py catches `GraphSnapshotReadError` from the snapshot reader and re-raises `GraphMissingCheckError` with the same message (`raise ... from exc`), so `_graph_missing`'s `except GraphMissingCheckError` (cli/main.py:292) keeps working; `_graph_reflect` (cli/main.py:321-333) reads the snapshot itself, so its `except` must also catch `GraphSnapshotReadError` (tests/test_graph_cli.py:233-240). Callers of the removed function (cli/main.py:321, self_reflection.py:422) and tests that pass raw dicts (tests/test_graph_checks.py:23,47, tests/test_graph_self_reflection.py:53,165) are updated: the check functions accept a `GraphSnapshot`.
