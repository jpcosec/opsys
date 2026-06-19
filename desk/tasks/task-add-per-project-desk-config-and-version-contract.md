---
id: task-add-per-project-desk-config-and-version-contract
status: active
references:
- desk/drawer/tasks/task-add-per-project-desk-config-and-version-contract.md
depends_on: []
pills: []
files: []
routine: routine-task-add-per-project-desk-config-and-version-contract
checklists:
- checklist-task-add-per-project-desk-config-and-version-contract-execution-ready
- checklist-task-add-per-project-desk-config-and-version-contract-testing-ready
- checklist-task-add-per-project-desk-config-and-version-contract-closeout-ready
current_node: checklist-task-add-per-project-desk-config-and-version-contract-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
- source:drawer
---

# Add per-project desk config and version contract

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Give each project desk one explicit local configuration contract that declares desk identity, desk/version expectations, and per-project testing defaults such as sandbox behavior.

## Scope

_State what is in scope and what is out of scope._

- tracked project config for shared desk behavior
- optional local override file for machine-specific settings
- explicit desk format or migration version
- explicit model/workflow expectation version fields
- per-project testing sandbox policy instead of shell-global heuristics
- interaction with environment overrides and explicit CLI flags

## Implementation Path

_Outline the expected implementation route or affected surface._

Promoted from desk/drawer/tasks/task-add-per-project-desk-config-and-version-contract.md.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
