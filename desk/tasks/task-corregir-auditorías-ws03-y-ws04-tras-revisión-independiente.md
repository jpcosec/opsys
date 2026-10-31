---
id: task-corregir-auditorías-ws03-y-ws04-tras-revisión-independiente
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- runs/subagents/20261031-correccion-ws03-ws04/review-source.md
- runs/subagents/20261031-ws02-04-checkpoint/handoff.md
- desk/drawer/plans/workspace-documental/auditoria/infraestructura.md
- desk/drawer/plans/workspace-documental/auditoria/ui.md
- desk/rituals/context-review.md
depends_on: []
pills: []
files:
- desk/drawer/plans/workspace-documental/auditoria/infraestructura.md
- desk/drawer/plans/workspace-documental/auditoria/ui.md
- runs/subagents/20261031-ws02-04-checkpoint/handoff.md
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-corregir-auditorias-ws03-y-ws04-tras-revision.md
closeout_evidence:
- commit
- document
---

# Corregir auditorías WS03 y WS04 tras revisión independiente

## Rationale

_Explain why this task exists or the business driver behind it._

La revisión independiente del checkpoint WS02-WS04 halló cuatro afirmaciones documentales inexactas. Las tareas WS03 y WS04 ya cerraron, y sus cierres y evidencia se conservan: esta tarea corrige con commit propio. Fuente: runs/subagents/20261031-correccion-ws03-ws04/review-source.md.

## Goal

_Describe the concrete result this task must produce._

Dejar desk/drawer/plans/workspace-documental/auditoria/infraestructura.md y desk/drawer/plans/workspace-documental/auditoria/ui.md coherentes con las fuentes en los cuatro puntos revisados, sin ampliar alcance.

## Scope

_State what is in scope and what is out of scope._

Corrige exactamente estos cuatro puntos, descritos en runs/subagents/20261031-correccion-ws03-ws04/review-source.md. Las rutas ../ son relativas a la raíz de deskops.

Punto 1, desk/drawer/plans/workspace-documental/auditoria/infraestructura.md, §2.1 fila Verificación optimista en HTTP, filas de cache y resumen: hoy dice que el payload actual se extrae del archivo. Debe decir payload obtenido por carga runtime sujeta a cache, con el límite de frescura: una edición externa que no altere índices puede preceder a /save y no observarse en expected. Abrir http_server.py, save_routes.py, store/runtime_cache.py y store/runtime_cache_signature.py en ../sldb/src/sldb y citar las líneas reales, incluido dónde se llama o no new_operation. Decir que es deducción estática, no reproducida en runtime. No afirmar cache fresca por defecto. Mantener a la vez dos hechos: no hay CAS por hash, y expected sí es una comparación optimista pública por valor.

Punto 2, desk/drawer/plans/workspace-documental/auditoria/ui.md, fila de SPEC sobre + Add relation: SPEC.md:79-82 habla de aristas semánticas sin archivo físico directo; connect-dialog.js:9-17 modifica campos de referencia. No equivalen. La comparación debe decir capacidad no cubierta o no comprobada como arista autónoma, sin refutar al SPEC con WS19.2 sin un puente demostrado.

Punto 3, desk/drawer/plans/workspace-documental/auditoria/ui.md, línea de task.txt de ../UIs/graph_ui/runs/subagents/20261031-workspace-ui: es snapshot histórico. Comprobar con git que f16fcd1 elimina o cierra la TaskDoc y que 134a665 actualiza Board, y dejar registrado que no hay contradicción actual.

Punto 4, desk/drawer/plans/workspace-documental/auditoria/infraestructura.md, fila Consultas guardadas: delimitar con la capacidad vecina ProjectionDoc de pron, persistida y evaluada: pron/models/projection.py:14, world/projection_reader.py:22, world/lexicon.py:137 bajo ../pron/src. Precisar qué selecciona, cómo se evalúa y por qué no equivale a un where guardado ni a ViewDoc. El grep de saved_query no alcanza para negar toda selección persistida; la fila distingue lo verificado.

Roles: el Executor edita solo esos dos archivos y escribe evidencia en runs/subagents/20261031-correccion-ws03-ws04/ (result-summary.md). El Supervisor agrega en runs/subagents/20261031-ws02-04-checkpoint/handoff.md una nota de supersesión fechada, sin borrar el texto original, y escribe el handoff nuevo. El Supervisor corre validaciones, commits y closeout. Un Tester independiente de solo lectura verifica.

Fuera de alcance: código de sldb, pron, spec2viz o graph_ui, dag.yaml, reconciliacion.md, brief.md, WS02, WS06, las demás filas, y reabrir cierres previos. Si algo no se puede comprobar leyendo, queda «no ejecutado» o «fuera de alcance», nombrando el test aislado futuro que lo probaría, sin diseñarlo. Si la fuente contradice un punto de la revisión, no lo corrijas a ciegas: repórtalo con cita en result-summary.md.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Leer review-source.md y las fuentes citadas. 2. Editar solo las filas de los cuatro puntos y el resumen afectado, conservando el formato de tabla. 3. Agregar a cada archivo una línea en su encabezado con fecha y motivo de la corrección. 4. Escribir result-summary.md con antes y después de cada fila.

## Validation

_List the checks required before this task can close._

- test -s desk/drawer/plans/workspace-documental/auditoria/infraestructura.md
- test -s desk/drawer/plans/workspace-documental/auditoria/ui.md
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status
- git diff --stat 2286b976..HEAD sobre deskops, tests, dag.yaml y reconciliacion.md vacío
- Tester independiente de solo lectura deja runs/subagents/20261031-correccion-ws03-ws04/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

Los cuatro puntos están corregidos con citas abiertas en la fuente, sin afirmar nada ejecutado, sin tocar otras filas, y un Tester independiente da PASS.
