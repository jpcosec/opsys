---
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-ui01-vista-de-datos-de-deskops-para-la-ui-deskops-view-y-su-contrato.md
- desk/tasks/task-gc01-tipos-de-tarea-como-modelos-con-jerarquía-y-evidencia-de-cierre-declarada-en-el-tipo.md
# List of pill-xxx paths
pills:
- pill-001-task-closure-commit
- pill-005-subagent-execution
- pill-007-phase-gated-task-flow
- pill-durable-pill-knowledge-graduates-to-atoms-at-closeout
- pill-phase-closeout-reconciles-pills-and-surfaces-next-work
- pill-ready-phases-prove-dependencies-and-non-overlap
- pill-board-routed-pills-stay-minimal-and-reusable
# List of ritual-xxx paths
rituals:
- ritual-phase
- ritual-execution
- ritual-closeout
- ritual-testing
- desk/rituals/context-review.md
# e.g., system:sldb, workspace:desk
tags:
- system:sldb
- workspace:desk
- topic:routing
---

# Desk Board

## Purpose

_Explain what this board routes and why it exists._

Route the active execution set for deskops.

## Notes

_Add short operational notes about the current routed set._

No active tasks routed.

## Task Details

_Generated from the task references above._

- UI01: vista de datos de deskops para la UI (deskops view) y su contrato [draft] - Clase de servicio de solo lectura en deskops (deskops/services/desk_view.py) que compone, desde las operaciones existentes listadas en alcance.md, cinco vistas JSON: board (columnas por nodo del ciclo de vida en el orden del spec, cada tarjeta con id, título, status, current_node, gates con condición y si se cumple, conteo cumplidos/total, evidencia declarada y encontrada de verify_task_closeout, pills y atoms resueltos a título); task (lo del board más goal, scope, implementation_path, validation, done_when, why, references, files, depends_on, inherits_from, pills con what/when/how_not, atoms con answer, next_actions y advance_when de next_action_report, y revision = sha256 de Board + archivo de tarea como la guarda de graph_ui); drawer (tareas de desk/drawer/tasks con id, título, status, primeras líneas del cuerpo y ruta, más el comando add task --from-drawer listo para copiar); inbox (notas con id, kind, título, emisor, destino, fecha del nombre de archivo, estado de ack, cuerpo); agents (runtime workers y las últimas N corridas de runs/subagents/index.jsonl). Toda referencia que no resuelve aparece en una lista errors de la vista con su causa, nunca como dato. Subcomando deskops view {board,task <id>,drawer,inbox,agents} --root --format json|text registrado en cli/registry.py. Documento docs/deskops-ui.md con el contrato JSON de cada vista y la tabla de mapeo de alcance.md. Solo lectura: nada escribe.
- GC01: Tipos de tarea como modelos con jerarquía y evidencia de cierre declarada en el tipo [draft] - Módulo deskops/models/task_types.py con las subclases de TaskDoc de la tabla de brief.md §Tipos: TaskCodeDoc (task.code), TaskDocsDoc (task.docs), TaskDebugDoc (task.debug, hereda de TaskDoc: exige reproduction en lugar de bundle y por eso no puede ser subtipo de task.code, donde los gates solo se suman), TaskRefactorDoc (task.refactor, hereda de TaskCodeDoc y suma goldens), TaskDecisionDoc (task.decision), TaskAggregateDoc (task.aggregate; sus campos parent_id/children los agrega GC09), TaskExternalDoc (task.external). Cada subclase fija task_type a su nombre (Literal con default) y declara dos atributos de clase: __closeout_evidence__ (tupla del vocabulario de closeout_gates.py:23, más children para el agregado y goldens para refactor, que este nodo solo declara: su verificación es de GC09 y de un nodo posterior) y __activation_receipts__ (tupla de kinds de ReviewDoc que la regla de GC05 exigirá: preflight, bundle, reproduction, goldens, owner). TaskDoc base conserva el campo task_type: str para leer documentos viejos y declara __contract__ = [title, goal, scope, implementation_path, files, validation, done_when] (sintaxis de sldb GO02 (e); si la versión de sldb instalada no la lee, el atributo es inerte hasta que la lea). Registro: las subclases entran en MODEL_REFS (bootstrap.py:26) y se heredan en cada desk como los demás modelos (bootstrap.py:118-160); un desk agrega tipos propios en desk/models/*.py (DC7) y deskops desk update --apply los registra con sldb add_model y pythonpath = raíz del desk; hipótesis a verificar en el TaskDoc: sldb registra una subclase cuya base es un modelo heredado (federado) y base_models la resuelve. add task --task-type <nombre> rechaza un nombre que no sea un tipo registrado (familia model <= TaskDoc) con el mensaje que lista los tipos; sin --task-type, el default es task.code y se avisa en el envelope. closeout_evidence deja de escribirse en la tarea nueva: se lee del tipo (TASK_TYPE_EVIDENCE y evidence_for_task_type se borran); --evidence solo puede agregar kinds a los del tipo (piso; pendiente del dueño en decisiones.md) y un kind que quite falla. Las tareas existentes conservan su campo closeout_evidence, que el cierre sigue leyendo como override por encima del tipo. El documento de una tarea se guarda bajo el modelo de su tipo (TaskCodeDoc:task-x), de modo que model <= TaskCodeDoc lo encuentra; migración: deskops desk update --apply re-trackea cada tarea de desk/tasks bajo el modelo que su task_type legado indica (code|implementation|test → task.code; docs|spec|design → task.docs; external → task.external; vacío → task.code) y reescribe task_type; la migración es idempotente y reporta cada tarea movida. Produce G_TYPES.
