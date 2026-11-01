---
id: task-completar-productores-en-los-campos-nodo-de-ws08
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/workspace-documental/borradores/user-flows.md
- desk/drawer/plans/workspace-documental/cobertura.md
- desk/drawer/plans/workspace-documental/auditoria/ui.md
- desk/drawer/plans/workspace-documental/auditoria/deskops.md
- desk/drawer/plans/workspace-documental/dag.yaml
- runs/subagents/20261101-ws08-completitud/review-source.md
- desk/rituals/context-review.md
depends_on: []
pills: []
files:
- desk/drawer/plans/workspace-documental/borradores/user-flows.md
- desk/drawer/plans/workspace-documental/cobertura.md
- runs/subagents/20261101-ws08-completitud/completeness-matrix.md
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-completar-productores-en-ws08.md
closeout_evidence:
- commit
- document
---

# Completar productores en los campos Nodo de WS08

## Rationale

_Explain why this task exists or the business driver behind it._

La revisión root no aprobó WS08: la aceptación exige listas completas y los campos Nodo omiten productores que el propio flujo nombra.

## Goal

_Describe the concrete result this task must produce._

Que cada operación o error con productor necesario tenga ese productor en Nodo y en cobertura.md, con matriz que lo demuestre.

## Scope

_State what is in scope and what is out of scope._

Una sola pasada documental sobre desk/drawer/plans/workspace-documental/borradores/user-flows.md y desk/drawer/plans/workspace-documental/cobertura.md, con matriz runs/subagents/20261101-ws08-completitud/completeness-matrix.md. Autoriza: runs/subagents/20261101-ws08-completitud/review-source.md. No se añaden aristas, tareas ni gates: estos productores ya existen. Los textos UF y los gates humanos no cambian. Lista cerrada de cambios.

En user-flows.md, línea **Nodo:** de cada UF:
- UF03: añadir `WS29 (extensión de impacto/Changes; no es prerrequisito del lector ni del manual básico)`.
- UF05: añadir `WS13.3` y `WS23` a la implementación.
- UF06: añadir `WS44` a preparación/contrato.
- UF07: añadir `WS12` a preparación/contrato.
- UF09: añadir `WS29 (impacto avanzado, opcional y propuesto según evidencia; no bloquea WS31)`.
- UF10: añadir `WS11` a preparación/contrato.
- UF01: Nodo no cambia. WS22 es base existente citada, no productor necesario: no añadir bloqueo a WS16.

En user-flows.md, línea **Operación:**:
- UF05: `list ritual`/`show ritual` pasa a `deskops list rituals`/`show ritual` (forma auditada en deskops.md:78).
- UF05: añadir un hueco: renderer de RitualDoc/StepDoc y procedimientos (`ui.md:68`); dueño graph_ui, productor WS23.
- Ninguna otra línea cambia. WS23 no se añade al gate básico WS16 de UF01.

En cobertura.md, filas de la tabla, sin cambiar la columna Gate de aceptación salvo donde se indica:
- UF03, implementación: añadir `WS20/45 precondiciones; WS29 extensión de impacto, no prerrequisito`.
- UF05, implementación: añadir `WS13.3`, `WS23`.
- UF06, preparación: añadir `WS44`. Gate de aceptación: tras WS37 añadir `; WS38 publicación`.
- UF07, preparación: añadir `WS12`.
- UF08, implementación: añadir `WS40 corpus`.
- UF09, implementación: añadir `WS13 lector; WS29 impacto avanzado, opcional`.
- UF10, preparación: añadir `WS11`. Implementación: añadir `WS43 publicación real`.

Matriz, en runs/subagents/20261101-ws08-completitud/completeness-matrix.md: una tabla por UF, una fila por cada WS citado en Operación o Error: ID, dónde se cita, clase (productor necesario, extensión opcional, citación contextual o fuera de alcance), si está en Nodo, si está en cobertura.md. Un agregado cubre a sus hijos. No se enumeran dependencias transitivas ni IDs citados solo para decir que quedan fuera.

Si la matriz muestra otro productor necesario ausente, NO se edita: se anota en result-summary.md para el Supervisor.

No editar manual.md, decisiones.md, la guía, dag.yaml, helper, validadores ni código. Los huecos de bundle (UF06) y Corpus.rank se conservan: son honestos y no llevan productor inventado. Roles: el Executor escribe solo user-flows.md, cobertura.md, la matriz y runs/subagents/20261101-ws08-completitud/result-summary.md. No hay commits ni corrida de revisiones del Executor. Sin preguntar al solicitante. Fuera de alcance: WS09, WS11, WS12 como tareas, UI, Scion, push, suite general.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Aplicar la lista cerrada. 2. Escribir la matriz leyendo las 10 UF. 3. Escribir runs/subagents/20261101-ws08-completitud/result-summary.md. 4. El Supervisor congela y entrega diff y hashes a root antes de renovar revisiones.

## Validation

_List the checks required before this task can close._

- grep -c "^## UF" desk/drawer/plans/workspace-documental/borradores/user-flows.md
- test -s runs/subagents/20261101-ws08-completitud/completeness-matrix.md
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status
- Tester independiente de solo lectura deja runs/subagents/20261101-ws08-completitud/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

Acceptance: todos los cambios de la lista aplicados y ninguno más; matriz sin productor necesario ausente; Tester independiente PASS; root comprueba la congelación; revisiones renovadas; build --check, validate --check y status en verde.
