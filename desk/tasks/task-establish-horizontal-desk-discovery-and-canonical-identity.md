---
id: task-establish-horizontal-desk-discovery-and-canonical-identity
status: active
references:
- desk/drawer/tasks/task-establish-horizontal-desk-discovery-and-identity.md
depends_on: []
pills: []
files: []
routine: routine-task-establish-horizontal-desk-discovery-and-canonical-identity
checklists:
- checklist-task-establish-horizontal-desk-discovery-and-canonical-identity-execution-ready
- checklist-task-establish-horizontal-desk-discovery-and-canonical-identity-testing-ready
- checklist-task-establish-horizontal-desk-discovery-and-canonical-identity-closeout-ready
current_node: checklist-task-establish-horizontal-desk-discovery-and-canonical-identity-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
- source:drawer
---

# Establish horizontal desk discovery and canonical identity

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Make desks discoverable to each other through one canonical per-project identity path, so cross-repo workflow commands can resolve sibling desks without ambiguous local heuristics.

## Scope

_State what is in scope and what is out of scope._

- define the minimal per-project desk identity contract
- decide how local desk identity relates to SLDB-backed ecosystem registration
- make repo self-discovery answer "who am I?" reliably at the current root
- make sibling desk discovery answer "where is that repo's desk?" reliably from canonical identity
- route duplicate-root and duplicate-id ambiguity into explicit failure instead of first-match guessing

## Implementation Path

_Outline the expected implementation route or affected surface._

Promoted from desk/drawer/tasks/task-establish-horizontal-desk-discovery-and-identity.md.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
