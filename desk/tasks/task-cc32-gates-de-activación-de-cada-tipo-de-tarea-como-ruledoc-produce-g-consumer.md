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
- deskops/cli/commands/operations.py
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

PRECISIONES DEL COLD-BUNDLE (review-...-bundle-1, 2026-11-08):
c1 (goldens): manda b4. Los goldens de ayuda quedan idénticos. Los de salida también, salvo show_task.text y show_task.json, que solo cambian por la sección de findings. El Done When se corrigió en ese sentido.
c2 (GO07 disponible): GO07 (anclas doc:) entró en sldb con GO08 (gate G_GO08, satisfied: sldb 3af872e7, closeout 556408da), y el venv usa el main editable de sldb. sldb calcula anchor_state (src/sldb/api/anchors/, rules_on_write.py); el test no lo simula. El docstring y el comentario de deskops/models/review.py (:14 y :40-41, «Until GO07 exists ... stays inert») quedaron viejos: el worker los corrige sin cambiar el modelo. Si anchor_state no se resuelve sobre ReviewDoc.subject en el desk temporal, el worker para y avisa con la evidencia (hipótesis para sldb), sin suplirlo con Python.

PRECISIONES DE EJECUCIÓN (2026-11-08, coordinador del plan, a pedido del worker):
d1 (operations.py entra en files): para que show y next impriman los findings en texto se toca deskops/cli/commands/operations.py, solo en _format_task_detail y _print_next_action_report (unas 8 líneas). CC35a no toca ese archivo, así que no se cruza con su rebase.
d2 (anchor_state sin CC35a): en main sin CC35a, la vía de escritura de deskops (render + track, sin save_document_payload) no pinnea ReviewDoc.subject. Los recibos de deskops review + dispose quedan con anchor_state = lost y la regla no activa. Con sldb.api transaction.update el ancla se pinnea (intact), y editar goal da changed. Los tests escriben los recibos con sldb.api (b8). El informe lo lista como consecuencia: CC35a es prerrequisito operativo para que un recibo de deskops review active una tarea real. CC32 no cambia la vía de escritura (a1).
e1 (desvío aceptado por el coordinador de proyecto, 2026-11-08): la regla de task.refactor solo suma la cláusula de goldens y no repite all(depends_on: status = "closed"), porque TaskRefactorDoc <= TaskCodeDoc ya hereda esa cláusula de la regla de task.code (a5). b1 se lee para los tipos que no heredan otra regla. Entrega: wt/cc32 0896a2b1, verificado y sin integrar; el orden de integración es CC35a primero y CC32 después (G_CONSUMER y la nota a sldb van cuando los dos estén en main).

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

El test de integración G_CONSUMER pasa en sus tres pasos; task.debug exige reproduction y no bundle; task.refactor exige además goldens por herencia de task.code; un subtipo task.code.cli de un desk temporal hereda las reglas de task.code sin código y una RuleDoc propia suma una cláusula; una dependencia abierta bloquea y el finding la nombra; grep de __activation_receipts__ en deskops/ vacío; en una copia del desk de deskops tras desk update --apply, sldb rules check sin --subject sin errores y sldb rules explain de la regla de task.code sobre una tarea activa existente devuelve el finding con su cláusula; goldens de ayuda idénticos y de salida idénticos salvo show_task.text y show_task.json por la sección de findings (b4); CHANGELOG y docs/workflow-policy-reference.md con la tabla de reglas por tipo. La nota a sldb (G_CONSUMER) la envía el coordinador al integrar.
