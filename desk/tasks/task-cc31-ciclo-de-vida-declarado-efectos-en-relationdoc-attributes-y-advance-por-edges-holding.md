---
id: task-cc31-ciclo-de-vida-declarado-efectos-en-relationdoc-attributes-y-advance-por-edges-holding
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- pytest tests/test_lifecycle_graph.py
- tests/test_lifecycle_graph.py
- pytest tests/test_lifecycle_end_to_end.py
- tests/test_lifecycle_end_to_end.py
- desk/drawer/tasks/task-closeout-una-materialization-con-target-identity-de-paquete-no-cubre-los-archivos-del-paquete.md
- 439150d716d4a15dd305ecc387fca974577e86ea
- desk/atoms/atom-las-transiciones-del-ciclo-de-vida-de-una-tarea-son-aristas-con-efectos-declarados.md
depends_on:
- task-cc30-limpieza-previa-operations-py-como-fachada-y-fuera-los-spec-yaml-duplicados
- task-cc36-plantillas-del-desk-board-rituales-drawer-faq-como-datos-escritos-por-el-scaffold-de-sldb
pills: []
files:
- deskops/lifecycle.py
- deskops/lifecycle_migration.py
- deskops/spec/workflows/task_lifecycle.yaml
- deskops/data/lifecycle/
- deskops/data/desk_declaration.yaml
- deskops/workspace.py
- deskops/services/tasks.py
- deskops/workflow/next_actions.py
- deskops/cli/commands/desk.py
- deskops/cli/commands/core.py
- tests/
- pyproject.toml
- docs/workflow-policy-reference.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/deskops-como-config/dag.yaml
---

# CC31: Ciclo de vida declarado - efectos en RelationDoc.attributes y advance por edges_holding

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo CC31 del plan desk/drawer/plans/deskops-como-config/dag.yaml rev 3 (autorizado por el dueño 2026-11-05), hijo de PF2, árbol T3.1. Rehace GC04 de gates-por-tipo (DK2) sobre la API general de sldb. Depende de CC30 (93cc1943) y CC36 (d4b49ff6), los dos en main. Gates: G_GO09 y G_GD26, satisfied.

## Goal

_Describe the concrete result this task must produce._

El ciclo de vida es grafo con efectos. Cada RelationDoc de desk/lifecycle/ lleva attributes {sets: {status}, terminal} (GO09) y se escribe como semilla managed del paquete. advance usa edges_holding y apply_effects en vez de los campos sets_status/terminal del YAML. task_lifecycle.yaml queda solo con states. lifecycle.py se reduce a cargar configuración, llamar a sldb y escribir history.

## Scope

_State what is in scope and what is out of scope._

En alcance: deskops/lifecycle.py, deskops/lifecycle_migration.py (k6), deskops/spec/workflows/task_lifecycle.yaml, deskops/data/lifecycle/ y deskops/data/desk_declaration.yaml (semillas managed e include), deskops/workspace.py (solo si la carga de la declaración lo pide), deskops/services/tasks.py, deskops/workflow/next_actions.py, deskops/cli/commands/desk.py y core.py (llamadas a ensure_lifecycle_graph), tests, docs/workflow-policy-reference.md y CHANGELOG.md. Fuera: doc_io/transacción (CC35a), gates de activación (CC32), cierre y _add_closeout_facts (CC33), escrituras en sldb, formato del desk salvo desk/lifecycle/ (gestionado por deskops) y gramática del CLI.

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (desk/drawer/plans/deskops-como-config/dag.yaml rev 3, CC31). SCOPE: Rehace GC04 de gates-por-tipo (DK2) sobre la API general. Los RelationDoc y RelationTypeDoc de desk/lifecycle/ se declaran como semillas managed del paquete (deskops/data/lifecycle/, mecanismo de CC36 sobre sldb scaffold_store, GD26): cada RelationDoc lleva attributes: {sets: {status: <valor>}, terminal: <bool>} según la convención de GO09; desk update --apply reescribe un RelationDoc que difiera y lo reporta (reemplaza ensure_lifecycle_graph, lifecycle.py:275-374, que hoy deja los existentes como están, :328, :354); la migración de rituales legados de lifecycle.py:204-272 y lifecycle_migration.py se conserva mientras algún desk de los 6 la necesite (lo dice desk update en dry-run) y si ninguno la necesita se borra. task_lifecycle.yaml queda solo con states (next_actions, advance_when) para el comando next; transitions sale del YAML (su contenido vive en las semillas). lifecycle.py: se borran Transition.sets_status/terminal (:40-49) y LifecycleSpec.effect (:62-66); transitions_from usa edges_holding con effects; advance toma la primera arista de edges_holding en el orden de los RelationDoc (campo order en attributes si hace falta desempatar, como clave extra que GO09 conserva), aplica apply_effects(payload, effects, modelo del tipo de la tarea) y, si terminal, current_node = complete; history la sigue escribiendo deskops. lifecycle.py queda en: cargar la configuración, llamar a sldb y escribir history; objetivo < 150 líneas. _add_closeout_facts sigue hasta CC33. La transición terminal sigue sin persistirse desde advance (la puerta de cierre es closeout commit).

ACCEPTANCE: En un desk temporal, desk update --apply escribe los RelationDoc con attributes.sets.status (active, ready_for_testing, closed) y terminal true en task_completes; cambiar el sets de un RelationDoc del desk temporal (con la API de sldb en el test) hace que advance escriba ese valor sin tocar ningún YAML; un RelationDoc de la versión anterior (sin attributes) queda reescrito por desk update --apply y una segunda corrida no cambia nada; grep de sets_status y de "effect" como atributo de LifecycleSpec en deskops/ vacío; task_lifecycle.yaml sin la clave transitions; tests/test_lifecycle_graph.py y tests/test_lifecycle_end_to_end.py verdes (adaptados a effects, sin cambiar los escenarios); goldens de ayuda y salida de advance y next idénticos; deskops doctor sin hallazgos nuevos en los 6 desks tras desk update --apply en una copia de cada uno; líneas de lifecycle.py antes y después; CHANGELOG; docs/workflow-policy-reference.md.

OUTPUT_SCOPE: deskops/lifecycle.py, deskops/lifecycle_migration.py, deskops/spec/workflows/task_lifecycle.yaml, deskops/data/lifecycle/, deskops/services/tasks.py, deskops/workflow/next_actions.py, deskops/cli/commands/desk.py, tests/, docs/workflow-policy-reference.md, CHANGELOG.md

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

PRECISIONES DE PROMOCIÓN (2026-11-06, coordinador del plan):
k1 (gates y base): G_GO09 y G_GD26 están satisfied (sldb 33b3c7a0 y d39bf915 para GO09; 96d7b823 para GD26). El pin efectivo es el main de sldb editable, y pyproject.toml no se toca. CC30 (93cc1943) y CC36 (d4b49ff6) están en main. Las dos quedan abiertas solo por la verificación de goldens de task.refactor, lo que no bloquea a este nodo.
k2 (líneas vigentes en main, en lugar de las del SCOPE): deskops/lifecycle.py tiene 406 líneas: Transition :41-50 (sets_status :48, terminal :49), LifecycleSpec.effect :62, load_lifecycle_spec :90, transitions_from :135, advance :178-216, migración de rituales legados :228-298 (_ensure_ritual_readable, _archive_legacy_ritual), ensure_lifecycle_graph :299-400 y lifecycle_graph_present :401. deskops/lifecycle_migration.py tiene 172 líneas y lo usan cli/commands/desk.py:196-211. ensure_lifecycle_graph lo llaman cli/commands/core.py:48-50 (init), cli/commands/desk.py:146-148 y :436-440, y lifecycle_migration.py:168. desk/lifecycle/ del desk de deskops tiene 3 RelationDoc (execution-task_activates, testing-task_hands_to_closeout, closeout-task_completes) y 3 RelationTypeDoc (type-*.md).
k3 (semillas con el mecanismo de CC36): los 6 documentos de desk/lifecycle/ se declaran como semillas mode: managed en deskops/data/desk_declaration.yaml (o en un archivo hermano de deskops/data/lifecycle/ que la declaración incluye) y se rinden en proceso como en CC36 (H1: todo a texto, comparando bytes). Un RelationDoc del desk que difiera se reescribe y se reporta (rewritten). El tracking que hoy hace ensure_lifecycle_graph (registrar los modelos de relación de sldb, trackear los RelationDoc y RelationTypeDoc y trackear los rituales por su id) pasa a include declarados ({model, glob} para desk/lifecycle/*.md por modelo y {model, paths: [{path, name}]} para los rituales con nombre ritual-<x>), aplicados con apply_includes. Si algo no se expresa así, queda como código del caso y se anota como hipótesis.
k4 (orden de aristas): hoy cada nodo de ritual tiene una sola arista saliente, así que no hace falta desempate. advance toma la primera arista de edges_holding en el orden que devuelve sldb. No se agrega attributes.order. Si al implementar aparece más de una arista que se cumple a la vez desde un mismo nodo, el worker para y avisa.
k5 (modelo para apply_effects): es el modelo registrado del tipo de la tarea (el registro de tipos de tareas de deskops, services/tasks.registered_task_types; TaskCodeDoc si el tipo no está). history la sigue escribiendo deskops como hoy. La transición terminal sigue sin persistirse desde advance, porque la puerta de cierre es closeout commit.
k6 (migración legada, decisión por evidencia): antes de borrar nada se corre desk update en dry-run sobre una copia de cada uno de los 6 desks (deskops, sldb, spec2viz, scion, pron, graph_ui), bajo /dev/shm y borrada al terminar, con el código de main. Si alguno reporta que necesita la migración de rituales legados o lifecycle_migration, ambas se conservan y el informe dice cuál la necesita. Si ninguno la necesita, se borran (lifecycle.py :228-298 y lifecycle_migration.py, con sus llamadas en desk.py) en el mismo commit.
k7 (fuera): doc_io sigue en ensure_lifecycle_graph o en lo que lo reemplace hasta CC35a. Este nodo no migra escrituras a sldb.api.transaction. _add_closeout_facts sigue hasta CC33. Las gates de activación por tipo son de CC32.

PRECISIONES DEL PREFLIGHT (review-...-preflight-1, 2026-11-06; prevalecen sobre el SCOPE):
m1 (orden): manda k4. No se agrega attributes.order; advance toma la primera arista de edges_holding en el orden que devuelve sldb. Si dos aristas se cumplen a la vez desde un mismo nodo, el worker para y avisa. La frase del SCOPE sobre «campo order si hace falta desempatar» no se aplica en este nodo.
m2 (task_lifecycle.yaml): las claves de nivel superior que quedan son id, version, source_files, entry_node y states. Sale solo transitions. Cada elemento de states conserva sus campos actuales (id, current_node, phase, ritual, purpose, next_actions, advance_when). «Solo con states» quiere decir sin transitions, no que cambie la forma de states.
m3 (objetivo de líneas): «< 150 líneas» es un objetivo, no aceptación. Si k6 conserva la migración de rituales legados, ese código (lifecycle.py :228-298) pasa a deskops/lifecycle_migration.py y lifecycle.py se mide sin él. Las líneas de ambos archivos, antes y después, van en el informe.
m4 (referencias de línea): mandan las de k2 (ensure_lifecycle_graph :299-400 en main). Las del SCOPE (:275-374) son de antes de CC30.

PRECISIONES DEL COLD-BUNDLE (review-...-bundle-1, 2026-11-06):
n1 (ubicación de las semillas): las semillas de desk/lifecycle/ se declaran en deskops/data/desk_declaration.yaml (un solo archivo de declaración, sin archivo hermano). Sus cuerpos son plantillas en deskops/data/lifecycle/<nombre>.md (fuente file:, rendidas en proceso como en CC36), una por cada uno de los 6 documentos de desk/lifecycle/ con el mismo nombre de archivo.
n2 (contrato de apply_effects, sldb/src/sldb/api/edges/apply_effects.py): apply_effects(subject: dict, effects: dict, model) -> dict devuelve una copia de subject donde cada clave de effects['sets'] reemplaza o agrega la clave de primer nivel (sin merge anidado). El resultado se valida contra model. Lanza ValueError si un valor de sets es un mapa o una lista anidada, y pydantic.ValidationError si el payload no valida. No persiste nada. terminal no lo aplica apply_effects: lo lee deskops del edge (effects['terminal']) para poner current_node = complete.
n3 (orden): edges_holding devuelve las aristas que se cumplen y deskops no les impone orden. En este desk hay como máximo una arista saliente por nodo (k4), así que el orden no decide nada. Un test fija que hay una sola arista por nodo de ritual en las semillas. Si se cumplen dos, se aplica k4: parar y avisar.
n4 (qué se reescribe): solo los 6 documentos declarados como semillas managed (3 RelationDoc y 3 RelationTypeDoc con los nombres de k2). Cualquier otro archivo de desk/lifecycle/ queda intacto y se reporta como no gestionado si sldb lo reporta. El test de «versión anterior» usa uno de esos 3 RelationDoc sin attributes.
n5 (señal de k6): la migración legada hace falta en un desk si, con el código de main y sobre la copia, «deskops desk update --root <copia>» en dry-run imprime alguna línea de lifecycle_migration (inspect_legacy_lifecycle: «Legacy task lifecycle ...») o de la migración de rituales legados (_ensure_ritual_readable / _archive_legacy_ritual: archivar o reescribir un ritual). Las salidas por desk van al informe. Una línea que sea artefacto de la copia (como «graph missing» porque el owner store es otro, lo que ya se vio en CC36) se distingue, se explica y no cuenta.
n6 (history): advance obtiene el payload nuevo con apply_effects y, si terminal, pone current_node = complete. Después deskops agrega la entrada de history como hoy y escribe el documento. apply_effects no toca history.
n7 (6 desks): baseline = deskops doctor con el código de main sobre una copia de cada desk. Después, sobre otra copia, desk update --apply con el código de la rama y deskops doctor con el código de la rama. Se comparan los hallazgos, y uno nuevo que no se explique bloquea. Las copias van bajo /dev/shm y se borran al terminar. Los desks reales no se tocan.

DESVÍOS AUTORIZADOS DURANTE LA EJECUCIÓN (coordinador del plan, 2026-11-06):
d1 (package-data): pyproject.toml entra en files solo para agregar "data/lifecycle/**/*" a [tool.setuptools.package-data]. Sin eso, las plantillas de deskops/data/lifecycle/ no viajan en un wheel (la instalación editable no lo nota). tests/test_packaging.py comprueba que viajan, como en CC36 (c6). No se toca la dependencia de sldb.
d2 (ruta de graph_ui): el sexto desk está en ~/proyectos/SLDB_1/UIs/graph_ui. El brief del worker decía ~/proyectos/SLDB_1/graph_ui por error.
d3 (golden del scaffold de CC36): tests/fixtures/golden/scaffold/init.json y update.json fijan los bytes de desk/lifecycle/. Los 3 RelationDoc cambian a propósito al llevar attributes (sets/terminal), que es lo que pide la aceptación de este nodo. Por eso el golden se recaptura con --update-golden, con dos condiciones: el diff de los dos JSON contra main se limita a los sha256 de esos 3 RelationDoc, y las líneas del reporte de desk update y los demás archivos quedan idénticos. El informe muestra ese diff. Cualquier otra diferencia bloquea.
d4 (modelo para apply_effects, corrige k5): si task_type es un tipo registrado, se usa el modelo de ese tipo. Si no lo es (vacío, legado o desconocido), se usa TaskDoc, el modelo con que advance lee la tarea, y no TaskCodeDoc: TaskCodeDoc fija task_type al Literal 'task.code' y rechazaría tareas que hoy avanzan bien (test_promotion_nesting::test_advance_task_keeps_nested_h3_sections_inside_scope, con task_type ''). El informe lo cubre con un test o con ese test existente.

## Validation

_List the checks required before this task can close._

- En un desk temporal, desk update --apply escribe los RelationDoc con attributes.sets.status y terminal; segunda corrida sin cambios; un RelationDoc sin attributes queda reescrito (test)
- Cambiar el sets de un RelationDoc con la API de sldb hace que advance escriba ese valor sin tocar YAML (test)
- grep -rn 'sets_status' deskops/ vacío; grep de effect como atributo de LifecycleSpec vacío; task_lifecycle.yaml sin la clave transitions
- Evidencia de k6: desk update en dry-run sobre copias de los 6 desks y decisión sobre la migración legada
- TMPDIR=/dev/shm pytest -q, uno a la vez: test_lifecycle_graph, test_lifecycle_end_to_end, test_scaffold_golden, test_desk_sync, test_output_goldens y test_cli_help_examples (sin --update-golden), y los que importen módulos tocados
- deskops doctor sin hallazgos nuevos en los 6 desks tras desk update --apply en una copia de cada uno
- wc -l deskops/lifecycle.py antes (406) y después (objetivo < 150)
- CHANGELOG y docs/workflow-policy-reference.md
- RESULTADO (coordinador de proyecto, 2026-11-06, squash 439150d7 sobre origin/main): lifecycle_graph 9, lifecycle_end_to_end 5, promotion_nesting 2, desk_sync 8, scaffold_golden 3, packaging 6, closeout_gates 7, model_validators 14, cli_help_examples 11, cli 101, output_goldens 7: todos verdes, de a uno. w1:pW terminó el nodo porque el worker quedó trabado en el diálogo de auto mode. n7: con cwd neutro el apply rinde y la segunda corrida queda al día; las 12 alertas 'lost' salen igual con main (previas). Desvíos d1-d4 en el TaskDoc. lifecycle_migration.py borrado y deskops/data/lifecycle (carpeta) cubiertos por el seguimiento enrutado de paquetes y archivos borrados.

## Done When

_Name the observable condition that makes the task complete._

En un desk temporal, desk update --apply escribe los RelationDoc con attributes.sets.status (active, ready_for_testing, closed) y terminal true en task_completes; cambiar el sets de un RelationDoc del desk temporal (con la API de sldb en el test) hace que advance escriba ese valor sin tocar ningún YAML; un RelationDoc de la versión anterior (sin attributes) queda reescrito por desk update --apply y una segunda corrida no cambia nada; grep de sets_status y de "effect" como atributo de LifecycleSpec en deskops/ vacío; task_lifecycle.yaml sin la clave transitions; tests/test_lifecycle_graph.py y tests/test_lifecycle_end_to_end.py verdes (adaptados a effects, sin cambiar los escenarios); goldens de ayuda y salida de advance y next idénticos; deskops doctor sin hallazgos nuevos en los 6 desks tras desk update --apply en una copia de cada uno; líneas de lifecycle.py antes y después; CHANGELOG; docs/workflow-policy-reference.md.
