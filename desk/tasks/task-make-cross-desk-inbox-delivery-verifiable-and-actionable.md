---
id: task-make-cross-desk-inbox-delivery-verifiable-and-actionable
status: active
references:
- desk/drawer/tasks/task-make-cross-desk-inbox-delivery-verifiable.md
depends_on: []
pills:
- desk/contexts/pill-cross-desk-inbox-needs-delivery-verification-and-follow-up.md
- desk/contexts/pill-canonical-desk-identity-enables-horizontal-routing.md
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
- desk/contexts/pill-cli-gaps-become-tracked-work.md
files: []
routine: routine-task-make-cross-desk-inbox-delivery-verifiable-and-actionable
checklists:
- checklist-task-make-cross-desk-inbox-delivery-verifiable-and-actionable-execution-ready
- checklist-task-make-cross-desk-inbox-delivery-verifiable-and-actionable-testing-ready
- checklist-task-make-cross-desk-inbox-delivery-verifiable-and-actionable-closeout-ready
current_node: checklist-task-make-cross-desk-inbox-delivery-verifiable-and-actionable-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
- source:drawer
---

# Make cross-desk inbox delivery verifiable and actionable

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Make cross-desk inbox communication operationally useful by ensuring the sender, target, delivery result, and follow-up path are explicit across project desks.

## Scope

_State what is in scope and what is out of scope._

- define what successful cross-desk inbox delivery must prove
- require clear sender and target identity instead of inferred ambiguity
- decide how recipients discover, acknowledge, or pull pending cross-desk updates
- design a reply or follow-up path so inbox notes do not become write-only dead drops
- identify the minimum implementation slice needed before inbox can be treated as a real horizontal coordination surface

## Implementation Path

_Outline the expected implementation route or affected surface._

Promoted from desk/drawer/tasks/task-make-cross-desk-inbox-delivery-verifiable.md.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
