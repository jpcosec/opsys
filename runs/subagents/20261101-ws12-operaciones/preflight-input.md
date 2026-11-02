FILE:desk/tasks/task-ws12-cerrar-contrato-de-operaciones-y-escritura.md
---
id: task-ws12-cerrar-contrato-de-operaciones-y-escritura
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/workspace-documental/contratos/navegacion.md
- desk/drawer/plans/workspace-documental/contratos/navegacion-aprobacion.md
- desk/drawer/plans/workspace-documental/decisiones.md
- desk/drawer/plans/workspace-documental/dag.yaml
- desk/drawer/plans/workspace-documental/auditoria/deskops.md
- desk/drawer/plans/workspace-documental/auditoria/infraestructura.md
- desk/drawer/plans/workspace-documental/auditoria/ui.md
- desk/drawer/plans/workspace-documental/borradores/user-flows.md
- desk/drawer/plans/workspace-documental/borradores/vistas.md
- runs/subagents/20261031-atribucion-decisiones/root-decision-20261101.md
- runs/subagents/20261031-ajuste-canonico-ws06/promotion-notes.md
- runs/subagents/20261101-ws11-disponibilidad/review-source.md
depends_on: []
pills:
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-001-task-closure-commit.md
files:
- desk/drawer/plans/workspace-documental/contratos/operaciones.md
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/workspace-documental/task-ws12.md
closeout_evidence:
- commit
- document
---

# WS12: Cerrar contrato de operaciones y escritura

## Rationale

_Explain why this task exists or the business driver behind it._

La revisión root aprobó el contrato WS11 y autorizó solo WS12. Los deltas de escritura no pueden prepararse sin una matriz de capacidades, efectos y huecos con dueño.

## Goal

_Describe the concrete result this task must produce._

Crear desk/drawer/plans/workspace-documental/contratos/operaciones.md con la matriz por operación, modelo, campo, canal, actor, revisión, Git y efectos, separando lo existente con evidencia citable de los huecos con dueño y productor.

## Scope

_State what is in scope and what is out of scope._

Autoriza: runs/subagents/20261101-ws11-disponibilidad/review-source.md, última parte, que prevalece sobre este resumen. Autorización acotada: execution_authorized global sigue false.
Contrato del nodo: WS12 en desk/drawer/plans/workspace-documental/dag.yaml, scope y acceptance completos.

Secciones obligatorias de contratos/operaciones.md, en este orden:

1. Alcance y estado: qué fija, qué no, commits observados.
2. Matriz: una fila por operación, con modelo, campo, canal público, actor, revisión o precondición, Git, efectos y estado (existente con evidencia citada, o hueco con dueño y productor). Incluye lectura y mutación, y los comandos de diagnóstico clasificados por efectos.
3. Campos protegidos por modelo y lifecycle auditados: por modelo y operación. No lista universal inventada. Ningún estado se edita por payload.
4. Adapter: canal público existente por operación. Si no existe, hueco y dueño.
5. Política de coordinador y modo manual exclusivo (T-P03.1): definición operativa, formas de comprobarla y respuesta ante falta de evidencia. La ausencia de señal no declara exclusividad. El lock de UI no coordina CLI ni agentes. Con otro coordinador escritor, lectura o handoff hasta autoridad compartida probada.
6. Precondición de escritura: distinguir before-image por valor con expected y 409, token publicado y capacidad compartida aún no probada. WS12 elige justificadamente la representación, las operaciones y los escritores alcanzados. WS45 la verifica, independiente de raw-source. Sin CAS por hash en toda CLI por reflejo.
7. Captura a drawer y protoátomo: comparar API pública existente, composición de llamadas y eventual wrapper, con origen, colisiones y no crear tarea activa, con prueba real. message send más promote no queda aprobado.
8. Ack y respuesta local de inbox: no pasan a disponibles por un comando parecido.
9. Git, guardar no commitea, cierre y promoción por workflow, fallos parciales, permisos y canales de closeout fuera del servidor UI.
10. Recepción por delta: qué recibo o prueba corresponde a cada delta, receptor y efecto. G_WRITE_CONTRACT y G_UI_WRITE por IDs y efecto, nunca conjuntos. G_CLOSEOUT, G_SOURCE, G_SLDB_WRITE y G_PAYLOAD_PRECONDITION según la aceptación. En deltas de deskops no hay recepción nueva. No se crean actas.
11. Ramal E: sección por delta de WS34.1 y WS34.2 con política de timeout de dispatch y reply, clasificación observable (al menos aceptado, rechazado, vencido sin confirmación), actor y momento de preparación. Sin valor nuevo ahora. Su ausencia no impide cerrar el núcleo.
12. Huecos: tabla con hueco, clase, dueño, productor o «sin productor en el DAG». El contrato puede cerrar con huecos asignados.
13. Trazabilidad: cada frase de aceptación de WS12, T-P03.1, y lo que las notas de promoción y contratos/navegacion.md remiten a WS12.

Evidencia: toda capacidad se apoya en path:línea o símbolo abierto en el commit citado. Comprobado requiere API o prueba existente citada. Lectura estática no es prueba de runtime: se dice cuál es cuál. Negaciones por búsqueda declarada, nunca por conteo. Distinguir existe de aceptado.

Roles: el Executor escribe solo desk/drawer/plans/workspace-documental/contratos/operaciones.md y runs/subagents/20261101-ws12-operaciones/result-summary.md. Sin commits ni revisiones.

Fuera de alcance: código de UI, API, sldb, actas interrepo, habilitar mutaciones, Scion, push, dag.yaml, fuentes comunes, helper, validadores, suite general, repos hermanos salvo lectura. Sin preguntar al solicitante.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Leer contrato aprobado de navegación, decisiones.md con T-P03.1, nodo WS12 y consumidores, auditorías, user-flows y vistas. 2. Abrir el código real citado. 3. Escribir el contrato. 4. Escribir result-summary.md.

## Validation

_List the checks required before this task can close._

- test -s desk/drawer/plans/workspace-documental/contratos/operaciones.md
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status
- Tester independiente de solo lectura deja runs/subagents/20261101-ws12-operaciones/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

Acceptance: la del nodo WS12 de dag.yaml completa, más T-P03.1; matriz publicada con capacidades y huecos asignados; G_WRITE_CONTRACT sigue pendiente de root; Tester independiente PASS antes del closeout; revisiones afectadas renovadas solo si hay staleness medida; build --check, validate --check y status en verde; checkpoint root antes de código UI, SLDB o ramal Scion.

