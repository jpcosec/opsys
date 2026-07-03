---
id: atom-materializations-are-projections-not-primary-read-surfaces
title: Materializations are projections not primary read surfaces
five_wh_one_plus: what
tags:
- system:deskops
- system:sldb
- topic:diagnosis
- topic:materialization
type: atom
description: Expected model for docs and rendered workflow surfaces.
---

# Materializations are projections not primary read surfaces

## Answer

Materialized docs, diagrams, and similar rendered surfaces should primarily act as human-facing projections over structured knowledge. They should not be the default operational input path for deskops when a structured query or composition can provide the needed information more precisely.

## Related Tasks

- `desk/tasks/task-define-materialization-contract-slice-deskops-surface.md`
- `desk/tasks/task-add-drift-check-review-loop.md`
- `desk/tasks/task-wire-closeout-to-knowledge-gates.md`

## Evidence

- `docs/diagrams/README.md` — explicitly says diagrams are human-facing materializations.
- `docs/diagrams/workflow/workflow-model.md` — describes docs as materialized from atoms.
- `desk/atoms/workflow-model/atom-docs-are-human-facing-atom-materializations.md` and `atom-rendered-diagrams-are-projections.md` — express the same architectural direction.
