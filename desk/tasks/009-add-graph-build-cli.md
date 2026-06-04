# Add graph build CLI

ID: task-009-add-graph-build-cli

## Goal

Expose graph snapshot generation through one CLI command.

## Candidate Command

```bash
deskops graph build
```

## Scope

- Build only. No neighbor, trace, or missing checks in this task.
- Delegate extraction and snapshot writing to the graph adapter code.

## Output

- Add or update CLI command registration for `deskops graph build`.
- Add `tests/test_graph_cli.py` or extend an existing CLI test file with only build-command tests.

## Pills

- `desk/contexts/pill-003-capture-cli-gaps.md`
- `desk/contexts/pill-007-phase-gated-task-flow.md`
- `desk/contexts/pill-010-graph-runtime-output-policy.md`

## Done When

- CLI test proves the command creates or reports the graph output path.
- Missing KGDB/SLDB capabilities produce explicit routed issues or clear error messages.

## Validation

- Focused CLI test.
- Manual `deskops graph build` smoke test.

## Tags

- system:deskops
- system:kgdb
- topic:cli
