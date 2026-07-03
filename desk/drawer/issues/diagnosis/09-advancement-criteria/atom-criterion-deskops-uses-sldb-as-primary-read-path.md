---
id: atom-criterion-deskops-uses-sldb-as-primary-read-path
title: Deskops uses SLDB as its primary read path
five_wh_one_plus: done_when
tags:
- system:deskops
- system:sldb
- topic:diagnosis
- topic:criteria
type: atom
description: Advancement criterion for this diagnosis line.
---

# Deskops uses SLDB as its primary read path

## Answer

This diagnosis line starts to resolve when deskops can serve common reads of atoms, tasks, and materializations through SLDB-backed queries and compositions by default, while raw Markdown reads become an exception instead of the main operational habit.

## Related Tasks

- `desk/tasks/task-define-materialization-contract-slice-deskops-surface.md`
- `desk/tasks/task-add-json-output-for-modeled-documents.md`
- `desk/tasks/task-design-operational-cli-grammar.md`

## Evidence

- `README.md` and `.skills/sldb/SKILL.md` describe the target architecture this criterion is measuring against.
- `docs/diagrams/process/current-agent-workflow-and-automation.md` records the current hybrid state, which gives a baseline for improvement.
- Future deskops compose operations and reduced raw Markdown dependency would provide the direct evidence that this criterion is being met.
