---
id: task-corregir-revisión-9-del-plan-workspace-tras-revisión-root
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- runs/subagents/20261031-correccion-revision9/review-source.md
- runs/subagents/20261031-ajuste-canonico-ws06/handoff.md
- desk/drawer/plans/workspace-documental/dag.yaml
- desk/rituals/context-review.md
depends_on: []
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-007-phase-gated-task-flow.md
- desk/contexts/pill-ready-phases-prove-dependencies-and-non-overlap.md
files:
- desk/drawer/plans/workspace-documental/dag.yaml
- runs/subagents/20261031-correccion-revision9/comparison-ledger.md
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-corregir-revision-9-del-plan-tras-revision-root.md
closeout_evidence:
- commit
- document
---

# Corregir revisión 9 del plan workspace tras revisión root

## Rationale

_Explain why this task exists or the business driver behind it._

La revisión root aceptó cuatro decisiones pero no aprobó la revisión 9: un contrato incondicional, una interfaz sin productor, un dry-run faltante y una atribución de revisión que no ocurrió. Fuente: runs/subagents/20261031-correccion-revision9/review-source.md.

## Goal

_Describe the concrete result this task must produce._

Corregir esos cuatro puntos con evidencia sincera y dejar el plan con build --check, validate --check y status en verde, sin implementar nada.

## Scope

_State what is in scope and what is out of scope._

Planificación en deskops. Archivos: desk/drawer/plans/workspace-documental/dag.yaml y sus proyecciones generadas, evidencia en runs/subagents/20261031-correccion-revision9/ y disposiciones nuevas o atestaciones en runs/subagents/20261031-workspace-context-reviews/context-review/. runs/subagents/20261031-correccion-revision9/review-source.md es contrato obligatorio.

Punto 1. En la aceptación de WS12, la cláusula que mantiene a WS21 bloqueado pasa a decir G_PAYLOAD_PRECONDITION y, solo en variante editable, G_SOURCE. No cambia P04, ni añade gate ni actor.

Punto 2. WS12 asume en su aceptación producir, para el ramal E, la política y el umbral de timeout de dispatch y reply y su clasificación observable, como sección de contrato por delta. Sin elegir duración ahora, sin bloquear el cierre del contrato núcleo y sin permisos ni red nuevos. WS34.1 y WS34.2 declaran que solo avanzan con esa política aplicable y probada en el contrato de su delta. No se modifican los gates.

Punto 3. WS19.1 recibe un proceso barato nuevo que reformule y describa cambios futuros concretos de campos, consumo de precondición, bloqueo de campos protegidos, buffer y conflicto, y validación, sin ejecutar. El intento anterior se conserva sin crédito. No se inyecta su salida ni se rescata con experto. Si solo cambia la instrucción, se registran bytes y argv y no se usa el runner cuando devolvería answered.

Punto 4. Las disposiciones existentes se conservan: dicen revisado por el coordinador sin que esa revisión ocurriera nodo por nodo. Se escribe runs/subagents/20261031-correccion-revision9/comparison-ledger.md con supersesión fechada y, por cada nodo final: rol y actor real, sha de input, output y disposición, alcance de la comparación, resultado y fecha. El coordinador compara de verdad output y disposición finales de todos los nodos y asume la aceptación; el ledger dice exactamente qué leyó. Los defectos hallados se corrigen, no se waivan.

Además: result-summary.md de la consolidación afirma que WS42 no guarda payload por campos, y eso es falso; se corrige con nota fechada. WS42 sale de la justificación por tener guardas y contrato propios y WS19 transitivo, sin forzar un gate universal. promotion-notes.md se actualiza: no da por futuro lo que no tiene productor.

Roles: el Supervisor edita contratos, que la revisión root aceptó; corre revisiones, compara, firma el ledger, valida y cierra. Un agente puede preparar borradores, y el ledger lo dice. Un Tester independiente de solo lectura verifica los cuatro puntos y el cambio protector de G_SOURCE.

Fuera de alcance: código, validadores salvo fallo real con tarea específica, decisiones P01-P09, auditorías, reconciliacion.md salvo que un punto lo exija, WS07, WS08-12, UI, Scion, push.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Editar WS12, WS34.1 y WS34.2. 2. Regenerar y congelar. 3. Correr revisiones de los afectados según hashes. 4. Revisión nueva de WS19.1. 5. Comparar todos los nodos finales y corregir lo que aparezca. 6. Registrar context_review y ledger. 7. Tester. 8. Closeout y handoff.

## Validation

_List the checks required before this task can close._

- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status
- test -s runs/subagents/20261031-correccion-revision9/comparison-ledger.md
- git diff --name-only 5f05281c..HEAD -- deskops/ tests/ docs/ desk/drawer/plans/workspace-documental/decisiones.md desk/drawer/plans/workspace-documental/auditoria/ desk/drawer/plans/workspace-documental/validate_plan.py desk/drawer/plans/workspace-documental/build_plan.py desk/drawer/plans/workspace-documental/context_review.py queda vacío
- Tester independiente de solo lectura deja runs/subagents/20261031-correccion-revision9/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

WS12 condiciona G_SOURCE a la variante editable; WS12 produce la política de timeout y WS34.1 y WS34.2 dependen de ella sin bloquear el núcleo; WS19.1 tiene dry-run real; cada nodo final tiene comparación verdadera en el ledger; build --check, validate --check y status en verde; y un Tester independiente da PASS.
