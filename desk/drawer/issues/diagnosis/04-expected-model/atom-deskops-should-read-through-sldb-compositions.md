---
id: atom-deskops-should-read-through-sldb-compositions
title: Deskops should read through SLDB compositions
five_wh_one_plus: how
tags:
- system:deskops
- system:sldb
- topic:diagnosis
- topic:composition
type: atom
description: Expected model for reading workflow knowledge.
---

# Deskops should read through SLDB compositions

## Answer

Deskops should treat SLDB as the primary read/query/compose layer for structured workflow knowledge. Reading an atom, task, or materialization should usually mean resolving a structured document and asking SLDB for the appropriate composition or field view, not opening the materialized Markdown file as the default operational path.

## Related Tasks

- `desk/tasks/task-define-materialization-contract-slice-deskops-surface.md`
- `desk/tasks/task-add-json-output-for-modeled-documents.md`

## Evidence

- `README.md` — defines the SLDB boundary and says SLDB owns structured Markdown operations while deskops owns the workflow domain on top of that infrastructure.
- `.skills/sldb/SKILL.md` — lists the exact SLDB query, field, model, and composition commands that form the intended structured access path.
- `desk/atoms/workflow-model/atom-sldb-is-read-write-edit-surface.md` — names SLDB as the preferred structured document surface for these operations.
