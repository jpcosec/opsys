---
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-gc01-tipos-de-tarea-como-modelos-con-jerarquía-y-evidencia-de-cierre-declarada-en-el-tipo.md
- desk/tasks/task-gc02-reviewdoc-como-recibo-anclado-al-contrato-de-la-tarea.md
- desk/tasks/task-gc06-cierre-de-las-vías-de-escape-advance-to-y-edit-task-sobre-campos-del-ciclo-de-vida.md
- desk/tasks/task-gc03-comando-deskops-review-que-reemplaza-a-los-dos-scripts-de-revisión-en-frío.md
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

- GC01: Tipos de tarea como modelos con jerarquía y evidencia de cierre declarada en el tipo [draft] - Módulo deskops/models/task_types.py con las subclases de TaskDoc de la tabla de brief.md §Tipos: TaskCodeDoc (task.code), TaskDocsDoc (task.docs), TaskDebugDoc (task.debug, hereda de TaskDoc: exige reproduction en lugar de bundle y por eso no puede ser subtipo de task.code, donde los gates solo se suman), TaskRefactorDoc (task.refactor, hereda de TaskCodeDoc y suma goldens), TaskDecisionDoc (task.decision), TaskAggregateDoc (task.aggregate; sus campos parent_id/children los agrega GC09), TaskExternalDoc (task.external). Cada subclase fija task_type a su nombre (Literal con default) y declara dos atributos de clase: __closeout_evidence__ (tupla del vocabulario de closeout_gates.py:23, más children para el agregado y goldens para refactor, que este nodo solo declara: su verificación es de GC09 y de un nodo posterior) y __activation_receipts__ (tupla de kinds de ReviewDoc que la regla de GC05 exigirá: preflight, bundle, reproduction, goldens, owner). TaskDoc base conserva el campo task_type: str para leer documentos viejos y declara __contract__ = [title, goal, scope, implementation_path, files, validation, done_when] (sintaxis de sldb GO02 (e); si la versión de sldb instalada no la lee, el atributo es inerte hasta que la lea). Registro: las subclases entran en MODEL_REFS (bootstrap.py:26) y se heredan en cada desk como los demás modelos (bootstrap.py:118-160); un desk agrega tipos propios en desk/models/*.py (DC7) y deskops desk update --apply los registra con sldb add_model y pythonpath = raíz del desk; hipótesis a verificar en el TaskDoc: sldb registra una subclase cuya base es un modelo heredado (federado) y base_models la resuelve. add task --task-type <nombre> rechaza un nombre que no sea un tipo registrado (familia model <= TaskDoc) con el mensaje que lista los tipos; sin --task-type, el default es task.code y se avisa en el envelope. closeout_evidence deja de escribirse en la tarea nueva: se lee del tipo (TASK_TYPE_EVIDENCE y evidence_for_task_type se borran); --evidence solo puede agregar kinds a los del tipo (piso; pendiente del dueño en decisiones.md) y un kind que quite falla. Las tareas existentes conservan su campo closeout_evidence, que el cierre sigue leyendo como override por encima del tipo. El documento de una tarea se guarda bajo el modelo de su tipo (TaskCodeDoc:task-x), de modo que model <= TaskCodeDoc lo encuentra; migración: deskops desk update --apply re-trackea cada tarea de desk/tasks bajo el modelo que su task_type legado indica (code|implementation|test → task.code; docs|spec|design → task.docs; external → task.external; vacío → task.code) y reescribe task_type; la migración es idempotente y reporta cada tarea movida. Produce G_TYPES.
- GC02: ReviewDoc como recibo anclado al contrato de la tarea [draft] - Modelo deskops/models/review.py ReviewDoc (StructuredNLDoc, como RunDoc) con campos: id (review-<task>-<kind>-<n>), title, kind (preflight | bundle | reproduction | goldens | owner; vocabulario cerrado validado), subject (str; valor doc:<Modelo>:<id> o vacío para revisiones de nodos de plan), subject_ref (str libre: ruta#node:ID cuando subject está vacío), engine (nombre del RuntimeProfileDoc o "human"), actor (identidad que corrió o dispuso; deskops/identity.py), run_dir (ruta relativa bajo runs/), input_sha256, output_sha256, verdict (pending | accepted | rejected | incomplete), reason (str), created_at, disposed_at, disposed_by, tags; cuerpo: sección Summary y sección Disposition. __doc_anchors__ = ["subject"] y __references__ = ["subject"] (GO07 trata __doc_anchors__ también como references; antes de GO07 el campo es una referencia normal que resuelve doc:Model:name sin sufijo, hipótesis: la versión actual de sldb acepta en un campo __references__ un valor con prefijo doc: o GC02 lo declara solo en __doc_anchors__ y espera a GO07; el TaskDoc fija cuál). Un ReviewDoc vive en desk/reviews/<task-id>/<kind>-<n>.md y se trackea; deskops init/desk update crean desk/reviews/. Validación al escribir: kind y verdict en su vocabulario; verdict accepted o rejected exige reason no vacía y disposed_by; subject con forma doc:<Modelo>:<id> o vacío. Un ReviewDoc no se edita con edit review verdict: edit lo rechaza (el veredicto se escribe con deskops review dispose, GC03). Registro en MODEL_REFS. Este nodo no escribe ReviewDocs desde ningún comando; GC03 lo hace.
- GC06: Cierre de las vías de escape: advance --to y edit task sobre campos del ciclo de vida [draft] - Se retira la opción --to de deskops advance (registry y tasks.py:179-192); cada uso documentado se reemplaza: cerrar → closeout commit; superseded → closeout supersede; blocked → nada que escribir (DC4: blocked es la regla que no se cumple; mientras GC05 no exista, el mensaje de bloqueo de advance ya lo dice). edit task rechaza status, current_node, task_type, closeout_evidence e history con un error que dice quién escribe cada campo (advance y closeout; add task para task_type) y con exit 1 (error de dominio); el resto de campos sigue editable. El inbox 20261029-213633 (advance --to superseded no cambia status) se cierra con ack porque la opción desaparece. Sin dependencia de sldb: con task_activates aún sin condición (hasta GC05) retirar --to no bloquea a nadie.
- GC03: Comando deskops review que reemplaza a los dos scripts de revisión en frío [draft] - Comando deskops review con subcomandos: node <plan-dir> [IDS...] (revisa nodos de un dag.yaml del drawer: contrato del nodo con las claves KEEP del script gobernado, vecinos como edge, gates, y los cuatro archivos base del plan si existen: context-review-guide.md, brief.md, alcance.md, decisiones.md), preflight <task> (input = solo el TaskDoc), bundle <task> (TaskDoc + rituales enrutados por el Board + pills ligadas + átomos ligados + archivos que files nombra, menores de 60 KB + validación), status [<task> | <plan-dir>] (compara el hash del input vigente con los ReviewDoc existentes; sin llamar al modelo), dispose <review-id> --verdict accepted|rejected|incomplete --reason <texto> (escribe verdict, reason, disposed_at, disposed_by; falla si el ReviewDoc ya tiene veredicto distinto de pending). Cada corrida escribe la evidencia que el ritual pide bajo runs/subagents/<run>/context-review/<clave>/<sha256 del input>/attempt-N/ (input.md con FILE:<ruta> en orden documentado, manifest.json con argv, modelo, perfil, selection_reason, fuentes con sha256; output.md; stderr.log; receipt.json) y además un ReviewDoc (GC02) con verdict pending, subject = doc:<Modelo>:<id> de la tarea (sin hash: lo pinnea sldb cuando exista GO07; para node, subject vacío y subject_ref = <plan>/dag.yaml#node:<ID>), engine, run_dir, input_sha256, output_sha256. Motor: --engine <RuntimeProfileDoc> con default el perfil pi deepseek-flash del ritual (context-review.md paso 3), escrito por init como desk/runtimes/runtime-pi-deepseek-flash.md con los flags de aislamiento (--offline --no-session --no-context-files --no-skills --no-extensions --no-prompt-templates --no-tools) y el system prompt SYSTEM del script gobernado como texto del perfil; el perfil Scion queda como opción futura detrás de --engine y este nodo no lo implementa. Topes (D9): un input sin cambios no se vuelve a revisar (status lo dice); --max-attempts 2 por clave a nivel de plan; para preflight y bundle una por hash de contrato de la tarea, y una repetición exige --force con --reason, que queda en manifest.json y en el ReviewDoc. Falla de transporte (exit distinto de 0 o salida sin la sección REFORMULACION) deja receipt.json con technical_ok false y ReviewDoc con verdict incomplete y reason "technical", separado de los hallazgos de comprensión (ritual, paso 5). Retiro: se borran desk/drawer/plans/workspace-documental/context_review.py y tests/test_context_review_helper.py (los sustituyen los tests de este nodo); sldb/desk/drawer/plans/grafo-operable/context_review.py es de sldb y no se toca: se le manda nota por deskops message send --to sldb de que deskops review lo cubre. Produce G_RECEIPTS.
