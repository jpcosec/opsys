---
sldb:
  by: agent
  at: '2026-11-12T03:13:05Z'
  authority: generated
  via: save_document_payload
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-los-tests-de-deskops-leen-la-ruta-del-sldb-hermano-de-la-variable-de-entorno-sldb-src-con-un-helper.md
- desk/tasks/task-deskops-quita-las-guardas-que-esquivaban-h1-h3-de-sldb-cerrar-por-cli-dos-tareas-inválidas-del-mismo.md
- desk/tasks/task-add-task-y-el-doctor-sugieren-task-external-o-una-tarea-espejo-cuando-los-files-o-las-referencias-de.md
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
- deskops quita las guardas que esquivaban H1-H3 de sldb: cerrar por CLI dos tareas inválidas del mismo modelo y reparar un desk que tiene un documento inválido [draft] - Con sldb corregido, deskops cierra por CLI dos o más tareas inválidas del mismo modelo (retire, supersede, resolved-by), y desk update --apply sobre un desk con documentos inválidos hace todas las reparaciones sin saltarse ninguna, mientras la migración de estados heredados y el listado de las tareas inválidas se quedan.
- add task y el doctor sugieren task.external (o una tarea espejo) cuando los files o las referencias de una tarea apuntan a otro repo [draft] - Al crear una tarea cuyos files apuntan a otro repo, add task lo avisa con una línea (no bloquea) que nombra el repo y sugiere task.external o una tarea espejo en el desk de ese repo; y el doctor lista como alerta, sin cambiar su código de salida, las tareas existentes con esa forma que no son task.external.
