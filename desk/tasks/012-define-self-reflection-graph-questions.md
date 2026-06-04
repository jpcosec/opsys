# Define self reflection graph questions

ID: task-012-define-self-reflection-graph-questions

## Goal

Define the first small set of graph-backed self-reflection questions before implementing any automatic writing.

## Scope

- Missing atom references.
- Unlinked source files.
- Dangling generated artifacts.
- Open issues without related atoms.
- Do not create atoms or issues in this task.

## Output

- Create `docs/knowledge-graph/self-reflection-graph-questions.md`.
- Each question must include graph pattern, expected finding shape, confidence requirement, and whether later automation may create an atom, issue, or routed inbox note.

## Pills

- `desk/contexts/pill-007-phase-gated-task-flow.md`
- `desk/contexts/pill-011-self-reflection-noise-control.md`

## Done When

- The questions are documented with expected graph patterns and output shape.
- Each question states whether it produces a finding, task, issue, or atom candidate later.

## Validation

- Review against `desk/drawer/issues/issue-define-self-reflection-loop.md`.
- Atom tests still pass.

## Tags

- system:deskops
- topic:self-reflection
- topic:knowledge-graph
