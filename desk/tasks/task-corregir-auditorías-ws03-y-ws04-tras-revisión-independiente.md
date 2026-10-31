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

La revisión independiente del checkpoint WS02-WS04 halló varias afirmaciones documentales inexactas. Las tareas WS03 y WS04 ya cerraron, y sus cierres y evidencia se conservan: esta tarea corrige con commit propio. Fuente: runs/subagents/20261031-correccion-ws03-ws04/review-source.md.

## Goal

_Describe the concrete result this task must produce._

Dejar desk/drawer/plans/workspace-documental/auditoria/infraestructura.md y desk/drawer/plans/workspace-documental/auditoria/ui.md coherentes con las fuentes en los seis puntos revisados, sin ampliar alcance.

## Scope

_State what is in scope and what is out of scope._

Corrige exactamente estos seis puntos, detallados aquí y en runs/subagents/20261031-correccion-ws03-ws04/review-source.md. Las rutas ../ son relativas a la raíz de deskops.

Punto 1, desk/drawer/plans/workspace-documental/auditoria/infraestructura.md, §2.1 fila Verificación optimista en HTTP, filas de cache y resumen: hoy dice que el payload actual se extrae del archivo. Debe decir payload obtenido por carga runtime sujeta a cache, con el límite de frescura: una edición externa que no altere índices puede preceder a /save y no observarse en expected. Abrir http_server.py, save_routes.py, store/runtime_cache.py y store/runtime_cache_signature.py en ../sldb/src/sldb y citar las líneas reales, incluido dónde se llama o no new_operation. Decir que es deducción estática, no reproducida en runtime. No afirmar cache fresca por defecto. Mantener a la vez dos hechos: no hay CAS por hash, y expected sí es una comparación optimista pública por valor.

Punto 2, desk/drawer/plans/workspace-documental/auditoria/ui.md, fila de SPEC sobre + Add relation: /home/jp/proyectos/softfactory_spec/SPEC.md:79-82 habla de aristas semánticas sin archivo físico directo; ../UIs/graph_ui/frontends/mindmap/views/documents/map/connect-dialog.js:9-17 modifica campos de referencia. No equivalen. La comparación debe decir capacidad no cubierta o no comprobada como arista autónoma, sin refutar al SPEC con WS19.2 sin un puente demostrado.

Punto 3, desk/drawer/plans/workspace-documental/auditoria/ui.md, línea del encabezado de discrepancias (hoy ui.md:42) sobre task.txt de ../UIs/graph_ui/runs/subagents/20261031-workspace-ui: es snapshot histórico. Comprobar con git que f16fcd1 borra el archivo de la TaskDoc con `git show --stat f16fcd1` y que 134a665 actualiza Board, y dejar registrado que no hay contradicción actual.

Punto 4, desk/drawer/plans/workspace-documental/auditoria/infraestructura.md, fila Consultas guardadas: delimitar con la capacidad vecina ProjectionDoc de pron, persistida y evaluada: pron/models/projection.py:14, world/projection_reader.py:22, world/lexicon.py:137 bajo ../pron/src. Precisar qué selecciona, cómo se evalúa y por qué no equivale a un where guardado ni a ViewDoc. El grep de saved_query no alcanza para negar toda selección persistida; la fila distingue lo verificado.

Roles: el Executor edita solo esos dos archivos y escribe evidencia en runs/subagents/20261031-correccion-ws03-ws04/ (result-summary.md). El Supervisor agrega en runs/subagents/20261031-ws02-04-checkpoint/handoff.md una nota de supersesión fechada, sin borrar el texto original, y escribe el handoff nuevo en runs/subagents/20261031-ws02-04-checkpoint/handoff-correccion.md. El Supervisor corre validaciones, commits y closeout. Un Tester independiente de solo lectura verifica.

Fuera de alcance: código de sldb, pron, spec2viz o graph_ui, dag.yaml, reconciliacion.md, brief.md, WS02, WS06, las demás filas, y reabrir cierres previos. Si algo no se puede comprobar leyendo, queda «no ejecutado» o «fuera de alcance», nombrando el test aislado futuro que lo probaría, sin diseñarlo. Si la fuente contradice un punto de la revisión, no lo corrijas a ciegas: repórtalo con cita en result-summary.md.

Punto 5, ViewDoc, en desk/drawer/plans/workspace-documental/auditoria/infraestructura.md §5.2 y §6 y en desk/drawer/plans/workspace-documental/auditoria/ui.md: el dictamen «solo modelo, sin evaluador» es válido únicamente dentro del universo sldb, pron y spec2viz de WS03, y eso debe decirse así. §6 no concluye que WS18 deba construir un evaluador: remite a que graph_ui ya tiene un consumidor. En ui.md, agregar como base reutilizable lo que exista en ../UIs/graph_ui: frontends/mindmap/projection_views.py (evaluate_view, selección, relation_edges, list_views, find_view), views_routes.py (GET /api/views, GET y POST /api/views/evaluate, POST /api/views/save), su conexión en serve.py incluido el límite local-only (remote 501), tests/test_projection_views.py y tests/e2e_review_workbench_views.py como pruebas existentes no ejecutadas, y los commits 0eb7dd7, b9ab83c y 2a15356. Abrir cada archivo y citar las líneas reales. Enlazar WS18 y WS24 donde corresponda; WS18 no está en la lista de 35 nodos graph_ui de ui.md, así que se agrega como nota o fila solo referencia indicando que su dueño es otro repo. Mantener separados modelo, evaluador, renderer y notación. No anunciar aceptación del producto ampliado.

Precisiones. Los repos de los commits f16fcd1, 134a665, 0eb7dd7, b9ab83c y 2a15356 son ../UIs/graph_ui. Las auditorías son fuentes authored, no generadas: build_plan.py no las reescribe. «Resumen» = secciones de la propia auditoría que repitan la afirmación corregida, incluida §6 de infraestructura.md. «Filas de cache» = filas de §1 y §2.1 que mencionen runtime_cache, cache o frescura. Línea de encabezado: una línea de texto bajo el título, con «Corrección 2026-10-31» y motivo. Nota de supersesión: párrafo fechado 2026-10-31 al inicio de handoff.md. Este PASS del Tester es requisito de closeout.

Punto 6, desk/drawer/plans/workspace-documental/auditoria/ui.md y desk/drawer/plans/workspace-documental/auditoria/infraestructura.md: en ui.md, «sin dueño» de frontends/workspace significa sin reclamo en Board o TaskDoc observados, no autoría desconocida; la ausencia de /app.js se respalda citando que su serve.py sirve ese directorio sin ruta JS ni fallback; no se presenta como requisito previo de WS06 sino de adoptarlo como base ejecutable autorizada. En ambos archivos, lo que diga que un comportamiento no se pudo probar se expresa como «no ejecutado: fuera de alcance», sin sugerir imposibilidad, y con el test futuro en sandbox propio que lo probaría, sin diseñarlo. WS02 está aceptado y no se toca. La base del git diff de Validation, 2286b976, es el cierre de la fase documental anterior.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Leer review-source.md y las fuentes citadas. 2. Editar solo las filas de los seis puntos y el resumen afectado, conservando el formato de tabla. 3. Agregar a cada archivo una línea en su encabezado con fecha y motivo de la corrección. 4. Escribir result-summary.md con antes y después de cada fila.

## Validation

_List the checks required before this task can close._

- test -s desk/drawer/plans/workspace-documental/auditoria/infraestructura.md
- test -s desk/drawer/plans/workspace-documental/auditoria/ui.md
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status
- git diff --stat 2286b976..HEAD -- deskops/ tests/ docs/ desk/drawer/plans/workspace-documental/dag.yaml desk/drawer/plans/workspace-documental/reconciliacion.md queda vacío (deskops/ es el paquete de código, no el repo)
- Tester independiente de solo lectura deja runs/subagents/20261031-correccion-ws03-ws04/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

Los seis puntos están corregidos con citas abiertas en la fuente, sin afirmar nada ejecutado, sin tocar otras filas, y un Tester independiente da PASS.
