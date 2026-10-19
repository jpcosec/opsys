---
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-test-ci-knowledge-integrity-flow.md
# List of pill-xxx paths
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-007-phase-gated-task-flow.md
- desk/contexts/pill-durable-pill-knowledge-graduates-to-atoms-at-closeout.md
- desk/contexts/pill-phase-closeout-reconciles-pills-and-surfaces-next-work.md
- desk/contexts/pill-ready-phases-prove-dependencies-and-non-overlap.md
- desk/contexts/pill-board-routed-pills-stay-minimal-and-reusable.md
# List of ritual-xxx paths
rituals:
- desk/rituals/phase.md
- desk/rituals/execution.md
- desk/rituals/closeout.md
- desk/rituals/testing.md
# e.g., system:sldb, workspace:desk
tags:
- system:sldb
- workspace:desk
- topic:routing
---

# Desk Board

## Purpose

_Explain what this board routes and why it exists._

Route the active execution set for deskops.

## Notes

_Add short operational notes about the current routed set._

No active tasks routed.

## Task Details

_Generated from the task references above._

- Test the CI knowledge-integrity flow [draft] - scripts/ci-knowledge-check.sh <root> runs the desk integrity checks: `deskops doctor`, `sldb stores check` and `deskops graph missing`, which gate (non-zero fails), and `deskops drift check`, which is reported and does not gate because its findings are review items. A test runs the script against sandbox desks, and the GitHub workflow runs it on the repository after pytest.
