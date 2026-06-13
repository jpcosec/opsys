# Desk (opsys)

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
- `desk/inbox/` - incoming unclear points and suggestions.
- `desk/drawer/` - deferred work kept inside the desk system until it becomes active execution.
- `desk/atoms/` - durable atom documents for project knowledge.

## `desk install`

`deskops desk install <path>` creates a minimal repo-local desk surface.

Today that scaffold is intentionally local only: it creates `tasks/`, `contexts/`, `rituals/`, `inbox/`, and `drawer/` under the target repo's `desk/` directory, plus starter files for the board, pills, rituals, and drawer README.

It does not auto-register the repository in any ecosystem registry. Use `deskops repo register ...` as a separate explicit step when you want cross-repo registry discovery.

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
