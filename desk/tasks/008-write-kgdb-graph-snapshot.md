# Write KGDB graph snapshot

ID: task-008-write-kgdb-graph-snapshot

## Goal

Combine extracted nodes and declared edges into a KGDB-compatible graph snapshot or a clearly documented blocker if KGDB vocabulary support is not ready.

## Scope

- Use the current KGDB graph shape when possible.
- Write generated output to an ignored runtime path.
- Keep small versioned fixtures separate from runtime output.

## Output

- Add `deskops/graph/snapshot.py` or equivalent focused module.
- Add `tests/test_graph_snapshot.py`.
- Generated runtime output path: `.sldb/runtime/knowledge_graph.kg.json` unless a blocker requires changing it.

## Pills

- `desk/contexts/pill-007-phase-gated-task-flow.md`
- `desk/contexts/pill-008-kgdb-sldb-boundary.md`
- `desk/contexts/pill-010-graph-runtime-output-policy.md`

## Done When

- A graph snapshot can be produced from this repo.
- The output path policy is explicit and validated.
- If KGDB cannot ingest it yet, the blocker points to the relevant KGDB task.

## Validation

- Unit test for snapshot shape.
- KGDB ingest smoke test when available.
- Atom tests still pass.

## Tags

- system:deskops
- system:kgdb
- topic:knowledge-graph
