---
sldb:
  by: agent
  at: '2026-11-09T19:48:40Z'
  authority: generated
  via: save_document_payload
id: task-cc37-cerrar-vías-de-escape-ninguna-escritura-deja-el-ciclo-de-vida-fuera-de-las-reglas
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
- deskops/models/
- deskops/data/rules/
- deskops/services/
- deskops/lifecycle.py
- deskops/cli/commands/desk.py
- tests/
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/deskops-como-config/dag.yaml
---

# CC37: Cerrar vías de escape - ninguna escritura deja el ciclo de vida fuera de las reglas

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo CC37 del plan desk/drawer/plans/deskops-como-config/dag.yaml rev 3, en PF2 (reglas), árbol T3.7. Depende de CC31, CC32 y CC38, los tres en main (CC32: squash 6afc78b0, closeout 2ce88abd). Gate: G_GO08, satisfied. GC06 de gates-por-tipo ya retiró advance --to y las ediciones de campos del ciclo de vida por edit task; este nodo cierra lo que queda.

## Goal

_Describe the concrete result this task must produce._

Ninguna vía de escritura deja una TaskDoc con un ciclo de vida inconsistente: un validador del modelo TaskDoc (DK6, mecanismo de CC38) exige que status, current_node, history y task_type sean coherentes con el grafo del ciclo de vida, y sldb lo aplica en toda escritura (fields update, docs update, /save, transacción). Las escrituras internas de deskops que cambian el ciclo de vida pasan solo por advance y closeout. El inventario de vías de escritura queda en el TaskDoc.

## Scope

_State what is in scope and what is out of scope._

En alcance: deskops/models/ (el validador de TaskDoc y la tabla del ciclo de vida que lee), deskops/data/rules/ (solo si una parte necesita otro documento), deskops/services/ y deskops/lifecycle.py (solo si una escritura interna de status/current_node queda fuera de advance o closeout; cambios mínimos), deskops/cli/commands/desk.py (que desk update reporte las tareas inconsistentes sin escribirlas, si hace falta), tests/ y CHANGELOG.md. Fuera: un campo «solo por transición» en sldb (DA6), las reglas de cierre (CC33), los selectores (CC35b), closeout resolved-by (en curso en otra rama) y la forma del desk.

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (dag.yaml rev 3, CC37). SCOPE: GC06 de gates-por-tipo (entra por G_GATES_FROZEN) ya retiró advance --to y hace que edit task rechace status, current_node, history, task_type y closeout_evidence (tests/test_cli_escape_hatches.py). Este nodo cubre lo que queda: (1) inventario, en el TaskDoc, de toda vía que escribe un TaskDoc (CLI de deskops, servicios internos, graph_ui, sldb fields update, sldb docs update, sldb serve /save) y cuál pasa por una transición; (2) consistencia del ciclo de vida como validador del modelo TaskDoc (DA6, DK6; mecanismo de CC38): status es el sets.status de la última arista que llevó a current_node (tabla derivada de los RelationDoc de CC31), el último elemento de history nombra current_node, y task_type coincide con el modelo del documento; sldb aplica el validador en toda escritura (roundtrip en sldb api/documents/payload_save_steps.py:62; GD24 lo prueba por ruta), así una escritura directa por sldb que deja una tarea inconsistente es rechazada con el mensaje del validador; si la tabla depende de RelationDocs, el validador la lee del paquete deskops, y lo que solo se puede ver entre documentos queda como RuleDoc; (3) las escrituras internas de deskops que cambian el ciclo de vida pasan solo por advance (apply_effects) y closeout commit, comprobado por grep; (4) no se pide a sldb un campo "solo por transición" (DA6): un estado consistente escrito sin transición es aceptable.

ACCEPTANCE: sldb fields update de status sobre una tarea en ritual-execution a closed es rechazado con el mensaje del validador de TaskDoc; sldb fields update de current_node sin status coherente es rechazado; sldb docs update y /save con el mismo payload inconsistente son rechazados; una tarea migrada de cada uno de los 6 desks (copia) pasa las reglas tras desk update --apply (o el desk update reporta las inconsistentes sin escribirlas); advance y closeout commit siguen funcionando (tests de lifecycle y closeout verdes); grep de escrituras de status/current_node fuera de lifecycle.advance y closure en deskops/ vacío (patrón fijado en el TaskDoc); inventario en el TaskDoc; tests/test_cli_escape_hatches.py verde; CHANGELOG.

OUTPUT_SCOPE: deskops/models/, deskops/data/rules/, deskops/services/, deskops/lifecycle.py, deskops/cli/commands/desk.py, tests/, CHANGELOG.md

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

PRECISIONES DE PROMOCIÓN (2026-11-09, coordinador del plan; base origin/main 5d9e2338):
a1 (tabla del ciclo de vida): las RelationDoc de deskops/data/lifecycle/ (CC31) fijan sets.status por arista: execution-task_activates → status active (destino ritual-testing); testing-task_hands_to_closeout → ready_for_testing (destino ritual-closeout); closeout-task_completes → closed y terminal (destino complete). El validador lee esa tabla del paquete deskops (los archivos de deskops/data/lifecycle/, no el store), como pide el scope. Un desk que cambie su copia managed de esas RelationDoc la ve restaurada por desk update --apply (CC31), así que el paquete es la fuente.
a2 (estados válidos): una TaskDoc es coherente si cumple una de estas condiciones:
(i) estado de entrada: current_node = entry_node (ritual-execution, de task_lifecycle.yaml), history vacía y status en el conjunto de entrada, que es status_default «draft» (models/task.py:33) más los status que hoy escriben add task y promote (el worker los inventaría; por ejemplo «active» si compile_task_spec lo pone, specs/compiler.py:131);
(ii) tras transiciones: el último elemento de history es el relation_type de la arista cuyo destino es current_node, y status es el sets.status de esa arista;
(iii) cerrada por closeout: status en {closed, superseded, resolved} con history que termina en el registro de cierre que escribe closure.py (superseded en :164; «resolved-by» lo agrega la rama wt/closeout-resolved-by, en curso; el validador acepta las dos formas: el conjunto de cierre es un dato del validador y se amplía con una línea);
(iv) task_type coincide con el modelo del documento: un TaskCodeDoc tiene task_type task.code, etc. TaskDoc genérico acepta task_type vacío o legacy (d4 de CC31).
Lo que no cumple ninguna es ValidationError con un mensaje que nombra el campo y el valor esperado.
a3 (inventario): en el informe y en el TaskDoc (vía disposición), cada vía que escribe un TaskDoc: CLI de deskops (add task, edit task, advance, closeout commit/supersede/retire/resolved-by, promote, desk update), servicios internos (grep de a5), graph_ui (UIs/graph_ui, solo lectura del código), sldb fields update, sldb docs update y sldb serve /save. Para cada una: si pasa por una transición, si la cubre el validador y con qué test.
a4 (pruebas por vía sldb): en una copia de un desk temporal, sldb fields update de status a closed sobre una tarea en ritual-execution es rechazado con el mensaje del validador; fields update de current_node sin status coherente, rechazado; sldb docs update y /save con el mismo payload inconsistente, rechazados. Si /save no es probable sin levantar un servidor, el worker usa la función de sldb que /save llama y lo explica.
a5 (grep de escrituras internas): patrón fijado. grep -rnE '\["(status|current_node)"\]\s*=|"(status|current_node)":' deskops/ filtrado a los payloads de TaskDoc. Cada aparición queda en lifecycle.advance, en closure (closeout) o en la creación (compile_task_spec, add task). Cualquier otra se lista con su razón o se corrige. En main hoy: lifecycle.py :288, :300 y :302; closure.py:163; specs/compiler.py :49, :69 y :131; services/tasks.py:313 (restored, no se escribe). El resto de los hits (message, repo, issues, desk_view, drawer, runtime) son de otros modelos.
a6 (los 6 desks): sobre copias, desk update --apply con la rama y cwd neutro (plantilla ~/proyectos/SLDB_1/coord2-ccconfig/cc35a/doctor6.sh). Toda tarea existente de los 6 desks pasa el validador, o desk update la reporta como inconsistente sin escribirla. El informe da la lista. En el desk de deskops hoy hay 5 tareas, todas draft en ritual-execution con history vacía: estado de entrada.
a7 (en paralelo): CC35b (selectores, wt/cc35b) toca services/ y doc_access; closeout resolved-by (wt/closeout-resolved-by) agrega un método a closure.py. Este nodo no toca doc_access ni la resolución. En services/ y closure.py, cambios mínimos y solo si a5 lo exige.
a8 (tests): un test por cada caso de a2 (válido e inválido) construyendo el modelo; los casos de a4 por vía sldb. Además, de a uno: test_cli_escape_hatches, test_lifecycle_*, test_closeout, test_activation_rules, test_model_validators y test_task_types; test_cli y test_output_goldens desde una copia en /dev/shm, sin --update-golden.

PRECISIONES DEL PREFLIGHT (review-...-preflight-2, 2026-11-09; el intento 1 fue un timeout técnico del modelo):
b1 (cómo lo aplica sldb, sin tocar sldb): el validador es un model_validator de pydantic en deskops/models (en TaskDoc o en su base), como los de CC38. sldb no se toca. En toda escritura (fields update, docs update, /save y la transacción), sldb hace render_checked y validate_model_input_roundtrip (sldb src/sldb/api/documents/payload_save_steps.py:55-70), que construye el modelo registrado del documento y por eso corre el validador. Las pruebas de a4 lo comprueban por cada vía.
b2 (status de entrada): el conjunto de entrada es {"draft"}, el status_default de TaskDoc (compile_task_spec, specs/compiler.py:49), más cada status que el inventario de a6 encuentre en tareas existentes de los 6 desks con current_node = entry_node e history vacía. El worker lo fija como constante en el validador y la lista en el informe con el desk y la tarea que la justifican. Con cualquier otro status en el estado de entrada, ValidationError.
b3 (RuleDoc): si las cuatro condiciones de a2 se deciden con el payload de la tarea y la tabla del paquete, no hay RuleDoc y deskops/data/rules/ no se toca. Si alguna necesita otro documento, va como RuleDoc on_write severity error en deskops/data/rules/, con subject «model <= TaskDoc», y el informe explica por qué no cabe en el validador. Lo esperado es que no haga falta ninguna.
b4 (dónde queda el inventario de a3): en el informe del worker, en una tabla «vía | pasa por transición | la cubre el validador | test». El coordinador del plan lo copia al TaskDoc al cerrar, con deskops edit task. El worker no edita el TaskDoc.
b5 (estado cerrado, «las dos formas»): status «superseded» con el último elemento de history «superseded» (closure.py:163-164, hoy en main); status «resolved» con el último elemento de history «resolved-by» (lo agrega la rama wt/closeout-resolved-by); status «closed» con history que termina en la arista terminal task_completes (lo que escribe advance/closeout commit). El conjunto de cierre es una constante: pares (status, último de history).

PRECISIONES DEL COLD-BUNDLE (review-...-bundle-2, 2026-11-09; el bundle-1 fue un timeout técnico):
c1 (status de entrada): mandan los dos, unidos: {"draft"} (lo único que escribe el código, compile_task_spec, cuando el payload no trae status) más los status que el inventario de a6 encuentra en tareas reales en estado de entrada. Los datos solo agregan valores legacy al conjunto, nunca lo reducen.
c2 (cerrada): advance no persiste la transición terminal, y closeout commit saca la tarea del desk (una tarea cerrada deja de existir, DC6). En la práctica no hay TaskDoc persistidas con status closed. El par (closed, task_completes) queda en el conjunto de cierre por coherencia, para una escritura directa por sldb. Los pares que sí aparecen en disco son (superseded, superseded) y, tras resolved-by, (resolved, resolved-by).
c3 (filtro del grep de a5): cuentan los hits en código que arma o muta un payload de TaskDoc: lifecycle.py, services/closure.py, specs/compiler.py (compile_task_spec), services/tasks.py y doc_access (hidratación de tareas). Los hits de otros modelos (message, repo, issues, desk_view, drawer, runtime, review, atoms) se listan en el informe con una línea cada uno, como «otro modelo».
c4 (6 desks): la aceptación exige que desk update no escriba ninguna tarea inconsistente y que la reporte. Si alguna tarea real de los 6 desks no pasa el validador, el worker para y avisa con la lista antes de seguir: una tarea que no pasa ya no se puede editar por sldb, y eso es una decisión del coordinador.
c5 (d4 de CC31): una tarea cuyo task_type no es un tipo registrado (vacío o legacy, como «code» en graph_ui) se valida contra TaskDoc genérico (services/tasks.py, comentario de advance_task). TaskDoc genérico acepta task_type vacío o cualquier string no registrado. Cada modelo tipado acepta solo su literal (TaskCodeDoc → task.code, etc.).

## Validation

_List the checks required before this task can close._

- Validador de TaskDoc: un test por caso de a2 (válidos e inválidos)
- sldb fields update / docs update / save con payload inconsistente rechazados con el mensaje del validador (a4)
- grep de a5 limpio
- Las tareas de los 6 desks pasan o desk update las reporta sin escribir (a6)
- TMPDIR=/dev/shm pytest -q, uno a la vez: test_cli_escape_hatches, test_lifecycle_*, test_closeout, test_activation_rules, test_model_validators, test_task_types; test_cli y test_output_goldens desde /dev/shm
- Inventario de vías en el TaskDoc (a3)
- CHANGELOG

## Done When

_Name the observable condition that makes the task complete._

Las escrituras directas por sldb (fields update, docs update, /save) de un ciclo de vida inconsistente son rechazadas con el mensaje del validador de TaskDoc. Las tareas de los 6 desks pasan o desk update las reporta sin escribirlas. advance y closeout siguen funcionando. El grep de a5 queda limpio. Inventario en el TaskDoc. test_cli_escape_hatches y los tests de a8 verdes. CHANGELOG.
