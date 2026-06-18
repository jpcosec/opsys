---
name: use-deskops
description: Use when working in deskops, desk/ documents, atoms, tasks, routines, or workflow operations in the hum ecosystem.
---

# Use Deskops

Deskops is the workflow-domain layer for repository-local operational documents.

Use `deskops` when the task involves:

- `desk/` document surfaces.
- Atoms, tasks, pills, routines, rituals, primitives, inbox, repo registry, or graph commands.
- Creating or reading workflow artifacts through SLDB-backed models.
- Building or checking the deskops knowledge graph snapshot.

Workflow vocabulary:

- `drawer task`: deferred repo-local work under `desk/drawer/tasks/`.
- `board-routed task`: work referenced by `desk/tasks/Board.md`.
- `active task bundle`: task plus generated routine/primitives created by promotion.
- Avoid inventing alternate categories such as active/inactive unless a repo document uses them.

Core boundaries:

- `desk/` is document data only.
- Python implementation code belongs under `deskops/`.
- Structured document infrastructure belongs to SLDB.
- Graph contract/runtime validation belongs to KGDB.
- Diagram rendering belongs to spec2viz.

Drawer-first workflow:

- New unrouted repo-local project work starts directly in `desk/drawer/tasks/`, not `desk/inbox/`.
- Use `desk/inbox/` for incoming notes, unclear external input, or cross-repo intake that needs triage.
- Commit drawer task creation before promoting it.
- Promote drawer work before implementation starts.
- Commit drawer-to-active promotion before implementation starts.
- For board-routed work, run execution, testing, and closeout gates; do not jump from implementation to closeout.
- Every closed task ends with its own atomic closeout commit.

Role skills:

- Load `use-deskops` for `desk/` workflow surfaces, drawer/task routing, pills, rituals, routines, primitives, and repo registry work.
- Load `use-sldb` when the change touches SLDB models, reversible markers, `.sldb` stores, document tracking, rendering, extraction, or field operations.
- Load `use-kgdb` when the change touches graph contracts, graph snapshots, provenance, nodes, edges, or `deskops graph` behavior.
- Load `use-spec2viz` when the change touches diagram specs, Mermaid outputs, generated diagram projections, or `docs/diagrams/` surfaces.
- Load `customize-opencode` only for opencode config, `.opencode/` agents, skills, plugins, MCP servers, permissions, or opencode routing files.

Common commands:

```bash
deskops --help
deskops init .
deskops desk install .
deskops add atom --root . --title "..." --answer "..." --five-wh-one-plus what --tag system:deskops
deskops add task --root . --title "..." --goal "..." --scope "..." --implementation-path "..." --done-when "..."
deskops list tasks --root .
deskops show task <task-id> --root .
deskops graph build --root .
deskops graph missing --root .
deskops graph neighbors atom:<atom-id> --root .
```

Validation:

```bash
pytest
```

Atom format:

```markdown
---
id: atom-example
title: Example
five_wh_one_plus: what
tags:
- system:deskops
---

# Example

## Answer

The atom answer goes here.
```

When editing models, update tests and existing document examples together.
