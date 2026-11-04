---
# ritual-xxx
id: ritual-drawer-triage
# Ordered prose steps; not document references
steps:
- 1. Capture repo-local work directly in desk/drawer/tasks/ (inbox notes from other
  desks arrive there with deskops promote inbox-to-drawer-task).
- '2. Keep the item lightweight and future-oriented, but readable as a TaskDoc: id,
  title and status deferred.'
- 3. Separate speculative backlog items from active implementation tasks.
- 4. Route the item on desk/drawer/tasks/Board.md.
- 5. When the work is ready to execute, author a full task with deskops add task --from-drawer
  <item>; nothing promotes a drawer item into an active task.
- 6. Remove the drawer item by hand once the authored task supersedes it.
# e.g., layer:workflow, system:sldb
tags:
- system:deskops
- workspace:desk
- topic:triage
---

# Drawer triage

## Purpose

_Explain why this ritual exists._

Keep deferred work organized without mixing it into active execution.

## Trigger

_State when this ritual should start._

When a new future feature, plan, or non-immediate idea should be recorded.

## Preconditions

_List the conditions that must hold before running the ritual._

- The work is not being executed right now.
- The idea is concrete enough to deserve a written record.

## Validation

_List the checks that prove the ritual was performed correctly._

- The work is recorded under desk/drawer/tasks/, routed by desk/drawer/tasks/Board.md, and reads as a TaskDoc.
- No drawer item is treated as active execution.
- The path to execution is an authored task (deskops add task --from-drawer), not a promotion.

## Failure Modes

_List common mistakes this ritual prevents._

- Treating deferred work as if it were already active.
- Letting speculative backlog items crowd the execution surface.
- Leaving a drawer item unrouted with no promotion path.

## Completion

_Describe what completion looks like._

The deferred work is parked on the drawer board and becomes active only through a task authored with deskops add task --from-drawer.
