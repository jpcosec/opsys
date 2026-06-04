# Report self reflection findings

ID: task-013-report-self-reflection-findings

## Goal

Produce reviewable self-reflection findings from graph checks without automatically writing atoms or issues.

## Scope

- Read graph output and self-reflection question definitions.
- Emit a report of findings with provenance and confidence.
- No automatic mutation of desk artifacts.

## Output

- Add `deskops/graph/self_reflection.py` or equivalent focused module.
- Add tests for report generation and duplicate suppression.
- Generated report path should be runtime-only unless explicitly promoted as a fixture.

## Pills

- `desk/contexts/pill-007-phase-gated-task-flow.md`
- `desk/contexts/pill-010-graph-runtime-output-policy.md`
- `desk/contexts/pill-011-self-reflection-noise-control.md`

## Done When

- A fixture proves a finding report can be generated.
- Duplicate findings are suppressed or clearly grouped.

## Validation

- Focused report-generation test.
- Atom tests still pass.

## Tags

- system:deskops
- topic:self-reflection
- topic:knowledge-graph
