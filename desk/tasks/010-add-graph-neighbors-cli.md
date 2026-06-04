# Add graph neighbors CLI

ID: task-010-add-graph-neighbors-cli

## Goal

Expose neighborhood lookup for one graph node through the deskops CLI.

## Candidate Command

```bash
deskops graph neighbors <id>
```

## Scope

- Read an existing graph snapshot.
- Show incoming and outgoing neighbors for one node.
- Do not implement trace or missing checks.

## Output

- Extend graph CLI support with `deskops graph neighbors <id>`.
- Add focused CLI tests using `tests/fixtures/knowledge_graph/static_desk_source_graph.json`.

## Pills

- `desk/contexts/pill-003-capture-cli-gaps.md`
- `desk/contexts/pill-007-phase-gated-task-flow.md`
- `desk/contexts/pill-008-kgdb-sldb-boundary.md`

## Done When

- CLI test proves known fixture neighbors are displayed.
- Missing graph file and missing node cases are handled clearly.

## Validation

- Focused CLI test.
- Manual CLI smoke test.

## Tags

- system:deskops
- system:kgdb
- topic:cli
