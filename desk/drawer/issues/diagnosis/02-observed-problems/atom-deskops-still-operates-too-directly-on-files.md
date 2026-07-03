---
id: atom-deskops-still-operates-too-directly-on-files
title: Deskops still operates too directly on files
five_wh_one_plus: what
tags:
- system:deskops
- topic:diagnosis
- topic:workflow-model
type: atom
description: Observed problem in how deskops consumes workflow surfaces.
---

# Deskops still operates too directly on files

## Answer

Deskops still relies too often on direct file-shaped surfaces such as task Markdown, atom Markdown, and materialized docs instead of consistently routing those reads through SLDB-backed queries and compositions. This keeps deskops too close to document storage and too far from the structured domain layer it is meant to provide.

## Related Tasks

- `desk/tasks/task-make-task-lifecycle-runnable-from-intake-to-closeout.md`
- `desk/tasks/task-define-materialization-contract-slice-deskops-surface.md`
- `desk/tasks/task-design-operational-cli-grammar.md`

## Evidence

- `deskops/operations.py` — uses `_resolve_glob`, `_read_doc`, direct task paths, and board file paths throughout operational flows.
- `deskops/workflow/next_actions.py` — reads workflow YAML directly from `spec/workflows/task_lifecycle.yaml` and matches states by current node.
- `README.md` — says deskops should sit on top of SLDB rather than duplicate document infrastructure behavior.
