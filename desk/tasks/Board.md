---
sldb:
  by: agent
  at: '2026-11-10T05:43:58Z'
  authority: generated
  via: save_document_payload
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-cc37-cerrar-vías-de-escape-ninguna-escritura-deja-el-ciclo-de-vida-fuera-de-las-reglas.md
- desk/tasks/task-cc33a-recibos-de-evidencia-closeout-verify-escribe-reviewdoc-kind-evidence-y-queda-como-orquestador.md
- desk/tasks/task-main-en-verde-los-10-fallos-de-la-suite-completa-en-ci-run-42694709414-c478614f.md
- desk/tasks/task-rendimiento-cada-comando-cli-tarda-30-s-desde-cc32-cc35b.md
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

- CC37: Cerrar vías de escape - ninguna escritura deja el ciclo de vida fuera de las reglas [draft] - Ninguna vía de escritura deja una TaskDoc con un ciclo de vida inconsistente: un validador del modelo TaskDoc (DK6, mecanismo de CC38) exige que status, current_node, history y task_type sean coherentes con el grafo del ciclo de vida, y sldb lo aplica en toda escritura (fields update, docs update, /save, transacción). Las escrituras internas de deskops que cambian el ciclo de vida pasan solo por advance y closeout. El inventario de vías de escritura queda en el TaskDoc.
- CC33a: Recibos de evidencia - closeout verify escribe ReviewDoc kind evidence y queda como orquestador [draft] - deskops closeout verify corre los productores de hechos de git y archivos y escribe, por cada kind de evidencia verificado, un ReviewDoc kind evidence (fact, value, verdict accepted o rejected, subject anclado al contrato de la tarea), sin duplicar recibos en una verificación repetida sin cambios. verify_task_closeout queda como orquestador y devuelve el mismo envelope que hoy. El gate de cierre todavía no cambia: lo cambia CC33b.
- main en verde: los 10 fallos de la suite completa en CI (run 42694709414, c478614f) [draft] - python -m pytest tests -q termina sin fallos sobre main de deskops, en local (TMPDIR=/dev/shm) y en el workflow tests de GitHub para 3.12 y 3.13.
- rendimiento: cada comando CLI tarda ~30 s desde CC32/CC35b [draft] - Se mide, se escribe la causa raíz y se arregla donde viva. Cada comando de deskops (show task, advance) vuelve a un tiempo del orden de antes de CC32, y test_activation_rules y test_lifecycle_end_to_end vuelven a quedar por debajo de ~90 s por archivo.
