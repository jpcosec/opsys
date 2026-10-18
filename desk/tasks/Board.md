---
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-write-end-to-end-deskops-operator-manual
- desk/tasks/task-rw-f3-single-closure-path.md
- desk/tasks/task-rw-f4-graph-on-sldb-edge-index.md
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

- One closure service behind every way of closing a task [draft] - `deskops/services/closure.py` performs every closure: gates (closeout_gates), Board update, bundle removal, exactly one commit with the route's trailers, and the index entry. `closeout commit` (both routes) uses it with its CLI unchanged.
- Declared graph edges come from the sldb edge index [draft] - Edges declared by model fields come from sldb's public edge index (per the API agreed in task-rw-f4-request-sldb-unresolved-references); document nodes use one id scheme `<kind>:<id>` with `drawer_task` folded into `task`; file nodes keep `source_file:<path>`/`test_file:<path>`; `graph missing` uses sldb's unresolved-reference report. Id mapping: kinds keyed by frontmatter `id` today (atom, task, pill, board, and the rest in deskops/graph/extract_docs.py:183-193) keep `<kind>:<frontmatter id>`; `drawer_task:<path>` becomes `task:<frontmatter id>`; path-keyed kinds (doc, spec, diagram) keep `<kind>:<path>`. Old ids get no alias.
