---
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-write-end-to-end-deskops-operator-manual.md
- desk/tasks/task-anti-pattern-monolithic-api-endpoint-in-sldb-viewer.md
- desk/tasks/task-track-generated-task-bundles-in-the-sldb-store-on-add-and-promote.md
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



## Notes

_Add short operational notes about the current routed set._

- Write end-to-end deskops operator manual [deferred] - Consolidate the methodology into one operational playbook after runnable slices are stable.
- Anti-pattern: Monolithic API endpoint in SLDB Viewer [draft] - Ensure we never couple independent SLDB surfaces into monolithic UI API endpoints.
- Fix sldb<->deskops CLI drift breaking 11 tests [draft] - Restore green deskops CLI test suite by realigning deskops to the current sldb CLI API and fixing the TaskDoc render expectation drift.
- Track generated task bundles in the sldb store on add and promote [draft] - deskops add task and promote track every generated bundle document in the .sldb store at creation time, like repo register does

## Task Details

_Generated from the task references above._

- Write end-to-end deskops operator manual [deferred] - Consolidate the methodology into one operational playbook after runnable slices are stable.
- Anti-pattern: Monolithic API endpoint in SLDB Viewer [draft] - Ensure we never couple independent SLDB surfaces into monolithic UI API endpoints.
