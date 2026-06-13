---
id: board-001
scope: desk
tasks: []
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-002-test-real-cli-surfaces.md
- desk/contexts/pill-003-capture-cli-gaps.md
- desk/contexts/pill-004-opsys-boundary.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-006-self-described-store-layout.md
- desk/contexts/pill-007-phase-gated-task-flow.md
- desk/contexts/pill-008-kgdb-sldb-boundary.md
- desk/contexts/pill-009-source-file-graph-traceability.md
- desk/contexts/pill-010-graph-runtime-output-policy.md
- desk/contexts/pill-011-self-reflection-noise-control.md
rituals:
- desk/rituals/execution.md
- desk/rituals/closeout.md
- desk/rituals/testing.md
tags:
- system:sldb
- workspace:desk
- topic:routing
---

# Desk Board

## Purpose

Route the active desk execution set: tasks, pills, and the ritual documents that govern execution and closure.

## Notes

Every closed task must end in its own closing commit. Every non-trivial task must pass explicit initialization, execution, testing, and closeout gates. Any missing SLDB capability discovered during execution must become a new active desk task.

The obsolete proposed task set `046-052` has been distilled into drawer issues because it assumed the old atom model. Promote only the revised issues that match the current `AtomDoc`, sldb composition, and workflow-derived CLI model.
