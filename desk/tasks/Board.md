---
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-write-end-to-end-deskops-operator-manual
- desk/tasks/task-rw-f3-closeout-gates-service.md
- desk/tasks/task-rw-f3-drawer-entry-removal-verb.md
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

- Closeout gates move to a service and verify real evidence [draft] - `deskops/services/closeout_gates.py` owns the gates and the closeout graph context; the commit gate accepts only a 7-40 character lowercase hex id that resolves to a commit that is HEAD or an ancestor of it (existing tests pass HEAD's own hash, tests/test_closeout.py:335 and tests/test_lifecycle_end_to_end.py:126); the tests gate accepts only a `.py` path inside `<root>/tests/` (optionally followed by `::node`, whose node part is not validated) that exists.
- A CLI verb removes a drawer entry [draft] - The approved verb removes one drawer file, untracks it if tracked, and deletes every Board.md bullet that starts with ``- `<its stem>` ``.
