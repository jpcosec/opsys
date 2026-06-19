# Add drift check review loop

ID: task-add-drift-check-review-loop
Status: deferred
Priority: medium

## Goal

Add a review-only drift check that compares atoms, materializations, graph links, tests, diagrams, and implementation surfaces.

## Scope

- provenance-backed findings
- confidence labels
- dedupe keys
- accepted/rejected decision storage
- promotion paths to tasks, questions, or atoms

## Done When

- Drift checks produce actionable review records without mutating durable knowledge automatically.

## Suggested Pills

- `desk/contexts/pill-drift-checks-are-review-surfaces-not-mutators.md`
- `desk/contexts/pill-010-graph-runtime-output-policy.md`
- `desk/contexts/pill-011-self-reflection-noise-control.md`
