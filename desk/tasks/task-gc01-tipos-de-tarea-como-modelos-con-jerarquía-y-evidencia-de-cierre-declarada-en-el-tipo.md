---
id: task-gc01-tipos-de-tarea-como-modelos-con-jerarquía-y-evidencia-de-cierre-declarada-en-el-tipo
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- pytest tests/test_task_types.py
- tests/test_task_types.py::test_add_task_with_task_type_tracks_under_the_type_model
- tests/test_task_types.py::test_closeout_verify_reads_evidence_from_the_type
- tests/test_task_types.py::test_legacy_task_type_migrates_idempotently
- pytest tests/test_model_contract_snapshot.py
- 9df4c82a
- desk/drawer/tasks/task-closeout-una-materialization-con-target-identity-de-paquete-no-cubre-los-archivos-del-paquete.md
depends_on: []
pills: []
files:
- deskops/models/task.py
- deskops/models/task_types.py
- deskops/models/__init__.py
- deskops/bootstrap.py
- deskops/services/closeout_gates.py
- deskops/services/tasks.py
- deskops/operations.py
- deskops/cli/registry.py
- deskops/cli/commands/operations.py
- deskops/cli/commands/desk.py
- deskops/workspace.py
- deskops/about.py
- deskops/data/faq.md
- .sldb/core/models/
- tests/
- tests/fixtures/model_contract_hashes.json
- tests/fixtures/golden/help/
- tests/e2e_agent/scenarios/
- docs/workflow-policy-reference.md
- docs/operator-manual.md
- docs/quickstart.md
- docs/faq.md
- README.md
- .opencode/skills/use-deskops/SKILL.md
- .pi/skills/deskops-task-lifecycle/SKILL.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
closeout_evidence:
- tests
- commit
- atom
- materialization
---

# GC01: Tipos de tarea como modelos con jerarquía y evidencia de cierre declarada en el tipo

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo GC01 del plan desk/drawer/plans/gates-por-tipo (dag.yaml rev 1, paquete PC01): lado consumidor del plan grafo-operable de sldb; los gates del ciclo de vida pasan a ser documentos que sldb evalúa (D2, DC1-DC7).

## Goal

_Describe the concrete result this task must produce._

Módulo deskops/models/task_types.py con las subclases de TaskDoc de la tabla de brief.md §Tipos: TaskCodeDoc (task.code), TaskDocsDoc (task.docs), TaskDebugDoc (task.debug, hereda de TaskDoc: exige reproduction en lugar de bundle y por eso no puede ser subtipo de task.code, donde los gates solo se suman), TaskRefactorDoc (task.refactor, hereda de TaskCodeDoc y suma goldens), TaskDecisionDoc (task.decision), TaskAggregateDoc (task.aggregate; sus campos parent_id/children los agrega GC09), TaskExternalDoc (task.external). Cada subclase fija task_type a su nombre (Literal con default) y declara dos atributos de clase: __closeout_evidence__ (tupla del vocabulario de closeout_gates.py:23, más children para el agregado y goldens para refactor, que este nodo solo declara: su verificación es de GC09 y de un nodo posterior) y __activation_receipts__ (tupla de kinds de ReviewDoc que la regla de GC05 exigirá: preflight, bundle, reproduction, goldens, owner). TaskDoc base conserva el campo task_type: str para leer documentos viejos y declara __contract__ = [title, goal, scope, implementation_path, files, validation, done_when] (sintaxis de sldb GO02 (e); si la versión de sldb instalada no la lee, el atributo es inerte hasta que la lea). Registro: las subclases entran en MODEL_REFS (bootstrap.py:26) y se heredan en cada desk como los demás modelos (bootstrap.py:118-160); un desk agrega tipos propios en desk/models/*.py (DC7) y deskops desk update --apply los registra con sldb add_model y pythonpath = raíz del desk; hipótesis a verificar en el TaskDoc: sldb registra una subclase cuya base es un modelo heredado (federado) y base_models la resuelve. add task --task-type <nombre> rechaza un nombre que no sea un tipo registrado (familia model <= TaskDoc) con el mensaje que lista los tipos; sin --task-type, el default es task.code y se avisa en el envelope. closeout_evidence deja de escribirse en la tarea nueva: se lee del tipo (TASK_TYPE_EVIDENCE y evidence_for_task_type se borran); --evidence solo puede agregar kinds a los del tipo (piso; pendiente del dueño en decisiones.md) y un kind que quite falla. Las tareas existentes conservan su campo closeout_evidence, que el cierre sigue leyendo como override por encima del tipo. El documento de una tarea se guarda bajo el modelo de su tipo (TaskCodeDoc:task-x), de modo que model <= TaskCodeDoc lo encuentra; migración: deskops desk update --apply re-trackea cada tarea de desk/tasks bajo el modelo que su task_type legado indica (code|implementation|test → task.code; docs|spec|design → task.docs; external → task.external; vacío → task.code) y reescribe task_type; la migración es idempotente y reporta cada tarea movida. Produce G_TYPES.

## Scope

_State what is in scope and what is out of scope._

Repo deskops. Archivos: deskops/models/task.py, deskops/models/task_types.py, deskops/models/__init__.py, deskops/bootstrap.py, deskops/services/closeout_gates.py, deskops/services/tasks.py, deskops/operations.py (creación y verify_task_closeout), deskops/cli/registry.py (add task, desk update), deskops/workspace.py (desk/models), tests/, tests/fixtures/model_contract_hashes.json, docs/workflow-policy-reference.md, CHANGELOG.md. Depende de: nada; requiere gates: ninguno. Fuera de alcance: brief.md §Fuera de alcance, los demás nodos GC del plan y todo cambio en sldb. Precisiones del preflight (2026-11-05, runs/subagents/deskops-gates-por-tipo-context-reviews/context-review/GC01-preflight/00126a29.../attempt-1): (1) Tabla normativa (brief.md §Tipos), tipo = clase (base): __activation_receipts__ | __closeout_evidence__. task.code = TaskCodeDoc (TaskDoc): (preflight, bundle) | (tests, commit, atom, materialization); task.docs = TaskDocsDoc (TaskDoc): (preflight) | (commit, document); task.debug = TaskDebugDoc (TaskDoc): (preflight, reproduction) | (tests, commit, atom, materialization); task.refactor = TaskRefactorDoc (TaskCodeDoc): (preflight, bundle, goldens) | (tests, commit, atom, materialization, goldens); task.decision = TaskDecisionDoc (TaskDoc): (owner) | (commit, document); task.aggregate = TaskAggregateDoc (TaskDoc): () | (children, commit); task.external = TaskExternalDoc (TaskDoc): (preflight) | (external). atom y materialization siguen siendo un solo gate con dos alternativas. Fuera de alcance de GC01: tocar sldb; ReviewDoc (GC02); RuleDocs y evaluación de __activation_receipts__ (GC05); parent_id/children (GC09); restricciones de edit task y advance --to (GC06); efectos de transición (GC04). (2) __contract__ es un atributo de clase lista de nombres de campo (sldb GO02 (e)); el sldb instalado (checkout editable ../sldb) no lo lee todavía: queda inerte, deskops no calcula ningún hash y el test solo comprueba el valor del atributo. (3) Vocabulario: CLOSEOUT_EVIDENCE_VOCABULARY conserva los seis kinds de hoy (tests, commit, atom, materialization, document, external) para --evidence; children y goldens solo aparecen declarados en los tipos. closeout verify de una tarea cuyo tipo declara children o goldens falla nombrando el kind como aún no verificable (lo verifican GC09 y un nodo posterior); no se salta. Kinds de recibo: preflight, bundle, reproduction, goldens, owner. (4) Migración de task_type legado: code|implementation|test → task.code; docs|spec|design → task.docs; external → task.external; vacío → task.code; un valor que ya es nombre de tipo registrado (task.*) se conserva; cualquier otro valor (p. ej. debug, refactor, decision, aggregate o desconocido) → task.code y el reporte de desk update lo marca como "tipo legado desconocido, migrado a task.code". En todos los casos se conserva el campo closeout_evidence de la tarea, así su cierre no cambia. (5) --evidence se implementa como piso tal como está escrito (solo agrega kinds a los del tipo; quitar uno falla). El pendiente del dueño no bloquea: si lo retira, lo hace un nodo posterior. (6) Semántica de override: closeout_evidence no vacío en la tarea es la lista completa y reemplaza a la del tipo; vacío = se usa la del tipo. add task deja closeout_evidence vacío salvo que --evidence agregue kinds, en cuyo caso escribe evidencia del tipo ∪ agregados en el orden del vocabulario. Las tareas existentes conservan su lista. (7) G_TYPES no es un artefacto: se satisface al cerrar GC01 (revisión aceptada, tests verdes, closeout commit, que hace el supervisor). Su evidencia es la de gates.G_TYPES de dag.yaml, corregida en rev 2: model <= TaskCodeDoc incluye task.refactor y NO task.debug (la tabla manda; rev 1 decía lo contrario por error).

## Implementation Path

_Outline the expected implementation route or affected surface._

Módulo deskops/models/task_types.py con las subclases de TaskDoc de la tabla de brief.md §Tipos: TaskCodeDoc (task.code), TaskDocsDoc (task.docs), TaskDebugDoc (task.debug, hereda de TaskDoc: exige reproduction en lugar de bundle y por eso no puede ser subtipo de task.code, donde los gates solo se suman), TaskRefactorDoc (task.refactor, hereda de TaskCodeDoc y suma goldens), TaskDecisionDoc (task.decision), TaskAggregateDoc (task.aggregate; sus campos parent_id/children los agrega GC09), TaskExternalDoc (task.external). Cada subclase fija task_type a su nombre (Literal con default) y declara dos atributos de clase: __closeout_evidence__ (tupla del vocabulario de closeout_gates.py:23, más children para el agregado y goldens para refactor, que este nodo solo declara: su verificación es de GC09 y de un nodo posterior) y __activation_receipts__ (tupla de kinds de ReviewDoc que la regla de GC05 exigirá: preflight, bundle, reproduction, goldens, owner). TaskDoc base conserva el campo task_type: str para leer documentos viejos y declara __contract__ = [title, goal, scope, implementation_path, files, validation, done_when] (sintaxis de sldb GO02 (e); si la versión de sldb instalada no la lee, el atributo es inerte hasta que la lea). Registro: las subclases entran en MODEL_REFS (bootstrap.py:26) y se heredan en cada desk como los demás modelos (bootstrap.py:118-160); un desk agrega tipos propios en desk/models/*.py (DC7) y deskops desk update --apply los registra con sldb add_model y pythonpath = raíz del desk; hipótesis a verificar en el TaskDoc: sldb registra una subclase cuya base es un modelo heredado (federado) y base_models la resuelve. add task --task-type <nombre> rechaza un nombre que no sea un tipo registrado (familia model <= TaskDoc) con el mensaje que lista los tipos; sin --task-type, el default es task.code y se avisa en el envelope. closeout_evidence deja de escribirse en la tarea nueva: se lee del tipo (TASK_TYPE_EVIDENCE y evidence_for_task_type se borran); --evidence solo puede agregar kinds a los del tipo (piso; pendiente del dueño en decisiones.md) y un kind que quite falla. Las tareas existentes conservan su campo closeout_evidence, que el cierre sigue leyendo como override por encima del tipo. El documento de una tarea se guarda bajo el modelo de su tipo (TaskCodeDoc:task-x), de modo que model <= TaskCodeDoc lo encuentra; migración: deskops desk update --apply re-trackea cada tarea de desk/tasks bajo el modelo que su task_type legado indica (code|implementation|test → task.code; docs|spec|design → task.docs; external → task.external; vacío → task.code) y reescribe task_type; la migración es idempotente y reporta cada tarea movida. Produce G_TYPES. Aceptación: add task --task-type task.code crea una tarea tracked como TaskCodeDoc:<id> con task_type task.code; --task-type foo falla nombrando los tipos registrados; sin --task-type se crea task.code con aviso; en un desk temporal con un desk/models/local_types.py que define TaskCliDoc(TaskCodeDoc) (task.code.cli), desk update --apply lo registra y add task --task-type task.code.cli funciona; sldb docs find --where "model <= TaskCodeDoc" devuelve tareas task.code y task.refactor y no task.docs ni task.debug; closeout verify de una tarea task.docs exige commit y document sin que la tarea tenga closeout_evidence; --evidence que quite un kind del tipo falla y uno que agregue se guarda; una tarea legada con task_type implementation queda task.code tras desk update --apply y una segunda corrida no cambia nada; grep de TASK_TYPE_EVIDENCE en deskops/ no devuelve nada; tests/fixtures/model_contract_hashes.json actualizado; CHANGELOG y docs/workflow-policy-reference.md con la tabla de tipos. Reglas comunes (alcance.md §Reglas comunes): validación con pytest tests en robocop2, ningún nodo cierra con tests rojos ni saltados; toda capacidad nueva entra con modelo o documento, comando CLI con envelope, pruebas, entrada en CHANGELOG.md y doc en docs/; nada de Python supliendo una regla que sldb debería evaluar: si sldb (grafo-operable rev 9) no fija lo que el nodo necesita, se registra la hipótesis en este TaskDoc y, si bloquea, se manda nota con deskops message send --to sldb; compatibilidad: los desks existentes migran con deskops desk update --apply de forma idempotente y probada; ninguna bandera para saltar un gate (D2). Reglas del dueño: no tocar el repo sldb; nada escrito a mano en desk/ ni .sldb/ (solo los CLI deskops y sldb); código, tests y docs se editan normal; trabajo en el worktree deskops-wt-gates, rama wt/gates-por-tipo, nunca push a main; nunca git add -A.

## Validation

_List the checks required before this task can close._

- add task --task-type task.code crea una tarea tracked como TaskCodeDoc:<id> con task_type task.code
- --task-type foo falla nombrando los tipos registrados
- sin --task-type se crea task.code con aviso
- en un desk temporal con un desk/models/local_types.py que define TaskCliDoc(TaskCodeDoc) (task.code.cli), desk update --apply lo registra y add task --task-type task.code.cli funciona
- sldb docs find --where "model <= TaskCodeDoc" devuelve tareas task.code y task.refactor y no task.docs ni task.debug
- closeout verify de una tarea task.docs exige commit y document sin que la tarea tenga closeout_evidence
- --evidence que quite un kind del tipo falla y uno que agregue se guarda
- una tarea legada con task_type implementation queda task.code tras desk update --apply y una segunda corrida no cambia nada
- grep de TASK_TYPE_EVIDENCE en deskops/ no devuelve nada
- tests/fixtures/model_contract_hashes.json actualizado
- CHANGELOG y docs/workflow-policy-reference.md con la tabla de tipos.
- PYTHONPATH=$PWD python -m pytest -q tests (suite completa verde en robocop2)

## Done When

_Name the observable condition that makes the task complete._

add task --task-type task.code crea una tarea tracked como TaskCodeDoc:<id> con task_type task.code; --task-type foo falla nombrando los tipos registrados; sin --task-type se crea task.code con aviso; en un desk temporal con un desk/models/local_types.py que define TaskCliDoc(TaskCodeDoc) (task.code.cli), desk update --apply lo registra y add task --task-type task.code.cli funciona; sldb docs find --where "model <= TaskCodeDoc" devuelve tareas task.code y task.refactor y no task.docs ni task.debug; closeout verify de una tarea task.docs exige commit y document sin que la tarea tenga closeout_evidence; --evidence que quite un kind del tipo falla y uno que agregue se guarda; una tarea legada con task_type implementation queda task.code tras desk update --apply y una segunda corrida no cambia nada; grep de TASK_TYPE_EVIDENCE en deskops/ no devuelve nada; tests/fixtures/model_contract_hashes.json actualizado; CHANGELOG y docs/workflow-policy-reference.md con la tabla de tipos.
