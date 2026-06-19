# Desk (opsys)

This guide is a human-facing materialization of these atoms:

- `desk/atoms/workflow-model/atom-docs-are-human-facing-atom-materializations.md`
- `desk/atoms/workflow-model/atom-desk-is-document-data-only.md`
- `desk/atoms/workflow-model/atom-drawer-is-not-active-work.md`
- `desk/atoms/workflow-model/atom-inbox-is-coordination-intake.md`

Operational workspace for the SLDB-driven routine.

`desk/` is the entrypoint for the **opsys** workflow-domain layer — the repo's operating system around work.

It contains:

1. active execution surfaces
2. deferred surfaces kept inside the same operational system
3. rituals for changing code, testing, documenting, and keeping the repo and git state clean

Nothing in `desk/` is durable project history. Stable knowledge must end up in code, tests, docs, or git history.

## Structure

- `desk/tasks/` - active task documents only.
- `desk/tasks/Board.md` - active routing board.
- `desk/contexts/` - active context documents only.
- `desk/contexts/pills.md` - pill conventions and current base shape.
- `desk/rituals/` - structured ritual documents for execution, testing, and closeout.
- `desk/inbox/` - incoming messages to this project, including requests, blockers, questions, or self-messages that identify the sending project.
- `desk/drawer/` - internal deferred work, plans, ideas, and questions kept inside the desk system until they become active execution.
- `desk/atoms/` - durable atom documents for project knowledge.

## `desk install`

`deskops desk install <path>` creates a minimal repo-local desk surface.

Today that scaffold is intentionally local only: it creates `tasks/`, `contexts/`, `rituals/`, `inbox/`, and `drawer/` under the target repo's `desk/` directory, plus starter files for the board, pills, rituals, and drawer README.

It does not auto-register the repository in any ecosystem registry. Use `deskops repo register ...` as a separate explicit step when you want cross-repo registry discovery.

## Inbox vs Drawer

Use `desk/inbox/` for messages addressed to this project. A message can come from another registered project or from this project itself, but it should record the sending project and should be triaged rather than treated as active work.

Use `desk/drawer/` when an agent or maintainer wants to leave internal work for later, sketch a plan, keep an unresolved project question, or hold a deferred task candidate.

## Code Boundary

`desk/` is document data only. Python code for the workflow-domain layer lives under `deskops/`, including:

- `deskops/models/` - SLDB `StructuredNLDoc` models for desk documents.
- `deskops/cli/` - command parsing and handlers.
- `deskops/materializers/` - document materialization helpers.

This keeps the installed desk surface readable as documents while keeping implementation code in the package namespace.

## Exclusions

- No resolved tasks.
- No historical reports.
- No duplicate project documentation.
