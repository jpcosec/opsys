---
id: atom-workline-add-execution-plan-to-task-model
title: Add an execution plan to the task model
five_wh_one_plus: how
tags:
- system:deskops
- topic:diagnosis
- topic:tasks
type: atom
description: Workline for making tasks more executable by subagents.
---

# Add an execution plan to the task model

## Answer

The task model should gain a field or composition layer for execution plans that describe concrete edit actions. These plans can name target files, replacement patterns, insertion points, donor examples, refactor shapes, and validation obligations so the executor lane receives a bounded operational recipe rather than only a semantic goal.

## Related Tasks

- `desk/tasks/task-make-task-lifecycle-runnable-from-intake-to-closeout.md`
- `desk/tasks/task-write-end-to-end-deskops-operator-manual.md`

## Evidence

- `deskops/operations.py` current task normalization and bundle creation show the present task contract and where an execution-plan layer could attach.
- `desk/rituals/execution.md` requires explicit touched files and validation, which aligns with a more concrete execution-plan field or composition.
- `/home/jp/.pi/agent/agents/deskops-executor.md` describes the need for exact touched surfaces and bounded action, which an execution plan could encode directly.
