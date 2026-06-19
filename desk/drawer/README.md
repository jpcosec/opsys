# Drawer (opsys)

This guide is a human-facing materialization of these atoms:

- `desk/atoms/workflow-model/atom-docs-are-human-facing-atom-materializations.md`
- `desk/atoms/workflow-model/atom-drawer-is-not-active-work.md`
- `desk/atoms/workflow-model/atom-drawers-feed-tasks-through-promotion.md`
- `desk/atoms/workflow-model/atom-inbox-is-coordination-intake.md`

`desk/drawer/` holds deferred opsys workflow-domain work that should not enter active execution yet.

It is the place for internal planning and deferred work. Do not use `desk/inbox/` as an agent scratchpad for future work; inbox is for messages addressed to the project and records the sending project.

Use it for:

- future features
- backlog plans
- ideas that still need shaping before they become desk tasks

## Surfaces

- `desk/drawer/features/` holds deferred feature documents.
- `desk/drawer/attention/` holds inbox items that need human attention before they can be promoted, rejected, or deleted.
- `desk/drawer/questions/` holds unresolved workflow/model questions before they become tasks, atoms, docs, specs, diagrams, or rituals.
- `desk/drawer/rituals/` holds deferred ritual drafts before they are promoted into active `desk/rituals/` or decomposed into routines and hooks.
- `desk/drawer/tasks/Board.md` routes deferred items without promoting them into execution.

## Rule

Work in `desk/drawer/` is not currently executing.

When a drawer item becomes real implementation work, promote it into the active surfaces of `desk/` and bind it to the execution rituals there.
