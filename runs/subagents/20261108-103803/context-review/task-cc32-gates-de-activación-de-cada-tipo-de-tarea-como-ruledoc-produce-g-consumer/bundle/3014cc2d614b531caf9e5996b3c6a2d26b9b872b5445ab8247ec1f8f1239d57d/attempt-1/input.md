FILE:desk/tasks/task-cc32-gates-de-activación-de-cada-tipo-de-tarea-como-ruledoc-produce-g-consumer.md
---
id: task-cc32-gates-de-activación-de-cada-tipo-de-tarea-como-ruledoc-produce-g-consumer
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-cc38-invariantes-de-documento-al-modelo-validadores-pydantic-en-lugar-de-chequeos-sueltos-y-tests
pills: []
files:
- deskops/data/rules/
- deskops/data/desk_declaration.yaml
- deskops/models/task_types.py
- deskops/models/review.py
- deskops/lifecycle.py
- deskops/services/tasks.py
- deskops/workflow/next_actions.py
- deskops/cli/commands/desk.py
- tests/
- docs/workflow-policy-reference.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/deskops-como-config/dag.yaml
---

# CC32: Gates de activación de cada tipo de tarea como RuleDoc (produce G_CONSUMER)

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo CC32 del plan desk/drawer/plans/deskops-como-config/dag.yaml rev 3, en PF2 (reglas), árbol T3.2. Rehace GC05 de gates-por-tipo (congelado por DK2). Depende de CC31 y CC38, los dos en main. Gates: G_GO06, G_GO08 y G_GATES_FROZEN, satisfied. Produce G_CONSUMER, el gate externo que sldb grafo-operable espera de deskops. Se promueve sobre origin/main sin CC35a (verificado en wt/cc35a, sin integrar, a la espera de la decisión del dueño sobre el bloque de proveniencia sldb:), por autorización del overlord del 2026-11-08.

## Goal

_Describe the concrete result this task must produce._

El gate de activación de cada tipo de tarea de fábrica (task.code, task.docs, task.debug, task.refactor, task.decision, task.aggregate, task.external) es una RuleDoc semilla managed, on_transition sobre ritual-execution, que sldb evalúa al avanzar: exige los recibos de revisión que el tipo pide (accepted e intactos) y las dependencias cerradas. Los atributos __activation_receipts__ se borran. deskops advance, next y show muestran los findings de edges_blocked (cláusula, nodo, valor visto). El test de integración G_CONSUMER pasa en sus tres pasos.

## Scope

_State what is in scope and what is out of scope._

En alcance: deskops/data/rules/ (nuevo), deskops/data/desk_declaration.yaml (seeds e include de las reglas), deskops/models/task_types.py, deskops/models/review.py, deskops/lifecycle.py, deskops/services/tasks.py, deskops/workflow/next_actions.py, deskops/cli/commands/desk.py (solo si la salida de desk update lo necesita), tests/, docs/workflow-policy-reference.md y CHANGELOG.md. Fuera: deskops/doc_io.py y la capa de escritura de deskops/doc_access.py (CC35a), selectores, referencias entrantes y tags (CC35b-d), la consistencia status/current_node/history (CC37), las reglas de cierre (CC33), escrituras en sldb y la nota a sldb (la envía el coordinador al integrar).

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (desk/drawer/plans/deskops-como-config/dag.yaml rev 3, CC32). SCOPE: Rehace GC05 de gates-por-tipo (DK2). Por cada tipo de fábrica de GC01 (task.code, task.docs, task.debug, task.refactor, task.decision, task.aggregate, task.external; tabla normativa de gates-por-tipo brief.md §Tipos) una RuleDoc semilla managed en deskops/data/rules/ (escrita en desk/lifecycle/ por desk update --apply, DP3): subject "model <= <Clase del tipo>", where current_node = "ritual-execution", moment on_transition, severity error, condition = conjunción de any(^subject: kind = "<kind>" and anchor_state = "intact" and verdict = "accepted") por cada recibo que el tipo exige y all(depends_on: status = "closed") (DC6 de gates-por-tipo: una dependencia cerrada ya no existe y se omite del conjunto), message en español que nombra el tipo. Los chequeos entre documentos que el inventario de CC38 asigna a CC32 pasan a RuleDoc aquí y su chequeo viejo se borra en el mismo paso (DK6). task.aggregate: all(children: status = "closed") si GC09 de gates-por-tipo no existe, hipótesis en el TaskDoc (children no existe todavía como campo; la regla se escribe cuando exista y mientras tanto el tipo no tiene regla de activación de hijos). Un subtipo de desk (desk/models/*.py, DC7) suma reglas por herencia de familia sin código (DP1). Los atributos de clase __activation_receipts__ de GC01 se borran; la regla es la fuente. ReviewDoc.subject queda en __doc_anchors__ (GO07), pinneado por sldb. advance: sin arista en edges_holding, el mensaje de bloqueo lista los findings de edges_blocked (cláusula, nodo, valor visto) en lugar de las condiciones crudas; next y show los muestran también. blocked deja de ser un status guardado: es la arista bloqueada visible en show/next. Test de integración G_CONSUMER (texto del gate): desk temporal, tarea task.code sin recibos → advance falla y el mensaje nombra la cláusula any(^subject: kind = "preflight" ...); con recibos preflight y bundle de deskops review accepted e intactos → advance la activa; editar goal → los recibos quedan changed → vuelve a bloquear con anchor_state = changed. Al cerrar: deskops message send --to sldb con el hash del commit (produce G_CONSUMER).

ACCEPTANCE: El test de integración G_CONSUMER pasa en sus tres pasos; una tarea task.debug exige reproduction y no bundle; una tarea task.refactor exige además goldens (herencia de familia de task.code); un subtipo task.code.cli de un desk temporal hereda las reglas de task.code sin código y una RuleDoc propia del desk suma una cláusula; una tarea con depends_on abierta no se activa y el finding nombra la dependencia; grep de __activation_receipts__ en deskops/ vacío; en una copia del desk de deskops tras desk update --apply, sldb rules check sin --subject no reporta errores (las reglas de activación son on_transition y rules check sin --subject solo recorre on_check) y sldb rules explain de la regla de task.code sobre una tarea activa existente devuelve el finding con su cláusula; goldens de ayuda idénticos; nota a sldb enviada y su archivo en sldb/desk/inbox; CHANGELOG; docs/workflow-policy-reference.md con la tabla de reglas por tipo. Produce G_CONSUMER.

OUTPUT_SCOPE: deskops/data/rules/, deskops/models/task_types.py, deskops/models/review.py, deskops/lifecycle.py, deskops/services/tasks.py, deskops/workflow/next_actions.py, deskops/cli/commands/desk.py, tests/, docs/workflow-policy-reference.md, desk/rituals (vía deskops), CHANGELOG.md

INVARIANTE (alcance.md):
1. **El formato del desk no cambia.** Los archivos que hoy existen en `desk/` (Board, tareas, rituales, pills, átomos, drawer, inbox, `desk/lifecycle/`, `desk/reviews/`, `tag-namespaces.yaml`, `config.json`) conservan su ruta, su modelo y su forma. Un nodo puede agregar documentos nuevos en carpetas que ya existen (`RuleDoc` en `desk/lifecycle/`; las `ViewDoc` viven solo en el paquete, sin `desk/views/`, DA4), siempre escritos por `deskops desk update --apply` y nunca a mano; no reescribe los existentes salvo los que ya eran gestionados por deskops (`desk/lifecycle/`).
2. **La gramática del CLI no cambia.** Los goldens de ayuda (`tests/fixtures/golden/help/*.txt`, 120 archivos, `test_output_goldens.py:316 test_help_goldens`) y de salida (`tests/fixtures/golden/output/`, `test_command_output_goldens` :669) quedan iguales. Excepción ya decidida: lo que `gates-por-tipo` GC06 retiró (`advance --to`), que entra con GC06 antes de este plan.
3. **Cada superficie borra su código viejo en el mismo paso.** Un nodo que cambia una superficie a sldb borra en el mismo commit el código de deskops que la implementaba, con un grep en su aceptación. No hay periodo con dos caminos.
4. **En cada paso**, los tests de los archivos tocados verdes, `deskops doctor` y `deskops view board` correctos en los 6 desks (deskops, sldb, spec2viz, scion, pron, graph_ui), y la suite completa del repo tocado sin fallas nuevas contra main (la corre el supervisor sobre el resultado integrado; ver regla 3).

REGLAS COMUNES (alcance.md):
1. Cada nodo se promueve con `deskops add task --from-drawer` en el desk de deskops, con `--task-type` y `files` completos. Las revisiones en frío (preflight, cold-bundle con `deskops review`) las decide el supervisor; quien opera el desk dispone los hallazgos como correcciones del TaskDoc (`deskops edit task`) y resume en `coordinator-status.md`. Nada a mano en `desk/` fuera de `drawer/plans` ni en `.sldb/`.
2. Se ejecuta en robocop2, en un worktree de deskops por nodo o grupo de nodos que el coordinador fije.
3. Validación: los tests de los archivos tocados (`pytest -q <archivos>`, uno a la vez); la suite completa la corre el supervisor una vez sobre el resultado integrado, sin fallas nuevas contra main. Un nodo no cierra con tests rojos ni saltados.
4. Antes de cambiar una superficie, el nodo captura sus goldens de salida (si no existen) sobre un desk de prueba; después del cambio deben ser idénticos, salvo lo que su aceptación nombre.
5. Toda capacidad entra con prueba, `CHANGELOG.md` y doc en `docs/`; los rituales del desk que nombran el comportamiento cambiado se actualizan con `deskops` en el mismo nodo.
6. Compatibilidad de desks: lo que un nodo agrega o reescribe en `desk/` lo escribe `deskops desk update --apply` de forma idempotente (segunda corrida sin cambios), probado.
7. Nada de Python supliendo una regla: si el lenguaje de sldb no la expresa, hipótesis en el TaskDoc y nota a sldb.
8. Promoción de nodos con hijos (`node_role: aggregate`): nunca se promueve el agregado; se promueven los hijos.

PRECISIONES DE PROMOCIÓN (2026-11-08, coordinador del plan; base origin/main 7bb0f168):
a1 (base sin CC35a): CC35a (toda escritura por sldb.api.transaction, borra doc_io.py) está verificado en wt/cc35a y no está en main. Reescribe doc_access.py y toca lifecycle.py, services/tasks.py, closure.py, atoms.py, review.py, workspace.py, bootstrap.py, cli/commands/desk.py y message.py. Para que su rebase sea limpio: CC32 no toca deskops/doc_io.py ni la capa de escritura de deskops/doc_access.py; escribe por las funciones existentes de doc_access sin cambiarlas. En lifecycle.py, services/tasks.py y cli/commands/desk.py los cambios son mínimos: solo lo que el gate necesita, sin mover ni reformatear código vecino. Si algo de este nodo obliga a tocar esas zonas, el worker para y avisa.
a2 (inventario en main): __activation_receipts__ vive en deskops/models/task_types.py (:17 docstring, :41 TaskCodeDoc ("preflight","bundle"), :52 TaskDocsDoc ("preflight",), :67 TaskDebugDoc ("preflight","reproduction"), :78 TaskRefactorDoc(TaskCodeDoc) ("preflight","bundle","goldens"), :89 TaskDecisionDoc ("owner",), :100 TaskAggregateDoc (), :111 TaskExternalDoc ("preflight",), :166-171 task_type_activation_receipts) y en tests/test_task_types.py (:113-137, :281). Todo eso se borra; la tabla de recibos por tipo pasa a las RuleDoc. ReviewKind (models/review.py:33) ya tiene preflight, bundle, reproduction, goldens, owner y node; ReviewDoc.subject ya está en __doc_anchors__ (:42).
a3 (CC38 no asignó nada a CC32): el inventario de CC38 (TaskDoc de CC38, RESULTADO) deja 9 chequeos entre documentos para CC33 y 0 para CC32. La frase del scope «Los chequeos entre documentos que el inventario de CC38 asigna a CC32 pasan a RuleDoc aquí» no tiene objeto; el informe lo dice en una línea.
a4 (dónde viven y cómo se siembran las reglas): las RuleDoc fuente van en deskops/data/rules/, una por tipo de fábrica que tenga cláusulas, y se escriben en desk/lifecycle/ como seeds managed de deskops/data/desk_declaration.yaml (file: rules/<archivo>), con su include para que desk update --apply las trackee, como el grafo de CC31. Por eso deskops/data/desk_declaration.yaml entra en files aunque no esté en el output_scope del dag. Segunda corrida de desk update --apply sin cambios (regla 6), probado.
a5 (herencia de familia): la regla de cada tipo tiene subject «model <= <Clase>», y las tareas se trackean con su modelo tipado (desk de deskops: .sldb/core/documents/TaskCodeDoc/...). TaskRefactorDoc hereda de TaskCodeDoc, así que su regla propia solo suma la cláusula de goldens; la de task.code ya le aplica. task.debug no hereda de task.code: su regla pide preflight y reproduction, no bundle. task.aggregate: sin cláusula de recibos; la de hijos (all(children: ...)) queda como hipótesis en el informe porque children no existe como campo. Si no queda ninguna cláusula, task.aggregate no tiene RuleDoc; si lleva depends_on, se decide en el informe.
a6 (advance y la lectura de findings): sldb.api.edges_holding y edges_blocked (sldb src/sldb/api/edges/) solo corren las reglas on_transition cuando reciben document=<id del documento de la tarea>. lifecycle.transitions_holding pasa document; sin arista en holding, el mensaje de bloqueo de advance lista los findings de edges_blocked (cláusula, nodo, valor visto) en lugar de las condiciones crudas de las aristas. Exit 1 como hoy (cli/commands/operations.py:203). next y show muestran los mismos findings.
a7 (blocked): hoy ningún código de deskops guarda status blocked (grep en main: solo TransitionResult.blocked, lifecycle.py:88, y la descripción del campo status en models/task.py:123), y ninguna tarea del desk de deskops tiene status: blocked. El trabajo de «blocked deja de ser status guardado» es que el bloqueo se vea en show/next como arista bloqueada; no se agrega un status nuevo. models/task.py no entra en files: si su descripción tuviera que cambiar, se anota como seguimiento.
a8 (recibos en los tests): los tests construyen los ReviewDoc del desk temporal con la vía de escritura existente de deskops (la que usa deskops review / review dispose, sin llamar al modelo) o con sldb.api, nunca a mano en el archivo. «Intacto» y «changed» son el anchor_state que sldb calcula (GO07): el paso 3 edita goal con deskops edit task y espera anchor_state = changed en el finding.
a9 (recibos sin comando): deskops review solo produce recibos preflight, bundle y node. reproduction, goldens y owner no tienen comando, y la gramática del CLI no cambia (invariante 2). Tras desk update --apply, una tarea task.debug, task.refactor o task.decision real no se puede activar hasta que exista una vía para esos recibos. El nodo no la crea; el informe lo lista como consecuencia para el dueño, con cuántas tareas de los 6 desks están hoy en ritual-execution por tipo.
a10 (efecto sobre desks en uso): con las reglas instaladas, toda tarea en ritual-execution sin sus recibos accepted e intactos queda bloqueada. El informe da, para el desk de deskops (copia, tras desk update --apply), la lista de tareas en ritual-execution y cuáles quedarían bloqueadas, con su finding.
a11 (nota a sldb y G_CONSUMER): el worker no escribe en sldb ni corre deskops message send --to sldb. El coordinador la envía al integrar, con el hash del commit integrado, y marca G_CONSUMER. El informe trae el texto propuesto de la nota.
a12 (rituales, regla 5): si un ritual de desk/ nombra el comportamiento de activación cambiado, el worker no lo edita en su worktree: lista en el informe el comando deskops exacto y el coordinador lo corre sobre el desk.
a13 (verificación en 6 desks; lección de CC31): deskops doctor y desk update --apply sobre copias de los 6 desks con main y con la rama, con cwd neutro (plantilla: ~/proyectos/SLDB_1/coord2-ccconfig/cc35a/doctor6.sh o cc31/coord/n7c.sh). Sin hallazgos nuevos atribuibles a la rama, salvo las reglas nuevas trackeadas.

PRECISIONES DEL PREFLIGHT (review-...-preflight-1, 2026-11-08):
b1 (task.aggregate): toda RuleDoc de activación lleva la cláusula all(depends_on: status = "closed"); la de task.aggregate lleva solo esa, sin cláusula de recibos. La cláusula de hijos (all(children: ...)) no se escribe: va como hipótesis en el informe porque children no existe como campo. Esto reemplaza la última frase de a5.
b2 (inventario de CC38): manda a3. No hay chequeo viejo que borrar por esa frase del scope; el único código viejo que se borra es __activation_receipts__ (a2).
b3 (mensaje): el campo message de cada RuleDoc es una frase en español que nombra el tipo, por ejemplo «Una tarea task.code se activa con recibos preflight y bundle aceptados e intactos y sus dependencias cerradas.». sldb antepone ese texto a la explicación de la cláusula en cada finding. El mensaje de advance bloqueado por reglas imprime cada finding de edges_blocked con su cláusula, el nodo y el valor visto. El test G_CONSUMER fija que la salida contiene la cláusula any(^subject: kind = "preflight" ...) en el paso 1 y anchor_state = "changed" (o el valor visto que sldb dé) en el paso 3. El texto exacto lo elige el worker y lo fija el test.
b4 (goldens y tests existentes):
- Cuando las aristas no se toman por su propia condition y ninguna regla da error (los gates de ritual-testing y ritual-closeout), el mensaje de advance queda igual que hoy («Gate <node> is not complete (...)»). Las aserciones de tests/test_cli.py:1883, :2061, :2090, :2107 y tests/test_lifecycle_end_to_end.py:123 no cambian.
- Los goldens de ayuda quedan idénticos.
- De los goldens de salida, solo show_task.text y show_task.json (su tarea está en ritual-execution) pueden cambiar, y solo por la sección nueva de findings, que nombra la aceptación («next y show los muestran también»). Cualquier otro cambio de golden de salida: el worker para y avisa. El informe trae el diff.
- Los tests existentes que avanzan una tarea desde ritual-execution en un desk temporal recién creado van a quedar bloqueados por la regla nueva. Se les agrega un helper de tests/ que escribe los recibos accepted (vía de a8); sus aserciones no cambian.
b5 (forma de la declaración): mismas formas que las seeds del grafo de CC31 en deskops/data/desk_declaration.yaml (:127-144: path, mode: managed, file) y su include (:145-152, model + glob o paths). Las reglas van en desk/lifecycle/rule-activation-<tipo>.md (por ejemplo rule-activation-task-code.md), con fuente en deskops/data/rules/rule-activation-<tipo>.md, e include {model: RuleDoc, glob: desk/lifecycle/rule-activation-*.md}. El esquema del documento es sldb.models.rule_doc.RuleDoc (title, subject, where, condition, severity, moment, message). Escribir una RuleDoc exige que el modelo RuleDoc esté registrado en el store y que cada model <= X de su subject también lo esté (sldb api/rules/rule_writes.py). El registro de RuleDoc va en lifecycle.write_lifecycle_graph, junto al de los modelos de relación (:260-261), con sldb.api directo (is_model_registered / register_model de sldb.api), no con doc_io (a1). Es una adición de pocas líneas; el conflicto con CC35a en esas líneas lo resuelve el coordinador al rebasar CC35a.
b6 (informe): runs/subagents/cc32-worker-report.md, commiteado en wt/cc32, en Markdown, con una sección por cada punto de a3, a9, a10, a11 y a12.
b7 (cli/commands/desk.py): se toca solo si la salida de desk update --apply no informa las reglas escritas o trackeadas con las líneas que ya da para el grafo («wrote desk/lifecycle/...», «tracked ...»). Si write_lifecycle_graph ya las informa (las reglas pasan por seed_desk y apply_desk_includes), desk.py no se toca.
b8 (recibos sin comando en los tests): los ReviewDoc de kind reproduction, goldens u owner los tests los crean con sldb.api.transaction (create con el modelo ReviewDoc de deskops) o con la función de deskops que escribe el recibo en deskops review, si acepta el kind. Nunca escribiendo el archivo a mano. verdict accepted se pone con la vía de review dispose o en el mismo create.

## Validation

_List the checks required before this task can close._

- Test de integración G_CONSUMER en tres pasos (sin recibos falla nombrando la cláusula; con preflight y bundle accepted e intactos activa; goal editado bloquea con anchor_state = changed)
- Tests por tipo: task.debug exige reproduction y no bundle; task.refactor suma goldens; subtipo task.code.cli de desk temporal hereda y una RuleDoc propia suma cláusula; depends_on abierta bloquea y el finding la nombra
- grep -rn __activation_receipts__ deskops/ vacío
- Copia del desk de deskops tras desk update --apply (segunda corrida sin cambios): sldb rules check sin --subject sin errores; sldb rules explain de la regla de task.code sobre una tarea activa devuelve el finding con su cláusula
- TMPDIR=/dev/shm pytest -q, uno a la vez: tests de los archivos tocados, test_task_types, test_lifecycle_*, test_closeout_gates, test_scaffold_golden, test_cli, test_output_goldens y test_cli_help_examples (sin --update-golden)
- deskops doctor y desk update --apply en los 6 desks con main y rama, cwd neutro (a13)
- wc -l antes y después por archivo tocado
- CHANGELOG y docs/workflow-policy-reference.md con la tabla de reglas por tipo

## Done When

_Name the observable condition that makes the task complete._

El test de integración G_CONSUMER pasa en sus tres pasos; task.debug exige reproduction y no bundle; task.refactor exige además goldens por herencia de task.code; un subtipo task.code.cli de un desk temporal hereda las reglas de task.code sin código y una RuleDoc propia suma una cláusula; una dependencia abierta bloquea y el finding la nombra; grep de __activation_receipts__ en deskops/ vacío; en una copia del desk de deskops tras desk update --apply, sldb rules check sin --subject sin errores y sldb rules explain de la regla de task.code sobre una tarea activa existente devuelve el finding con su cláusula; goldens de ayuda y salida idénticos; CHANGELOG y docs/workflow-policy-reference.md con la tabla de reglas por tipo. La nota a sldb (G_CONSUMER) la envía el coordinador al integrar.

FILE:desk/rituals/context-review.md
---
sldb:
  by: agent
  at: '2026-10-31T04:05:18Z'
  authority: generated
  via: create_document
# ritual-xxx
id: ritual-context-review
# Ordered prose steps; not document references
steps:
- '1. Map the multilevel DAG: root, packages, leaves and dependency edges. Start with
  the question at the current node; review every node and its edges, not only the
  root.'
- '2. Save input.md as an explicit concatenation of FILE:<path> headers and UTF-8
  texts in documented order. Hash the exact saved bytes with SHA-256, without additional
  normalization. Evidence directory: runs/subagents/<run-dir>/context-review/<node-id>/<bundle-sha256>/attempt-<n>/.'
- '3. Launch a new ephemeral process for each attempt. On this machine the verified
  profile is: pi --provider deepseek --model deepseek-flash --thinking low --offline
  --no-session --no-context-files --no-skills --no-extensions --no-prompt-templates
  --no-tools --system-prompt <reviewer-role> --print @<input.md>. Save the command,
  provider/model/profile and reason for cheap selection. No --continue or --resume.
  Record isolation flags and supplied input as operational evidence; this does not
  assert knowledge of provider internal memory.'
- '4. Instruct the non-executing reviewer to restate the objective and scope, enumerate
  ambiguities and produce a detailed dry-run: which supplied sources it would read,
  proposed edits, dependency/interface implications, commands it would run later and
  expected validation outcomes. It may name commands but must not run them, inspect
  unsupplied sources or edit files.'
- 5. Save output and coordinator comparison with owner intent, including missing guardrails,
  required textual corrections and disposition. A word such as APTO is never sufficient.
  Keep transport/quota/unavailable-model failures separately from comprehension findings;
  stop or retry an available cheap model with explicit reason, without expert rescue.
- 6. Use misunderstandings as feedback on the brief. Correct its text; split oversized
  or ambiguous nodes recursively into coherent children and explicit dependency edges.
  Review root, packages and all leaves, plus contracts across edges. Do not execute
  while ambiguity remains unresolved.
- 7. Retry the revised explicit input in a new process, with no prior review or oral
  fixes injected. A new input or changed dependency contract invalidates affected
  reviews, including dependent nodes whose supplied contract changed; unrelated typos
  do not revoke every review. Preserve previous attempts for traceability.
- '8. Before Executor dispatch, run two separate cheap roles under this protocol:
  TaskDoc-only preflight (save reformulation also at runs/subagents/<run-dir>/preflight.md),
  then cold-bundle coverage using TaskDoc, routed instructions/rituals, bound pills,
  linked atoms/files and validation targets supplied explicitly. The coordinator accepts
  both comparisons before dispatch.'
- 9. Only reviewed ready leaves may enter the execution ritual. Expert council review
  of design, an Executor implementation and a fresh independent Tester are separate
  gates; none substitutes for cheap comprehension or human product decisions.
# e.g., layer:workflow, system:sldb
tags:
- system:sldb
- workspace:desk
- topic:rituals
- topic:context-review
---

# Cheap recursive zero-context brief review

## Purpose

_Explain why this ritual exists._

Test whether a cheap isolated reviewer understands the written question before planning, promotion or execution. Durable rule: [source atom](../atoms/workflow-model/atom-cheap-zero-context-reviews-test-the-brief-recursively.md). This ritual is a documentary gate; it adds no lifecycle state or runtime enforcement.

## Trigger

_State when this ritual should start._

Run while drafting or revising a plan, root, package or leaf, before promotion or execution and again when its explicit input or dependency contract changes.

## Preconditions

_List the conditions that must hold before running the ritual._

- The coordinator names the node, exact versioned brief, explicit dependencies/interfaces and expected intent. Large nodes can still be drafts; they need not be promoted to receive review.
- The supplied context is minimal: exact brief plus only necessary explicitly supplied references, with a documented order and paths. No chat history, previous outputs, oral corrections, persistent memory or automatically loaded context/skills.
- A cheap available provider/model is selected with a recorded reason and profile. Do not claim global minimum price without measurement; do not replace a failed cheap reviewer with an expert to obtain approval.

## Validation

_List the checks that prove the ritual was performed correctly._

- Every required root/package/leaf review has exact input/hash, provider/model/profile and selection reason, command/isolation evidence, reformulation, ambiguities, detailed non-executing dry-run, coordinator comparison and required changes.
- The coordinator compares understanding with intent rather than accepting a verdict token; no unresolved ambiguity remains before execution.
- Each attempt used a new process without history, memory, automatic skills/context or reviewer tools. TaskDoc-only and cold-bundle evidence remain separate.
- Changed node inputs and dependency contracts invalidate the affected reviews; review coverage is explicit by node/revision, never inferred from council approval or plan structure.

## Failure Modes

_List common mistakes this ritual prevents._

- Asking an expert council to compensate for an unclear brief, or treating APTO/structural PASS as comprehension or execution authorization.
- Reviewing only the root or whole large DAG and claiming every descendant passed.
- Letting a reviewer execute the dry-run or loading implicit chat history, skills, memory or previous corrections.
- Retrying in the same session, fabricating node evidence, or marking pending reviews approved.
- Confusing transport/quota failures with ambiguous intent, or replacing cheap review with execution/testing.

## Completion

_Describe what completion looks like._

For the reviewed node/version, the coordinator has accepted a faithful reformulation and detailed dry-run with no unresolved ambiguity; all required descendant and interface reviews are traceable. This proves brief comprehension only. Promotion, execution, independent testing, product decisions and closeout retain their own gates.

FILE:deskops/data/desk_declaration.yaml
# The desk a fresh repository gets: what `deskops init`, `deskops desk install`, `deskops desk
# update --apply` and the first desk operation create when it is missing (CC36, DP3).
#
# This is an sldb StoreDeclaration (`sldb.api.StoreDeclaration`) restricted to `folders`,
# `seeds` and `include`; deskops reads it, renders every seed for the desk at hand and passes
# the result in process to `sldb.api.scaffold_store` (`deskops.workspace.seed_desk`):
#
# - `{desk_name}` in a `file:` template or in a `document:` payload is replaced with the
#   project directory's name (`str.replace`, no other placeholder exists);
# - `file:` sources are read from `deskops/data/` (`templates/` for the desk's own files,
#   `lifecycle/` for the lifecycle graph);
# - `document:` seeds are rendered through their deskops model, as the Board and the review
#   runtime profile always were; the runtime profile's `system_prompt` is not data here: it
#   is `deskops.services.review.SYSTEM`, injected while the declaration is built.
#
# A desk's own files are `if_missing` seeds: a desk that already has the file keeps its own.
# The task lifecycle graph (CC31, GO09) is `managed`: the three RelationTypeDoc and the three
# RelationDoc under `desk/lifecycle/` are deskops' documents, written from `lifecycle/` and
# rewritten whenever a desk's copy differs (`deskops desk update --apply` reports it). Each
# RelationDoc carries the transition's effects in `attributes`: `sets` (the fields written on
# the task when the edge is taken) and `terminal` (the task closes). The `include` rules say
# which desk documents `deskops desk update --apply` tracks under which model
# (`sldb.api.stores.apply_declaration.apply_includes`): the lifecycle documents, the three
# lifecycle rituals by their ids (`RitualDoc:ritual-<x>`, what the graph's edges name) and
# one glob per desk folder. The Board and the tasks are tracked by their own paths.
folders:
- desk/tasks
- desk/contexts
- desk/rituals
- desk/atoms
- desk/roles
- desk/inbox
- desk/reviews
- desk/drawer
- desk/runtimes
- desk/materializations
- desk/steps
- desk/registry
- desk/faq
seeds:
- path: desk/config.json
  mode: if_missing
  file: templates/config.json
- path: desk/tasks/Board.md
  mode: if_missing
  track: false
  document:
    model: BoardDoc
    name: board-001
    payload:
      id: board-001
      title: '{desk_name} Board'
      scope: desk
      purpose: Route the active execution set for {desk_name}.
      tasks: []
      pills:
      - desk/contexts/pills.md
      rituals:
      - desk/rituals/phase.md
      - desk/rituals/execution.md
      - desk/rituals/testing.md
      - desk/rituals/closeout.md
      notes: Bootstrap complete. Add active task docs under `desk/tasks/` and route them here.
      tags:
      - workspace:desk
- path: desk/contexts/pills.md
  mode: if_missing
  file: templates/contexts/pills.md
- path: desk/rituals/phase.md
  mode: if_missing
  file: templates/rituals/phase.md
- path: desk/rituals/execution.md
  mode: if_missing
  file: templates/rituals/execution.md
- path: desk/rituals/testing.md
  mode: if_missing
  file: templates/rituals/testing.md
- path: desk/rituals/closeout.md
  mode: if_missing
  file: templates/rituals/closeout.md
- path: desk/drawer/README.md
  mode: if_missing
  file: templates/drawer/README.md
- path: desk/atoms/tag-namespaces.yaml
  mode: if_missing
  file: templates/atoms/tag-namespaces.yaml
- path: desk/runtimes/runtime-pi-deepseek-flash.md
  mode: if_missing
  track: false
  document:
    model: RuntimeProfileDoc
    name: runtime-pi-deepseek-flash
    payload:
      id: runtime-pi-deepseek-flash
      title: Pi deepseek-flash isolated reviewer
      status: active
      kind: pi
      binary: pi
      model_flag: --model
      fallback_models_flag: ''
      fallback_models_join: comma
      tools_flag: ''
      tools_join: comma
      system_prompt_flag: --system-prompt
      system_prompt_delivery: inline
      session_flag: ''
      extra_args:
      - --provider
      - deepseek
      - --model
      - deepseek-flash
      - --thinking
      - low
      - --offline
      - --no-session
      - --no-context-files
      - --no-skills
      - --no-extensions
      - --no-prompt-templates
      - --no-tools
      - --print
      unsupported_role_fields: []
      notes: 'Verified cheap profile for ritual-context-review step 3 (D4): offline, no session/context/skills/extensions/prompt-templates/tools.'
      summary: Isolated cheap reviewer profile (pi deepseek-flash) used by `deskops review`.
      tags:
      - system:deskops
- path: desk/lifecycle/type-task_activates.md
  mode: managed
  file: lifecycle/type-task_activates.md
- path: desk/lifecycle/type-task_hands_to_closeout.md
  mode: managed
  file: lifecycle/type-task_hands_to_closeout.md
- path: desk/lifecycle/type-task_completes.md
  mode: managed
  file: lifecycle/type-task_completes.md
- path: desk/lifecycle/execution-task_activates.md
  mode: managed
  file: lifecycle/execution-task_activates.md
- path: desk/lifecycle/testing-task_hands_to_closeout.md
  mode: managed
  file: lifecycle/testing-task_hands_to_closeout.md
- path: desk/lifecycle/closeout-task_completes.md
  mode: managed
  file: lifecycle/closeout-task_completes.md
include:
- model: RelationTypeDoc
  glob: desk/lifecycle/type-*.md
- model: RelationDoc
  paths:
  - desk/lifecycle/execution-task_activates.md
  - desk/lifecycle/testing-task_hands_to_closeout.md
  - desk/lifecycle/closeout-task_completes.md
- model: RitualDoc
  paths:
  - path: desk/rituals/execution.md
    name: ritual-execution
  - path: desk/rituals/testing.md
    name: ritual-testing
  - path: desk/rituals/closeout.md
    name: ritual-closeout
- model: BoardDoc
  glob: desk/tasks/board-*.md
- model: PillDoc
  glob: desk/contexts/pill-*.md
- model: RitualDoc
  glob: desk/rituals/ritual-*.md
- model: AtomDoc
  glob: desk/atoms/atom-*.md
- model: ProtoAtomDoc
  glob: desk/atoms/proto-*.md
- model: RoleDoc
  glob: desk/roles/*.md
- model: RepositoryDoc
  glob: desk/registry/*.md
- model: StepDoc
  glob: desk/steps/*.md
- model: DeskFAQDoc
  glob: desk/faq/*.md

FILE:deskops/models/task_types.py
"""Factory task types: ``TaskDoc`` subclasses that fix ``task_type`` and declare their gates.

A task type is a model, not a string: the family ``model <= TaskCodeDoc`` names the
documents of ``task.code`` and of every subtype that extends it (``task.refactor``), while
``task.debug`` deliberately extends ``TaskDoc`` instead of ``TaskCodeDoc`` because it swaps
``bundle`` for ``reproduction`` — a subtype only ever *adds* gates, it cannot remove one
(brief.md §Tipos, decisions.md DC1/D2).

Each concrete type fixes ``task_type`` to its name with a ``Literal`` default and declares two
class attributes:

- ``__closeout_evidence__``: the closeout evidence kinds ``deskops closeout verify`` checks.
  It uses the vocabulary of ``deskops.services.closeout_gates.CLOSEOUT_EVIDENCE_VOCABULARY``
  (tests, commit, atom, materialization, document, external) plus, for this node, ``children``
  (the aggregate) and ``goldens`` (the refactor) — both are only *declared* here; their
  verification lands in GC09 and a later node (TaskDoc precisión 3).
- ``__activation_receipts__``: the ``ReviewDoc`` kinds the GC05 activation rule will require
  (preflight, bundle, reproduction, goldens, owner). Declared here, evaluated later.

``TaskDoc`` itself keeps ``task_type: str`` so old documents still read, and declares
``__contract__`` (the contract fields; sldb GO02 (e)).
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from .task import TaskDoc


class TaskCodeDoc(TaskDoc):
    """``task.code``: code changes gated by tests, a commit and an atom|materialization link."""

    task_type: Literal["task.code"] = Field(
        default="task.code",
        description="Workflow task type; fixed to 'task.code' for this model.",
    )
    __closeout_evidence__ = ("tests", "commit", "atom", "materialization")
    __activation_receipts__ = ("preflight", "bundle")


class TaskDocsDoc(TaskDoc):
    """``task.docs``: document-only work gated by a commit and a document."""

    task_type: Literal["task.docs"] = Field(
        default="task.docs",
        description="Workflow task type; fixed to 'task.docs' for this model.",
    )
    __closeout_evidence__ = ("commit", "document")
    __activation_receipts__ = ("preflight",)


class TaskDebugDoc(TaskDoc):
    """``task.debug``: gated like ``task.code`` but activated by a reproduction, not a bundle.

    It extends ``TaskDoc`` directly: a subtype only adds gates, and this type replaces the
    ``bundle`` receipt of ``task.code`` with ``reproduction``, so it cannot be a ``task.code``.
    """

    task_type: Literal["task.debug"] = Field(
        default="task.debug",
        description="Workflow task type; fixed to 'task.debug' for this model.",
    )
    __closeout_evidence__ = ("tests", "commit", "atom", "materialization")
    __activation_receipts__ = ("preflight", "reproduction")


class TaskRefactorDoc(TaskCodeDoc):
    """``task.refactor``: a ``task.code`` that additionally requires goldens before and after."""

    task_type: Literal["task.refactor"] = Field(
        default="task.refactor",
        description="Workflow task type; fixed to 'task.refactor' for this model.",
    )
    __closeout_evidence__ = ("tests", "commit", "atom", "materialization", "goldens")
    __activation_receipts__ = ("preflight", "bundle", "goldens")


class TaskDecisionDoc(TaskDoc):
    """``task.decision``: gated by an owner receipt, a commit and a document."""

    task_type: Literal["task.decision"] = Field(
        default="task.decision",
        description="Workflow task type; fixed to 'task.decision' for this model.",
    )
    __closeout_evidence__ = ("commit", "document")
    __activation_receipts__ = ("owner",)


class TaskAggregateDoc(TaskDoc):
    """``task.aggregate``: closes when its children do (``children`` is declared, GC09 verifies it)."""

    task_type: Literal["task.aggregate"] = Field(
        default="task.aggregate",
        description="Workflow task type; fixed to 'task.aggregate' for this model.",
    )
    __closeout_evidence__ = ("children", "commit")
    __activation_receipts__ = ()


class TaskExternalDoc(TaskDoc):
    """``task.external``: external work evidenced by an http(s) URL."""

    task_type: Literal["task.external"] = Field(
        default="task.external",
        description="Workflow task type; fixed to 'task.external' for this model.",
    )
    __closeout_evidence__ = ("external",)
    __activation_receipts__ = ("preflight",)


#: Factory task type name -> model class. Desk-local types extend this set through
#: ``desk/models/*.py`` and are registered into the store by ``deskops desk update --apply``.
TASK_TYPE_MODELS: dict[str, type[TaskDoc]] = {
    "task.code": TaskCodeDoc,
    "task.docs": TaskDocsDoc,
    "task.debug": TaskDebugDoc,
    "task.refactor": TaskRefactorDoc,
    "task.decision": TaskDecisionDoc,
    "task.aggregate": TaskAggregateDoc,
    "task.external": TaskExternalDoc,
}

#: Legacy ``task_type`` strings -> canonical factory type name. Mirrors the migration in
#: ``deskops desk update --apply`` (TaskDoc precisión 4).
LEGACY_TASK_TYPE_MAP: dict[str, str] = {
    "code": "task.code",
    "implementation": "task.code",
    "test": "task.code",
    "docs": "task.docs",
    "spec": "task.docs",
    "design": "task.docs",
    "external": "task.external",
    "": "task.code",
}


def canonical_task_type_name(task_type: str) -> str:
    """Map a stored ``task_type`` to its canonical factory type name.

    A value that is already a factory type name is kept; a known legacy string is mapped;
    anything else (including an unknown value) resolves to ``task.code``, matching the
    ``desk update --apply`` migration.
    """
    name = str(task_type or "").strip().lower()
    if name in TASK_TYPE_MODELS:
        return name
    return LEGACY_TASK_TYPE_MAP.get(name, "task.code")


def factory_task_type_model(task_type: str) -> type[TaskDoc] | None:
    """The factory model class a canonical task type name resolves to, if any."""
    return TASK_TYPE_MODELS.get(canonical_task_type_name(task_type))


def task_type_closeout_evidence(task_type: str) -> tuple[str, ...] | None:
    """The ``__closeout_evidence__`` a factory type declares, or ``None`` when unknown."""
    model = factory_task_type_model(task_type)
    if model is None:
        return None
    return tuple(getattr(model, "__closeout_evidence__", ()))


def task_type_activation_receipts(task_type: str) -> tuple[str, ...]:
    """The ``__activation_receipts__`` a factory type declares (empty when unknown)."""
    model = factory_task_type_model(task_type)
    if model is None:
        return ()
    return tuple(getattr(model, "__activation_receipts__", ()))


def declared_evidence_list(value: object) -> list[str]:
    """The stored ``closeout_evidence`` as plain strings; the vocabulary is checked where it is used."""
    if isinstance(value, list):
        items = [str(item) for item in value]
    elif value in (None, ""):
        items = []
    else:
        items = [str(value)]
    return [item.strip() for item in items if item.strip()]

FILE:deskops/models/review.py
"""A review receipt anchored to the contract of the document it reviewed (``ReviewDoc``).

A review is a document, not a fact computed in Python (plan gates-por-tipo, D2): the
``ReviewDoc`` records what was reviewed (``subject``), who ran it and with which engine, the
run evidence under ``runs/``, the input/output hashes, and the verdict written by whoever
operates the desk. ``deskops review`` (GC03) writes the receipt with ``verdict: pending``;
``deskops review dispose`` writes the verdict; ``deskops edit review`` refuses to touch it
because a new review is a new document (DC3).

The subject is a document anchor: ``doc:<Model>:<id>`` (optionally pinned with
``@sha256:<contract hash>`` when sldb GO07 pins it). Until GO07 exists the installed sldb does
not resolve a ``doc:`` value declared in ``__references__`` (it reads it as a
``store:Model:name`` with store ``doc``), so the field is declared only in
``__doc_anchors__`` and stays inert; GO07 treats every ``__doc_anchors__`` field as a
reference field too (``G_SLDB_ANCHORS``). Nothing here fabricates that edge.
"""

from __future__ import annotations

import re
from typing import Literal

from pydantic import Field, model_validator

from sldb import StructuredNLDoc


REVIEW_ID_PATTERN = r"^review-.+-(preflight|bundle|reproduction|goldens|owner|node)-[0-9]+$"
SUBJECT_PATTERN = r"^(doc:[A-Z][A-Za-z0-9_]*:[^\s:@]+(@sha256:[0-9a-f]{64})?)?$"
SUBJECT_REF_PATTERN = r"^([^\s#]+#node:[A-Za-z0-9_-]+)?$"
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")

ReviewKind = Literal["preflight", "bundle", "reproduction", "goldens", "owner", "node"]
ReviewVerdict = Literal["pending", "accepted", "rejected", "incomplete"]


class ReviewDoc(StructuredNLDoc):
    """Receipt of one cold review (or another external check) bound to a document contract."""

    #: GO07 treats every ``__doc_anchors__`` field as a reference too; before it, the field
    #: stays inert so no Python here has to fake the anchor edge (TaskDoc precisión 1).
    __doc_anchors__ = ["subject"]
    __references__ = []
    __semantics__ = {"type": ["workflow", "review"], "workspace": ["desk", "runs"]}
    __template__ = """---
# review-<task>-<kind>-<n>
id: ⸢rev•id⸥
# preflight | bundle | reproduction | goldens | owner | node
kind: ⸢rev•kind⸥
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: ⸢rev•subject⸥
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ⸢rev•subject_ref⸥
# RuntimeProfileDoc name or "human"
engine: ⸢rev•engine⸥
actor: ⸢rev•actor⸥
# Run evidence directory under runs/, relative to the project root
run_dir: ⸢rev•run_dir⸥
input_sha256: ⸢rev•input_sha256⸥
output_sha256: ⸢rev•output_sha256⸥
# pending | accepted | rejected | incomplete
verdict: ⸢rev•verdict⸥
reason: ⸢rev•reason⸥
# ISO 8601 timestamp
created_at: ⸢rev•created_at⸥
# ISO 8601 timestamp, empty while pending
disposed_at: ⸢rev•disposed_at⸥
disposed_by: ⸢rev•disposed_by⸥
# e.g. workspace:desk
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Summary

_Summarize what was reviewed and the evidence this receipt records._

⸢rev•summary⸥

## Disposition

_Record the verdict rationale and who disposed of the review._

⸢rev•disposition⸥
""".strip()

    id: str = Field(
        description="Stable review identifier: 'review-<task-id>-<kind>-<n>'.",
        pattern=REVIEW_ID_PATTERN,
    )
    title: str = Field(description="Short human-readable label for the review.")
    kind: ReviewKind = Field(description="Review kind: preflight, bundle, reproduction, goldens, or owner.")
    subject: str = Field(
        default="",
        description="Document anchor 'doc:<Model>:<id>' (optionally pinned with @sha256:<hash>); "
        "empty for reviews of plan nodes.",
        pattern=SUBJECT_PATTERN,
    )
    subject_ref: str = Field(
        default="",
        description="Plan-node reference '<plan>/dag.yaml#node:<ID>'; empty when subject names a document.",
        pattern=SUBJECT_REF_PATTERN,
    )
    engine: str = Field(default="", description="RuntimeProfileDoc name that produced the review, or 'human'.")
    actor: str = Field(default="", description="Identity that ran or disposed of the review (deskops/identity.py).")
    run_dir: str = Field(
        default="", description="Run evidence directory under runs/, relative to the project root."
    )
    input_sha256: str = Field(default="", description="SHA-256 of the review input, 64 lowercase hex digits or empty.")
    output_sha256: str = Field(default="", description="SHA-256 of the review output, 64 lowercase hex digits or empty.")
    verdict: ReviewVerdict = Field(
        default="pending", description="Review verdict: pending, accepted, rejected, or incomplete."
    )
    reason: str = Field(default="", description="Why the verdict was reached; required when accepted or rejected.")
    created_at: str = Field(description="ISO 8601 timestamp when the review receipt was created.")
    disposed_at: str = Field(default="", description="ISO 8601 timestamp of the disposition; empty while pending.")
    disposed_by: str = Field(default="", description="Identity that disposed of the review; empty while pending.")
    summary: str = Field(default="", description="What was reviewed and what evidence the receipt records.")
    disposition: str = Field(default="", description="Verdict rationale and who disposed of the review.")
    tags: list[str] = Field(
        default_factory=list,
        description="Semantic tags placed at the end, using namespaced forms such as 'workspace:desk'.",
    )

    @model_validator(mode="after")
    def _validate_review(self) -> "ReviewDoc":
        subject = self.subject.strip()
        subject_ref = self.subject_ref.strip()
        if bool(subject) == bool(subject_ref):
            raise ValueError("exactly one of subject or subject_ref must be non-empty")
        if self.verdict in {"accepted", "rejected"}:
            if not self.reason.strip():
                raise ValueError(f"verdict {self.verdict!r} requires a non-empty reason")
            if not self.disposed_by.strip():
                raise ValueError(f"verdict {self.verdict!r} requires disposed_by")
        if self.verdict == "pending" and (self.disposed_at.strip() or self.disposed_by.strip()):
            raise ValueError("disposed_at and disposed_by must be empty while verdict is pending")
        for field_name in ("input_sha256", "output_sha256"):
            value = getattr(self, field_name).strip()
            if value and not SHA256_PATTERN.fullmatch(value):
                raise ValueError(f"{field_name} must be 64 lowercase hex digits or empty")
        if self.run_dir and self.run_dir != "runs" and not self.run_dir.startswith("runs/"):
            raise ValueError("run_dir must be relative to the project root and under runs/")
        return self

FILE:deskops/lifecycle.py
"""The task lifecycle as a graph in the desk's sldb store.

States are the desk's tracked rituals (``RitualDoc:ritual-execution`` and its siblings).
Transitions are sldb ``RelationDoc`` edges between those rituals, typed by a
``RelationTypeDoc`` whose name is the verb (``task_activates``), with a ``condition``
written as an sldb ``--where`` predicate over the task and the transition's effects in
``attributes``: ``sets`` (the task fields the transition writes, ``status`` today) and
``terminal`` (the task closes), the convention sldb reads (GO09). The six documents are
managed seeds of the package (``deskops/data/desk_declaration.yaml``, templates in
``deskops/data/lifecycle/``): ``deskops init`` and ``deskops desk update --apply`` write
them under ``desk/lifecycle/`` and rewrite a desk's copy that differs.

deskops keeps three things: the states ``deskops next`` describes
(``deskops/spec/workflows/task_lifecycle.yaml``), the call to sldb for the edges whose
condition holds (``sldb.api.edges_holding``) and their effects (``sldb.api.apply_effects``),
and the task's ``history``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from deskops import doc_io
from deskops.paths import data_path
from deskops.paths import package_pythonpath

SPEC_PATH = data_path("spec", "workflows", "task_lifecycle.yaml")
LIFECYCLE_DIR = Path("desk") / "lifecycle"
COMPLETE = "complete"
RELATION_TYPE_MODEL = "RelationTypeDoc"
RELATION_MODEL = "RelationDoc"
RITUAL_MODEL = "RitualDoc"


class LifecycleGraphMissing(RuntimeError):
    """The desk's store has no lifecycle graph, or it does not cover a task's state."""


@dataclass(frozen=True, slots=True)
class Transition:
    """One edge of the lifecycle graph leaving ``source``, with its effects as the edge declares them."""

    relation_type: str
    source: str
    target: str
    condition: str
    sets: dict[str, Any] = field(default_factory=dict)
    terminal: bool = False

    @property
    def effects(self) -> dict[str, Any]:
        return {"sets": dict(self.sets), "terminal": self.terminal}


@dataclass(frozen=True, slots=True)
class LifecycleSpec:
    """The states of ``task_lifecycle.yaml``: what ``deskops next`` says at each node."""

    entry_node: str
    states: tuple[dict[str, Any], ...] = field(default_factory=tuple)

    @property
    def rituals(self) -> list[str]:
        return [node for node in (str(state.get("current_node") or "") for state in self.states) if node and node != COMPLETE]


@dataclass(slots=True)
class ReadSnapshot:
    """Task-independent graph reads shared by every task read of one read-only pass.

    ``DeskopsOperations.read_snapshot`` opens one; ``transitions_from`` keeps the transitions
    leaving each node in it and the closure service keeps the closeout graph context.
    """

    transitions: dict[str, list["Transition"]] = field(default_factory=dict)
    graph_context: Any = None


@dataclass(slots=True)
class TransitionResult:
    current_node: str
    status: str
    progressed: bool
    blocked: bool
    message: str


def load_lifecycle_spec(path: Path = SPEC_PATH) -> LifecycleSpec:
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    states = tuple(state for state in payload.get("states") or [] if isinstance(state, dict))
    if not states:
        raise ValueError(f"Lifecycle spec declares no states: {path}")
    return LifecycleSpec(entry_node=str(payload.get("entry_node") or states[0].get("current_node") or ""), states=states)


# ---------------------------------------------------------------- conditions
def condition_holds(condition: str, payload: dict[str, Any]) -> bool:
    """Whether an sldb ``--where`` condition (predicates joined by `` and ``) holds on a task payload."""
    from sldb.api import where_matches

    return where_matches(condition, payload)


# ---------------------------------------------------------------- the graph
def _store(root: Path) -> Path:
    return root / ".sldb"


def ritual_export_id(ritual_id: str) -> str:
    return f"{RITUAL_MODEL}:{ritual_id}"


def _transition(node: str, edge: Any) -> Transition:
    """The edge as a transition; ``effects`` (filled by ``edges_holding``) else the declared attributes."""
    attributes = edge.metadata.get("attributes") or {}
    effects = edge.effects or {"sets": attributes.get("sets") or {}, "terminal": attributes.get("terminal")}
    return Transition(
        relation_type=edge.relation,
        source=node,
        target=edge.target.rsplit(":", 1)[-1],
        condition=str(edge.metadata.get("condition") or ""),
        sets=dict(effects.get("sets") or {}),
        terminal=bool(effects.get("terminal")),
    )


def _is_lifecycle_edge(edge: Any) -> bool:
    """An authored edge (a RelationDoc) whose target is a ritual (`sldb://document/RitualDoc:<id>`)."""
    return edge.metadata.get("origin") == "relation_doc" and edge.target.rsplit("/", 1)[-1].startswith(f"{RITUAL_MODEL}:")


def _lifecycle_edges(node: str, edges: list[Any]) -> list[Transition]:
    """The authored edges between rituals, in the order sldb returns them."""
    return [_transition(node, e) for e in edges if _is_lifecycle_edge(e)]


def transitions_from(root: Path, node: str, *, snapshot: ReadSnapshot | None = None) -> list[Transition]:
    """The lifecycle transitions leaving ``node``, as the desk's graph declares them.

    Topology, conditions and effects all come from the graph. The lifecycle graph lives in the
    desk's own store, so only that store's edge index is read (sldb keeps it composed while
    its shards do not move), not the index composed with every linked store.

    With a ``snapshot``, the transitions leaving a node are read once and reused.
    """
    if snapshot is not None:
        if node not in snapshot.transitions:
            snapshot.transitions[node] = transitions_from(root, node)
        return snapshot.transitions[node]
    from sldb.api import edges_from

    return _lifecycle_edges(node, edges_from(_store(root), ritual_export_id(node), include_linked=False))


def transitions_holding(root: Path, node: str, payload: dict[str, Any]) -> list[Transition]:
    """The transitions leaving ``node`` whose condition holds on ``payload`` (``sldb.api.edges_holding``),
    each with its effects resolved for that payload."""
    from sldb.api import edges_holding

    return _lifecycle_edges(node, edges_holding(_store(root), ritual_export_id(node), payload, include_linked=False))


def lifecycle_transitions(root: Path, spec: LifecycleSpec | None = None) -> list[Transition]:
    """Every transition of the desk's lifecycle graph, ritual by ritual; empty without a store."""
    if not (_store(root) / "core").exists():
        return []
    spec = spec or load_lifecycle_spec()
    return [t for node in spec.rituals for t in transitions_from(root, node)]


def advance(root: Path, payload: dict[str, Any], model: type[Any], spec: LifecycleSpec | None = None) -> TransitionResult:
    """Take the first transition out of the task's current node whose condition holds.

    The edge's effects are applied with ``sldb.api.apply_effects`` (``sets`` replaces the
    payload's top-level keys; the result validates against ``model``, the task type's model)
    and, when the edge is ``terminal``, ``current_node`` becomes ``complete``; the relation type
    is appended to ``history``. Mutates ``payload`` and reports what happened; one call takes
    at most one transition. The graph has one edge leaving each ritual, so the order sldb
    returns the holding edges in decides nothing (k4).
    """
    from sldb.api import apply_effects

    spec = spec or load_lifecycle_spec()
    node = str(payload.get("current_node") or spec.entry_node)
    status = str(payload.get("status") or "")
    if node == COMPLETE:
        return TransitionResult(COMPLETE, status, False, False, "Task already complete.")
    if not (_store(root) / "core").exists():
        raise LifecycleGraphMissing(
            f"No sldb store at {_store(root)}: run 'deskops init' (or 'deskops desk update --apply' on an "
            "existing store) to create the lifecycle graph that 'deskops advance' reads."
        )
    transitions = transitions_from(root, node)
    if not transitions:
        raise LifecycleGraphMissing(
            f"No lifecycle transition leaves '{node}' in the graph of {_store(root)}. "
            "Run 'deskops desk update --apply' to write the lifecycle graph."
        )
    holding = transitions_holding(root, node, payload)
    if not holding:
        payload["current_node"] = node
        gates = "; ".join(f"{t.relation_type}: {t.condition}" for t in transitions)
        return TransitionResult(node, status, False, True, f"Gate {node} is not complete ({gates}).")
    transition = holding[0]
    payload.update(apply_effects(payload, transition.effects, model))
    history = payload.setdefault("history", [])
    if isinstance(history, list):
        history.append(transition.relation_type)
    target = COMPLETE if transition.terminal else transition.target
    payload["current_node"] = target
    verb = "Completed" if transition.terminal else "Advanced to"
    return TransitionResult(target, str(payload.get("status") or ""), True, False, f"{verb} {target} via {transition.relation_type}.")


# ---------------------------------------------------------------- writing the graph
def seed_changes(root: Path, result: Any) -> list[str]:
    """What a desk scaffold did to the lifecycle graph: ``wrote <path>`` and ``rewrote <path>`` lines."""
    root = root.resolve()
    prefix = LIFECYCLE_DIR.as_posix() + "/"
    created = [path.resolve().relative_to(root).as_posix() for path in result.created_paths]
    rewritten = [path.resolve().relative_to(root).as_posix() for path in result.rewritten_paths]
    return [f"wrote {rel}" for rel in created if rel.startswith(prefix)] + [f"rewrote {rel}" for rel in rewritten]


def _ritual_paths(spec: LifecycleSpec) -> dict[str, str]:
    return {f"desk/rituals/{node.removeprefix('ritual-')}.md": node for node in spec.rituals}


def tracked_line(model: str, path: str, spec: LifecycleSpec | None = None) -> str | None:
    """The change line for a lifecycle document the declared includes tracked; None for any other."""
    if path.startswith(LIFECYCLE_DIR.as_posix() + "/"):
        return f"tracked {path}"
    ritual = _ritual_paths(spec or load_lifecycle_spec()).get(path)
    if model == RITUAL_MODEL and ritual:
        return f"tracked {path} as {ritual_export_id(ritual)}"
    return None


def write_lifecycle_graph(root: Path) -> list[str]:
    """Make the desk's store carry the lifecycle graph; return what was written or tracked.

    Idempotent: writes the managed lifecycle seeds and restores one the desk changed
    (``workspace.seed_desk``), registers sldb's relation models when the store lacks them and
    tracks the declared desk documents
    (``workspace.apply_desk_includes``): the lifecycle documents and the lifecycle rituals by
    their ids. Any other declared document pending is tracked too and reported in the same way.
    """
    from sldb.api import is_model_registered

    from deskops.workspace import apply_desk_includes
    from deskops.workspace import pending_desk_includes
    from deskops.workspace import seed_desk

    root = root.resolve()
    changes = seed_changes(root, seed_desk(root, restore_managed=True))
    if not all(is_model_registered(_store(root), name) for name in (RELATION_MODEL, RELATION_TYPE_MODEL)):
        doc_io.init_relations_in(root, pythonpath=package_pythonpath())
    spec = load_lifecycle_spec()
    pending = {path: model for model, path in pending_desk_includes(root)}
    for path in apply_desk_includes(root):
        model = pending.get(path, "")
        changes.append(tracked_line(model, path, spec) or f"tracked {path} as {model}")
    return changes

FILE:deskops/services/tasks.py
"""Task lifecycle service: create, list, show, advance, next, and the task type registry.

TaskDoc reads go only through sldb's ``extract_model_data``; this service never
overlays a regex parse on top of the model. Document storage (read/write/track,
selector resolution, the task payload with its inherited context) is
``deskops.doc_access``; the lifecycle graph is ``deskops.lifecycle``.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Any
from typing import TYPE_CHECKING

from deskops import doc_access
from deskops import doc_io
from deskops import lifecycle
from deskops.lifecycle import TransitionResult
from deskops.models import BoardDoc
from deskops.models import PillDoc
from deskops.models import TaskDoc
from deskops.models.validation import validated
from deskops.models.task_types import TASK_TYPE_MODELS
from deskops.models.task_types import canonical_task_type_name
from deskops.runtime import Task
from deskops.specs import compile_task_spec
from deskops.workflow.next_actions import match_workflow_state
from deskops.workflow.next_actions import render_workflow_mermaid

if TYPE_CHECKING:
    from deskops.operations import DeskopsOperations


@dataclass(slots=True)
class TaskBundle:
    task_id: str
    task_path: Path


def registered_task_types(root: Path) -> dict[str, type[Any]]:
    """task_type name -> model class: the factory types plus desk-local types in the store.

    A desk adds its own types as ``desk/models/*.py`` subclasses; ``desk update --apply``
    registers them with ``pythonpath`` = the desk root. Factory types are importable directly
    and are merged in first, so local modules never shadow them.
    """
    registry: dict[str, type[Any]] = dict(TASK_TYPE_MODELS)
    store_dir = root / ".sldb"
    if store_dir.exists():
        try:
            from sldb.api.model_registry.model_reference import resolve_model_ref

            from deskops.bootstrap import SLDBBootstrap

            entries = SLDBBootstrap()._registered_model_entries(store_dir)
            pythonpath = str(doc_access.desk_root(root))
            for name, entry in entries.items():
                if name in registry:
                    continue
                model_ref = getattr(entry, "model_ref", "") or ""
                if not model_ref:
                    continue
                try:
                    cls = resolve_model_ref(model_ref, pythonpath=pythonpath)
                except Exception:
                    continue
                if not isinstance(cls, type) or not issubclass(cls, TaskDoc):
                    continue
                field = cls.model_fields.get("task_type")
                default = getattr(field, "default", None)
                if default not in (None, ""):
                    registry[str(default)] = cls
        except Exception:
            pass
    return registry


class TasksService:
    def __init__(self, root: Path, operations: "DeskopsOperations") -> None:
        self._ops = operations
        self.root = operations.root
        self.desk_root = operations.desk_root
        self.logger = operations.logger
        self._task_type_registry: dict[str, type[Any]] | None = None

    def registered_task_types(self) -> dict[str, type[Any]]:
        """The task type registry of this desk, read once per service instance."""
        if self._task_type_registry is None:
            self._task_type_registry = registered_task_types(self.root)
        return self._task_type_registry

    # ---------------------------------------------------------------- create
    def create_task_bundle(self, raw_payload: dict[str, Any]) -> TaskBundle:
        """Write one task and route it on the Board. Its lifecycle is the desk's graph
        (deskops/lifecycle.py), so nothing else is written per task."""
        doc_access.ensure_workspace(self.root)
        # A task's closeout evidence is declared by its type, not written into the task. The
        # task is stored under its type's model so `model <= TaskCodeDoc` finds it.
        raw_task_type = str(raw_payload.get("task_type") or "").strip()
        registry = self.registered_task_types()
        task_type = raw_task_type if raw_task_type in registry else canonical_task_type_name(raw_task_type)
        type_model = registry.get(task_type) or registry.get("task.code") or TaskDoc
        spec = lifecycle.load_lifecycle_spec()
        compiled = compile_task_spec({**raw_payload, "task_type": task_type}, entry_node=spec.entry_node)
        validated(type_model, compiled.task_payload)
        task_id = compiled.task_payload["id"]
        task_path = self._task_path(task_id)

        with doc_io.DocTransaction(self.root):
            doc_access.write_new_doc(self.root, task_path, type_model, compiled.task_payload)
            doc_access.track_created_document(self.root, type_model, task_path, task_id)
            self._append_task_to_board(task_id)
        return TaskBundle(task_id=task_id, task_path=task_path)

    def _append_task_to_board(self, task_id: str) -> None:
        board_path = self.desk_root / "tasks" / "Board.md"
        board_payload = doc_access.read_doc(board_path, BoardDoc)
        task_ref = f"desk/tasks/{task_id}.md"
        tasks = list(board_payload.get("tasks") or [])
        if task_ref not in tasks:
            tasks.append(task_ref)
            board_payload["tasks"] = tasks
            doc_access.write_doc(self.root, board_path, BoardDoc, board_payload)

    def bind_pill_to_task(self, task_selector: str, pill_selector: str) -> tuple[doc_access.DocumentRecord, str, bool]:
        doc_access.ensure_workspace(self.root)
        task_path = doc_access.resolve_artifact_selector(self.root, "artifact.task", self.desk_root / "tasks", task_selector)
        pill_path = doc_access.resolve_artifact_selector(self.root, "artifact.pill", self.desk_root / "contexts", pill_selector)
        task_payload = doc_access.read_doc(task_path, TaskDoc)
        doc_access.read_doc(pill_path, PillDoc)
        pill_ref = str(pill_path.relative_to(self.root))
        pills = list(task_payload.get("pills") or [])
        record = doc_access.DocumentRecord(kind="task", doc_id=str(task_payload.get("id", task_path.stem)), path=task_path)
        if pill_ref in pills:
            return record, pill_ref, False
        task_payload["pills"] = [*pills, pill_ref]
        doc_access.write_doc(self.root, task_path, TaskDoc, task_payload)
        return record, pill_ref, True

    # ---------------------------------------------------------------- read
    def list_tasks(self) -> list[Task]:
        task_dir = self.desk_root / "tasks"
        if not task_dir.exists():
            if not self.desk_root.exists():
                raise FileNotFoundError(f"Desk root not found at {self.desk_root}. Run 'deskops init' to initialize.")
            return []
        tasks: list[Task] = []
        for path in sorted(task_dir.glob("task-*.md")):
            try:
                tasks.append(doc_access.load_task(self.root, path.stem))
            except Exception as e:
                print(f"Warning: Failed to load task {path}: {e}", file=sys.stderr)
        return tasks

    def show_task(self, task_id: str) -> tuple[Task | None, list[dict[str, Any]]]:
        """The task and the lifecycle transitions leaving its current node, each with
        whether its condition holds now (empty when the graph is missing or the task is
        complete)."""
        try:
            task = doc_access.load_task(self.root, task_id)
        except FileNotFoundError:
            return None, []
        return task, self._lifecycle_gates(task)

    def _lifecycle_gates(self, task: Task) -> list[dict[str, Any]]:
        if not task.current_node or task.current_node == lifecycle.COMPLETE:
            return []
        try:
            transitions = lifecycle.transitions_from(self.root, task.current_node, snapshot=self._ops.snapshot)
        except Exception:
            return []
        payload = doc_access.read_doc(doc_access.resolve_glob(self.root, self.desk_root / "tasks", task.id), TaskDoc)
        self.add_closeout_facts(payload)
        return [
            {
                "relation_type": t.relation_type,
                "target": lifecycle.COMPLETE if t.terminal else t.target,
                "condition": t.condition,
                "holds": lifecycle.condition_holds(t.condition, payload),
            }
            for t in transitions
        ]

    def add_closeout_facts(self, payload: dict[str, Any]) -> None:
        """Facts the lifecycle conditions test with has(): present only when they hold."""
        closure = self._ops.closure
        for key, holds in (
            ("closeout_evidence_verified", closure.has_verified_task_closeout_evidence(payload)),
            ("pill_graduation_verified", closure.has_verified_task_pill_graduation(payload)),
        ):
            if holds:
                payload[key] = "verified"
            else:
                payload.pop(key, None)

    def render_next_action_diagram(self) -> str:
        spec = lifecycle.load_lifecycle_spec()
        return render_workflow_mermaid(spec, lifecycle.lifecycle_transitions(self.root, spec))

    def next_action_report(self, task_selector: str | None = None) -> dict[str, Any]:
        board_path = self.desk_root / "tasks" / "Board.md"
        board_ref = str(board_path.relative_to(self.root))
        if not task_selector:
            task_refs = list(doc_access.read_doc(board_path, BoardDoc).get("tasks") or [])
            if not task_refs:
                return {
                    "kind": "no_board_task",
                    "board": board_ref,
                    "suggested_commands": [
                        "deskops list tasks --root .",
                        "deskops promote inbox-to-drawer-task <selector> --root .",
                        'deskops add task --root . --title "..." ...',
                    ],
                }
            if len(task_refs) > 1:
                tasks = []
                for task_ref in task_refs:
                    path = self.root / str(task_ref)
                    payload = doc_access.read_doc(path, TaskDoc)
                    tasks.append(
                        {
                            "id": str(payload.get("id") or path.stem),
                            "status": str(payload.get("status") or ""),
                            "title": str(payload.get("title") or ""),
                        }
                    )
                return {
                    "kind": "multiple_board_tasks",
                    "board": board_ref,
                    "tasks": tasks,
                    "suggested_commands": [
                        "deskops next <task-id> --root .",
                        "deskops list tasks --root .",
                    ],
                }
        task_path = self._next_task_path(task_selector, board_path)
        payload = doc_access.resolve_task_payload(self.root, task_path.stem)
        spec = lifecycle.load_lifecycle_spec()
        state = match_workflow_state(spec, str(payload.get("current_node") or ""))
        pills = list(dict.fromkeys([*self._board_pills(board_path), *list(payload.get("effective_pills") or payload.get("pills") or [])]))
        sources = {
            "task": str(task_path.relative_to(self.root)),
            "board": str(board_path.relative_to(self.root)),
            "workflow": "deskops/spec/workflows/task_lifecycle.yaml",
        }
        why = [
            "task selected by explicit selector"
            if task_selector
            else "task selected from the single board route",
            f"current_node {payload.get('current_node', '')} matched workflow state {state['id']} in {sources['workflow']}",
            "pills merged from desk/tasks/Board.md and the task",
            f"source task: {sources['task']}",
            f"source board: {sources['board']}",
            f"source workflow: {sources['workflow']}",
        ]
        return {
            "task": {
                "id": payload["id"],
                "title": payload["title"],
                "status": payload["status"],
                "current_node": payload.get("current_node", ""),
                "task_type": payload.get("task_type", ""),
                "inherits_from": list(payload.get("inherits_from") or []),
            },
            "phase": state["phase"],
            "ritual": state.get("ritual", ""),
            "pills": pills,
            "next_actions": list(state.get("next_actions") or []),
            "advance_when": list(state.get("advance_when") or []),
            "why": why,
            "sources": sources,
        }

    # ---------------------------------------------------------------- advance
    def advance_task(self, task_id: str) -> tuple[Task | None, TransitionResult | None]:
        try:
            task_path = doc_access.resolve_glob(self.root, self.desk_root / "tasks", task_id)
        except FileNotFoundError:
            return None, None
        payload = doc_access.read_doc(task_path, TaskDoc)

        current_node = str(payload.get("current_node") or "")
        current_status = str(payload.get("status") or "")
        self.add_closeout_facts(payload)
        # The edge's effects validate against the task type's model. A task whose task_type is
        # not a registered type (empty or legacy, what `desk update --apply` migrates) validates
        # against TaskDoc, the model it was read with: a typed model's `task_type` literal could
        # not accept it (d4, instead of k5's TaskCodeDoc).
        model = self.registered_task_types().get(str(payload.get("task_type") or "")) or TaskDoc
        result = lifecycle.advance(self.root, payload, model)
        for key in ("closeout_evidence_verified", "pill_graduation_verified"):
            payload.pop(key, None)
        if result.progressed and payload.get("current_node") == lifecycle.COMPLETE:
            # The lifecycle graph would close the task. Do not persist it; the
            # only closing entry point is `deskops closeout commit`.
            self.logger.info(f"Task {task_id} reached the closure gate; deferring to closeout commit.")
            restored = {**payload, "current_node": current_node, "status": current_status}
            return doc_access.hydrate_task(restored), self._closure_required(task_id, restored)
        advanced_task = doc_access.hydrate_task(payload)
        if result.progressed:
            doc_access.write_doc(self.root, task_path, TaskDoc, payload)
        self.logger.info(f"Advanced task {task_id} to node {payload.get('current_node')}")
        return advanced_task, result

    @staticmethod
    def _closure_required(task_id: str, payload: dict[str, Any]) -> TransitionResult:
        node = str(payload.get("current_node") or "")
        status = str(payload.get("status") or "")
        message = (
            f"Task {task_id} closes with 'deskops closeout commit --task {task_id} "
            f"--run-dir <runs/subagents/dir>' or 'deskops closeout commit --task {task_id} "
            f"--no-run --reason <why>'."
        )
        return TransitionResult(node, status, False, True, message)

    # ---------------------------------------------------------------- paths
    def _task_path(self, task_id: str) -> Path:
        return self.desk_root / "tasks" / f"{task_id}.md"

    def _next_task_path(self, task_selector: str | None, board_path: Path) -> Path:
        if task_selector:
            return doc_access.resolve_artifact_selector(self.root, "artifact.task", self.desk_root / "tasks", task_selector)
        board_payload = doc_access.read_doc(board_path, BoardDoc)
        task_refs = list(board_payload.get("tasks") or [])
        if not task_refs:
            raise FileNotFoundError("No active tasks routed by desk/tasks/Board.md")
        if len(task_refs) > 1:
            raise ValueError("Multiple active tasks are routed; pass a task selector")
        return self.root / str(task_refs[0])

    def _board_pills(self, board_path: Path) -> list[str]:
        try:
            board_payload = doc_access.read_doc(board_path, BoardDoc)
        except Exception:
            return []
        return [str(pill) for pill in board_payload.get("pills") or []]

FILE:deskops/workflow/next_actions.py
from __future__ import annotations

from typing import Any

from deskops.lifecycle import COMPLETE
from deskops.lifecycle import LifecycleSpec
from deskops.lifecycle import SPEC_PATH
from deskops.lifecycle import Transition


def match_workflow_state(spec: LifecycleSpec, current_node: str) -> dict[str, Any]:
    """The state of ``deskops/spec/workflows/task_lifecycle.yaml`` whose ``current_node``
    is the task's; an empty node matches the first state."""
    node = current_node or ""
    for state in spec.states:
        if state.get("current_node") == node:
            return state
    if not node:
        return _first_state(spec)
    raise ValueError(f"No workflow state in {SPEC_PATH} matches current node '{current_node}'")


def render_workflow_mermaid(spec: LifecycleSpec, transitions: list[Transition]) -> str:
    """Mermaid of the lifecycle graph: one node per state, one arrow per transition of the
    desk's graph, labelled with its relation type and condition."""
    states = list(spec.states)
    by_node = {str(state.get("current_node")): str(state["id"]) for state in states}
    lines = ["flowchart TD"]
    for state in states:
        state_id = str(state["id"])
        label = str(state.get("phase") or state_id).replace('"', "'")
        lines.append(f'    {state_id}["{label}"]')
    for transition in transitions:
        source = by_node.get(transition.source, transition.source)
        target_node = COMPLETE if transition.terminal else transition.target
        target = by_node.get(target_node, target_node)
        label = transition.relation_type
        if transition.condition:
            label += f": {transition.condition}"
        lines.append(f'    {source} -->|"{label.replace(chr(34), chr(39))}"| {target}')
    return "\n".join(lines)


def _first_state(spec: LifecycleSpec) -> dict[str, Any]:
    if not spec.states:
        raise ValueError(f"Workflow spec has no states: {SPEC_PATH}")
    return spec.states[0]

FILE:deskops/cli/commands/desk.py
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from deskops import doc_io
from deskops.workspace import ensure_target_directory
from deskops.workspace import inspect_desk
from deskops.workspace import migrate_desk
from deskops.workspace import migrate_task_types
from deskops.workspace import apply_desk_includes
from deskops.workspace import pending_local_task_type_models
from deskops.workspace import pending_task_type_migration
from deskops.workspace import pending_desk_includes
from deskops.workspace import register_local_task_type_models
from deskops.workspace import seed_desk
from deskops.bootstrap import SLDBBootstrap, MODEL_REFS
from deskops.errors import DeskopsEnvironmentError
from deskops.paths import package_pythonpath
import deskops.models as models

#: The deskops FAQ model used to be registered with the same name sldb uses for its
#: own model. sldb federates models by name, so the old name must be migrated.
LEGACY_FAQ_MODEL = "FAQDoc"
LEGACY_FAQ_MODEL_REF = "deskops.models:FAQDoc"
FAQ_MODEL = "DeskFAQDoc"
FAQ_MODEL_REF = "deskops.models:DeskFAQDoc"


def legacy_faq_model_pending(entries: dict[str, Any]) -> bool:
    """Whether a store still registers the old deskops FAQ model name."""
    entry = entries.get(LEGACY_FAQ_MODEL)
    return entry is not None and getattr(entry, "model_ref", None) == LEGACY_FAQ_MODEL_REF


def moved_model_contracts(root: Path, entries: dict[str, Any]) -> list[str]:
    """Registered deskops models whose store contract no longer matches this checkout."""
    from sldb.store.hashing import hash_model_contract
    from sldb.store.io import load_models_index

    moved: list[str] = []
    for name, entry in sorted(entries.items()):
        model_ref = getattr(entry, "model_ref", "") or ""
        model_type = getattr(models, name, None)
        models_index = getattr(entry, "models_index", None)
        if not model_ref.startswith("deskops.models:") or model_type is None or not models_index:
            continue
        try:
            stored = load_models_index(root / models_index).contract_hash
        except Exception:
            continue
        if stored != hash_model_contract(model_type):
            moved.append(name)
    return moved


def migrate_legacy_faq_model(root: Path, *, pythonpath: str | None = None) -> list[str]:
    """Move an existing store from `FAQDoc` to `DeskFAQDoc`, keeping its documents.

    sldb exposes no model rename, so this registers the new name, retracks every
    document the old model owns, and removes the old entry with its document
    records. The Markdown files are never touched, so they stay byte-identical.
    """
    from sldb.store.io import load_documents_index
    from sldb.store.io import load_models_index

    store_dir = root / ".sldb"
    pythonpath = pythonpath or package_pythonpath()
    bootstrap = SLDBBootstrap()
    entries = bootstrap._registered_model_entries(store_dir)
    if not legacy_faq_model_pending(entries):
        return []

    changes: list[str] = []
    if FAQ_MODEL not in entries:
        doc_io.register_model(root, FAQ_MODEL_REF, pythonpath=pythonpath)
        changes.append(f"registered {FAQ_MODEL}")

    # The old class no longer exists, so its documents are read from the indexes
    # instead of resolving the model reference.
    legacy_entry = entries[LEGACY_FAQ_MODEL]
    legacy_index = load_models_index(root / legacy_entry.models_index)
    old_documents = load_documents_index(root / legacy_index.documents_index).documents
    tracked: set[str] = set()
    new_entry = bootstrap._registered_model_entries(store_dir).get(FAQ_MODEL)
    if new_entry is not None:
        new_index = load_models_index(root / new_entry.models_index)
        tracked = {document.name for document in load_documents_index(root / new_index.documents_index).documents}
    for document in old_documents:
        if document.name in tracked:
            continue
        doc_io.track(root, document.path, FAQ_MODEL, name=document.name, pythonpath=pythonpath)
        changes.append(f"tracked {document.name} as {FAQ_MODEL}")

    doc_io.remove_model_from(
        root, LEGACY_FAQ_MODEL, pythonpath=pythonpath, untrack_documents=True
    )
    changes.append(f"removed {LEGACY_FAQ_MODEL}")
    return changes


class DeskCLI:
    """Handle desk workspace scaffolding and rituals."""

    def run(self, args: Any) -> int:
        if args.desk_command == "install":
            return self.install(args)
        if args.desk_command == "migrate":
            return self.migrate(args)
        if args.desk_command == "replace":
            return self.replace(args)
        if args.desk_command == "update":
            return self.update(args)
        return 1

    def replace(self, args: Any) -> int:
        from deskops.services.replace import replace_text

        result = replace_text(
            Path(args.root),
            args.path,
            args.old,
            args.new,
            count=args.count,
        )
        print(f"Replaced {result.replacements} occurrence(s) in {result.path}")
        return 0

    def install(self, args: Any) -> int:
        target_path = Path(args.path).resolve()
        ok, error = ensure_target_directory(target_path)
        if not ok:
            print(error)
            return 1

        desk_dir = target_path / "desk"
        print(f"Scaffolding local desk at {desk_dir}...")
        result = seed_desk(target_path)
        for path in result.created_paths:
            print(f"Wrote {path}")
        for path in result.rewritten_paths:
            print(f"Rewrote {path}")

        if (target_path / ".sldb").exists():
            from deskops.lifecycle import write_lifecycle_graph

            for change in write_lifecycle_graph(target_path):
                print(f"Lifecycle graph: {change}")
        else:
            print("No .sldb store yet: run 'deskops init' to create it and the lifecycle graph that 'deskops advance' reads.")
        print("Scaffold complete.")
        print("Register the repo separately with 'deskops repo register ...' when you are ready.")
        return 0

    def migrate(self, args: Any) -> int:
        target_path = Path(args.root).resolve()
        ok, error = ensure_target_directory(target_path)
        if not ok:
            print(error)
            return 1

        result = migrate_desk(target_path)
        print(f"Desk migration report for {target_path}:")

        print("Adopted:")
        if result.adopted:
            for item in result.adopted:
                print(f"- {item}")
        else:
            print("- none")

        print("Preserved:")
        if result.preserved:
            for item in result.preserved:
                print(f"- {item}")
        else:
            print("- none")

        print("Still manual:")
        if result.still_manual:
            for item in result.still_manual:
                print(f"- {item}")
        else:
            print("- none")

        return 0

    def update(self, args: Any) -> int:
        root = Path(args.root).resolve()
        apply = getattr(args, "apply", False)

        desk_dir = root / "desk"
        store_dir = root / ".sldb"

        from deskops import lifecycle

        inspection = inspect_desk(root)

        missing_desk_files: list[str] = []
        if inspection.classification == "absent":
            missing_desk_files.append("desk/")
        elif desk_dir.exists():
            if not (desk_dir / "tasks" / "Board.md").exists():
                missing_desk_files.append("desk/tasks/Board.md")
            if not (desk_dir / "drawer").exists():
                missing_desk_files.append("desk/drawer/")
            if not (desk_dir / "reviews").exists():
                missing_desk_files.append("desk/reviews/")
            if not (desk_dir / "rituals" / "phase.md").exists():
                missing_desk_files.append("desk/rituals/phase.md")
            if not (desk_dir / "runtimes" / "runtime-pi-deepseek-flash.md").exists():
                missing_desk_files.append("desk/runtimes/runtime-pi-deepseek-flash.md")

        # The lifecycle graph's documents are managed seeds: a desk's copy that differs from the
        # package's is rewritten. A missing one is written with the rest of the scaffold.
        scaffold_plan = seed_desk(root, apply=False, restore_managed=True) if desk_dir.exists() else None
        lifecycle_rewrites = (
            [path.relative_to(root).as_posix() for path in scaffold_plan.rewritten_paths] if scaffold_plan else []
        )
        lifecycle_missing = bool(scaffold_plan) and any(
            path.relative_to(root).as_posix().startswith("desk/lifecycle/") for path in scaffold_plan.created_paths
        )

        bootstrap = SLDBBootstrap()
        registered_entries: dict[str, Any] = {}
        if store_dir.exists():
            try:
                registered_entries = bootstrap._registered_model_entries(store_dir)
            except Exception:
                pass

        legacy_faq_pending = legacy_faq_model_pending(registered_entries)
        if legacy_faq_pending and apply:
            print(f"Migrating the deskops FAQ model from {LEGACY_FAQ_MODEL} to {FAQ_MODEL}...")
            try:
                for change in migrate_legacy_faq_model(root):
                    print(f"- {change}")
                registered_entries = bootstrap._registered_model_entries(store_dir)
            except Exception as exc:
                print(f"Error: {exc}")
                return 1
            legacy_faq_pending = False

        moved_contracts = (
            moved_model_contracts(root, registered_entries) if store_dir.exists() else []
        )
        if moved_contracts and apply:
            pythonpath = package_pythonpath()
            for model_name in moved_contracts:
                print(f"Updating the {model_name} contract...")
                result = subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "sldb",
                        "models",
                        "update",
                        model_name,
                        "--store",
                        str(store_dir),
                        "--pythonpath",
                        pythonpath,
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if result.returncode != 0:
                    detail = result.stderr.strip() or result.stdout.strip()
                    print(f"Error: could not update the {model_name} contract: {detail}")
                    return 1
                print(f"Updated {model_name} contract.")
            registered_entries = bootstrap._registered_model_entries(store_dir)
            moved_contracts = moved_model_contracts(root, registered_entries)

        unregistered_models: list[str] = []
        copied_models: list[str] = []
        # A non-editable install has no owner store to inherit from; its directly
        # registered models are the expected state, not copies to convert.
        owner_store = bootstrap._deskops_owner_store()
        if owner_store is not None and store_dir.exists() and store_dir.resolve() == owner_store.resolve():
            # The owner store registers the deskops models directly; that is what
            # the other stores link to, not a copy of it.
            owner_store = None
        for model_name, model_ref in MODEL_REFS.items():
            entry = registered_entries.get(model_name)
            if entry is None:
                unregistered_models.append(model_name)
            elif (
                owner_store is not None
                and not getattr(entry, "origin", None)
                and getattr(entry, "model_ref", None) == model_ref
            ):
                copied_models.append(model_name)

        invalid_docs: list[str] = []
        missing_docs: list[str] = []
        missing_store = not store_dir.exists()
        if not missing_store:
            result = subprocess.run(
                [sys.executable, "-m", "sldb", "stores", "check", "--store", str(store_dir), "--format", "json"],
                capture_output=True,
                text=True,
                check=False,
            )
            payload = None
            if result.stdout and result.stdout.strip():
                try:
                    payload = json.loads(result.stdout)
                except json.JSONDecodeError as exc:
                    raise DeskopsEnvironmentError(
                        f"Could not parse 'sldb stores check' output for {store_dir}: {exc}"
                    ) from exc
            if payload is None:
                if result.returncode != 0:
                    raise DeskopsEnvironmentError(
                        f"'sldb stores check' failed for {store_dir} with exit code {result.returncode}"
                    )
                raise DeskopsEnvironmentError(
                    f"'sldb stores check' produced no JSON output for {store_dir}"
                )
            for model in payload.get("models", []):
                for doc in model.get("documents", []):
                    doc_path = doc.get("path")
                    if not doc_path:
                        continue
                    if doc.get("note") not in ("ok",):
                        invalid_docs.append(f"{doc_path} ({doc.get('note')})")
                        if doc.get("note") == "missing":
                            missing_docs.append(doc.get("name") or Path(doc_path).stem)

        # The desk documents the package's declared includes name and the store does not
        # track yet, each with its declared model (deskops/data/desk_declaration.yaml).
        untracked_docs = pending_desk_includes(root) if desk_dir.exists() else []

        pending_local_types = pending_local_task_type_models(root)
        pending_migration = pending_task_type_migration(root)

        if not lifecycle_rewrites and not legacy_faq_pending and not missing_store and not missing_desk_files and not unregistered_models and not copied_models and not untracked_docs and not invalid_docs and not moved_contracts and not pending_local_types and not pending_migration:
            print("Desk is up to date.")
            return 0

        print("Desk divergence report:")
        if missing_store:
            print("- Missing store: .sldb")
        if legacy_faq_pending:
            print(
                f"- Legacy FAQ model: {LEGACY_FAQ_MODEL} ({LEGACY_FAQ_MODEL_REF}) should be {FAQ_MODEL}."
            )
        if moved_contracts:
            print(f"- Moved model contracts: {', '.join(moved_contracts)}")
        if lifecycle_rewrites:
            print(f"- Lifecycle documents to rewrite: {', '.join(lifecycle_rewrites)}")
        if missing_desk_files:
            print(f"- Missing desk structure: {', '.join(missing_desk_files)}")
        if unregistered_models:
            print(f"- Unregistered models: {', '.join(unregistered_models)}")
        if copied_models:
            print(f"- Copied deskops models: {', '.join(copied_models)}")
        if untracked_docs:
            print(f"- Untracked desk documents: {', '.join(path for _model, path in untracked_docs)}")
        if pending_local_types:
            print(f"- Unregistered desk-local task types: {', '.join(pending_local_types)}")
        if pending_migration:
            print(f"- Pending task type migration: {len(pending_migration)} task(s)")
        if invalid_docs:
            print(f"- Stale document hashes: {', '.join(invalid_docs)}")

        if not apply:
            print("\nRun with --apply to repair these issues.")
            return 1

        print("\nApplying repairs...")

        if missing_desk_files or lifecycle_rewrites or lifecycle_missing:
            scaffold = seed_desk(root, restore_managed=True)
            if missing_desk_files:
                print("Scaffolded missing desk structure.")
            for change in lifecycle.seed_changes(root, scaffold):
                print(f"Lifecycle graph: {change}")

        if unregistered_models or copied_models:
            bootstrap.init_local_store(root)
            print("Registered missing models and converted copied deskops models.")

        try:
            for change in register_local_task_type_models(root):
                print(f"- {change}")
        except Exception as exc:
            print(f"Error: {exc}")
            return 1
        for change in migrate_task_types(root):
            print(f"- {change}")

        # Recomputed: the scaffold may have written declared documents (the lifecycle graph).
        untracked_docs = pending_desk_includes(root) if desk_dir.exists() and store_dir.exists() else []
        if untracked_docs:
            declared_models = {path: model_name for model_name, path in untracked_docs}
            try:
                tracked_paths = apply_desk_includes(root)
            except Exception as exc:
                print(f"Error: could not track the declared desk documents: {exc}")
                return 1
            for path in tracked_paths:
                model_name = declared_models.get(path, "its declared model")
                line = lifecycle.tracked_line(model_name, path)
                print(f"Lifecycle graph: {line}" if line else f"Tracked {path} as {model_name}.")

        if missing_docs:
            # A tracked document whose file is gone must be untracked, not
            # re-indexed: the store would keep describing something that is not there.
            pythonpath = package_pythonpath()
            for name in missing_docs:
                try:
                    doc_io.untrack(root, name, pythonpath=pythonpath)
                    print(f"Untracked {name}: its file is gone.")
                except Exception as e:
                    print(f"Failed to untrack {name}: {e}")

        if invalid_docs:
            pythonpath = package_pythonpath()
            doc_io.update_store_indexes_in(root, pythonpath=pythonpath, wait=False)
            print("Updated store derived indexes.")

        return 0

FILE:docs/workflow-policy-reference.md
---
atoms:
- id: atom-cheap-zero-context-reviews-test-the-brief-recursively
  role: documents
- id: atom-docs-are-human-facing-atom-materializations
  role: documents
- id: atom-phase-gates-prevent-agent-skipping
  role: documents
- id: atom-code-changes-close-with-tests-and-commit
  role: documents
- id: atom-available-tasks-are-board-routed-work
  role: documents
- id: atom-drawers-feed-tasks-through-promotion
  role: documents
- id: atom-pills-carry-transitional-task-knowledge
  role: documents
- id: atom-pills-are-reusable-across-tasks
  role: documents
- id: atom-pills-end-as-atoms-docs-or-deletion
  role: documents
- id: atom-phases-are-dependency-layers-of-tasks
  role: documents
- id: atom-phase-closeout-reconciles-pills-and-next-work
  role: documents
- id: atom-tasks-enable-zero-context-subagents
  role: documents
- id: atom-task-board-phases
  role: documents
- id: atom-closeout-evidence-is-declared-at-task-creation-and-verified-exactly
  role: documents
---
# Workflow Policy Reference

Source atoms are declared in the YAML frontmatter.

This reference summarizes the current workflow policy used by `deskops`.

> **No task is complete without the closeout evidence it declared at creation and its own closing commit. No phase is complete without integration validation and pill reconciliation.**

## Quick Links

- [Task Management](../desk/tasks/Board.md) - Active tasks
- [Pills Reference](../desk/contexts/pills.md) - Context pill format
- [Deferred Work](../desk/drawer/README.md) - Waiting items
- [Context Review Ritual](../desk/rituals/context-review.md) - Cheap recursive brief comprehension
- [Phase Ritual](../desk/rituals/phase.md) - Dependency-layer execution and closeout

---

## Core Model

### Tasks

A task is the atomic workflow unit.

- One coherent deliverable.
- May depend on other tasks.
- Executes in a fresh subagent context.
- Declares how it closes by choosing a task type (`deskops add task --task-type`); the type declares its closeout evidence and its activation receipts, and closes only after exactly that evidence verifies, with its own atomic closing commit. `--evidence` only adds kinds to the type's floor, never removes one the type requires.

#### Task types

A task type is a model: a `TaskDoc` subclass registered in the store. `model <= <Tipo>` names the type's family (including its subtypes); a subtype inherits the gates of its ancestors and can only add, never remove.

| Type | Extends | Activation receipts | Closeout evidence |
|---|---|---|---|
| `task.code` | `TaskDoc` | `preflight` + `bundle` | `tests` + `commit` + `atom\|materialization` |
| `task.docs` | `TaskDoc` | `preflight` | `commit` + `document` |
| `task.debug` | `TaskDoc` | `preflight` + `reproduction` | `tests` + `commit` + `atom\|materialization` |
| `task.refactor` | `task.code` | `preflight` + `bundle` + `goldens` | `task.code` + `goldens` |
| `task.decision` | `TaskDoc` | `owner` | `commit` + `document` |
| `task.aggregate` | `TaskDoc` | (never executes; activates when children close) | `children` + `commit` |
| `task.external` | `TaskDoc` | `preflight` | `external` (URL) |

`atom|materialization` is one gate with two alternatives. `commit` means a commit reachable from `HEAD`. A desk adds its own subtypes in `desk/models/*.py`; `deskops desk update --apply` registers them and migrates legacy `task_type` strings (`code`/`implementation`/`test` → `task.code`; `docs`/`spec`/`design` → `task.docs`; `external` → `task.external`; empty → `task.code`).

### Task lifecycle graph

A task moves through the desk's lifecycle graph, which lives in the desk's sldb store: every state is a tracked ritual (`RitualDoc:ritual-execution`, `ritual-testing`, `ritual-closeout`) and every transition is a `RelationDoc` under `desk/lifecycle/`, typed by a `RelationTypeDoc` named by the verb (`task_activates`, `task_hands_to_closeout`, `task_completes`). Each `RelationDoc` declares the whole transition: its `condition` (an sldb `--where` predicate over the task, such as `nonempty(validation)`) and its effects in `attributes`, following sldb's transition convention (GO09): `sets` names the task fields the transition writes (`status: active`, `ready_for_testing`, `closed`) and `terminal: true` marks the transition that closes the task (`task_completes`).

`deskops advance task` asks sldb which edges leaving the task's current node hold (`sldb.api.edges_holding`), takes that edge, applies its effects with `sldb.api.apply_effects` (validated against the task type's model), sets `current_node: complete` when the edge is terminal and appends the relation type to the task's `history`. One edge leaves each ritual, so nothing depends on the order sldb returns edges in. A blocked task stays where it is with the gate named. The terminal transition is never persisted by `advance`: the only closing entry point is `deskops closeout commit`. `deskops next` reads only the states of `deskops/spec/workflows/task_lifecycle.yaml` (ritual, next actions, `advance_when`); `deskops next --diagram` draws the desk's graph.

The six lifecycle documents are managed seeds of the deskops package (`deskops/data/desk_declaration.yaml`, templates in `deskops/data/lifecycle/`). `deskops init` and `deskops desk update --apply` write them, track them (with the three lifecycle rituals by their ids) and rewrite a desk's copy that differs from the package's: `desk update` lists it under `Lifecycle documents to rewrite`, `--apply` reports `Lifecycle graph: rewrote <path>`, and a second run changes nothing. Every other scaffold only creates what is missing. Changing a transition's effect means changing the `RelationDoc` through sldb; no YAML of deskops has to change, and the next `desk update --apply` restores the package's version.

### Phases

Tasks form an execution dependency graph.

A **phase** is one horizontal dependency layer in that graph:

- task prerequisites are already satisfied
- tasks are ready at the same time
- planned operational changes do not overlap
- tasks may run in parallel when the environment supports it

A phase has execution meaning, not business meaning. It is the workflow unit above individual tasks and below the whole board.

### Boards

The board is the routing surface for active work.

- It names the active tasks.
- It routes board-wide pills and rituals.
- Its current ready dependency layer is the current phase.

---

## Cheap Context Review and Fresh Subagents

Before promoting or executing a draft, plan, package or leaf, run the [context-review ritual](../desk/rituals/context-review.md). It tests the quality of the written question with a cheap reviewer: faithful reformulation, explicit ambiguities and a detailed dry-run of proposed readings, changes, validation and dependencies. The reviewer names intended commands without executing them or editing sources.

Supply the exact versioned brief and only necessary explicit references. Use a new ephemeral process for every attempt, without chat history, earlier reviews, oral fixes, persistent memory, automatic context/skills or tools. Record the chosen cheap provider/model/profile and reason; an expert cannot rescue a failed cheap comprehension gate. The ritual specifies the verified Pi isolation profile and per-node evidence layout.

The coordinator compares understanding with intent, corrects the written brief and recursively decomposes large nodes into children and explicit edges. Review root, packages, every leaf and dependency interfaces before selecting ready leaves. A root-only review does not cover descendants. Unresolved ambiguity blocks execution. Changed input or a changed dependency contract invalidates affected reviews; retries use a new process. Technical transport/quota failures are recorded separately from ambiguity.

Before Executor dispatch, preserve two distinct cheap roles: TaskDoc-only preflight (also saved in `runs/subagents/<run-dir>/preflight.md`) and cold-bundle coverage. The explicit execution bundle contains task, board-routed instructions/rituals, bound pills, linked atoms/files and validation targets. Neither review executes implementation. Expert council review, Executor work, independent Tester validation and human product approval remain separate gates; a word such as APTO or structural PASS grants none of them.

Evidence lives at `runs/subagents/<run-dir>/context-review/<node-id>/<bundle-sha256>/attempt-<n>/`: exact input bytes/hash, model/profile/selection, command/isolation, reformulation/ambiguities/dry-run, coordinator comparison and required edits. These are process records, not runtime enforcement or a new lifecycle state. Each active task then executes in its own fresh context, and an independent Tester validates implementation. The coordinator integrates outputs and enforces task/phase closeout. Do not carry unrelated tasks through one long-lived context.

---

## Pill Lifecycle

Pills are temporary execution aids, but they are not task-specific instances. Correction: pills are not 1:1 with tasks.

```text
Draft or refresh reusable pills -> bind pills to tasks opportunistically -> execute tasks ->
close tasks -> reconcile pills at phase closeout ->
keep / delete / merge / graduate to atoms -> prepare next phase pills
```

At phase closeout, classify touched pills explicitly:

- **still active** - keep for the next phase
- **stale** - delete or retire
- **redundant** - merge or remove duplicates
- **durable** - promote the stabilized residue into atoms first
- **materialization-worthy** - land resulting changes in code, specs, or docs as needed

Do not let durable knowledge remain pill-only once it stabilizes. Do not create a new pill just because a new task exists; create or update a pill only when there is a reusable atomic truth worth rebinding.

---

## Ritual Stack

### 1. Phase Ritual

Before starting a ready dependency layer:

```text
0. REVIEW   -> Review root/packages/leaves and edges cheaply; correct briefs and decompose.
1. IDENTIFY -> Select reviewed ready non-overlapping leaves.
2. BUNDLE   -> Confirm each task has its fresh context bundle.
3. EXECUTE  -> Run the execution ritual per task.
4. CLOSE    -> Require each task to close with its declared evidence and a task commit.
5. VALIDATE -> Run phase-level integration or end-to-end checks.
6. REGRESS  -> Fix interaction regressions.
7. RECONCILE-> Audit pills; delete, merge, or graduate them.
8. SURFACE  -> Capture newly discovered tasks and next-phase pills.
9. COMMIT   -> Make the phase-closing commit.
```

### 2. Task Execution Ritual

For each task in the phase:

```text
1. INIT   -> Confirm task scope, files, pills, validation, and declared closeout evidence.
2. REVIEW -> Accept cheap TaskDoc-only preflight, then separate cheap cold-bundle coverage.
3. BIND   -> Bind every relevant pill.
4. IMPLEMENT -> Make only task-scoped changes.
5. HANDOFF   -> Open an explicit testing handoff.
```

### 3. Task Testing Ritual

```text
1. CHECK  -> Confirm the intended contract and pill guardrails.
2. UPDATE -> Fix stale tests or add missing ones.
3. RUN    -> Execute the smallest relevant scope first.
4. EXPAND -> Run broader checks when shared behavior changed.
5. HANDOFF-> Open an explicit closeout handoff.
```

### 4. Task Closeout Ritual

```text
1. VERIFY -> Run `deskops closeout verify`: it checks exactly the declared evidence
             (declared X; found Y) and the pill guardrails.
2. CLEAN  -> Remove stale task-local context when appropriate.
3. DELETE -> Remove the resolved task from active routing.
4. COMMIT -> Close with `deskops closeout commit`; `closeout supersede` when the
             subject no longer exists, `closeout retire` for a pre-lifecycle resolution.
5. WAIT   -> If this was the last task in the phase, do not start the next phase until phase closeout passes.
```

---

## Commit Rules

### Task commit

Every closed task gets its own atomic commit, made by `deskops closeout commit`, `closeout supersede`, or `closeout retire`. The evidence it must show is the set declared when the task was created, not a fixed list.

### Phase commit

When all tasks in a phase are closed, make one separate descriptive phase commit for:

- integration fixes
- pill reconciliation
- captured next work
- board/phase bookkeeping

Do not hide unfinished task work inside a phase commit.

---

## Anti-Patterns

- Starting implementation before identifying the ready phase.
- Treating semantic milestones as phases when tasks still depend on each other.
- Running multiple unrelated tasks through one stale context.
- Closing tasks without the evidence they declared or without a dedicated task commit.
- Starting the next phase after isolated green task tests without integration validation.
- Carrying stale or overlapping pills forward because each task passed independently.
- Leaving durable rules only in pills instead of promoting them into atoms.
- Skipping newly discovered task capture at phase closeout.

FILE:CHANGELOG.md
# Changelog

All notable changes to deskops are recorded here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Entries cover the unreleased changes since tag `v-stable-2026.08.29`.

## [Unreleased]

### Added

- Task types as models with a hierarchy (`deskops/models/task_types.py`): `TaskCodeDoc` (`task.code`), `TaskDocsDoc` (`task.docs`), `TaskDebugDoc` (`task.debug`), `TaskRefactorDoc` (`task.refactor`, extends `TaskCodeDoc`), `TaskDecisionDoc` (`task.decision`), `TaskAggregateDoc` (`task.aggregate`) and `TaskExternalDoc` (`task.external`). Each fixes `task_type` with a `Literal` default and declares `__closeout_evidence__` and `__activation_receipts__`; `TaskDoc` declares `__contract__`.
- `deskops add task --task-type` accepts only registered types (and lists them on an unknown name); without `--task-type` the type defaults to `task.code` with an envelope note. Tasks are stored under their type model, so `model <= TaskCodeDoc` names the family.
- A desk can add its own subtypes in `desk/models/*.py` (DC7); `deskops desk update --apply` registers them and migrates legacy `task_type` strings onto their canonical type (idempotent, with a per-task report).
- `ReviewDoc` (`deskops/models/review.py`): a review receipt for preflight, bundle, reproduction, goldens, or owner checks. `kind` and `verdict` are closed vocabularies; `subject` holds a `doc:<Model>:<id>` anchor (or `subject_ref` names a plan node), and `verdict: accepted|rejected` requires a reason and `disposed_by`. The model declares `subject` in `__doc_anchors__` and leaves `__references__` alone until sldb GO07 (`G_SLDB_ANCHORS`).
- `deskops init` and `deskops desk update` create `desk/reviews/`. The `review` subject is registered for `deskops edit review`, which refuses `verdict`, `reason`, `disposed_at`, and `disposed_by`: the verdict is written by `deskops review dispose` (GC03), and a new review is a new document.
- `deskops review` replaces the two governed `context_review.py` scripts with a CLI command (`node`, `preflight`, `bundle`, `status`, `dispose`). Each run writes the ritual evidence under `runs/subagents/<run>/context-review/<key>/<sha>/attempt-N/` and a `ReviewDoc` receipt; the default engine is the `runtime-pi-deepseek-flash` profile seeded idempotently under `desk/runtimes/` (`RuntimeProfileDoc` gains an optional `system_prompt`). `--max-attempts` (default 2) caps good attempts per key, `--force --reason` re-reviews an unchanged input, and transport failures leave `technical_ok: false` with `verdict: incomplete` / `reason: technical`.

### Changed

- The desk a repository gets is data the sldb scaffold writes (CC36, DP3): the templates `deskops init` used to carry as strings in `workspace.py` (`config.json`, `pills.md`, the four lifecycle rituals, `drawer/README.md`, `atoms/tag-namespaces.yaml`) live in `deskops/data/templates/`, and `deskops/data/desk_declaration.yaml` declares the desk's `folders` (the artifact directories `ensure_workspace` created among them), its `if_missing` seeds (the Board and the `runtime-pi-deepseek-flash` profile as `document` seeds rendered by their model) and `include` rules `{model, glob}` per desk folder. `workspace.seed_desk` renders the seeds for the desk's name (`{desk_name}`, the only placeholder) and passes them in process to `sldb.api.scaffold_store`; `scaffold_desk`, `_write_if_missing`, the `*_template` functions and `guess_model_for_path` are gone, `_write_or_patch_config` only patches an existing file, and `desk update --apply` tracks desk documents through the declared includes (`sldb.api.stores.apply_declaration.apply_includes`) instead of guessing a model by path. What `init` and `desk update --apply` write is byte for byte what they wrote before (`tests/fixtures/golden/scaffold/`, `tests/test_scaffold_golden.py`); `init` now also creates `desk/materializations/`, `desk/steps/`, `desk/registry/` and `desk/faq/`.
- Document invariants are validators of their model (DK6), so sldb applies them on every write (`deskops`, `sldb fields update`, `sldb docs update`): `AtomDoc` and `ProtoAtomDoc` check the slug convention of their id, the `namespace:value` form of each tag and the domain path of each `domain:` tag, `ProtoAtomDoc` takes one `domain:` tag, `CrossroadDoc` checks its path and that its id names it, and `TaskDoc` refuses a blank title. The same checks are gone from `domain_tree.py`, `atom_tags.py`, `services/atoms.py` and `specs/compiler.py`; what needs another document or the file tree (written parents, file names, the tag namespace registry, `typed_as` targets, provenance) stays where it was. Services report the validator's own line (`deskops.models.validation`), and `atoms validate` lists it next to the other findings of the document. `atoms crossroad`, `proto` and `type` write through `doc_access` again (they called facade names CC30 removed) (CC38).
- `deskops/operations.py` is a facade: each method delegates one call to a service, to the new `deskops/doc_access.py` (document reads, writes and selector resolution, as module functions over `root`) or to `deskops.lifecycle`. Task logic lives in `services/tasks.py`, closeout verification in `services/closure.py`, and no service constructs `DeskopsOperations`. The per-artifact YAML specs (`spec/artifacts/`, `spec/fields/`, `SpecRegistry`, `specs/mermaid.py`) are gone: each model declares `__artifact__` (`id_pattern`, `status_default`, `tags`), `compile_task_spec` is the one task normalization, and `task_lifecycle.yaml` is loaded only by `lifecycle.load_lifecycle_spec`. CLI grammar and output are unchanged (CC30).
- The desk graph is configuration over sldb: `deskops/graph/desk_graph.py` declares the desk's document surfaces, file rules, reference fields, section and line mentions, and which documents are history; sldb's `ProjectGraph` (`sldb.api.edges.project_graph`, branch `wt/closeout-graph-sldb`) reads the nodes, the store's cached edge index and the declarations. `deskops/graph/extract_docs.py`, `extract_edges.py` and `extract_sources.py` are removed; `graph build`, `graph missing`, atom traces and the closeout gate read the same graph (node, edge and finding output unchanged).
- `build_closeout_graph_context` returns a `CloseoutGraph` over `ProjectGraph`: tracked documents and schema edges come from one read of the store index, and only the materializations and the documents the gate asks about are read.
- `lifecycle.transitions_from` reads the desk's own store (`include_linked=False`), not the index composed with every linked store.
- The task lifecycle is a graph with effects, declared in the desk (CC31, GO09): each `RelationDoc` under `desk/lifecycle/` carries `attributes: {sets: {status: <value>}, terminal: <bool>}` (`active`, `ready_for_testing`, `closed`; `terminal: true` on `task_completes`), and `deskops advance` takes the edge `sldb.api.edges_holding` says holds, applies its effects with `sldb.api.apply_effects` (validated against the task type's model, `TaskDoc` when the task's type is not a registered one), sets `current_node: complete` when the edge is terminal and appends the relation type to `history`; the terminal transition is still not persisted from `advance` (the closing gate is `closeout commit`). The six lifecycle documents (three `RelationTypeDoc`, three `RelationDoc`) are `managed` seeds of `deskops/data/desk_declaration.yaml` with templates in `deskops/data/lifecycle/` (`file:` seeds are now relative to `deskops/data/`): `deskops init` and `deskops desk update --apply` write them, rewrite a desk's copy that differs (`desk update` lists it as `Lifecycle documents to rewrite`, `--apply` reports `Lifecycle graph: rewrote ...`) and track them through the declared includes, together with the three lifecycle rituals by their ids; any other scaffold only creates what is missing. Gone: `Transition.sets_status`/`terminal` from the YAML, `LifecycleSpec.effect`, the `transitions` key of `task_lifecycle.yaml` (only `entry_node` and `states` remain, read by `deskops next`), `ensure_lifecycle_graph` (now `write_lifecycle_graph`), the legacy ritual migration and `deskops/lifecycle_migration.py` (no desk needs them). `deskops next --diagram` draws the desk's graph.
- `DeskopsOperations._read_doc` parses a document once per text for the whole process, so a reader that builds a new `DeskView` per request (graph_ui's `serve.py`) does not re-parse unchanged documents.
- `deskops view board` on the deskops desk: ~30 s cold / ~11 s warm before, ~1.7 s cold / ~0.4 s warm after (new `DeskView` per call). `tests/test_closeout_gates.py` compares the new path with the old extractors, frozen in `tests/graph_oracle_v1/`.
- `deskops advance task --to` is removed (breaking): a task moves only through a lifecycle transition whose condition holds, and a blocked task stays where it is with the gate named. Close with `deskops closeout commit` (or `closeout supersede`/`closeout retire`), never by forcing a node.
- `edit task` refuses `status`, `current_node`, `history`, `task_type` and `closeout_evidence` with exit 1 and names the command that writes each field. Ordinary fields such as `goal` stay editable. `force`-style flags that skip a gate are not offered (D2).
- Closeout evidence is read from the task's type, not written into the task (`TASK_TYPE_EVIDENCE` and `evidence_for_task_type` are gone). `--evidence` is a floor: it can only add kinds to the type's, never remove one. A task's own non-empty `closeout_evidence` still overrides the type.
- `closeout verify` names `children` and `goldens` (declared by `task.aggregate` and `task.refactor`) as not yet verifiable.
- `tests/fixtures/model_contract_hashes.json` records the new `RelationDoc` contract from sldb GO09 (`attributes.sets`/`terminal`; sldb 33b3c7a0, closeout d39bf915); the deskops store was migrated with `sldb stores update` in 09b5075c. The other desks are migrated by their own repos.

### Fixed

- `tests/test_cli_grammar.py` classifies the `review` noun (GC03) once, under `operational`, and fixes its `mutates` guards as the registry declares them (`review` and `review dispose` mutate, `review status` does not); the grammar test passes again.
- `tests/test_gitignore_policy.py` asserts the current `.sldb` layout policy: `.sldb/store.yaml` and `.sldb/core/` are tracked, `.sldb_cache/` is ignored, and nothing under `.sldb/runtime/` is tracked.

## [0.2.0] - Unreleased

### Added (rewrite plan F1–F6)

- Model contract snapshot (`tests/fixtures/model_contract_hashes.json`), CLI contract tests, and golden files for help, output, and graph.
- One selector resolution module (`deskops/desk_paths.py`) for every desk artifact lookup.
- Typed errors with fixed exit codes (1 domain, 2 usage, 3 unexpected) and `--debug` for tracebacks.
- Transactional document I/O (`deskops/doc_io.py`): a command writes all its documents and store records, or none.
- Services for drawer routing, closeout gates, tasks, atoms, and closure.
- `deskops drawer remove`, which refuses while an active task names the entry in `from_drawer` (`--force` skips the check).
- Command registry, one output renderer with a JSON error envelope, and `--root`/`--store` agreement checks.
- `scripts/migrate_desk_stores.py` to migrate every store that tracks deskops models (dry-run by default).
- CI running `pytest tests` on Python 3.13, and this changelog.

### Changed (rewrite plan F1–F6)

- `deskops closeout commit` is the only way to close a task; `advance` stops at closeout and points to it (breaking). The closure runs the full `closeout verify` gate.
- `init` links deskops models from the deskops store (federated) instead of copying them; bootstrap registers every deskops model.
- The graph reads sldb's edge index (`__reference_models__`, structuredLanguageDB >= 0.1.12) and one snapshot reader.
- TaskDoc declares its frontmatter explicitly; `pills`, `current_node`, and `atoms` are references, not containment.
- `inbox`, `status`, `atoms list`, and `atoms show` remain as deprecated aliases with a warning.
- The package runs outside an editable install: specs live in `deskops/spec/`, the FAQ ships as `deskops/data/faq.md`.
- `desk update --apply` writes the lifecycle graph.

### Removed (rewrite plan F1–F6)

- `deskops/graph/extract_coverage.py` (recovery issue points at c378d15).

### Fixed (rewrite plan F1–F6)

- Tasks written before the explicit TaskDoc frontmatter (no `tags:` key) validate again.
- Task selectors resolve tracked tasks whose file name predates `task-*`.
- Rewrites (`edit`, `advance`, `bind`) refuse instead of silently erasing headings or frontmatter keys the model does not declare.
- `edit` keeps text field values literal: multi-line text and values starting with `**` survive.
- The test suite no longer writes to the real `~/.sldb`.

### Added (desk-to-zero, 2026-10-18)

- `deskops issue close|list` closes an issue in any of the three status formats with a Resolution section (reason, refs) and keeps the file.
- `deskops closeout supersede` closes a task whose subject no longer exists (reason plus a resolvable ref); `deskops closeout retire` removes a task resolved before the ritual lifecycle (`Closeout-Mode: legacy-resolved`).
- `deskops repo remove` takes a repository out of the registry so it can be registered again under the right id.
- `deskops next --why`, and guidance from `deskops next` when the Board routes no task or several.
- `docs/operator-manual.md`, whose runnable examples the suite executes.
- Drift findings for invalid atom-reference roles, the legacy `related_atoms` field, and global policy restated inside tasks.

### Changed (desk-to-zero, 2026-10-18)

- Requires Python >=3.12 (Python 3.10 reaches end of life in October 2026; the whole suite moves to 3.12). CI runs the suite on 3.12 and 3.13. The test that kept the package importable on 3.10 and 3.11 is removed.
- Requires structuredLanguageDB>=0.1.13 (link replacement, broken-link detection, and the extraction fixes in sldb main).
- `closeout commit` folds the run index line into the closing commit; the tree stays clean.
- deskops' FAQ model is `DeskFAQDoc`; ritual steps are prose, not StepDoc references.
- `desk update --apply` archives legacy rituals RitualDoc cannot carry to `desk/drawer/rituals/legacy-*.md` and re-signs moved deskops model contracts.

### Fixed (desk-to-zero, 2026-10-18)

- `promote inbox-to-drawer-task` writes a TaskDoc; `closeout commit` accepts a directory in `--paths`; `edit` reaches drawer tasks and finds rituals by id; message delivery and ack work with desks that do not register the sender or themselves.

### Added

- Task lifecycle in the SLDB graph: rituals are states and gated relations are transitions.
- `deskops message send|list|read|ack` for cross-desk transport.
- `deskops closeout verify` with a strict all-of evidence gate.
- `deskops closeout commit --no-run --reason` to close without a subagent run.
- `deskops desk update` to reconcile a desk and its store.
- `deskops desk migrate` and `deskops doctor` findings for absent, empty, and legacy desks.
- `deskops repo whoami` and one canonical cross-repo identity resolution path.
- Verifiable cross-desk inbox delivery with a delivery result and `--ack`.
- Live Herdr agent inventory in `deskops runtime`, grouped by Herdr space.
- Supervised execution over Herdr.
- RoleDoc model, `desk/roles/` sources, and materialize/drift-check commands.
- MaterializationContractDoc model, spec, CLI surface, and reference-resolution validation.
- Atom validate and delete commands, plus split with provenance-safe rerouting and merge with reference reconciliation.
- Protoatoms, domain crossroads, and protoatom typing.
- Configurable atom folder axis by tag namespace.
- Declared graph edges derived from model containment and references.
- Per-project desk config and version contract with deterministic deep merge.
- Drift-check review loop and knowledge-surface findings.
- Graph snapshot and graph CLI commands.

### Changed

- Agent-facing inbox transport is renamed to the `message` command family (breaking).
- A drawer item becomes an active task only through `deskops add task --from-drawer`.
- Bootstrap and init drive SLDB in process instead of one subprocess per model.
- The store uses SLDB's per-document layout.
- Doctor excludes unmodeled desk surfaces from untracked findings and clarifies broken-tracking wording.
- Promotion and TaskDoc reads flatten structured source sections into task fields.

### Removed

- Direct drawer-to-active-task promotion command (breaking).
- The old `inbox` transport subcommands (breaking).
- The kgdb dependency: `graph build` validates and writes through `sldb.api.graph`; requires structuredLanguageDB >= 0.1.11.

### Fixed

- F0: the closeout commit `advance` makes contains only the closing task's paths; unrelated staged changes stay staged.
- F0: merge retargets whole tokens instead of substrings.
- F0: pytest collects only `tests/`.
- F0: ambiguous selectors are rejected instead of guessed.
- F0: the payload and flag drawer paths resolve the same way.
- F0: the graph ignores vendored trees.
- F0: closing a task amends HEAD only when HEAD's `Task-Id` trailer is that task.
- F0: doctor no longer crashes on desk-less roots.
- `graph missing` reports findings from archived records (`record: true`) as informational and exits 0 when only those remain.
- `desk update --apply` re-renders lifecycle rituals RitualDoc cannot read before tracking them.
- `closeout verify` no longer aborts on a multi-document YAML block in docs.
- `message` tracks a delivered note in the target repo's store with a relative path, and `--ack` re-signs it.
- Empty and whitespace-only selectors are rejected before any lookup.
- Graph commands import on Python 3.10/3.11 and report the real error.
- `from_drawer` is treated as provenance, not as a reference that must resolve.
- Edit keeps literal text fields and only guards deletion when the document is unreadable.
- Unreadable documents are no longer rewritten.
- Closeout commits the closure before deleting the task bundle.
- `init` scaffolds `desk/rituals/phase.md`, which the doctor requires.
- Tracked documents are written through the store, not under it.
- Repo registry supports `repo register --path`, tolerates model-entry shadowing, and reports actionable errors.
- Cross-repo identity resolution and inbox targeting precedence are unified.
- Doctor detects unregistered models and proposes a `desk update` repair.
- Optional-field and untrack paths are realigned with current SLDB.

FILE:instruccion
Cold-bundle de la tarea task-cc32-gates-de-activación-de-cada-tipo-de-tarea-como-ruledoc-produce-g-consumer: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Test de integración G_CONSUMER en tres pasos (sin recibos falla nombrando la cláusula; con preflight y bundle accepted e intactos activa; goal editado bloquea con anchor_state = changed)
- Tests por tipo: task.debug exige reproduction y no bundle; task.refactor suma goldens; subtipo task.code.cli de desk temporal hereda y una RuleDoc propia suma cláusula; depends_on abierta bloquea y el finding la nombra
- grep -rn __activation_receipts__ deskops/ vacío
- Copia del desk de deskops tras desk update --apply (segunda corrida sin cambios): sldb rules check sin --subject sin errores; sldb rules explain de la regla de task.code sobre una tarea activa devuelve el finding con su cláusula
- TMPDIR=/dev/shm pytest -q, uno a la vez: tests de los archivos tocados, test_task_types, test_lifecycle_*, test_closeout_gates, test_scaffold_golden, test_cli, test_output_goldens y test_cli_help_examples (sin --update-golden)
- deskops doctor y desk update --apply en los 6 desks con main y rama, cwd neutro (a13)
- wc -l antes y después por archivo tocado
- CHANGELOG y docs/workflow-policy-reference.md con la tabla de reglas por tipo

