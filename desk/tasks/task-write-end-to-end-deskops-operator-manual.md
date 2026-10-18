---
id: task-write-end-to-end-deskops-operator-manual
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
- source:drawer
current_node: ritual-execution
history: []
references: []
depends_on: []
pills:
- desk/contexts/pill-operator-manual-follows-stable-runnable-slices.md
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
- desk/contexts/pill-cli-gaps-become-tracked-work.md
files: []
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Write end-to-end deskops operator manual

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Consolidate the methodology into one operational playbook after runnable slices are stable.

## Scope

_State what is in scope and what is out of scope._

Coordinator decision (2026-10-18): the manual lives at docs/operator-manual.md. It is for both agents and people who operate a desk. It walks every CLI verb end to end, with examples. Those examples are executable: a test in tests/ (not tests/e2e_agent/, which the coordinator owns) extracts the fenced shell examples from docs/operator-manual.md and runs them in order in a sandbox desk, so the manual cannot drift from the CLI. Out of scope: re-documenting sldb.

## Implementation Path

_Outline the expected implementation route or affected surface._

Promoted from desk/drawer/tasks/task-write-end-to-end-operator-manual.md.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
