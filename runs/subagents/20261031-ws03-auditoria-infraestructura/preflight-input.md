FILE:desk/tasks/task-ws03-inventariar-persistencia-consultas-y-notaciones.md
---
id: task-ws03-inventariar-persistencia-consultas-y-notaciones
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/workspace-documental/cierre.md
- desk/drawer/plans/workspace-documental/dag.yaml
- desk/drawer/plans/workspace-documental/brief.md
- runs/subagents/20261031-ws02-04-checkpoint/activation.md
- desk/rituals/context-review.md
depends_on: []
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-007-phase-gated-task-flow.md
- desk/contexts/pill-ready-phases-prove-dependencies-and-non-overlap.md
files:
- desk/drawer/plans/workspace-documental/auditoria/infraestructura.md
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/workspace-documental/task-ws03.md
closeout_evidence:
- commit
- document
---

# WS03: Inventariar persistencia, consultas y notaciones

## Rationale

_Explain why this task exists or the business driver behind it._

Primera capa real del núcleo del plan workspace (cierre.md). Activada por runs/subagents/20261031-ws02-04-checkpoint/activation.md; las auditorías alimentan WS06 y WS08-12 con datos comprobados.

## Goal

_Describe the concrete result this task must produce._

Producir desk/drawer/plans/workspace-documental/auditoria/infraestructura.md como auditoría de solo lectura del estado actual, verificable fila por fila.

## Scope

_State what is in scope and what is out of scope._

Auditoría de solo lectura de sldb/pron/spec2viz: fuente/payload, conflictos y límites de locks (control de concurrencia real de sldb/pron: CAS por revisión/hash, locks de archivo o DB; a auditar), referencias documentales, búsquedas (índices o consultas expuestas) y alcance real ViewDoc. Kimun solo referencia. Solo lectura fuera del entregable. Rutas de lectura: ../sldb, ../pron, ../spec2viz. Kimun no se usa como fuente de decisión. Se escribe únicamente desk/drawer/plans/workspace-documental/auditoria/infraestructura.md y evidencia en runs/subagents/20261031-ws03-auditoria-infraestructura/. No se modifica código, otro repo, dag.yaml, reconciliacion.md, Board ajeno ni tareas de otros. Fuera de alcance: WS05 Scion, contratos nuevos, implementación.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Leer fuentes actuales. 2. Escribir desk/drawer/plans/workspace-documental/auditoria/infraestructura.md: encabezado con fecha, commit HEAD de cada repo leído y universo auditado; luego las filas. 3. Registrar comandos usados en runs/subagents/20261031-ws03-auditoria-infraestructura/commands.log. 4. Dejar runs/subagents/20261031-ws03-auditoria-infraestructura/result-summary.md (qué se hizo, huecos, qué revisar). Lo no comprobado se marca «no comprobado» con causa: no se infiere. El Executor no hace commits, no escribe en desk/ salvo desk/drawer/plans/workspace-documental/auditoria/infraestructura.md, y no corre closeout.

## Validation

_List the checks required before this task can close._

- test -s desk/drawer/plans/workspace-documental/auditoria/infraestructura.md
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status
- Tester independiente muestrea filas contra la fuente citada y deja runs/subagents/20261031-ws03-auditoria-infraestructura/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

Acceptance: Una salida documental, sin cambios interrepo; distinguir API comprobada (lectura citada del estado actual), ausencia y hueco.

