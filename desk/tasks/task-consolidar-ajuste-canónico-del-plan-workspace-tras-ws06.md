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
