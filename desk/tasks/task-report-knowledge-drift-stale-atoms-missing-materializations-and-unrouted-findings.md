---
id: task-report-knowledge-drift-stale-atoms-missing-materializations-and-unrouted-findings
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
routine: routine-task-report-knowledge-drift-stale-atoms-missing-materializations-and-unrouted-findings
current_node: checklist-task-report-knowledge-drift-stale-atoms-missing-materializations-and-unrouted-findings-testing-ready
history:
- operator-task-report-knowledge-drift-stale-atoms-missing-materializations-and-unrouted-findings-activate
references: []
depends_on: []
pills: []
files: []
checklists:
- checklist-task-report-knowledge-drift-stale-atoms-missing-materializations-and-unrouted-findings-execution-ready
- checklist-task-report-knowledge-drift-stale-atoms-missing-materializations-and-unrouted-findings-testing-ready
- checklist-task-report-knowledge-drift-stale-atoms-missing-materializations-and-unrouted-findings-closeout-ready
task_type: feature
inherits_from: []
inherit_acceptance_context: false
atoms: []
closeout_evidence_verified: false
pill_graduation_verified: true
---

# Report knowledge drift: stale atoms, missing materializations and unrouted findings

## Rationale

_Explain why this task exists or the business driver behind it._

desk/drawer/issues/issue-add-knowledge-drift-check-routine.md (which now also holds the knowledge-surface closeout check and the self-reflection loop): nothing asks whether a change made an atom stale, left a materialization pointing at something gone, or produced knowledge no atom carries. The workflow relies on an agent noticing.

## Goal

_Describe the concrete result this task must produce._

A drift command that reports, from the desk and the graph: atoms whose declared targets or materializations no longer resolve, documents that point at atoms with no inbound trace, and graph findings that no atom or issue covers.

## Scope

_State what is in scope and what is out of scope._

The drift surface and a routine doc describing when to run it. Starts as a review report; it must not mutate the desk.

## Implementation Path

_Outline the expected implementation route or affected surface._

deskops/cli/commands/drift.py exists and already reports some of this; extend it and deskops/graph/self_reflection.py rather than adding a parallel command. desk/drawer/issues/issue-drift-checks-are-review-surfaces-not-mutators.md's atom is the rule: report, never repair. Add the routine under desk/routines/ if the workflow needs one.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_cli.py -q

## Done When

_Name the observable condition that makes the task complete._

deskops drift check reports each of the three conditions on a desk built to have them, and leaves the desk untouched.
