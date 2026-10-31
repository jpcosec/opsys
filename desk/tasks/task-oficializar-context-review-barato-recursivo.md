---
id: task-oficializar-context-review-barato-recursivo
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/atoms/workflow-model/atom-tasks-enable-zero-context-subagents.md
- desk/atoms/workflow-model/atom-clean-subagent-ambiguity-review.md
depends_on: []
pills:
- pill-001
- pill-005
- pill-007
files:
- desk/atoms/workflow-model/atom-cheap-zero-context-reviews-test-the-brief-recursively.md
- desk/rituals/context-review.md
- desk/rituals/execution.md
- desk/rituals/phase.md
- docs/workflow-policy-reference.md
- .pi/skills/deskops-task-lifecycle/SKILL.md
- desk/drawer/plans/workspace-documental
- desk/drawer/tasks/workspace-documental
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-oficializar-context-review-barato-recursivo.md
closeout_evidence:
- commit
- document
---

# Oficializar context review barato recursivo

## Rationale

_Explain why this task exists or the business driver behind it._

Decisión explícita del dueño: zero-context review prueba calidad del encargo; no es un concilio experto.

## Goal

_Describe the concrete result this task must produce._

Hacer oficial el review barato, aislado, no ejecutor y recursivo del DAG; reconocer revisiones pendientes del plan workspace.

## Scope

_State what is in scope and what is out of scope._

Solo átomo, ritual nuevo/context-review, ejecución y fase, docs/workflow-policy-reference.md, skill Pi lifecycle y anotaciones/generación del paquete workspace-documental. No tocar dirty closeout, código de producto, skill global ni .opencode.

## Implementation Path

_Outline the expected implementation route or affected surface._

Capturar átomo por CLI y actualizar documentos modelados por SLDB. Añadir ritual de context review antes de planificación/promoción/ejecución sin crear nuevo estado lifecycle. Revisor barato desde proceso efímero Pi deepseek-flash con no-session/no-context-files/no-skills/no-extensions/no-tools; paquete explícito sin historial. Salida: reformulación, ambigüedades y dry-run detallado SIN ejecutar. Usar fallos para corregir encargo/descomponer jerarquía; revisar raíz/paquetes/hojas y aristas; evidencias por nodo/revisión y fresh retry. Conservar preflight TaskDoc-only y cobertura de bundle con roles distintos y baratos. Revisión experta, ejecución y tester son gates diferentes. Actualizar skill Pi mediante skill-creator; opencode no tiene copia lifecycle aplicable. Marcar concilio del plan como experto y cold baratos pendientes, no correr ni aprobar 44 nodos en esta tarea. La fase sigue abierta por otra tarea; cerrar solo esta entrega documental.

## Validation

_List the checks required before this task can close._

- Validar lectura/model roundtrip de rituales/átomo modificados
- Comprobar links y consistencia documentación/skill
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check

## Done When

_Name the observable condition that makes the task complete._

Regla durable y superficies oficiales coherentes; comprensión barata guarda evidencia no ejecutora; plan no atribuye contexto cero al concilio experto; gate docs pasa y commit oficial propio.
