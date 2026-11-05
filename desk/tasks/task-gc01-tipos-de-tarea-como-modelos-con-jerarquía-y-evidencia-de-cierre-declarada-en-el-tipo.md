---
id: task-gc01-tipos-de-tarea-como-modelos-con-jerarquía-y-evidencia-de-cierre-declarada-en-el-tipo
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
- deskops/models/task.py
- deskops/models/task_types.py
- deskops/models/__init__.py
- deskops/bootstrap.py
- deskops/services/closeout_gates.py
- deskops/services/tasks.py
- deskops/operations.py
- deskops/cli/registry.py
- deskops/workspace.py
- tests/
- tests/fixtures/model_contract_hashes.json
- tests/fixtures/golden/help/
- docs/workflow-policy-reference.md
- CHANGELOG.md
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

# GC01: Tipos de tarea como modelos con jerarquía y evidencia de cierre declarada en el tipo

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo GC01 del plan desk/drawer/plans/gates-por-tipo (dag.yaml rev 1, paquete PC01): lado consumidor del plan grafo-operable de sldb; los gates del ciclo de vida pasan a ser documentos que sldb evalúa (D2, DC1-DC7).

## Goal

_Describe the concrete result this task must produce._

Módulo deskops/models/task_types.py con las subclases de TaskDoc de la tabla de brief.md §Tipos: TaskCodeDoc (task.code), TaskDocsDoc (task.docs), TaskDebugDoc (task.debug, hereda de TaskDoc: exige reproduction en lugar de bundle y por eso no puede ser subtipo de task.code, donde los gates solo se suman), TaskRefactorDoc (task.refactor, hereda de TaskCodeDoc y suma goldens), TaskDecisionDoc (task.decision), TaskAggregateDoc (task.aggregate; sus campos parent_id/children los agrega GC09), TaskExternalDoc (task.external). Cada subclase fija task_type a su nombre (Literal con default) y declara dos atributos de clase: __closeout_evidence__ (tupla del vocabulario de closeout_gates.py:23, más children para el agregado y goldens para refactor, que este nodo solo declara: su verificación es de GC09 y de un nodo posterior) y __activation_receipts__ (tupla de kinds de ReviewDoc que la regla de GC05 exigirá: preflight, bundle, reproduction, goldens, owner). TaskDoc base conserva el campo task_type: str para leer documentos viejos y declara __contract__ = [title, goal, scope, implementation_path, files, validation, done_when] (sintaxis de sldb GO02 (e); si la versión de sldb instalada no la lee, el atributo es inerte hasta que la lea). Registro: las subclases entran en MODEL_REFS (bootstrap.py:26) y se heredan en cada desk como los demás modelos (bootstrap.py:118-160); un desk agrega tipos propios en desk/models/*.py (DC7) y deskops desk update --apply los registra con sldb add_model y pythonpath = raíz del desk; hipótesis a verificar en el TaskDoc: sldb registra una subclase cuya base es un modelo heredado (federado) y base_models la resuelve. add task --task-type <nombre> rechaza un nombre que no sea un tipo registrado (familia model <= TaskDoc) con el mensaje que lista los tipos; sin --task-type, el default es task.code y se avisa en el envelope. closeout_evidence deja de escribirse en la tarea nueva: se lee del tipo (TASK_TYPE_EVIDENCE y evidence_for_task_type se borran); --evidence solo puede agregar kinds a los del tipo (piso; pendiente del dueño en decisiones.md) y un kind que quite falla. Las tareas existentes conservan su campo closeout_evidence, que el cierre sigue leyendo como override por encima del tipo. El documento de una tarea se guarda bajo el modelo de su tipo (TaskCodeDoc:task-x), de modo que model <= TaskCodeDoc lo encuentra; migración: deskops desk update --apply re-trackea cada tarea de desk/tasks bajo el modelo que su task_type legado indica (code|implementation|test → task.code; docs|spec|design → task.docs; external → task.external; vacío → task.code) y reescribe task_type; la migración es idempotente y reporta cada tarea movida. Produce G_TYPES.

## Scope

_State what is in scope and what is out of scope._

Repo deskops. Archivos: deskops/models/task.py, deskops/models/task_types.py, deskops/models/__init__.py, deskops/bootstrap.py, deskops/services/closeout_gates.py, deskops/services/tasks.py, deskops/operations.py (creación y verify_task_closeout), deskops/cli/registry.py (add task, desk update), deskops/workspace.py (desk/models), tests/, tests/fixtures/model_contract_hashes.json, docs/workflow-policy-reference.md, CHANGELOG.md. Depende de: nada; requiere gates: ninguno. Fuera de alcance: brief.md §Fuera de alcance, los demás nodos GC del plan y todo cambio en sldb.

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
