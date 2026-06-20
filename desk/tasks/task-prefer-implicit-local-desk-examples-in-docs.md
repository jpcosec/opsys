---
id: task-prefer-implicit-local-desk-examples-in-docs
status: active
references:
- desk/drawer/tasks/task-prefer-implicit-local-desk-examples.md
depends_on: []
pills:
- desk/contexts/pill-operational-cli-grammar-follows-spoken-workflow.md
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
- desk/contexts/pill-cli-gaps-become-tracked-work.md
files:
- AGENTS.md
- docs/faq.md
- docs/quickstart.md
- desk/drawer/rituals/knowledge-distillation-pass.md
- desk/tasks/Board.md
routine: routine-task-prefer-implicit-local-desk-examples-in-docs
checklists:
- checklist-task-prefer-implicit-local-desk-examples-in-docs-execution-ready
- checklist-task-prefer-implicit-local-desk-examples-in-docs-testing-ready
- checklist-task-prefer-implicit-local-desk-examples-in-docs-closeout-ready
current_node: checklist-task-prefer-implicit-local-desk-examples-in-docs-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
- source:drawer
---

# Prefer implicit local-desk examples in docs

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Update operator-facing guidance so commands run from the repo root prefer the implicit local-desk default instead of spelling `--root .` everywhere, while keeping explicit-root examples where cross-repo, sandbox, or unusual targeting matters.

## Scope

_State what is in scope and what is out of scope._

- adjust local-repo examples in README/docs/agent guidance
- keep explicit `--root` only where override behavior is the point
- preserve clarity for graph, cross-repo, and sandbox guidance where explicit targeting still helps

## Implementation Path

_Outline the expected implementation route or affected surface._

Promoted from desk/drawer/tasks/task-prefer-implicit-local-desk-examples.md.

Prefer implicit local-desk command examples whenever the operator is already at the repo root, while preserving explicit root targeting where the example is specifically about alternate workspaces, cross-repo actions, or scripted disambiguation.

## Validation

_List the checks required before this task can close._

- python -m deskops list tasks
- python -m deskops list pills
- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
