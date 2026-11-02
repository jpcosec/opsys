FILE:desk/tasks/task-ws09-precisar-catálogo-de-renderizaciones.md
---
id: task-ws09-precisar-catálogo-de-renderizaciones
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/workspace-documental/borradores/vistas.md
- desk/drawer/plans/workspace-documental/borradores/user-flows.md
- desk/drawer/plans/workspace-documental/borradores/manual.md
- desk/drawer/plans/workspace-documental/decisiones.md
- desk/drawer/plans/workspace-documental/dag.yaml
- desk/drawer/plans/workspace-documental/auditoria/deskops.md
- desk/drawer/plans/workspace-documental/auditoria/infraestructura.md
- desk/drawer/plans/workspace-documental/auditoria/ui.md
- runs/subagents/20261101-ws08-completitud/root-approval.md
- desk/rituals/context-review.md
depends_on: []
pills: []
files:
- desk/drawer/plans/workspace-documental/borradores/vistas.md
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/workspace-documental/task-ws09.md
closeout_evidence:
- commit
- document
---

# WS09: Precisar catálogo de renderizaciones

## Rationale

_Explain why this task exists or the business driver behind it._

La revisión root aprobó la capa WS08/WS10 y autorizó solo WS09. vistas.md tiene 20 filas sin ficha completa.

## Goal

_Describe the concrete result this task must produce._

Completar desk/drawer/plans/workspace-documental/borradores/vistas.md con una ficha por fila: origen, contrato, renderer, acción/dueño, error, estado y clase, con evidencia de auditorías WS02-04 y UF01-UF10.

## Scope

_State what is in scope and what is out of scope._

Inventariar fuente, queries, Board, ritual, conocimiento/crossroads, issues, FAQ, Code y vistas existentes; ViewDoc es grafo, no contrato universal de UI.

Autoriza: runs/subagents/20261101-ws08-completitud/root-approval.md. execution_authorized global sigue false. Reutilizar antes de editar: los textos y tablas existentes de vistas.md no se borran ni se reescriben por estilo.

Consignas. Una ficha por cada fila de las dos tablas de vistas.md: 12 + 8 = 20 fichas, F01 a F20, en el orden de las tablas, en una sección nueva «Fichas por fila». Ninguna fila se omite ni se muestrea. Una fila compuesta se separa solo si un componente tiene evidencia o estado distinto, con sufijo a/b; si no, usa listas.

Campos de cada ficha, todos obligatorios: Propósito humano; Origen (documento o consulta); Identidad; Contrato o «sin contrato»; Campos y relaciones; Renderer existente o requerido; Navegación; Acción/dueño; Destino de escritura; Error; Estado; Clase; UF; Evidencia.

Estado: exactamente disponible, propuesto o bloqueado, según las definiciones de borradores/manual.md. Disponible exige versión o commit implementado, pruebas relevantes y acta humana: hoy no hay actas, así que ninguna ficha es disponible, aunque exista renderer. Un renderer ya implementado se anota en Renderer como «base existente» con cita; su Estado es bloqueado si hay dependencia o contrato identificado pendiente, y propuesto si no. auditoria/ui.md aporta el hecho observado, no la etiqueta. G_PRODUCT no prueba implementación.

Clase: authored, derivado o preferencia local, por componente en filas compuestas.

No definido: todo campo sin evidencia dice «no definido» con productor. Productor de contrato: WS11 o WS12. Productor de implementación: ID de nodo real del DAG. Si ningún nodo lo produce: «sin productor en el DAG» y repo dueño. Nunca inventar actor, API, renderer ni correspondencia.

Error: fallo visible esperado para esa fila. En propuesto o bloqueado, error condicionado a contrato o implementación, o no definido con productor. Nunca inventar un error actual.

UF: lista de UF01-UF10 que usan la fila, o «ninguna» con motivo. El campo «aceptación mediante user-flow» de la ficha original es esto.

Evidencia: cita archivo:línea de auditoria/deskops.md, infraestructura.md o ui.md, y de user-flows.md. Leer esas auditorías con Read, completas en las filas relevantes: no usar cut, truncar celdas ni afirmar sobre la cola de una celda no leída.

Límites: vistas como representaciones de documentos Markdown con modelo opcional y consultas; reutilizar host Mindmap y registry real; sin otro workspace ni IA de navegación codificada. ViewDoc de grafo no es contrato universal de UI. Code, origen y foco solo con soporte y correspondencia reales: lo que falte se señala para WS11, sin inventar mapeo ni rebajar escenarios comprometidos. Sin manual completo, pasos o capturas ficticios, API o renderer nuevos, ni cambios en repos hermanos.

Roles: el Executor escribe solo desk/drawer/plans/workspace-documental/borradores/vistas.md y runs/subagents/20261101-ws09-vistas/result-summary.md. Sin commits ni revisiones del Executor. Fuera de alcance: WS11, WS12, UI, Scion, push, dag.yaml, otras fuentes, helper, validadores, suite general. Sin preguntar al solicitante.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Leer vistas.md, user-flows.md, manual.md, decisiones.md, reconciliacion.md y las auditorías. 2. Escribir 20 fichas. 3. Escribir runs/subagents/20261101-ws09-vistas/result-summary.md con reuso, huecos y límites.

## Validation

_List the checks required before this task can close._

- grep -c "^### F" desk/drawer/plans/workspace-documental/borradores/vistas.md
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status
- Tester independiente de solo lectura deja runs/subagents/20261101-ws09-vistas/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

Acceptance: Cada fila inventaría origen, contrato (o «sin contrato» si el soporte no lo tiene), renderer, acción/dueño, error y estado desde auditorías WS02–04/decisiones y UFs WS08. Campo sin evidencia se marca no definido con productor WS11/12 o futura implementación, incluido renderer/actor/campos/relaciones; nunca inventar actor/API disponible. Distinguir authored/derivado/preferencia local. Aplica a cada fila de las tablas de vistas.md y completa la ficha por fila. Estado = disponible/propuesto/bloqueado según WS10; disponibilidad actual viene de auditoria/ui.md (WS04); error = fallo visible esperado para esa fila. Filas compuestas admiten listas de contratos/renderers/acciones/errores y clasificación por componente authored/derivado/local; separar fila solo si el delta tiene evidencia/estado independiente. Para propuesto/bloqueado indicar error esperado condicionado a contrato/implementación, o no definido con productor WS11/12 si falta; nunca inventar error actual. Revisión de WS09 renovada tras congelar, build --check, validate --check y status en verde, y Tester independiente PASS antes del closeout.
