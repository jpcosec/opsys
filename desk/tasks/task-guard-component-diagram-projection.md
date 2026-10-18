---
id: task-guard-component-diagram-projection
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- docs/diagrams/codebase/sldb-primitives-docs-cli-components.md
- docs/diagrams/codebase/sldb-primitives-docs-cli-components.mmd
- tests/test_diagram_projections.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Guard the SLDB components diagram projection

## Rationale

_Explain why this task exists or the business driver behind it._

`docs/diagrams/codebase/sldb-primitives-docs-cli-components.md` renders a Mermaid block that
currently matches its `.mmd` sibling, but nothing enforces that relationship. The diagram can
drift silently, and spec2viz migration is not yet available in this repo.

## Goal

_Describe the concrete result this task must produce._

Add a focused test that the rendered Markdown block equals the `.mmd` source for the components
diagram, and fix the block from the source if the test fails.

## Scope

_State what is in scope and what is out of scope._

In scope: one test and the named diagram pair. Out of scope: spec2viz YAML authoring, renderer
changes, and every other diagram pair.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Create `tests/test_diagram_projections.py`.
2. Read `docs/diagrams/codebase/sldb-primitives-docs-cli-components.mmd`.
3. Extract the first fenced ` ```mermaid ... ``` ` block from
   `docs/diagrams/codebase/sldb-primitives-docs-cli-components.md`.
4. Compare after stripping trailing whitespace on each line and the final newline.
5. If they differ, replace only the Markdown fenced block with the `.mmd` content; do not edit the
   `.mmd` source.
6. Do not add spec2viz source in this task. Record in the test docstring that spec2viz migration is
   deferred until a spec2viz source workflow exists in this repo.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_diagram_projections.py -q
- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

The components Markdown fenced block and `.mmd` source are identical, the test fails if either is
changed alone, and `pytest` is green.
