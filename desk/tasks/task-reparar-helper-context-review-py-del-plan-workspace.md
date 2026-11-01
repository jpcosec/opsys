---
id: task-reparar-helper-context-review-py-del-plan-workspace
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- runs/subagents/20261031-cierre-revision9/review-source.md
- desk/drawer/plans/workspace-documental/context_review.py
- desk/rituals/context-review.md
- desk/drawer/plans/workspace-documental/validate_plan.py
depends_on: []
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-007-phase-gated-task-flow.md
files:
- desk/drawer/plans/workspace-documental/context_review.py
- tests/test_context_review_helper.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-reparar-helper-context-review.md
closeout_evidence:
- tests
- commit
---

# Reparar helper context_review.py del plan workspace

## Rationale

_Explain why this task exists or the business driver behind it._

attempts() lanza KeyError con los recibos manuales de WS12 y WS37, el helper no permite repetir una revisión tras rechazo semántico porque devuelve answered, y la instrucción de ejecución hipotética solo existió en memoria. Autorización: runs/subagents/20261031-cierre-revision9/review-source.md, punto 3.

## Goal

_Describe the concrete result this task must produce._

Dejar desk/drawer/plans/workspace-documental/context_review.py con instrucción durable, intento nuevo tras rechazo semántico, recibo y manifest propios coherentes, y recibos históricos incompletos reconocidos sin crash, con pruebas en tests/test_context_review_helper.py.

## Scope

_State what is in scope and what is out of scope._

Solo desk/drawer/plans/workspace-documental/context_review.py y tests/test_context_review_helper.py, más evidencia en runs/subagents/20261031-helper-context-review/. No se tocan validate_plan.py, build_plan.py, dag.yaml, brief.md ni otros archivos del plan, UI, Scion ni repos hermanos. Las rutas son relativas a la raíz del repo deskops. Las firmas públicas que usa validate_plan.py se conservan: all_nodes, stale_reviews.

Requisitos:

1. Instrucción durable. La constante SYSTEM incorpora que REFORMULACION describe el encargo del nodo y no esta revisión, y que DRY-RUN describe cómo lo ejecutaría un ejecutor futuro, hipotéticamente y sin ejecutar nada: archivos, cambios concretos, consumo de dependencias y gates, errores y validación esperada. Para un agregado o paquete no ejecutable agrega: decirlo y además recorrer cómo lo cumplen sus hijos, qué transfiere cada uno al siguiente y cómo se valida el resultado conjunto; no basta listar prerrequisitos ni verificar aceptaciones. Se agrega INSTRUCTION_VERSION con valor nuevo. El texto de FILE:instruccion dentro de bundle() no cambia, porque cambiaría el hash de input de los 73 nodos.

2. Intento nuevo tras rechazo semántico. `run <ids> --new-attempt --reason <texto>`: exige ids explícitos y razón no vacía; falla sin efecto si faltan o si se combina con --stale. Crea un intento nuevo aunque exista uno answered para el mismo input. Sin ese flag sigue reutilizando answered.

3. Manifest y recibo propios de cada intento: número real de intento, argv efectivo, instruction_version, system_prompt_sha256 del prompt efectivo y, en intento forzado, retry_reason y retry_of. El recibo conserva todos los campos actuales. Cada manifest se genera para su intento, no se copia.

4. Recibos históricos incompletos. attempts() no lanza con un recibo sin technical_failure y conserva su retorno de dos valores. Un recibo incompleto no cuenta como answered ni como fallo técnico. Se expone una función que clasifica un recibo en completo, incompleto o fallo técnico, listando los campos faltantes. Sin answered completo, run crea intento nuevo. stale_reviews agrega un problema `<id>: receipt incomplete` cuando el intento registrado en dag.yaml como evidencia tiene recibo incompleto, y sigue devolviendo una lista: nada se vuelve válido en silencio. No se rellenan recibos históricos, ni PIDs, ni fechas.

Hoy los recibos de WS12 y WS37 están incompletos y son evidencia registrada: tras este cambio status los listará y validate_plan.py --check fallará por eso hasta que sus revisiones se repitan. Es el efecto esperado y declarado; lo resuelve la tarea de cierre siguiente.

Pruebas en tests/test_context_review_helper.py, sin invocar proveedor: stub de Popen o de pi, y RUN y ROOT dirigidos a tmp_path. Casos: recibo incompleto no lanza y no cuenta como answered; answered completo se reutiliza sin flag y no llama al proceso; --new-attempt crea attempt-n+1 con manifest y recibo coherentes con argv, número y razón; --new-attempt sin razón o sin ids falla; stale_reviews reporta receipt incomplete; SYSTEM contiene la cláusula de agregado y el hash de bundle no depende de SYSTEM.

Roles: el Executor edita esos dos archivos y escribe runs/subagents/20261031-helper-context-review/result-summary.md; corre solo pytest de ese archivo; sin commits ni closeout, y no corre `context_review.py run`. El Supervisor valida, hace commits y closeout. Tester independiente de solo lectura.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Leer desk/drawer/plans/workspace-documental/context_review.py completo y validate_plan.py para no romper su uso. 2. Implementar los cuatro requisitos con el menor cambio. 3. Escribir pruebas. 4. Dejar runs/subagents/20261031-helper-context-review/result-summary.md con diff resumido y salida de pytest.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_context_review_helper.py
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status lista exactamente WS12 y WS37 como receipt incomplete
- git diff --name-only 6d41f301..HEAD -- desk/drawer/plans/workspace-documental/validate_plan.py desk/drawer/plans/workspace-documental/build_plan.py queda vacío
- Tester independiente de solo lectura deja runs/subagents/20261031-helper-context-review/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

Los cuatro requisitos cumplidos, pytest de tests/test_context_review_helper.py en verde, build --check en verde, status lista exactamente WS12 y WS37 como receipt incomplete, y un Tester independiente da PASS.
