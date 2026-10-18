---
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-message-tracks-only-in-the-target-store.md
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

- Make role prompts sldb-tracked RoleDocs with pi-agent materialization [active] - Roles become canonical sldb-tracked documents; installed pi agents become regenerated artifacts; drift is detectable via `deskops drift check`.

## Task Details

_Generated from the task references above._

- A sent note is tracked only in the target repo's store, never in the sender's [draft] - `deskops message send` and the deprecated `deskops inbox` alias, in every addressing form (--root, --repo, --to), track the delivered note only in the target repo's store, with a target-relative path. The sender's store does not change.
