---
id: atom-diagnosis-deskops-subutilizes-sldb
title: Deskops subutilizes SLDB as its operational reading layer
five_wh_one_plus: what
tags:
- system:deskops
- system:sldb
- topic:diagnosis
- topic:workflow-model
type: atom
description: Architectural diagnosis summary for the current deskops workflow.
---

# Deskops subutilizes SLDB as its operational reading layer

## Answer

The current workflow still treats too many structured workflow surfaces as Markdown files to read directly instead of as structured documents to query, compose, and render through SLDB. That weakens the intended architecture where deskops should sit on top of SLDB and expose workflow operations over compositions rather than raw file reads.

## Related Tasks

- `desk/tasks/task-make-task-lifecycle-runnable-from-intake-to-closeout.md`
- `desk/tasks/task-define-materialization-contract-slice-deskops-surface.md`
- `desk/tasks/task-write-end-to-end-deskops-operator-manual.md`

## Evidence

- `README.md` — declares that deskops is built on top of `sldb` and that `sldb` owns structured document infrastructure.
- `.skills/sldb/SKILL.md` — describes the intended SLDB-first path for structured document reads, writes, field queries, and model operations.
- `deskops/operations.py` — still contains multiple direct file/path resolution and document-loading paths in the deskops runtime.
