# Alcance y estado de partida

## Invariante de toda la migración

1. **El formato del desk no cambia.** Los archivos que hoy existen en `desk/` (Board, tareas, rituales, pills, átomos, drawer, inbox, `desk/lifecycle/`, `desk/reviews/`, `tag-namespaces.yaml`, `config.json`) conservan su ruta, su modelo y su forma. Un nodo puede agregar documentos nuevos en carpetas que ya existen (`RuleDoc` en `desk/lifecycle/`, `ViewDoc` en `desk/views/` si DK4 lo confirma), siempre escritos por `deskops desk update --apply` y nunca a mano; no reescribe los existentes salvo los que ya eran gestionados por deskops (`desk/lifecycle/`).
2. **La gramática del CLI no cambia.** Los goldens de ayuda (`tests/fixtures/golden/help/*.txt`, 120 archivos, `test_output_goldens.py:316 test_help_goldens`) y de salida (`tests/fixtures/golden/output/`, `test_command_output_goldens` :669) quedan iguales. Excepción ya decidida: lo que `gates-por-tipo` GC06 retiró (`advance --to`), que entra con GC06 antes de este plan.
3. **Cada superficie borra su código viejo en el mismo paso.** Un nodo que cambia una superficie a sldb borra en el mismo commit el código de deskops que la implementaba, con un grep en su aceptación. No hay periodo con dos caminos.
4. **En cada paso**, los tests de los archivos tocados verdes, `deskops doctor` y `deskops view board` correctos en los 6 desks (deskops, sldb, spec2viz, scion, pron, graph_ui), y la suite completa del repo tocado sin fallas nuevas contra main (la corre el supervisor sobre el resultado integrado; ver regla 3).

## Estado de partida de deskops (verificado 2026-11-05, `main` en `827f3db7`)

- **Ramas sin integrar que cambian la base.** `wt/gates-por-tipo` (`deskops-wt-gates`, `e80fdef5`): GC01 `9c95ac90`, GC02 `b344d24f`, GC06 `6179e567`, GC03 `e80fdef5`; 81 archivos (+4576/-504): `models/task_types.py`, `services/review.py` (865 líneas), `operations.py` +169, `workspace.py` +279, `registry.py` +188. `wt/closeout-graph-sldb` (`deskops-wt-graph`): `graph/desk_graph.py` nuevo, `extract_docs|edges|sources.py` movidos a `tests/graph_oracle_v1/`, `read_snapshot` en `operations.py`/`desk_view.py`, Board ~1.63 s frío / ~0.355 s caliente. Este plan parte de las dos integradas (gates `G_GATES_FROZEN`, `G_P0`).
- **`operations.py` (1356) y `services/` se llaman en ambas direcciones.** Las funciones de operations delegan en servicios (`create_task_bundle` :344 → `tasks.py:80`; `advance_task` :347 → `tasks.py:172`; átomos :468-525 → `atoms.py`; drawer :358-362) y los servicios vuelven a operations por ~25 pass-throughs privados (`tasks.py:44-78`, `atoms.py:51-79`), construyendo un `DeskopsOperations` si no se les pasa uno (`tasks.py:35-37`, `atoms.py:42-44`, `closure.py:63-65`). Duplicados reales: `_normalize_task_payload` (`operations.py:537-567`) y `compile_task_spec` (`specs/compiler.py:25-61`), los dos llamados en `tasks.py:84-88`; `task_lifecycle.yaml` cargado dos veces (`lifecycle.py:78` y `workflow/next_actions.py:9`). La CLI solo llama a la fachada `operations.*`. graph_ui importa privados: `ops._read_doc`, `_resolve_glob`, `_registered_repositories`, `_repository_root` (`UIs/graph_ui/frontends/mindmap/deskops_routes.py:34,41,46,67`; `frontends/desk/serve.py:66-75`).
- **Specs YAML.** `spec/artifacts/*.yaml` (10), `spec/fields/*.yaml` (49), cargados por `specs/loader.py:17-31`; `registry.fields` solo lo usa `tests/test_specs.py`; `id_pattern` lo leen `compiler.py:33-40` y `operations.py:1118-1123`; `cli/model_introspection.py` (365) ya deriva los campos de los modelos pero repite `id_pattern`, `status_default` y `tags` en `_ARTIFACT_DEFAULTS` (:302-349). Dos fuentes de verdad.
- **Ciclo de vida.** `lifecycle.py` (382): `Transition.sets_status/terminal` (:40-49), `LifecycleSpec.effect` (:62-66), `transitions_from` toma topología y condición del grafo y el efecto del YAML (:123-151), `advance` (:154-190), `ensure_lifecycle_graph` no reescribe existentes (:328, :354). `task_lifecycle.yaml`: `task_activates` sin condición; `task_completes` exige `has(closeout_evidence_verified)`, hecho inyectado por `_add_closeout_facts` (`operations.py:441-450`) y borrado por `tasks.py:196-199`.
- **Closeout.** `verify_task_closeout` (`operations.py:602-723`); productores de hechos de git/archivos: `reference_points_to_commit` (`closeout_gates.py:197-229`), `_to_test` (:177-195), `_to_document` (:160-175), `_closeout_link_gate` (`operations.py:732-794`), `_skill_guard_test_evidence` (:895-926), `_generated_artifact_source_finding` (:939-984), `_reference_points_to_atom`/`_routed_follow_up` (:806-849). Reglas sobre campos: vocabulario, alerta de código implícito, `python_changes_without_declared_tests`, forma de URL, graduación de pills.
- **Vistas.** `services/desk_view.py` (534): `board` :249, `task` :286, `drawer` :331, `inbox` :377, `agents` :438; `_closeout` llama a `verify_task_closeout` por tarjeta (:184-213); contrato en `docs/deskops-ui.md`, `CONTRACT_VERSION = 1` (:26). graph_ui importa `DeskView` en proceso (`frontends/desk/serve.py:158-162`) y llama a `deskops.cli.main.main` para acciones (:217-238).
- **Escrituras.** `doc_io.DocTransaction` (:250) es el único escritor al store vía `sldb.api`; callers en `operations.py:266,1327`, `tasks.py:92`, `atoms.py:179,294,356`, `drawer.py:116,168`, `retire.py:103`, `closure.py:429`, `issues.py:337`, `replace.py:85`, `runtime/scion.py:394`. `message send/ack` escribe crudo sin transacción (`cli/commands/message.py:123,181`).
- **Plantillas.** Strings en `workspace.py` (`scaffold_desk` :166-233, `_write_if_missing` :251, Board :292, pills :322, rituales :340-398, drawer :412, namespaces :419); FAQ empaquetada `deskops/data/faq.md`; `desk update` adivina modelos por ruta (`cli/commands/desk.py:100 guess_model_for_path`).

## Habilitadores (gates) y qué consume cada nodo

| Gate | Lo produce | Lo consumen |
|---|---|---|
| `G_P0` | P0 del árbol: T0.1 (`wt/board-perf` / `read_snapshot`) y T0.3 (`wt/closeout-graph-sldb`) integrados en main | CC30 |
| `G_GATES_FROZEN` | `gates-por-tipo`: GC01, GC02, GC03 y GC06 cerrados en main; dag.yaml de gates-por-tipo marcado congelado | CC30, CC32 |
| `G_GO06` | sldb grafo-operable GO06 (`RuleDoc`, `rules check/explain`) | CC32, CC33 |
| `G_GO08` | sldb GO08 (evaluación en escritura/transición, `edges_blocked`; GO07 anclas incluido transitivamente) | CC32, CC33, CC37 |
| `G_GO09` | sldb GO09 (`attributes.sets/terminal`, `effects`, `apply_effects`) | CC31 |
| `G_GD21` … `G_GD27` | sldb generalizar-desde-deskops GD21 … GD27 | ver `dag.yaml` (`requires` de cada nodo) |

Un gate de sldb se satisface cuando el nodo cerró en `main` de sldb, mandó su nota de cierre a deskops y deskops pinnea en `pyproject.toml` una versión de sldb que lo contiene. Hasta entonces, los nodos que lo requieren no se promueven.

## Qué produce este plan para sldb

`G_CONSUMER` de `grafo-operable` (antes asignado a GC05 de gates-por-tipo, que queda congelado): lo produce CC32 como test de integración y lo informa con `deskops message send --to sldb`.

## Reglas comunes de ejecución

1. Cada nodo se promueve con `deskops add task --from-drawer` en el desk de deskops, con `--task-type` y `files` completos. Las revisiones en frío (preflight, cold-bundle con `deskops review`) las decide el supervisor; quien opera el desk dispone los hallazgos como correcciones del TaskDoc (`deskops edit task`) y resume en `coordinator-status.md`. Nada a mano en `desk/` fuera de `drawer/plans` ni en `.sldb/`.
2. Se ejecuta en robocop2, en un worktree de deskops por nodo o grupo de nodos que el coordinador fije.
3. Validación: los tests de los archivos tocados (`pytest -q <archivos>`, uno a la vez); la suite completa la corre el supervisor una vez sobre el resultado integrado, sin fallas nuevas contra main. Un nodo no cierra con tests rojos ni saltados.
4. Antes de cambiar una superficie, el nodo captura sus goldens de salida (si no existen) sobre un desk de prueba; después del cambio deben ser idénticos, salvo lo que su aceptación nombre.
5. Toda capacidad entra con prueba, `CHANGELOG.md` y doc en `docs/`; los rituales del desk que nombran el comportamiento cambiado se actualizan con `deskops` en el mismo nodo.
6. Compatibilidad de desks: lo que un nodo agrega o reescribe en `desk/` lo escribe `deskops desk update --apply` de forma idempotente (segunda corrida sin cambios), probado.
7. Nada de Python supliendo una regla: si el lenguaje de sldb no la expresa, hipótesis en el TaskDoc y nota a sldb.
8. Promoción de nodos con hijos (`node_role: aggregate`): nunca se promueve el agregado; se promueven los hijos.
