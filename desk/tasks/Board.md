---
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-ui01-vista-de-datos-de-deskops-para-la-ui-deskops-view-y-su-contrato.md
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

- UI01: vista de datos de deskops para la UI (deskops view) y su contrato [draft] - Clase de servicio de solo lectura en deskops (deskops/services/desk_view.py) que compone, desde las operaciones existentes listadas en alcance.md, cinco vistas JSON: board (columnas por nodo del ciclo de vida en el orden del spec, cada tarjeta con id, título, status, current_node, gates con condición y si se cumple, conteo cumplidos/total, evidencia declarada y encontrada de verify_task_closeout, pills y atoms resueltos a título); task (lo del board más goal, scope, implementation_path, validation, done_when, why, references, files, depends_on, inherits_from, pills con what/when/how_not, atoms con answer, next_actions y advance_when de next_action_report, y revision = sha256 de Board + archivo de tarea como la guarda de graph_ui); drawer (tareas de desk/drawer/tasks con id, título, status, primeras líneas del cuerpo y ruta, más el comando add task --from-drawer listo para copiar); inbox (notas con id, kind, título, emisor, destino, fecha del nombre de archivo, estado de ack, cuerpo); agents (runtime workers y las últimas N corridas de runs/subagents/index.jsonl). Toda referencia que no resuelve aparece en una lista errors de la vista con su causa, nunca como dato. Subcomando deskops view {board,task <id>,drawer,inbox,agents} --root --format json|text registrado en cli/registry.py. Documento docs/deskops-ui.md con el contrato JSON de cada vista y la tabla de mapeo de alcance.md. Solo lectura: nada escribe.
