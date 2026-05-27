# Enable opsys operation over repo-local sldb desk tasks

ID: task-021
Status: active

## Goal

Make the opsys layer able to discover, route, and operate over repo-local `desk/tasks` surfaces in sibling repos so backlog state does not have to be duplicated across `issues`, `inbox`, and manual handoff notes.

## Scope

In scope: discovery of sibling repo desks, conventions for reading repo-local `desk/tasks`, and the smallest command or routing slice that proves opsys can act on that surface.

Out of scope: generalized orchestration across every desk document type, historical migration of old backlog artifacts, or pushing workflow logic back into SLDB infra.

## References

- /home/jp/proyectos/hum-ecosystem/tools/sldb/desk/tasks/task-002-export-opsys-guides.md
- /home/jp/proyectos/hum-ecosystem/tools/sldb/desk/tasks/task-003-cli-model-discovery-and-global-store.md
- /home/jp/proyectos/hum-ecosystem/tools/sldb/docs/workspaces.md
- desk/inbox/20260526-000000-suggestion-opsys-not-ready-for-sldb-desk-tasks.md
- desk/contexts/pill-004-opsys-boundary.md

## Dependencies

- 

## Pills

- pill-004
- pill-006
- pill-007

## Files

- desk/cli/commands/repo.py
- desk/cli/commands/desk.py
- desk/cli/commands/inbox.py
- desk/tasks/Board.md

## Implementation Path

Start by defining one unambiguous downstream convention: how opsys locates a sibling repo desk and which task files count as the active source of truth.

Then add the smallest routed command or board-facing slice that can list or attach those repo-local task docs without copying them into opsys-owned backlog storage.

Treat the current local repo name mismatch between conceptual `opsys` and concrete `deskops` as part of the routing problem, not as something for SLDB to solve.

## Validation

- prove the chosen convention against the sibling `sldb` repo in this workspace
- verify that opsys can resolve `sldb/desk/tasks/Board.md` and its active task docs without manual duplication
- keep the resulting behavior compatible with pill-004 boundary rules

## Done When

Opsys has a concrete, documented way to operate over repo-local `desk/tasks` in sibling repos, and the `sldb` handoff no longer depends only on manual inbox notes.

## Tags

- system:sldb
- system:opsys
- workspace:desk
- topic:routing
- topic:tasks
