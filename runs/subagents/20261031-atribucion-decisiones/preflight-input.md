FILE:desk/tasks/task-separar-procedencia-humana-y-técnica-en-el-registro-de-decisiones.md
---
id: task-separar-procedencia-humana-y-técnica-en-el-registro-de-decisiones
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- runs/subagents/20261031-atribucion-decisiones/review-source.md
- runs/subagents/20261031-ws07-decisiones/coverage-report.md
- desk/drawer/plans/workspace-documental/decisiones.md
- runs/subagents/20261031-finalizar-plan-workspace/owner-decisions.json
- desk/rituals/context-review.md
depends_on: []
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-007-phase-gated-task-flow.md
files:
- desk/drawer/plans/workspace-documental/decisiones.md
- runs/subagents/20261031-atribucion-decisiones/attribution-map.md
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-separar-atribucion-en-decisiones-p01-p06.md
closeout_evidence:
- commit
- document
---

# Separar procedencia humana y técnica en el registro de decisiones

## Rationale

_Explain why this task exists or the business driver behind it._

La auditoría WS07 halló filas Humana con precisiones técnicas que el solicitante no dijo, y fuentes incompletas en P07 y P09. Root eligió corregir en fuente canónica. Autorización: runs/subagents/20261031-atribucion-decisiones/review-source.md.

## Goal

_Describe the concrete result this task must produce._

Dejar desk/drawer/plans/workspace-documental/decisiones.md con procedencia humana y técnica explícita y fuentes reales en P01, P03 a P07 y P09, sin cambiar ninguna decisión, y las 73 revisiones renovadas.

## Scope

_State what is in scope and what is out of scope._

Parche único en desk/drawer/plans/workspace-documental/decisiones.md. Hallazgos de partida: runs/subagents/20261031-ws07-decisiones/coverage-report.md. runs/subagents/20261031-atribucion-decisiones/review-source.md es contrato obligatorio.

Se mantienen sin cambio: IDs P01-P09, las preguntas y respuestas literales, source_tool_call, decisiones sustantivas, restricciones, actores, y la columna de nodos y gates. P02 y P08 no se reescriben por vocabulario. WS45 no se agrega. O1 a O5 no se tocan. dag.yaml solo cambia en context_review, no en contratos ni gates.

Parche: en P01, P03, P04, P05 y P06, la afirmación humana conserva solo lo aceptado en pregunta y respuesta, citando ítem. Las precisiones técnicas no se borran: pasan a una derivación técnica de planificación rotulada como tal, con fuente exacta existente: path, sección o líneas, y commit si aplica. preflight-input-v2.md 108-113 y 127-128 de runs/subagents/20261031-finalizar-plan-workspace son encargo técnico, no aprobación humana.

P07 y P09: siguen técnicas, sin firma humana y sin rediseño. Se sustituye la fuente sin ruta por la real. Buscar el registro técnico histórico de rutas/aliases, registry y WS43 tras validación en git log de decisiones.md y en los runs previos del plan. Distinguir registro histórico de regla técnica vigente: una cita al DAG sirve para la regla vigente, no prueba quién la decidió. Si un detalle solo tiene respaldo derivado, se etiqueta así y se declara el límite, sin inventar autor, fecha ni fuente.

Forma: el Executor elige la mínima que mantenga legible el registro; puede ser separar en la celda o agregar una sección de procedencia, sin mover IDs. El mapa de atribución queda en runs/subagents/20261031-atribucion-decisiones/attribution-map.md: por cada fragmento de P01 a P09, tipo, fuente exacta y límite.

No cambiar bundle ni fuentes para evitar invalidar revisiones. decisiones.md entra completo en todos los bundles, así que las 73 entradas se renuevan.

Roles. Executor: edita solo desk/drawer/plans/workspace-documental/decisiones.md, escribe attribution-map.md y result-summary.md en runs/subagents/20261031-atribucion-decisiones; sin commits. Supervisor: revisa y congela el parche, corre `context_review.py run --stale` con el helper sin cambios, compara contrato completo, reformulación y dry-run de cada nodo, registra context_review, valida y cierra. Agente preparatorio: puede redactar borradores de disposición, y debe declararse así. Tester independiente de solo lectura, que distingue lo que verificó de los datos del Supervisor.

Fuera de alcance: helper, validadores, código, UI, Scion, WS08-12, push, preguntar al solicitante, y la suite general.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Executor: fuentes históricas, parche, mapa. 2. Supervisor revisa y congela. 3. Tanda de 73 con v2. 4. Comparación y disposiciones. 5. Registro, chequeos, Tester. 6. Cobertura efectiva WS07, closeout y fase.

## Validation

_List the checks required before this task can close._

- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status
- test -s runs/subagents/20261031-atribucion-decisiones/attribution-map.md
- git diff --name-only 7b045a6f..HEAD -- deskops/ tests/ desk/drawer/plans/workspace-documental/context_review.py desk/drawer/plans/workspace-documental/validate_plan.py desk/drawer/plans/workspace-documental/build_plan.py queda vacío
- Tester independiente de solo lectura deja runs/subagents/20261031-atribucion-decisiones/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

Respuestas 0-2 intactas, mapa con fuentes reales, diff que prueba que no cambiaron decisiones, contratos ni gates; 73 bundles, recibos completos y disposiciones actuales con v2; build --check, validate --check y status en verde; Tester independiente PASS.

