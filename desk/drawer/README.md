# Drawer

This guide is a human-facing materialization of these atoms:

- `desk/atoms/workflow-model/atom-docs-are-human-facing-atom-materializations.md`
- `desk/atoms/workflow-model/atom-drawer-is-not-active-work.md`
- `desk/atoms/workflow-model/atom-drawers-feed-tasks-through-promotion.md`
- `desk/atoms/workflow-model/atom-inbox-is-coordination-intake.md`

`desk/drawer/` holds deferred opsys workflow-domain work that should not enter active execution yet.

## Remaining surfaces

- `desk/drawer/tasks/Board.md` — routes the deferred task backlog (`desk/drawer/tasks/`); the board lists every deferred task.
- `desk/drawer/plans/` — deferred plans with their own DAG and review evidence (`workspace-documental/`).

## Retired surfaces

The covered use-cases and stress-tests were retired on 2026-10-19 because their flows are exercised by the test suite; each retirement commit names the covering test. The findings archive was retired with them (git history is the record). The answered questions were removed after their answers were verified against the code. The drawer triage and knowledge distillation passes were promoted to `desk/rituals/`. `feature-agent-role-models.md` was replaced by `desk/roles/`; `feature-sldb-ui-surface-inspection.md` was routed to sldb/spec2viz; the master plan was retired because kgdb no longer exists; the runtime-and-launcher feature and the tmux launcher task were retired because `deskops runtime supervise` plus the external harness cover them. The attention review is in `desk/logbook/log-2026-06-21-workflow-baseline-before-roles-refactor.md`.

## Rule

Work in `desk/drawer/` is not currently executing.

When a drawer item becomes real work, author a full task from it with `deskops add task --from-drawer <item>` (see `desk/rituals/ritual-drawer-triage.md`); nothing promotes a drawer item into an active task.
