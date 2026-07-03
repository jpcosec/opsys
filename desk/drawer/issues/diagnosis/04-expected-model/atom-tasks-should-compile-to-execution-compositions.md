---
id: atom-tasks-should-compile-to-execution-compositions
title: Tasks should compile to execution compositions
five_wh_one_plus: how
tags:
- system:deskops
- topic:diagnosis
- topic:tasks
type: atom
description: Expected model for making tasks more executable.
---

# Tasks should compile to execution compositions

## Answer

A task should not stop at human-readable intent. Deskops should be able to compile a task into an execution composition that includes the exact surfaces to touch, relevant patterns or examples, intended edits, validation targets, and anti-patterns. That would reduce executor improvisation and make subagent lanes more deterministic.

## Related Tasks

- `desk/tasks/task-make-task-lifecycle-runnable-from-intake-to-closeout.md`
- `desk/tasks/task-write-end-to-end-deskops-operator-manual.md`

## Evidence

- `desk/atoms/workflow-model/atom-tasks-enable-zero-context-subagents.md` — pushes tasks toward bounded autonomous execution.
- `desk/rituals/execution.md` — requires explicit scope, touched files, and validation targets before implementation.
- `.agents/skills/subagent-execution/SKILL.md` and `.agents/skills/workflow-executor/SKILL.md` — already assume the need for bounded execution bundles and evidence, which points toward a compiled execution composition.
