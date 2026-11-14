---
sldb:
  by: agent
  at: '2026-11-14T08:25:51Z'
  authority: generated
  via: save_document_payload
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-los-tests-de-deskops-leen-la-ruta-del-sldb-hermano-de-la-variable-de-entorno-sldb-src-con-un-helper.md
- desk/tasks/task-add-task-y-el-doctor-sugieren-task-external-o-una-tarea-espejo-cuando-los-files-o-las-referencias-de.md
- desk/tasks/task-deskops-view-board-en-menos-de-2-5-s-construir-una-vez-por-corrida-lo-que-hoy-se-rehace-por-tarjeta.md
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
- context-review
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

- Los tests de deskops leen la ruta del sldb hermano de la variable de entorno SLDB_SRC, con un helper común [draft] - Un solo helper común resuelve la ruta de sldb para los tests: lee la variable de entorno SLDB_SRC y, si no está definida, usa la ruta hermana de hoy; los 18 archivos lo usan y ninguno repite la línea fija.
- add task y el doctor sugieren task.external (o una tarea espejo) cuando los files o las referencias de una tarea apuntan a otro repo [draft] - Al crear una tarea cuyos files apuntan a otro repo, add task lo avisa con una línea (no bloquea) que nombra el repo y sugiere task.external o una tarea espejo en el desk de ese repo; y el doctor lista como alerta, sin cambiar su código de salida, las tareas existentes con esa forma que no son task.external.
- deskops view board en menos de 2,5 s: construir una vez por corrida lo que hoy se rehace por tarjeta (transiciones, closeout, grafo del desk) y abrir el store menos veces [draft] - deskops view board, con el store construido y en un proceso nuevo, tarda 2,5 s o menos (mediana de 3, layout del benchmark de H11) y su salida es idéntica a la de hoy; lo que se construye una vez por corrida se comparte entre las tarjetas.
