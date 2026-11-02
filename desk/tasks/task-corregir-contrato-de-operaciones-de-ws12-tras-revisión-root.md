---
id: task-corregir-contrato-de-operaciones-de-ws12-tras-revisión-root
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/workspace-documental/contratos/operaciones.md
- desk/drawer/plans/workspace-documental/contratos/navegacion.md
- desk/drawer/plans/workspace-documental/dag.yaml
- desk/drawer/plans/workspace-documental/decisiones.md
- runs/subagents/20261102-ws12-correccion/review-source.md
depends_on: []
pills:
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-001-task-closure-commit.md
files:
- desk/drawer/plans/workspace-documental/contratos/operaciones.md
- desk/drawer/plans/workspace-documental/dag.yaml
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-corregir-contrato-ws12.md
closeout_evidence:
- commit
- document
---

# Corregir contrato de operaciones de WS12 tras revisión root

## Rationale

_Explain why this task exists or the business driver behind it._

La revisión root no aprobó contratos/operaciones.md ni G_WRITE_CONTRACT: ocho afirmaciones no se sostienen y varios huecos necesitan productor explícito.

## Goal

_Describe the concrete result this task must produce._

Aplicar los ocho hallazgos y las decisiones técnicas A a E en contratos/operaciones.md, y proponer en dag.yaml los productores, dependencias, aceptaciones y gates mínimos, congelando antes de cualquier renovación de revisiones.

## Scope

_State what is in scope and what is out of scope._

Autoridad: runs/subagents/20261102-ws12-correccion/review-source.md, que prevalece sobre este resumen. Lista cerrada.

Superficies: desk/drawer/plans/workspace-documental/contratos/operaciones.md; dag.yaml y sus derivados solo para la propuesta canónica mínima; runs/subagents/20261102-ws12-correccion/.

Hallazgos 1 a 8: §5.7 y 409; S01, S02 y §9.4 sobre /save; W01 y §4.2; S05; §4.3.1; W19; HO-11 y HO-11b; HO-10.
Decisiones técnicas de root, no del usuario: A HO-05; B HO-07; C HO-03; D HO-11 y HO-11b; E Origin y HO-04, HO-06, HO-09, HO-18.

Salida obligatoria: matriz hallazgo → cambio → productor → consumidor.

Sin ejecutar productores. Sin UI, implementación de SLDB, Scion ni push. Sin CAS universal. Sin modelo, API ni servicio de identidad nuevos. Lectura estática no es prueba. No tocar helper, validadores, fuentes comunes salvo la propuesta en dag.yaml, ni rutas ajenas. Si el encaje de productores cambia compromisos humanos, se expone antes de resolverlo. Sin preguntar al solicitante.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Contrastar cada hallazgo en fuente. 2. Parchear el contrato. 3. Proponer nodos y dependencias en dag.yaml. 4. Regenerar derivados y medir invalidación. 5. Revisión independiente de bloques afectados. 6. Congelar y entregar a root antes de renovar.

## Validation

_List the checks required before this task can close._

- test -s desk/drawer/plans/workspace-documental/contratos/operaciones.md
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status
- Tester independiente de solo lectura deja runs/subagents/20261102-ws12-correccion/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

Acceptance: ocho hallazgos y decisiones A a E resueltos; matriz entregada; Supervisor leyó §§1-13; revisión independiente con cobertura declarada; invalidación medida sin renovar; root revisó la congelación antes de cualquier renovación; G_WRITE_CONTRACT sigue pendiente.
