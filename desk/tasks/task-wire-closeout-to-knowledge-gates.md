---
id: task-wire-closeout-to-knowledge-gates
status: active
references: []
depends_on: []
pills:
- desk/contexts/pill-closeout-knowledge-gates-require-traceable-evidence.md
- desk/contexts/pill-durable-pill-knowledge-graduates-to-atoms-at-closeout.md
- desk/contexts/pill-materialization-contracts-declare-source-intent-and-target.md
- desk/contexts/pill-atom-lifecycle-preserves-provenance-and-materialization-links.md
files: []
routine: routine-task-wire-closeout-to-knowledge-gates
checklists:
- checklist-task-wire-closeout-to-knowledge-gates-execution-ready
- checklist-task-wire-closeout-to-knowledge-gates-testing-ready
- checklist-task-wire-closeout-to-knowledge-gates-closeout-ready
current_node: checklist-task-wire-closeout-to-knowledge-gates-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
- source:drawer
---

# Wire closeout to knowledge gates

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Make closeout check tests, atoms, graph links, materialization status, cleanup, and commit evidence before work leaves the active desk.

## Scope

_State what is in scope and what is out of scope._

- relevant tests pass
- changed files have atom/materialization links or routed follow-up work
- generated artifacts declare sources
- stale tasks/pills are deleted or promoted
- dedicated commit exists

## Resolved Decisions

Supervisor rulings (this task OWNS closeout evidence aggregation):

- Add a `deskops closeout verify --task <id> [--root]` surface that runs the evidence predicate and exits non-zero when a required gate is unmet, so the gate is enforced at commit time (not only during advance).
- Aggregation: keep the existing per-reference resolution (atom OR test OR commit) but expose a structured report of WHICH gates are satisfied (tests / atom-or-materialization link / commit). Do NOT silently tighten the existing advance-time any-of gate this pass (avoid breaking all in-flight tasks); the new `verify` surface is the strict all-of check operators run before the tool-made commit.
- 'changed files have links': check via graph materialization edges + atom references; if none, require a routed follow-up reference. Reference-resolution only (reuse Wave A materialization validation); no drift comparison (owned by drift-check task).
- 'generated artifacts declare sources': a rendered artifact with a sibling source but no declared source_atoms/provenance is a verify finding.
- pill->atom graduation item is OUT (owned by the enforce-pill-to-atom task); consume its `pill_graduation_verified` field if present but do not redefine it.
- Capture durable rule as atom(s) under desk/atoms/workflow-model/; reflect in desk/rituals/closeout.md.

## Implementation Path

_Outline the expected implementation route or affected surface._

deskops/cli/commands/closeout.py + parser.py: add 'closeout verify'; predicate helpers in operations.py; atom + closeout.md; tests in tests/test_closeout.py.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
