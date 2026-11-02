FILE:desk/tasks/task-ws11-cerrar-contrato-de-navegación-e-identidad.md
---
id: task-ws11-cerrar-contrato-de-navegación-e-identidad
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/workspace-documental/contratos/navegacion.md
- desk/drawer/plans/workspace-documental/borradores/vistas.md
- desk/drawer/plans/workspace-documental/borradores/user-flows.md
- desk/drawer/plans/workspace-documental/decisiones.md
- desk/drawer/plans/workspace-documental/reconciliacion.md
- desk/drawer/plans/workspace-documental/dag.yaml
- desk/drawer/plans/workspace-documental/auditoria/deskops.md
- desk/drawer/plans/workspace-documental/auditoria/infraestructura.md
- desk/drawer/plans/workspace-documental/auditoria/ui.md
- runs/subagents/20261101-ws09-vistas/result-summary.md
- runs/subagents/20261101-ws09-correccion/root-approval.md
- desk/rituals/context-review.md
depends_on: []
pills: []
files:
- desk/drawer/plans/workspace-documental/contratos/navegacion.md
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/workspace-documental/task-ws11.md
closeout_evidence:
- commit
- document
---

# WS11: Cerrar contrato de navegación e identidad

## Rationale

_Explain why this task exists or the business driver behind it._

La revisión root aprobó WS09 y autorizó solo WS11. Trece nodos dependen de un contrato que no existe.

## Goal

_Describe the concrete result this task must produce._

Crear desk/drawer/plans/workspace-documental/contratos/navegacion.md con identidad, origen, resolución repo/store, foco, enlaces, multidesk read-only, huecos clasificados y mapa de deltas, con APIs reales verificadas.

## Scope

_State what is in scope and what is out of scope._

Un documento Markdown mantiene identidad/ruta/modelo opcional; graph/code admiten otros nodos con origen. Resolución repo/store explícita, foco, enlaces/historia y modo read-only multidesk. Clasificar huecos sin modelos hipotéticos. Instancia = documento concreto que falta escribir. Vínculo = referencia o enlace que falta entre documentos existentes.

Autoriza: runs/subagents/20261101-ws09-correccion/root-approval.md. Autorización acotada: execution_authorized global sigue false. No existe contrato previo: se crea desk/drawer/plans/workspace-documental/contratos/navegacion.md.

Secciones obligatorias del contrato, en este orden:
1. Alcance y estado: qué fija, qué no, base observada (graph_ui 134a665, sldb 77bd6d00).
2. Identidad y origen: Markdown modelado frente a no modelado; ruta y modelo opcional; nodos graph y code con origen.
3. Resolución de repo y store: explícita por petición; aliases y roots autorizados; rutas seguras; sin cambiar SLDB_STORE global ni aceptar roots arbitrarios.
4. Fuente propia frente a Code referenciado.
5. Navegación, enlaces e historia.
6. Foco y correspondencias: tabla con selección origen, destino, correspondencia real, evidencia, estado. Sin mapeo no hay soporte ni prueba positiva por omisión. Si WS13.1 o el catálogo lo comprometen y falta mapeo, se registra hueco con productor o cambio de alcance explícito; nunca se elimina en silencio.
7. Errores de lectura y estados de red, incluido fallo de carga CDN, para WS15.1.
8. Lectura multidesk read-only, para WS41.
9. ViewDoc: solo grafo. Selección mínima concreta y notación para WS18 declaradas si hay evidencia; si no, declarar que su promoción se detiene.
10. Authored, derivado y preferencia local; runtime volátil no es documento compartido por defecto. Sin modelo nuevo para organizar entradas o listas derivables.
11. Huecos: tabla con hueco, clase, dueño, productor o «sin productor en el DAG». Candidaturas de vistas.md siguen como tales: genérico Markdown o modelado no implica renderer especial de FAQ, issues, roles o Specs.
12. Mapa de deltas graph_ui que requieren recepción: ID, efecto, actor P01, gate, y «sin acta registrada». G_SPEC_VIEW opcional aparte. No inventar actas. El contrato básico no espera Changes, Scion ni ViewDoc opcional.
13. Trazabilidad: cada punto de «Lo que WS11 deberá precisar» en runs/subagents/20261101-ws09-vistas/result-summary.md, resuelto o con hueco.

Clases de hueco: instancia = documento concreto que falta escribir; vínculo = referencia o enlace que falta entre documentos existentes; consulta = selección o lista derivable sin operación pública para obtenerla; API = operación pública ausente en repo dueño; renderer = representación ausente en graph_ui con datos ya disponibles. Si dos aplican, elegir la que falte primero y decirlo.

Evidencia: toda API o implementación se apoya en path:línea o símbolo verificado por lectura real en el commit citado, con el archivo abierto, además de la auditoría. Sin tablas internas, endpoints hipotéticos ni pruebas no ejecutadas. frontends/workspace/ no adoptado no es base. No confundir lo existente con lo aceptado.

Límites: lectura no espera guardado ni WS12 por el estado bloqueado de una ficha compuesta. Todo hueco de escritura se remite a WS12. No actuar en repos hermanos: solo lectura. No llamar Scion vivo ni usar credenciales. «Contrato básico revisado» = Tester independiente PASS y revisión root.

Roles: el Executor escribe solo desk/drawer/plans/workspace-documental/contratos/navegacion.md y runs/subagents/20261101-ws11-navegacion/result-summary.md. Sin commits ni revisiones. Fuera de alcance: WS12, UI, Scion, push, dag.yaml, otras fuentes, helper, validadores, suite general. Sin preguntar al solicitante.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Leer auditorías, vistas.md, user-flows.md, decisiones.md, reconciliacion.md y los nodos consumidores. 2. Abrir el código real citado en ../UIs/graph_ui y ../sldb. 3. Escribir el contrato. 4. Escribir runs/subagents/20261101-ws11-navegacion/result-summary.md.

## Validation

_List the checks required before this task can close._

- test -s desk/drawer/plans/workspace-documental/contratos/navegacion.md
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status
- Tester independiente de solo lectura deja runs/subagents/20261101-ws11-navegacion/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

Acceptance: Identidad/origen/foco/enlaces y lectura multidesk definidos con APIs reales citadas por auditorías WS02–04 (path/símbolo/commit y evidencia existente); cada hueco clasificado instancia/vínculo/consulta/API/renderer y productor dueño antes de code. Mapear recepción requerida por delta en graph_ui (actor P01, IDs y efectos); enlazar acta externa solo si el receptor ya la registró. El contrato básico puede cerrar sin recepción de Changes, Scion ni ViewDoc opcional; cada delta sigue bloqueado hasta su propio recibo. G_SPEC_VIEW se obtiene separadamente al preparar WS18, sin bloquear navegación base. WS11 cierra con contrato básico revisado, clasificación de huecos y mapa de deltas que requieren recepción; puede cerrar sin acta receptora. Recibos son producidos por solicitante P01/repo receptor al preparar cada delta, no por Executor de WS11 ni por escritura interrepo. Cada delta espera su propio recibo; contrato básico no afirma que ninguno se haya recibido. Revisiones afectadas renovadas si el helper marca alguna, build --check, validate --check y status en verde, y Tester independiente PASS antes del closeout.
