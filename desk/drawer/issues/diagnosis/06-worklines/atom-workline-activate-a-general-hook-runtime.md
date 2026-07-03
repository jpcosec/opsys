---
id: atom-workline-activate-a-general-hook-runtime
title: Activate a general hook runtime
five_wh_one_plus: how
tags:
- system:deskops
- topic:diagnosis
- topic:hooks
type: atom
description: Workline for turning modeled hooks into reusable runtime automation.
---

# Activate a general hook runtime

## Answer

Deskops should move from merely modeling hooks to running them through a general event-driven mechanism. A minimal runtime should resolve hook documents for an event, evaluate conditions, support dry-run visibility, persist evidence, and dispatch targets such as closeout automation or executor-lane launch.

## Related Tasks

- `desk/tasks/task-make-task-lifecycle-runnable-from-intake-to-closeout.md`
- `desk/tasks/task-wire-closeout-to-knowledge-gates.md`
- `desk/tasks/task-enforce-pill-to-atom-knowledge-graduation-during-task-closeout.md`

## Evidence

- `deskops/models/hook.py` and hook CLI surfaces show that hooks already exist as modeled documents.
- `deskops/operations.py` already contains narrow automatic behavior like auto-closeout commit, suggesting a candidate target for generalization into hook runtime behavior.
- `docs/diagrams/process/rituals-routines-hooks-workflow.md` and `llm-tasks-vs-automatic-routines.md` describe the intended role of hooks and automatic routines.
