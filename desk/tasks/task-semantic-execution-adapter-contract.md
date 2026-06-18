---
id: task-semantic-execution-adapter-contract
status: active
references:
- desk/drawer/tasks/task-semantic-execution-adapter-contract.md
depends_on: []
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-004-opsys-boundary.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-007-phase-gated-task-flow.md
files:
- docs/semantic-execution-adapter.md
- spec/events/semantic_execution.yaml
routine: routine-task-semantic-execution-adapter-contract
checklists:
- checklist-task-semantic-execution-adapter-contract-execution-ready
- checklist-task-semantic-execution-adapter-contract-testing-ready
- checklist-task-semantic-execution-adapter-contract-closeout-ready
current_node: checklist-task-semantic-execution-adapter-contract-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
- source:drawer
---

# Semantic execution adapter contract

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20260617-212711-suggestion-semantic-execution-adapter-contract.md`.

## Scope

_State what is in scope and what is out of scope._

Capture and implement the Semantic Execution Adapter architecture slice: document the adapter boundary and add a local event contract for semantic execution requests/completions. Keep Band.ai out of deskops core; Band is only a future external adapter. Scope excludes hook execution, callbacks, worktree leases, or adapter code.

## Implementation Path

_Outline the expected implementation route or affected surface._

Add a human architecture note under docs/ and a generic event contract under spec/events/. The promoted inbox source was consumed during routing; this active task scope is authoritative.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
