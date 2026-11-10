---
id: task-scion-autonomy-coordinator-contract
status: deferred
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ''
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Scion autonomy: consistent coordinator/executor/tester contract

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Owner authorization 2026-11-10: make the system recover a current desk, choose an
authorized ready unowned task, review it, dispatch, independently test, close and
continue without handholding. Scion owns runtime; DeskOps owns task gates. No
pi-subagents or second runtime scheduler.

Fix the source RoleDoc and generated Scion instructions, not only installed files.
Resolve the conflict between read-only bash and workflow mutation/closeout duties.
Permit routine clarifications from task/source evidence; escalate only unresolved
owner decisions, conflicting authorization or actual ownership conflicts.
Read configured current desk and tool source, use exact CLI syntax and explicit
project/auth/workspace when dispatching. Check current review/dependency/phase
gates and ownership before dispatch; skip blocked/owned tasks and consider the
remaining ready ones. Persist/reconcile stable run identity before dispatch so a
restart does not create a duplicate. Require separate tester and explicit failed
validation recovery. Finish the current phase gate before selecting another.

Bounded deliverable: coherent role/template contract, including tester templates
and executable command examples. Do not replace the lifecycle engine or introduce
a broad new framework. Code enforcement beyond existing gates must be explicit,
not claimed from prose tests. Capture durable rules in atoms before docs.

Files: deskops/runtime/scion.py, deskops/cli/registry.py if tester mode requires it,
desk/roles/deskops-supervisor.md, relevant new atom(s), tests/test_scion_runtime.py,
relevant CLI help golden if needed, docs/operator-manual.md, CHANGELOG.md.
Validation: focused template/runtime tests and real unattended integration after
the runtime bridge is installed. Depends on review-status correction.

## Scope

_State what is in scope and what is out of scope._

Historical drawer source; the separately authored active task owns implementation and closeout.

## Implementation Path

_Outline the expected implementation route or affected surface._

Use the authored task implementation contract.

## Validation

_List the checks required before this task can close._

-

## Done When

_Name the observable condition that makes the task complete._

Preserve the source candidate; the authored task owns execution and closeout.
