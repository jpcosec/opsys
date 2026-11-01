---
id: task-ws10-precisar-índice-y-convención-del-manual
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/workspace-documental/borradores/manual.md
- docs/operator-manual.md
- desk/drawer/plans/workspace-documental/decisiones.md
- desk/drawer/plans/workspace-documental/dag.yaml
- desk/drawer/plans/workspace-documental/auditoria/deskops.md
- desk/drawer/plans/workspace-documental/auditoria/infraestructura.md
- desk/drawer/plans/workspace-documental/auditoria/ui.md
- runs/subagents/20261031-atribucion-decisiones/phase-closeout.md
- desk/rituals/context-review.md
depends_on: []
pills: []
files:
- desk/drawer/plans/workspace-documental/borradores/manual.md
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/workspace-documental/task-ws10.md
closeout_evidence:
- commit
- document
---

# WS10: Precisar índice y convención del manual

## Rationale

_Explain why this task exists or the business driver behind it._

La revisión root aprobó WS07 y autorizó la capa WS08/WS10. manual.md tiene índice pero no propósito/entradas/salidas por capítulo ni definiciones de disponibilidad.

## Goal

_Describe the concrete result this task must produce._

Completar desk/drawer/plans/workspace-documental/borradores/manual.md con esquema de capítulos, ejemplo fijo y definiciones de disponibilidad, contrastados con las auditorías WS02-WS04, sin redactar el manual.

## Scope

_State what is in scope and what is out of scope._

Índice y esquema de capítulos conceptuales (propósito/entradas/salidas, no redacción del manual completo), ejemplo fijo y etiqueta de disponibilidad; reutilizar manual CLI. Usa auditoria WS02–WS04; WS03/WS04 llegan de forma transitiva por WS06/WS07. Ejemplo fijo acordado P08: Taller, graph_ui:.tmp/workspace-documental-ejemplo/, productor WS40; hasta generarse describir como corpus futuro, sin capturas ni pasos inventados.

Fijado para esta tarea: conservar el índice 1-17 y sus números, porque WS39 cita el capítulo 15. Añadir por capítulo propósito, entradas y salidas, y una etiqueta con su evidencia. Definiciones tal como dice la aceptación. Precedencia: «bloqueado» cuando hay una dependencia o contrato identificado pendiente; «propuesto» cuando no hay evidencia ni bloqueo identificado; «disponible» solo con versión/commit implementado, pruebas relevantes y acta humana. Ninguna capacidad nueva de UI queda disponible hoy: no hay actas. Las capacidades del CLI se remiten a docs/operator-manual.md, sin copiarlo. Sin pasos, capturas ni nombres de controles.

Autorización acotada: revisión root 2026-11-01, runs/subagents/20261031-atribucion-decisiones/root-approval-20261101.md. execution_authorized global sigue false. Reutilizar antes de editar: el texto existente no se borra ni se reescribe por estilo.

Independencia: este nodo no tiene arista con WS08 y no lee ni cita su entregable. WS07 está efectiva (runs/subagents/20261031-atribucion-decisiones/ws07-cobertura-efectiva.md). G_PRODUCT satisfecho es base de plan, no aceptación de producto, API ni UI. No reabrir decisiones P01-P09 ni preguntar al solicitante. Una capacidad se afirma solo con cita a auditoría; lo no auditado queda como hueco con dueño. Taller es corpus futuro de WS40, no producto operativo.

Roles: el Executor escribe solo desk/drawer/plans/workspace-documental/borradores/manual.md y runs/subagents/20261101-ws10-manual/result-summary.md. El Supervisor corre validaciones, commits, revisiones y closeout. Tester independiente de solo lectura. Fuera de alcance: WS09, WS11, WS12, código UI, Scion, push, dag.yaml, validadores, helper y la suite general.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Leer desk/drawer/plans/workspace-documental/borradores/manual.md, docs/operator-manual.md, decisiones.md y las auditorías. 2. Añadir definiciones y ejemplo fijo. 3. Añadir esquema por capítulo con etiqueta y evidencia. 4. Escribir runs/subagents/20261101-ws10-manual/result-summary.md.

## Validation

_List the checks required before this task can close._

- test -s desk/drawer/plans/workspace-documental/borradores/manual.md
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status
- Tester independiente de solo lectura deja runs/subagents/20261101-ws10-manual/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

Acceptance: Registrar en borradores/manual.md definiciones: disponible solo versión/commit implementado + pruebas relevantes + acta humana del recorrido y pasos verificados; propuesto intención sin esa evidencia; bloqueado dependencia/contrato identificado pendiente. Contrastar estado actual con auditorías WS02–04 y remitir pruebas/actas futuras a sus productores. No escribir pasos ni capturas ficticios. Revisiones afectadas renovadas, build --check, validate --check y status en verde, y Tester independiente PASS antes del closeout.
