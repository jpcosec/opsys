---
id: task-detect-and-migrate-legacy-desk-workspaces
status: active
references:
- desk/drawer/tasks/task-detect-and-migrate-legacy-desk-workspaces.md
depends_on: []
pills:
- desk/contexts/pill-legacy-desk-formats-need-explicit-adaptation.md
- desk/contexts/pill-doctor-separates-desk-repair-from-sldb-health.md
- desk/contexts/pill-list-surfaces-must-expose-malformed-docs.md
- desk/contexts/pill-project-local-config-carries-version-and-sandbox-policy.md
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
files: []
routine: routine-task-detect-and-migrate-legacy-desk-workspaces
checklists:
- checklist-task-detect-and-migrate-legacy-desk-workspaces-execution-ready
- checklist-task-detect-and-migrate-legacy-desk-workspaces-testing-ready
- checklist-task-detect-and-migrate-legacy-desk-workspaces-closeout-ready
current_node: checklist-task-detect-and-migrate-legacy-desk-workspaces-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
- source:drawer
---

# Detect and migrate legacy desk workspaces

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Make deskops detect legacy or hand-rolled desk layouts explicitly and provide a safe adaptation path into the current modeled workspace contract.

## Scope

_State what is in scope and what is out of scope._

- detect legacy `desk/` layouts whose board, task, pill, or ritual docs do not satisfy current deskops models
- distinguish empty/fresh desks from incompatible/legacy desks
- report which current modeled surfaces are missing or malformed
- define a migration or adoption path for legacy boards, tasks, pills, and contexts
- preserve user-authored legacy content instead of overwriting it blindly
- clarify how this interacts with per-project config and desk/version contracts

## Implementation Path

_Outline the expected implementation route or affected surface._

Promoted from desk/drawer/tasks/task-detect-and-migrate-legacy-desk-workspaces.md.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
