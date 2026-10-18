---
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-write-end-to-end-deskops-operator-manual
- desk/tasks/task-closeout-commit-leaves-the-run-index-clean.md
- desk/tasks/task-rename-deskops-faqdoc.md
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

- `closeout commit` leaves the run index clean [draft] - After `deskops closeout commit` (both --run-dir and --no-run) the working tree is clean, and runs/subagents/index.jsonl still records the closing commit's hash.
- deskops' FAQ model gets its own name instead of `FAQDoc` [draft] - The deskops FAQ model has a distinct name (for example `DeskFAQDoc`), and every store that tracks FAQ documents with the old name is migrated, with `sldb stores check` PASS.
