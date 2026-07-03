---
id: atom-use-case-auto-dispatch-executor-on-execution-ready
title: Auto-dispatch an executor when a task becomes execution-ready
five_wh_one_plus: when
tags:
- system:deskops
- topic:diagnosis
- topic:use-cases
type: atom
description: Priority use case for hook-driven workflow automation.
---

# Auto-dispatch an executor when a task becomes execution-ready

## Answer

When a task satisfies execution-ready conditions, deskops should be able to compose the bounded execution bundle, create the run evidence directory, and dispatch the executor lane automatically or in a reviewable dry-run mode. This use case would prove that hooks can drive real workflow automation rather than remain passive documentation artifacts.

## Related Tasks

- `desk/tasks/task-make-task-lifecycle-runnable-from-intake-to-closeout.md`
- `desk/tasks/task-wire-closeout-to-knowledge-gates.md`

## Evidence

- `spec/workflows/task_lifecycle.yaml` defines the execution gate and next actions conceptually.
- `deskops/operations.py` can already detect task state transitions and create runtime artifacts for task lifecycle handling.
- `.agents/skills/subagent-execution/SKILL.md` defines the run-evidence bundle that an automatic dispatch path would need to create.
