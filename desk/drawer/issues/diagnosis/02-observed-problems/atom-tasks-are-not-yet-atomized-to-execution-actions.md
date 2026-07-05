---
id: atom-tasks-are-not-yet-atomized-to-execution-actions
title: Tasks are not yet atomized to execution actions
five_wh_one_plus: what
tags:
- system:deskops
- topic:diagnosis
- topic:tasks
type: atom
description: Observed problem in the current task execution model.
---

# Tasks are not yet atomized to execution actions

## Answer

Current tasks usually capture goal, scope, files, and validation, but they do not yet consistently decompose execution into concrete edit-oriented actions such as replacing a pattern, introducing a method from an existing example, or applying a named refactor to a specific surface. That leaves too much semantic improvisation to the executor lane.

## Related Tasks

- `desk/tasks/task-make-task-lifecycle-runnable-from-intake-to-closeout.md`
- `desk/tasks/task-write-end-to-end-deskops-operator-manual.md`

## Evidence

- `spec/artifacts/task.yaml` — task artifacts are modeled at the current task-document layer rather than as detailed edit-action bundles.
- `deskops/operations.py` — normalized task payloads focus on title, goal, scope, references, files, validation, and routine linkage.
- `/home/jp/.pi/agent/agents/deskops-executor.md` — still frames execution mainly as reading task scope and then implementing, not as consuming a compiled edit-plan composition.
