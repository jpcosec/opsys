---
id: task-ws06-proponer-correspondencia-de-alcance-con-repos-dueños
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- runs/subagents/20261031-ws02-04-checkpoint/approval.md
- desk/drawer/plans/workspace-documental/auditoria/deskops.md
- desk/drawer/plans/workspace-documental/auditoria/infraestructura.md
- desk/drawer/plans/workspace-documental/auditoria/ui.md
- desk/drawer/plans/workspace-documental/dag.yaml
- desk/drawer/plans/workspace-documental/decisiones.md
- desk/drawer/plans/workspace-documental/alcance.md
- desk/rituals/context-review.md
depends_on: []
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-007-phase-gated-task-flow.md
- desk/contexts/pill-ready-phases-prove-dependencies-and-non-overlap.md
files:
- desk/drawer/plans/workspace-documental/reconciliacion.md
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/workspace-documental/task-ws06.md
closeout_evidence:
- commit
- document
---

# WS06: Proponer correspondencia de alcance con repos dueños

## Rationale

_Explain why this task exists or the business driver behind it._

Las auditorías WS02-WS04 fueron aprobadas como inventario documental y levantan la pausa de WS06 (runs/subagents/20261031-ws02-04-checkpoint/approval.md). La matriz traduce sus datos a capacidades y deltas por repo dueño antes de definir contratos.

## Goal

_Describe the concrete result this task must produce._

Agregar a desk/drawer/plans/workspace-documental/reconciliacion.md una matriz de correspondencia por capacidad o delta único, agrupada por repo dueño, con evidencia citada y sin aceptar nada.

## Scope

_State what is in scope and what is out of scope._

Una matriz con una fila por delta o capacidad única (varios nodos pueden remitir a la misma fila), agrupada por repo dueño: ya cubierto (capacidad observable en código implementado, citando path/símbolo y commit observado), extender ticket existente (incluido un draft del Board) o nuevo delta. La fila Scion RunDoc/cierre de reconciliacion.md conserva el tratamiento ya registrado (descomposición en WS32/33) sin requerir WS05. Registrar en reconciliacion.md la atomización propuesta, sin notificar, despachar ni modificar el Board de graph_ui; el responsable receptor ya designado en P01 acepta por delta en WS11/12.

Salida: agregar a desk/drawer/plans/workspace-documental/reconciliacion.md una sección «Matriz de correspondencia WS06» y conservar sin cambios el texto existente. Las rutas ../ son relativas a la raíz del repo deskops. Insumos autoritativos: desk/drawer/plans/workspace-documental/auditoria/deskops.md, infraestructura.md y ui.md, aprobados en runs/subagents/20261031-ws02-04-checkpoint/approval.md; desk/drawer/plans/workspace-documental/dag.yaml, decisiones.md, alcance.md y el texto actual de reconciliacion.md. Se puede abrir el código citado para confirmar una fila; no reauditar.

Formato: un subtítulo por repo dueño (graph_ui, sldb, spec2viz, deskops y otros si aparecen) y una tabla con columnas: ID estable C-nn; capacidad o delta; nodos DAG que remiten a ella; clasificación (ya cubierto, extender ticket, nuevo delta); path o símbolo y commit observado; ticket o delta destino; responsable; límites de evidencia. Una fila por capacidad: varios nodos pueden remitir a la misma fila, y no se agrupa por nodo. Clasificación: ya cubierto = capacidad observable en código, con path o símbolo y commit, sin afirmar aceptación ampliada; extender ticket = cabe en un ticket existente, incluido un draft del Board; nuevo delta = no cabe, se propone atomizado. El dueño de la fila es el repo donde vive el código a cambiar, no el owner_repo del nodo si difieren; la diferencia se dice en límites.

Cobertura: al final, una tabla con los 63 nodos de dag.yaml y su fila C-nn, o el motivo por el que no generan delta (planificación, validación humana, agregado). Ningún nodo queda sin fila.

Reglas de contenido:
- Responsable: P01 designa al solicitante para graph_ui, sldb y spec2viz. Si un repo dueño no está en P01, se escribe «no designado en P01», sin inventar. El operador Scion se designa después y solo aparece en el ramal E.
- Tickets de edición y Changes: comparten serve.py, views/workspace/ y docs/workspace-ui.md. Se extienden en serie; no se propone ejecución paralela a ellos.
- frontends/workspace de graph_ui no se adopta como base aprobada: fila con ese estado, sin reclamo en Board o TaskDoc, sin commit.
- ViewDoc: reutilización primero. El modelo vive en spec2viz; el evaluador y las rutas en graph_ui, solo en modo local. No proponer evaluador de cero.
- expected: existe como comparación pública por valor en HTTP, pero no acredita CAS compartido ni frescura para API o CLI. Fila de capacidad, limitación y tarea dueña, sin inventar garantía. No proponer API que no exista como si existiera: un faltante es delta con productor.
- Scion RunDoc/cierre conserva la descomposición en WS32/33, sin requerir WS05.
- WS06 no produce aceptación ni permiso interrepo. El texto «acepta por delta en WS11/12» se lee así: el receptor P01 produce recibos externos en su repo al preparar cada delta; WS11 y WS12 son fuente de contrato y solo enlazan recibos. Ninguna fila dice aceptado.
- Sin notificar, despachar, ni tocar el Board de graph_ui. No reabrir decisiones P01-P09.

Cambios fuera de scope: si la matriz revela algo imprescindible en brief.md, dag.yaml, candidatas u otro documento, no se aplica. Se lista en runs/subagents/20261031-ws06-reconciliacion/canonical-adjustments.md con archivo, cambio propuesto, evidencia y nodos afectados.

Efecto esperado y declarado: reconciliacion.md es input de revisión barata de 25 nodos (PK01, WS04, WS06, WS13, WS13.1, WS13.2, WS13.3, WS14, WS15, WS15.1, WS15.2, WS19, WS19.1, WS19.2, WS21, WS22, WS23, WS24, WS29, WS32, WS32.1, WS32.2, WS33, WS33.1, WS33.2). Tras editarla, context_review.py status debe listar exactamente esos nodos como «input changed» y validate_plan.py --check falla por eso. No se corrige en WS06, porque exige escribir en dag.yaml: el Supervisor lo captura como tarea de ajuste canónico.

Roles: el Executor edita solo reconciliacion.md y escribe runs/subagents/20261031-ws06-reconciliacion/canonical-adjustments.md y runs/subagents/20261031-ws06-reconciliacion/result-summary.md; sin commits ni closeout. El Supervisor corre validaciones, commits y closeout. Un Tester independiente de solo lectura verifica. Fuera de alcance: WS05, WS07, WS08-12, código, dag.yaml, brief.md, auditorías.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Leer insumos. 2. Extraer capacidades únicas de las tablas de ui.md, infraestructura.md y deskops.md y de reconciliacion.md. 3. Escribir la matriz por repo dueño. 4. Escribir la tabla de cobertura de nodos. 5. Escribir canonical-adjustments.md. 6. result-summary.md con conteos, decisiones de clasificación dudosas y lo no comprobado.

## Validation

_List the checks required before this task can close._

- test -s desk/drawer/plans/workspace-documental/reconciliacion.md
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status lista exactamente los 25 nodos declarados y ninguno más
- git diff --stat 3e1c24f0..HEAD -- deskops/ tests/ docs/ desk/drawer/plans/workspace-documental/dag.yaml desk/drawer/plans/workspace-documental/brief.md desk/drawer/plans/workspace-documental/auditoria/ vacío (deskops/ es el paquete de código)
- Tester independiente de solo lectura deja runs/subagents/20261031-ws06-reconciliacion/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

Acceptance: Matriz con una fila por delta o capacidad propuesta, agrupada por repo dueño, no por nodo del DAG; correspondencia ticket/delta y responsable ya designado P01; operador Scion posterior solo para ramal E; no produce gates de aceptación ni aprueba deltas que aún no están definidos. WS11/12 obtienen aceptación específica por repo receptor. Aclaración vigente: la aceptación específica la producen recibos externos del receptor P01; WS11 y WS12 son fuente de contrato. Además: cada nodo de dag.yaml aparece en la cobertura, y un Tester independiente da PASS.
