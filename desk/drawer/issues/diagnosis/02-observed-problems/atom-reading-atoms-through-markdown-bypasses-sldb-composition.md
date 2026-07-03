---
id: atom-reading-atoms-through-markdown-bypasses-sldb-composition
title: Reading atoms through Markdown bypasses SLDB composition
five_wh_one_plus: what
tags:
- system:deskops
- system:sldb
- topic:diagnosis
- topic:atoms
type: atom
description: Observed problem in the current reading path for atoms.
---

# Reading atoms through Markdown bypasses SLDB composition

## Answer

When an atom is consumed primarily by opening its `.md` file, the operational reading path bypasses SLDB's document model, field access, and composition capabilities. That makes the materialized file behave like the primary interface instead of a projection over structured knowledge.

## Related Tasks

- `desk/tasks/task-define-materialization-contract-slice-deskops-surface.md`
- `desk/tasks/task-add-drift-check-review-loop.md`

## Evidence

- `README.md` — states that docs are human-facing materializations and that SLDB should be the structured read/write/edit surface.
- `.skills/sldb/SKILL.md` — describes field/query/compose operations that should be preferred over ad hoc file reads.
- `docs/diagrams/workflow/workflow-model.md` — says docs should be materialized from atoms, which implies the projection should not become the primary operational read path.
