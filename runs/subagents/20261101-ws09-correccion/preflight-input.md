FILE:desk/tasks/task-corregir-fichas-de-ws09-tras-revisión-root.md
---
id: task-corregir-fichas-de-ws09-tras-revisión-root
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/workspace-documental/borradores/vistas.md
- deskops/models/ritual.py
- desk/rituals/testing.md
- desk/rituals/execution.md
- desk/drawer/plans/workspace-documental/auditoria/infraestructura.md
- desk/drawer/plans/workspace-documental/auditoria/deskops.md
- desk/drawer/plans/workspace-documental/borradores/user-flows.md
- desk/drawer/plans/workspace-documental/dag.yaml
- runs/subagents/20261101-ws09-correccion/review-source.md
- desk/rituals/context-review.md
depends_on: []
pills: []
files:
- desk/drawer/plans/workspace-documental/borradores/vistas.md
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-corregir-fichas-ws09.md
closeout_evidence:
- commit
- document
---

# Corregir fichas de WS09 tras revisión root

## Rationale

_Explain why this task exists or the business driver behind it._

La revisión root no aprobó WS09: cuatro afirmaciones de vistas.md no se sostienen contra sus fuentes.

## Goal

_Describe the concrete result this task must produce._

Corregir en una pasada F05, F16, F18a, F18b y F12, con las precisiones de F03 y F12 y la nota de candidaturas.

## Scope

_State what is in scope and what is out of scope._

Una sola pasada sobre desk/drawer/plans/workspace-documental/borradores/vistas.md. Autoriza runs/subagents/20261101-ws09-correccion/review-source.md. Lista cerrada. Cada cambio se coteja con su fuente directa, no por rango.

1. F05, campo Error: quitar «con 0 StepDoc el procedimiento carece de pasos que mostrar». Escribir que la inexistencia de instancias StepDoc no implica ausencia de pasos: RitualDoc.steps son pasos de prosa inline, no referencias a documentos (deskops/models/ritual.py:65-67; desk/rituals/testing.md y execution.md, campo steps). F05 Origen y Campos deben nombrar esos pasos de prosa. Sin inventar progreso, referencias a StepDoc ni autoavance.
2. F16, campo Error: mismo patrón. 0 StepDoc solo niega esas instancias, no los pasos de RitualDoc.
3. F18a, campo Clase: spec YAML fuente = authored; SpecDoc y SpecNodeDoc materializados por diagram sync = derivado regenerable, no fuente a editar. NotationDoc se clasifica por su origen real según infraestructura.md, sin cambiarlo por reflejo.
4. F18b, campo Destino de escritura: ruta sldb/views/ prevista, pendiente de confirmación y registro en WS18 al promover (dag.yaml:1222-1224). No decir confirmada. No inferir repo hermano por prefijo ni afirmar que save_view de graph_ui escribe en spec2viz. Conservar repo owner y recibo.
5. F12, campos Acción/dueño y Destino de escritura: la vista lee resultados; ejecutar un comando de diagnóstico se clasifica por sus efectos, no es lectura segura ni GET por ser diagnóstico. Efecto conocido: atoms validate llama ensure_workspace y puede crear andamiaje y tag-namespaces.yaml (deskops.md:113,266; user-flows.md:179). Conservar la advertencia de stores check como no corroborada. WS12 debe considerarlos. No asumir que la UI invoca el comando, no crear endpoint, no quitar operaciones del catálogo.

Precisiones en la misma pasada:
6. F03: «ningún comando la calcula» se acota a lo auditado o no encontrado.
7. F12: Corpus.rank y GET /corpus/rank existen, sin CLI, con 409 si falta índice y fallback difflib, embedder no comprobado (infraestructura.md:115). WS14 admite capacidad parcial o degradada; no se promete semántica.
8. F12: consulta documental guardada con where ausente no es ausencia total de selección persistida: ProjectionDoc es capacidad vecina distinta (infraestructura.md:121).

9. Nota nueva al final, «Candidaturas sin productor»: consulta guardada, búsqueda por significado, edición de RoleDoc y RuntimeProfileDoc (excluida por UF09), navegación de FAQ, lista de issues en UI, renderer de roles, vista Specs embebida. No son prerrequisito del lector ni capacidades comprometidas. La lectura básica de FAQ, issues y roles reutiliza el lector Markdown o modelado. Se conservan para que WS11 las clasifique. Si se adoptan, exigen alcance y productor real. Sin nodos nuevos.

10. Corregir los campos Evidencia de las fichas tocadas, y Clase o Renderer solo si el cambio lo exige. Los estados no cambian: 23 bloqueado.

No editar user-flows, cobertura, manual, decisiones, guía, dag.yaml, helper, validadores, código ni repos hermanos. El Executor escribe solo desk/drawer/plans/workspace-documental/borradores/vistas.md y runs/subagents/20261101-ws09-correccion/result-summary.md, sin commits ni revisiones. Sin preguntar al solicitante.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Cotejar cada fuente citada. 2. Aplicar la lista cerrada. 3. Escribir runs/subagents/20261101-ws09-correccion/result-summary.md con cambio, fuente abierta y resultado por ítem.

## Validation

_List the checks required before this task can close._

- grep -c "^### F" desk/drawer/plans/workspace-documental/borradores/vistas.md
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status
- Tester independiente de solo lectura deja runs/subagents/20261101-ws09-correccion/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

Acceptance: los diez ítems aplicados y ninguno más; Tester focal PASS sobre los bytes congelados antes del closeout; revisión afectada renovada; build --check, validate --check y status en verde.
