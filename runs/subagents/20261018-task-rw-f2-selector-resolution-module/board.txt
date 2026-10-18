---
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-write-end-to-end-deskops-operator-manual
- desk/tasks/task-rw-f2-selector-resolution-module.md
- desk/tasks/task-init-links-federated-models-instead-of-copying.md
- desk/tasks/task-rw-f4-request-sldb-unresolved-references.md
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

- One module resolves every desk selector [draft] - A new `deskops/desk_paths.py` implements that rule once; the four methods become one-line delegations to it.
- `deskops init` links the deskops models from their owner store instead of copying them [draft] - A store created by `deskops init` registers the deskops models as federated entries owned by the deskops store, and `deskops desk update --apply` converts an existing store's copied entries to federated ones.
- Write the sldb request for resolving bare ids and reporting unresolved references [draft] - runs/planning/sldb-request-unresolved-references.md contains a reproduction and a proposed public API for both gaps, and the coordinator's written reply is pasted into its `## Response` section.
