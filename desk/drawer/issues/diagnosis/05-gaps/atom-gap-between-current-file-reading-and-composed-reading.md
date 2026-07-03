---
id: atom-gap-between-current-file-reading-and-composed-reading
title: Gap between current file reading and composed reading
five_wh_one_plus: why
tags:
- system:deskops
- system:sldb
- topic:diagnosis
- topic:gaps
type: atom
description: Main architectural gap between current and target workflow behavior.
---

# Gap between current file reading and composed reading

## Answer

The main gap is that deskops has not yet fully turned SLDB queries and compositions into its normal operational interface. Until that happens, agents and humans will keep falling back to direct file reads, and the intended separation between structured source, composition, and materialization will remain incomplete.

## Related Tasks

- `desk/tasks/task-define-materialization-contract-slice-deskops-surface.md`
- `desk/tasks/task-make-task-lifecycle-runnable-from-intake-to-closeout.md`
- `desk/tasks/task-add-drift-check-review-loop.md`

## Evidence

- `README.md` and `.skills/sldb/SKILL.md` — define the intended SLDB-first architecture.
- `deskops/operations.py` and `deskops/workflow/next_actions.py` — show the current runtime still operating heavily through file-shaped document access.
- `docs/diagrams/process/current-agent-workflow-and-automation.md` — now records this mismatch between intended architecture and current operational behavior.
