FILE:desk/tasks/task-consolidar-ajuste-canónico-del-plan-workspace-tras-ws06.md
---
id: task-consolidar-ajuste-canónico-del-plan-workspace-tras-ws06
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- runs/subagents/20261031-ajuste-canonico-ws06/review-source.md
- runs/subagents/20261031-ws06-reconciliacion/handoff.md
- runs/subagents/20261031-ws06-reconciliacion/canonical-adjustments.md
- desk/drawer/plans/workspace-documental/dag.yaml
- desk/drawer/plans/workspace-documental/brief.md
- desk/drawer/plans/workspace-documental/reconciliacion.md
- desk/rituals/context-review.md
depends_on: []
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-007-phase-gated-task-flow.md
- desk/contexts/pill-ready-phases-prove-dependencies-and-non-overlap.md
files:
- desk/drawer/plans/workspace-documental/brief.md
- desk/drawer/plans/workspace-documental/dag.yaml
- desk/drawer/plans/workspace-documental/reconciliacion.md
- runs/subagents/20261031-ws06-reconciliacion/canonical-adjustments.md
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-ajuste-canonico-tras-ws06.md
closeout_evidence:
- commit
- document
---

# Consolidar ajuste canónico del plan workspace tras WS06

## Rationale

_Explain why this task exists or the business driver behind it._

La revisión root de WS06 rechazó dejar validate_plan en FAIL y corrigió extrapolaciones de la matriz. Autorización y seis cambios obligatorios en runs/subagents/20261031-ajuste-canonico-ws06/review-source.md.

## Goal

_Describe the concrete result this task must produce._

Dejar brief.md, dag.yaml, reconciliacion.md y canonical-adjustments.md coherentes con la evidencia, con los nodos afectados re-revisados y build --check, validate --check y context_review status en verde, sin implementar nada.

## Scope

_State what is in scope and what is out of scope._

Solo planificación en deskops. Archivos permitidos: desk/drawer/plans/workspace-documental/brief.md, desk/drawer/plans/workspace-documental/dag.yaml, desk/drawer/plans/workspace-documental/reconciliacion.md, runs/subagents/20261031-ws06-reconciliacion/canonical-adjustments.md y las proyecciones que build_plan.py y render_diagram.py generan, incluidas fichas en desk/drawer/tasks/workspace-documental/. Helpers locales del plan solo si son imprescindibles, nunca debilitando un validador. runs/subagents/20261031-ajuste-canonico-ws06/review-source.md es parte obligatoria del contrato: los puntos A a F rigen sobre este resumen.

A, ViewDoc: C-50 y ajuste 3. No falta portabilidad genérica: ViewDoc es datos sin ruta de store, y evaluate_view(store, view) evalúa con store por petición. C-50 pasa a nuevo delta de autoría de ViewDoc y NotationDoc concretos definidos por WS09/WS11 y su comprobación sobre stores reales reutilizando C-37 y C-49. Se retira «falta portabilidad o independencia del host» y toda extracción o compartición implícita del evaluador. WS18 no pide servicio, CLI ni runtime fuera de graph_ui. output_scope sldb/views/ con output_base spec2viz puede ser legítimo: se confirma ruta y registro según contrato, sin cambiar dueño por el prefijo.

B, revisión: C-41 y ajuste 1. Glosario de brief.md distingue tres cosas: before-image por valor existente (expected, HTTP 409); token publicado (version/content_hash); y comparación o escritura pública con precondición compartida, aún no probada. No se niega la capacidad optimista real, no se infiere frescura por cada CLI, no se fuerza CAS en toda CLI ni un algoritmo: WS12 define representación, precondición, operaciones y escritores alcanzados. P03 no cambia. Se crea un nodo productor nuevo, WS45, en sldb, para verificar o completar la precondición de escritura de payload, independiente de source_mode: primero reutilizar, pruebas reales focalizadas, código solo si falta al ejecutarlo. WS20 conserva raw-source; C-41 deja de decir que WS20 solo nombra raw-source. Consumidores conectados por efecto real o gate técnico explícito, sin bloquear al lector.

C, captura: C-55 y ajuste 2. Pasa a canal permitido de captura a drawer con origen preservado, sin tarea activa y colisiones controladas, pendiente del contrato WS12, que compara API SLDB existente, composición y eventual wrapper Deskops. Primitivas a citar: sldb.api create_document y DrawerService. No se crea API ni modelo por reflejo; message send más promote no queda aprobado, por borrar la nota y dejar why apuntando a una ruta borrada, y por meter trabajo local en inbox. Productor Deskops explícito solo si falta conducta de workflow, antes de WS25.2.

D, Scion y recibos: C-64 y ajuste 4. Precisar que WS06 puede clasificar y conservar la descomposición sin ejecutar WS05, y que WS32/33 conservan dependencias y gates canónicos. Textos ambiguos de WS06 pasan a acta del receptor P01 y WS11/12 como fuente de contrato, sin firmas, gates ni recepción ficticia. «No designado en P01» de deskops es dato de esa tabla, no un permiso que frene trabajo local.

E, coherencia: en esta consolidación no se preservan como prefijo intacto cláusulas viejas contradictorias de reconciliacion.md; la historia está en Git. No cambian P01-P09, código de producto, repos hermanos, Scion, ni frontends/workspace. WS45 lleva owner, prerrequisitos, entregable, aceptación y revisión real, sin mezclarse con UI ni con un productor condicional. El plan no afirma implementación ni aceptación de deltas.

F, orden y validación: primero los cambios A-D y correcciones de la matriz; luego fuentes congeladas; luego re-review barato de todos los inputs y contratos afectados y de todos los nodos nuevos y agrupadores. Los 25 son el estado actual, no el límite: un cambio en brief.md puede invalidar todos. Procesos frescos sin contexto ni herramientas, stdin DEVNULL, disposiciones sinceras por nodo. Regenerar proyecciones. Tester independiente. No debilitar validadores ni dar covered_work como cierre de TaskDoc. execution_authorized sigue false y status final_plan_reviewed.

Roles: el Executor edita los archivos permitidos y puede correr build_plan.py para regenerar, sin commits. No corre context_review.py run. El Supervisor congela, corre revisiones, escribe disposiciones, registra context_review en dag.yaml, hace commits y closeout. Si aparece una decisión de producto no cubierta, se registra en runs/subagents/20261031-ajuste-canonico-ws06/open-decisions.md antes de improvisar.

Fuera de alcance: WS07, WS08-12, WS05, código, tocar auditorías, reabrir cierres, push.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Leer review-source.md y las fuentes. 2. Executor aplica A-E y escribe runs/subagents/20261031-ajuste-canonico-ws06/result-summary.md con antes y después. 3. Supervisor revisa, regenera y congela. 4. context_review.py run --stale y disposiciones. 5. Si una revisión revela defecto, corregir y repetir solo lo afectado. 6. Tester. 7. Closeout y handoff.

## Validation

_List the checks required before this task can close._

- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status
- git diff --name-only 6d41f301..HEAD -- deskops/ tests/ docs/ desk/drawer/plans/workspace-documental/decisiones.md desk/drawer/plans/workspace-documental/auditoria/ queda vacío (deskops/ es el paquete de código)
- Tester independiente de solo lectura deja runs/subagents/20261031-ajuste-canonico-ws06/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

build_plan.py --check y validate_plan.py --check salen 0, context_review.py status dice all reviews current, WS45 existe con contrato completo, C-41, C-50, C-55 y C-64 cumplen A-D, sin código ni P01-P09 cambiados, y un Tester independiente da PASS.

FILE:runs/subagents/20261031-ajuste-canonico-ws06/review-source.md
# Decisión de revisión root WS06, texto recibido

Fuente: mensaje de Codex `w3Y:p2` en el pane Claude `w3Y:p1`, 2026-10-31. Autoriza la consolidación canónica acotada `task-ajuste-canonico-tras-ws06`.

Verificado por root: 68 filas únicas (33/32/2/1), 63/63, hash 7a85a581…6bce, prefijo 3e1c24f0 intacto, build --check PASS, validate --check FAIL por exactamente 25 inputs declarados. Ese FAIL no se acepta como estado final: se restaura antes de WS07 o código.

A) C50/ajuste 3: NO falta una capability genérica de portabilidad. ViewDoc es datos sin store path; projection_views.py:107 evaluate_view(store,view) y views_routes.py:9-10,69+ evalúan con store por petición. test_projection_views.py:151-156 usa dos stores (no ejecutado; cambia filtros, no alegar que prueba idéntico payload completo). WS18 «mismo ViewDoc sin código específico del host» NO pide crear servicio/CLI/runtime fuera de graph_ui. C50 puede ser NUEVO DELTA de AUTORÍA de ViewDoc/NotationDoc concretos que WS09/WS11 definan y su comprobación sobre stores reales REUTILIZANDO C37/C49. Retirar «falta portabilidad/independencia host» y extracción/compartición del evaluador como requisito implícito. `store.parent / sldb/views/` (views_routes.save_view) es carpeta en proyecto dueño del store, NO prueba que output_scope sldb/views/ pertenezca al repo hermano sldb. Con output_base spec2viz:repository_root puede ser spec2viz/sldb/views/ legítimo: confirmar ruta/registro según contrato, no cambiar dueño por prefijo textual.

B) C41/ajuste 1: fijar glosario distinguiendo before-image por VALOR existente (expected HTTP 409), token publicado (version/content_hash), y comparación/escritura pública con precondición compartida aún no probada. No negar capacidad optimista real, no inferir frescura por cada CLI. No forzar CAS en toda CLI ni algoritmo hash por inercia: contrato WS12 define representación/precondición/operaciones/escritores alcanzados; P03 sigue UI read-only/handoff si otro coordinador hasta canal seguro real. Como el guardado de CAMPOS no puede depender del modo raw-source, crear productor de verificación/compleción de la precondición de escritura payload INDEPENDIENTE de source_mode cuando no hay capacidad que satisfaga contrato (sldb; reuse first, test reales focalizados, código solo si falta al ejecutarlo). No meterlo silenciosamente en WS20 condicionado editable; WS20 conserva raw-source. Conectar consumidores por efecto real/gate técnico explícito sin bloquear lector. Corregir también C41 frase «WS20 solo nombra raw-source»: WS20 ya exige revisión/conflicto para raw-source; hueco de campos separado.

C) C55/ajuste 2: ausencia de comando DESKOPS especializado no equivale ausencia de primitiva pública. sldb.api.create_document(model,payload,path) existe (create_document.py:22); DrawerService define candidato TaskDoc drawer.py:255. No afirmo canal UI completo: hay colisiones/sobrescritura/origen/whitelist que verificar. Reformular C55 a CANAL PERMITIDO de captura drawer con origen preservado, sin tarea activa y colisiones controladas, pendiente contrato WS12. WS12 compara API SLDB existente, composición y eventual wrapper Deskops. No crear API/modelo nuevo por reflejo. message send + promote NO se aprueba automáticamente: promoción borra nota y why apunta a ruta borrada (drawer.py:261), hay que probar tipos de origen/fallo parcial y no meter trabajo local innecesariamente en inbox (AGENTS). Solo si falta conducta WORKFLOW, productor Deskops explícito ANTES de WS25.2; si API compuesta cumple, se documenta prueba/contrato y no se inventa otro productor. Dependencia futura WS12 está asignada, no es permiso para implementar fake.

D) C64/ajuste 4: precisar literal «WS06 puede clasificar y conservar descomposición sin EJECUTAR WS05; WS32/33 conservan dependencias/gates canónicos». Hoy «no se requiere WS05» puede leerse eliminar WS32→WS05; no hacerlo. Recibos externos: reemplazar textos ambiguos WS06 por receptor P01 acta / WS11/12 contract source, no agregar firmas, gates ni recepción ficticia. «No designado en P01» deskops es dato limitado de esa tabla, NO crear nuevo permiso que frene trabajo local autorizado por usuario.

E) AJUSTE COHERENTE: TaskDoc puede incluir reconciliacion.md (C41/C50/C55/C64 y referencias relacionadas), canonical-adjustments.md, brief.md, dag.yaml, candidatas/proyecciones/helpers locales imprescindibles. No preservar cláusulas viejas contradictorias como prefijo «intacto» en esta consolidación; historia ya en Git. No cambiar decisiones humanas P01-P09 ni código de producto/repos hermanos. No Scion ni adoptar frontends/workspace. Nuevo nodo productor debe tener owner/prerrequisitos/entregable/aceptación y review real; no mezclarlo con UI/producer condicional incompatible. Plan no afirma implementación ni aceptación del delta.

F) Validación: cambios 1-4 y correcciones matriz PRIMERO, congelar fuentes; re-review todos los inputs/contratos realmente afectados y TODOS los nodos nuevos/agrupadores. Los 25 son estado ACTUAL, NO límite: brief común puede invalidar todos. Procesos baratos fresh sin contexto/tools, stdin DEVNULL, evidencia/disposiciones sinceras; no green por APTO. Regenerar y Tester independiente; terminar build --check/validate --check PASS y status all current 0 stale. No debilitar validador ni dar covered_work como cierre TaskDoc. Capturar fuente nueva de autorización/revisión en run, commits drawer/promoción previos como agente proyecto establece; la captura de esta tarea era trabajo local y debió ir directo a drawer, no inbox: conservar historia, corregir ruta en futuras, no reset.

Siguiente checkpoint: ajuste canónico terminado con evidencia, primitivas nuevas SOLO planificadas, no código implementado, todos los reviews actuales. No activar WS07/WS08-12 ni UI antes de revisión root de ese checkpoint. Es autorización concreta de consolidación, no pedir otra aprobación para los mismos 6 puntos. Si aparece decisión de producto nueva no cubierta, registrar antes de improvisar.

