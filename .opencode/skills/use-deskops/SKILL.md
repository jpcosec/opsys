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

Core boundaries:

- `desk/` is document data only.
- Python implementation code belongs under `deskops/`.
- Structured document infrastructure belongs to SLDB.
- Graph contract/runtime validation belongs to KGDB.
- Diagram rendering belongs to spec2viz.

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
