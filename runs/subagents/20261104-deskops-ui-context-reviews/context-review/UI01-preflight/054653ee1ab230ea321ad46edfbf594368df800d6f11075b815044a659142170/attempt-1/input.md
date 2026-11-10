FILE:desk/tasks/task-ui01-vista-de-datos-de-deskops-para-la-ui-deskops-view-y-su-contrato.md
---
id: task-ui01-vista-de-datos-de-deskops-para-la-ui-deskops-view-y-su-contrato
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- deskops/services/desk_view.py
- deskops/cli/registry.py
- deskops/cli/commands/view.py
- tests/test_desk_view.py
- docs/deskops-ui.md
task_type: code
inherits_from: []
inherit_acceptance_context: false
atoms: []
closeout_evidence:
- tests
- commit
- atom
- materialization
---

# UI01: vista de datos de deskops para la UI (deskops view) y su contrato

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo UI01 del plan desk/drawer/plans/deskops-ui (DU1-DU6): el producto es la UI de deskops; la lógica de qué se muestra vive en deskops y graph_ui solo la sirve.

## Goal

_Describe the concrete result this task must produce._

Clase de servicio de solo lectura en deskops (deskops/services/desk_view.py) que compone, desde las operaciones existentes listadas en alcance.md, cinco vistas JSON: board (columnas por nodo del ciclo de vida en el orden del spec, cada tarjeta con id, título, status, current_node, gates con condición y si se cumple, conteo cumplidos/total, evidencia declarada y encontrada de verify_task_closeout, pills y atoms resueltos a título); task (lo del board más goal, scope, implementation_path, validation, done_when, why, references, files, depends_on, inherits_from, pills con what/when/how_not, atoms con answer, next_actions y advance_when de next_action_report, y revision = sha256 de Board + archivo de tarea como la guarda de graph_ui); drawer (tareas de desk/drawer/tasks con id, título, status, primeras líneas del cuerpo y ruta, más el comando add task --from-drawer listo para copiar); inbox (notas con id, kind, título, emisor, destino, fecha del nombre de archivo, estado de ack, cuerpo); agents (runtime workers y las últimas N corridas de runs/subagents/index.jsonl). Toda referencia que no resuelve aparece en una lista errors de la vista con su causa, nunca como dato. Subcomando deskops view {board,task <id>,drawer,inbox,agents} --root --format json|text registrado en cli/registry.py. Documento docs/deskops-ui.md con el contrato JSON de cada vista y la tabla de mapeo de alcance.md. Solo lectura: nada escribe.

## Scope

_State what is in scope and what is out of scope._

Solo lectura. Archivos: deskops/services/desk_view.py, deskops/cli/registry.py, deskops/cli/commands/view.py, tests/test_desk_view.py, tests/fixtures/golden/help/, docs/deskops-ui.md. Fuentes de datos y mapeo en desk/drawer/plans/deskops-ui/alcance.md (tabla "Mapeo de la pantalla de Stitch a fuentes reales"). Un elemento sin fuente real no entra a la vista (DU5): va a la lista errors con su causa.

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer alcance.md y brief.md del plan; componer sobre DeskopsOperations (show_task, _lifecycle_gates, next_action_report, verify_task_closeout, drawer, list de inbox) sin duplicar lógica; registrar el subcomando en cli/registry.py como los demás; tests con desks temporales reales (deskops init + add task). Ante un contrato ausente, hipótesis en este TaskDoc.

## Validation

_List the checks required before this task can close._

- pytest -q tests/test_desk_view.py
- pytest -q tests/test_output_goldens.py
- suite completa verde en robocop2

## Done When

_Name the observable condition that makes the task complete._

Tests sobre desks temporales reales (deskops init + add task): board agrupa por current_node y cuenta gates igual que show_task; task trae los campos listados y la misma revision que la guarda de graph_ui; una pill o atom inexistente aparece en errors y no en la lista; drawer, inbox y agents devuelven lo que hay en disco; ninguna vista escribe (hash del árbol igual antes y después); deskops view --help y golden de help; docs/deskops-ui.md existe con los cinco contratos; suite completa verde en robocop2.

FILE:instruccion
Preflight solo-TaskDoc del nodo UI01: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita y da el DRY-RUN. No ejecutes nada.

