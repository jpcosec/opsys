# Add graph missing check

ID: task-011-add-graph-missing-check

## Goal

Add the first graph consistency check that reports missing declared targets or dangling graph references.

## Candidate Command

```bash
deskops graph missing
```

## Scope

- Missing target nodes for declared edges.
- Dangling source atom references.
- No stale materialization or self-reflection writing yet.

## Output

- Add `deskops/graph/checks.py` or equivalent focused module.
- Add CLI support for `deskops graph missing` only if the graph CLI exists; otherwise add a unit-level checker and record the CLI dependency.
- Add tests for one dangling edge and one clean graph.

## Pills

- `desk/contexts/pill-007-phase-gated-task-flow.md`
- `desk/contexts/pill-009-source-file-graph-traceability.md`
- `desk/contexts/pill-011-self-reflection-noise-control.md`

## Done When

- A fixture with one dangling edge produces a finding.
- The command reports findings without mutating atoms/issues.

## Validation

- Focused CLI or unit test.
- Atom tests still pass.

## Tags

- system:deskops
- system:kgdb
- topic:validation
