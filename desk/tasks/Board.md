---
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-closeout-la-evidencia-exigida-depende-de-lo-que-la-tarea-toca-no-es-la-misma-para-todo.md
# List of pill-xxx paths
pills:
- pill-001-task-closure-commit
- pill-005-subagent-execution
- pill-007-phase-gated-task-flow
- pill-durable-pill-knowledge-graduates-to-atoms-at-closeout
- pill-phase-closeout-reconciles-pills-and-surfaces-next-work
- pill-ready-phases-prove-dependencies-and-non-overlap
- pill-board-routed-pills-stay-minimal-and-reusable
# List of ritual-xxx paths
rituals:
- ritual-phase
- ritual-execution
- ritual-closeout
- ritual-testing
- desk/rituals/context-review.md
# e.g., system:sldb, workspace:desk
tags:
- system:sldb
- workspace:desk
- topic:routing
---

# Desk Board

## Purpose

_Explain what this board routes and why it exists._

Route the active execution set for deskops.

## Notes

_Add short operational notes about the current routed set._

No active tasks routed.

## Task Details

_Generated from the task references above._

- Closeout: la evidencia exigida depende de lo que la tarea toca, no es la misma para todo [active] - La evidencia de cierre se declara al crear la tarea y el closeout verifica exactamente eso. TaskDoc gana el campo closeout_evidence (lista con vocabulario cerrado: tests, commit, atom, materialization, document, external). deskops add task lo recibe con --evidence; si falta, lo rellena por task_type (code -> tests+commit+atom|materialization; docs|spec|design -> commit+document; external -> external); sin --evidence ni task_type falla con el mensaje de cómo declararla. closeout verify/commit comprueban solo lo declarado. Si el diff trae .py y la tarea no declaró tests, no bloquea: alerta visible (nunca silenciosa). La compuerta siempre imprime 'esta tarea declaró X; encontré Y'.
