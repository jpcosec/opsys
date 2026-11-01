---
id: task-ws07-mantener-registro-trazado-de-decisiones-acordadas
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/workspace-documental/decisiones.md
- runs/subagents/20261031-finalizar-plan-workspace/owner-decisions.json
- desk/drawer/plans/workspace-documental/dag.yaml
- runs/subagents/20261031-cierre-revision9/phase-closeout.md
- desk/rituals/context-review.md
depends_on: []
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-007-phase-gated-task-flow.md
- desk/contexts/pill-ready-phases-prove-dependencies-and-non-overlap.md
files:
- runs/subagents/20261031-ws07-decisiones/coverage-report.md
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/workspace-documental/task-ws07.md
closeout_evidence:
- commit
- document
---

# WS07: Mantener registro trazado de decisiones acordadas

## Rationale

_Explain why this task exists or the business driver behind it._

La revisión root aprobó el cierre de la revisión 9 y autorizó solo WS07, verificando primero si ya está cubierto. Autorización acotada: runs/subagents/20261031-cierre-revision9/phase-closeout.md; execution_authorized global sigue false.

## Goal

_Describe the concrete result this task must produce._

Determinar con evidencia si el registro P01-P09 de desk/drawer/plans/workspace-documental/decisiones.md cumple la aceptación de WS07, y dejar el resultado en runs/subagents/20261031-ws07-decisiones/coverage-report.md. Si está cubierto, no se reescribe nada.

## Scope

_State what is in scope and what is out of scope._

Reutilizar decisiones.md y owner-decisions.json: respuestas humanas literales 0–2, mapeo P01–P09, actor/fecha/fuente. P07/P09 son defaults técnicos delegados, no firmas humanas. source_mode=editable condicionado a G_SOURCE. Responsabilidad producto/recepción graph_ui/sldb/spec2viz es del solicitante; operador y permisos Scion se designan al abordar E sin bloquear L/M. baseline_proposal es el string raíz de dag.yaml suministrado: conservar base acordada y actualizar solo ante nueva decisión explícita con fuente verificable. Cobertura documental se refiere a decisiones.md + owner-decisions.json y covered_work de este nodo, no sustituye cobertura de UFs ni auditorías WS06.

Primero verificar. Comprobar en runs/subagents/20261031-ws07-decisiones/coverage-report.md, por cada Pxx: resultado concreto, tipo humano o técnico, actor, fuente, nodos y gates. Citar para cada fila humana el ítem y texto literal de runs/subagents/20261031-finalizar-plan-workspace/owner-decisions.json, y comprobar que decisiones.md reproduce las respuestas 0 a 2 exactas. P07 y P09 se verifican como defaults técnicos delegados, sin atribuirles firma humana. Comprobar que cada nodo y gate citado existe en dag.yaml. Comprobar que baseline_proposal y parameters.source_mode coinciden con las respuestas. Comprobar el estado de G_PRODUCT y G_WRITE_POLICY sin inferir aceptación de API o UI ni permiso Scion.

Regla de edición. decisiones.md es input de revisión de todos los nodos; editarlo invalida esos bundles. Se edita solo si hay un defecto real frente a la aceptación: dato falso, fila sin actor o fuente, cita inexistente, o cambio real de decisión. Un nodo o gate derivado después, como WS45 y G_PAYLOAD_PRECONDITION, que no cambia decisión ninguna, se registra como observación en el informe y no motiva edición, salvo que la evidencia muestre que el registro queda falso. Si aparece un defecto real, no se corrige aquí: se describe con evidencia en el informe y el Supervisor decide.

Roles: el Executor solo lee y escribe runs/subagents/20261031-ws07-decisiones/coverage-report.md y runs/subagents/20261031-ws07-decisiones/result-summary.md. El Supervisor corre validaciones, commits y closeout. Tester independiente de solo lectura. Sin preguntar nada al solicitante. Fuera de alcance: WS08-12, código, Scion, UI, push, dag.yaml, y la suite general, que no es requisito de esta tarea.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Leer decisiones.md, runs/subagents/20261031-finalizar-plan-workspace/owner-decisions.json, dag.yaml. 2. Escribir tabla P01-P09 en runs/subagents/20261031-ws07-decisiones/coverage-report.md. 3. Comprobaciones de baseline, source_mode y gates. 4. Dictamen: cubierto, o defecto real con evidencia. 5. runs/subagents/20261031-ws07-decisiones/result-summary.md.

## Validation

_List the checks required before this task can close._

- test -s runs/subagents/20261031-ws07-decisiones/coverage-report.md
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status
- Tester independiente de solo lectura deja runs/subagents/20261031-ws07-decisiones/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

Acceptance: Registro concreto de cada Pxx con tipo humano/técnico, actor, fuente y nodos/gates. No repetir preguntas ya resueltas ni inferir aceptación de API/UI o permiso Scion. Verificar y reutilizar cobertura documental ya producida; actualizar solo por cambio real de decisión. El informe dictamina cubierto o describe el defecto real, build --check, validate --check y status siguen en verde, y un Tester independiente da PASS.
