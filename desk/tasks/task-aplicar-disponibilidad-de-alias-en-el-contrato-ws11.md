---
id: task-aplicar-disponibilidad-de-alias-en-el-contrato-ws11
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/workspace-documental/contratos/navegacion.md
- runs/subagents/20261101-ws11-disponibilidad/review-source.md
depends_on: []
pills:
- desk/contexts/pill-001-task-closure-commit.md
files:
- desk/drawer/plans/workspace-documental/contratos/navegacion.md
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-disponibilidad-alias-ws11.md
closeout_evidence:
- commit
- document
---

# Aplicar disponibilidad de alias en el contrato WS11

## Rationale

_Explain why this task exists or the business driver behind it._

La validación de §3.2 exigía que root y store existan y volvía inalcanzable E-MD3. Root distingue autorización de disponibilidad y preaprobó un reemplazo exacto.

## Goal

_Describe the concrete result this task must produce._

Sustituir la cadena de §3.2 por la frase preaprobada y obtener el sha256 aprobado por root.

## Scope

_State what is in scope and what is out of scope._

Autoridad: runs/subagents/20261101-ws11-disponibilidad/review-source.md.
En desk/drawer/plans/workspace-documental/contratos/navegacion.md, §3.2 Validación, sustituir la única cadena «`root` y `store` existen» por la frase preaprobada. Resultado esperado sha256 6a4f8518f3d69de6118550b3077921db4bbb46bc9123c26980c6c8fc5f62361e. Si difiere, se detiene y se comunica.
Sin otras frases, sin cambiar el estado del archivo, sin otras superficies. Sin revisiones del DAG: el contrato no es fuente del helper.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Aplicar el reemplazo y comprobar el hash. 2. Tester focal de §3.2 y §8.5. 3. Revisión fresca WS13.1 y WS41. 4. Comparar. 5. Checks. 6. Nota de aprobación y closeout.

## Validation

_List the checks required before this task can close._

- sha256sum desk/drawer/plans/workspace-documental/contratos/navegacion.md
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status
- Tester independiente de solo lectura deja runs/subagents/20261101-ws11-disponibilidad/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

Acceptance: sha256 exacto; Tester focal PASS; revisión fresca comparada sin contradicción real; build --check, validate --check y status en verde.
