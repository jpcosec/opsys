---
id: task-enforce-pill-to-atom-knowledge-graduation-during-task-closeout
status: active
references: []
depends_on: []
pills:
- desk/contexts/pill-durable-pill-knowledge-graduates-to-atoms-at-closeout.md
- desk/contexts/pill-closeout-knowledge-gates-require-traceable-evidence.md
files: []
routine: routine-task-enforce-pill-to-atom-knowledge-graduation-during-task-closeout
checklists:
- checklist-task-enforce-pill-to-atom-knowledge-graduation-during-task-closeout-execution-ready
- checklist-task-enforce-pill-to-atom-knowledge-graduation-during-task-closeout-testing-ready
- checklist-task-enforce-pill-to-atom-knowledge-graduation-during-task-closeout-closeout-ready
current_node: checklist-task-enforce-pill-to-atom-knowledge-graduation-during-task-closeout-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
- source:drawer
---

# Enforce pill-to-atom knowledge graduation during task closeout

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Make task closeout verify that durable knowledge discovered through pills is promoted into atoms before transient execution context is deleted.

## Scope

_State what is in scope and what is out of scope._

- define how closeout distinguishes transitional pill context from durable residue
- require pill audit during closeout for bugfix, feature, and migration tasks
- record or verify atom updates when a task refined project rulings or reusable patterns
- avoid forcing atom updates when a pill only routed already-existing knowledge
- integrate the rule with task deletion, pill cleanup, and closeout evidence

## Resolved Decisions

Supervisor rulings (frontier vs the wire-closeout task, which owns evidence aggregation):

- Mechanism: a soft, AFFIRMED closeout checklist item, NOT a hard heuristic gate. "Durable vs transitional" is not machine-detectable, so do not auto-block on it.
- This task OWNS only: adding `condition-<task>-pill-knowledge-graduated` + wiring it into `checklist-<task>-closeout-ready` as an affirmable item, plus the payload field `pill_graduation_verified` populated in advance_task. When the task has zero bound pills, the item passes trivially.
- The all-of evidence aggregation (test AND link AND commit) is OUT (owned by wire-closeout-to-knowledge-gates).
- Evidence form: reuse existing `references` list; an atom reference satisfies graduation. No new dedicated field.
- Scope by presence of bound pills (not by task_type; task_type default when unset would over-block).
- Capture the durable rule as an atom under desk/atoms/workflow-model/ first, then reflect in desk/rituals/closeout.md and the workspace _closeout_template.
- Keep this at task closeout only; phase-level pill reconciliation is already handled by the phase ritual.

## Implementation Path

_Outline the expected implementation route or affected surface._

deskops/operations.py: add pill_graduation_verified payload + condition + closeout checklist item; atom + closeout.md + _closeout_template; tests in tests/test_operational.py.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
