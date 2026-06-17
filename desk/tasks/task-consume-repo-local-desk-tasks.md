# Consume repo-local desk tasks across the ecosystem

ID: task-consume-repo-local-desk-tasks
Status: active
Priority: medium

## Goal

Make deskops able to discover and route repo-local `desk/tasks` surfaces from sibling projects without manual synchronization.

## Scope

- Define how deskops discovers sibling repo desks.
- Define the naming story for the conceptual opsys layer versus the `deskops` repo.
- Consume or route repo-local desk tasks without pushing workflow-specific assumptions into SLDB.

## Pills

- `desk/contexts/pill-004-opsys-boundary.md`
- `desk/contexts/pill-006-self-described-store-layout.md`
- `desk/contexts/pill-007-phase-gated-task-flow.md`
- `desk/contexts/pill-008-kgdb-sldb-boundary.md`

## Source Inbox Notes

- `20260526-000000-suggestion-opsys-not-ready-for-sldb-desk-tasks.md`

## Done When

- Deskops has a documented and testable path for routing sibling repo desk tasks.
- Manual synchronization remains a fallback, not the primary operating mode.
