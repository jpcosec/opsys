# CC34 — informe del worker (cc34-worker, 2026-11-11)

Vistas de la UI como ViewDoc servidas por sldb; `desk_view.py` desaparece.

- deskops: rama `wt/cc34` (base `797b89fe`), worktree `deskops-wt-cc34`.
- graph_ui: rama `wt/cc34-ui` (base `origin/wt/deskops-ui` `12c4076`), worktree `UIs/graph_ui-wt-cc34-ui`.
- sldb usado en las pruebas: `git archive` de sldb `origin/main` `1c3132aa` (0.1.13), instalado en `/dev/shm/deskops-cc34/venv` (deskops) y `/dev/shm/deskops-cc34/gvenv` (graph_ui, con pron `7f2e308` y spec2viz `b16c021` de sus `origin/master`).

## Decisiones del coordinador aplicadas (revisables)

1. **Default H1-H8** (aprobado con tres condiciones): `deskops view board|task` = `sldb.api.run_view` + proyección al contrato; para lo que el modelo de ViewDoc no expresa, el CLI llama solo a operaciones de lectura que ya existían (`show_task`, `verify_task_closeout` sin escribir recibos, `next_action_report`, `resolve_task_payload`, lectura del archivo). Ninguna regla reimplementada, ningún código nuevo para un campo. Lo que sale de `run_view` no tiene doble camino: el código viejo se borró con `desk_view.py`.
2. **Proyección (precisión de c6)**: la proyección vive en deskops como función pública `deskops.cli.commands.view.project(view, run_view_result, root)`. graph_ui hace `GET /views/<x>` con ETag a `sldb serve` y la llama en proceso, como las acciones (DP4). `app.js` no se tocó. c6 se prueba como: `GET /views/board == run_view(store, 'board')` y `project(GET /views/board) == deskops view board --format json`.
3. **DA4 → B** (coordinador): no hay copias de ViewDoc en el desk; `desk_declaration.yaml` no se tocó (c7 no aplica). La parte de vistas en desks ajenos queda bloqueada por H9 (sldb la promueve como task.debug; reproducción en `~/proyectos/SLDB_1/coord2-ccconfig/cc34/h9-repro/`).
4. **H10 → (2)**: drawer e inbox siguen como agregado CLI de lectura del disco; solo board y task salen de `run_view`. Las semillas `drawer` e `inbox` no se entregan (no tendrían lector). El tracking de inbox/drawer y que send/promote trackeen al escribir lo abre el coordinador como tarea aparte.
5. **pyproject.toml** sumado a files (aprobado): `data/views/**/*` en `[tool.setuptools.package-data]`, para que la instalación no editable (el CI de graph_ui instala deskops desde git) traiga las semillas.
6. **README de graph_ui** (`frontends/desk/README.md`): fuera de los files de graph_ui; lo toqué porque nombraba `deskops.services.desk_view` y el grep de aceptación sobre `UIs/graph_ui/frontends` no quedaba vacío. Si no corresponde, se revierte ese archivo y el grep deja una línea en un README.

## Qué cambió

### deskops (`wt/cc34`)

- `d6e8a422` **CC34: goldens primero (a3)**, commit solo: `tests/view_desk.py` (desk fijo: 3 tareas en execution, testing y closeout, 1 drawer, 1 nota con reloj fijo), `tests/test_view_goldens.py` y `tests/fixtures/golden/output/view_{board,task,drawer,inbox}.json`, capturados con `desk_view.py`. `test_output_goldens` no borra los `view_*.json` al regenerar los suyos.
- Commit de implementación (ver `git log`):
  - `deskops/data/views/board.md`, `task.md`: semillas ViewDoc, generadas con el modelo `ViewDoc` de sldb (ida y vuelta verificada). board: secciones `board` (Board.md, campos tasks/pills, aristas tasks/pills), `tasks` (TaskDoc en desk/tasks, `group_by: current_node`, `group_order` = los 3 rituales), `pills`, `atoms`. task: param `id` requerido, secciones `board`, `task` (`where: id = {id}`), `pills`, `atoms`.
  - `.sldb/store.yaml`, `.sldb/core/store_index.yaml`, `.sldb/core/models/ViewDoc.yaml`, `.sldb/core/documents/ViewDoc/`: el modelo `ViewDoc` registrado y las dos semillas trackeadas en el store del repo deskops con `sldb models add`, `sldb docs track` y `sldb stores declare --write` (b2). Nada a mano.
  - `deskops/cli/commands/view.py`: `run_view`, `project`, `board_view`, `task_view`, `task_params`, `drawer_view`, `inbox_view`, `render_text` (igual que antes), `ViewError` (antes `DeskViewError`).
  - `deskops/runtime/desk_agents.py`: la vista `agents` (Herdr + `runs/subagents/index.jsonl`), misma salida.
  - Borrados: `deskops/services/desk_view.py` (`DeskView`, `task_revision`, `note_revision`) y los cuatro alias privados de `DeskopsOperations` (`_read_doc`, `_resolve_glob`, `_registered_repositories`, `_repository_root`). Inventario c9: ni graph_ui (`frontends`) ni `deskops/domain_tree.py` los usaban ya; los usaban 3 tests (`test_operational`, `test_taskdoc_read_without_overlay`, `test_lifecycle_graph`), que ahora llaman a `doc_access.read_doc`. `domain_tree.py` no se tocó (b7 no tenía llamada que cambiar).
  - `tests/test_desk_view.py` → `tests/test_view.py`, reescrito sobre `run_view`.
  - `docs/deskops-ui.md` (fuentes y tabla campo -> fuente), `CHANGELOG.md`, `pyproject.toml`.

### graph_ui (`wt/cc34-ui`)

- `frontends/mindmap/deskops_routes.py`: `SldbServes` (un `sldb serve` por store de desk, en 127.0.0.1, arrancado al primer uso, o la URL dada; GET con `If-None-Match` y caché por ETag; 502 con el mensaje si no responde), `DeskopsViews` (GET + `project` en proceso). `DeskRoutes.detail` toma `gates` y `revision` de la vista `task` (ya no `show_task`; `revision` = ETag), y conserva su forma para el mindmap (`payload` y `next` de `next_action_report`, que el mindmap usa: `next.pills`).
- `frontends/desk/serve.py`: board/task por `DeskopsViews`; drawer/inbox/agents por `deskops view ... --format json` en proceso (DP4, H10); `--sldb-url`/`DESK_UI_SLDB_URL`; el servidor cierra los `sldb serve` que arrancó.
- `tests/deskops_viewdocs.py` (trackea las semillas en el store del desk temporal, por H9), `tests/test_desk_ui_routes.py` (+3 tests: c6, 409 editando la tarea, 502), `tests/test_mindmap_deskops.py`, `tests/e2e_desk_ui.py` (sin `DeskView`).

## Tabla campo -> fuente

| Campo del contrato | Fuente |
|---|---|
| `view`, `contract`, `root` | constantes del CLI |
| `board.path` | run_view, sección `board` (fila) |
| `board.pills` (ids) | run_view, sección `board`, campo `pills` |
| tareas del Board, su orden y los `errors` de referencias (fuera de desk/tasks, faltante, repetida) | run_view, secciones `board` (campo `tasks`) y `tasks` (filas por path) |
| columnas: nodo y agrupación | run_view, sección `tasks` (`group_by: current_node`, `group_order`) |
| columnas: `phase`, `purpose`, `in_lifecycle`, orden | agregado CLI, pendiente de sldb H5 (`lifecycle.load_lifecycle_spec`) |
| `CARD.id/title/status/current_node/task_type/path` | run_view, filas de `tasks`/`task` |
| `CARD.gates`, `gates_holding`, `gates_total`, error "no transition leaving" | agregado CLI, pendiente de sldb H1, H2, H3 (`show_task`) |
| `CARD.closeout` | agregado CLI, pendiente de sldb H4 (`verify_task_closeout`, sin recibos) |
| `CARD.pills`/`atoms`: títulos, `what/when/how_not`, `question/answer`; errores de no resolución | run_view, secciones `pills` y `atoms` |
| `CARD.pills`/`atoms`: qué ids (efectivos, con herencia, + `atom-*` de references) | agregado CLI, pendiente de sldb H6 (`resolve_task_payload`) |
| `counts` | suma del CLI sobre las tarjetas |
| `errors` | CLI, de los cruces anteriores |
| `task.on_board` | run_view, arista `tasks` del Board |
| `task.why/goal/scope/implementation_path/files/depends_on/inherits_from/from_drawer/history` | run_view, fila de `task` (`fields: *`) |
| `task.validation`, `done_when`, `references` (efectivos) | agregado CLI, pendiente de sldb H6 |
| `next` | agregado CLI, pendiente de sldb H5 (`next_action_report`) |
| `revision` (task) | run_view (ETag de GD25) |
| `drawer.*` (`id`, `title`, `status`, `markdown`, `excerpt`, `path`, `command`, `count`) | agregado CLI, lectura del archivo, pendiente de H7 y H10 |
| `inbox.*`, `notes[].date`, `notes[].revision` | agregado CLI, lectura del archivo, pendiente de H8 y H10 |
| `agents.*` | CLI (`deskops/runtime/desk_agents.py`), no son documentos (b5) |

`revision` de task (c9): cubre lo que el ETag de GD25 cubre para la vista task: las filas leídas (la tarea, el Board, todas las PillDoc y AtomDoc del store), la ViewDoc y la firma de shards. Un cambio del Board la invalida como antes (el Board es fila de la sección `board`); además la invalida un cambio de cualquier pill o atom (más conservador que el sha256 de Board + tarea). El test de 409 de graph_ui la invalida editando la tarea.

## Hipótesis para sldb (texto exacto enviado al coordinador)

- (H1) transitions.from_field necesita export id; current_node guarda 'ritual-execution' y edges_from no lo resuelve -> holding/blocked vacíos;
- (H2) transitions admite una sola relation y el ciclo tiene 3 (task_activates, task_hands_to_closeout, task_completes);
- (H3) gates con holds=false no aparecen (solo holding/blocked);
- (H4) closeout {declared,found,summary,implicit_code,alerts,evidence} no tiene fuente sin recibos evidence (hoy verify corre en lectura en cada render);
- (H5) next sale del spec yaml del paquete, no de documentos;
- (H6) effective_pills/atoms/validation por herencia no están en el índice;
- (H7) drawer markdown/excerpt (texto crudo) no está en las filas;
- (H8) revision por nota del inbox no existe por fila.

Además:

- (H9) run_view sobre un store que ENLAZA a otro con la ViewDoc da 'Unknown view'. El índice compuesto nombra el nodo enlazado '<link>:ViewDoc:<name>' y load_view busca 'ViewDoc:<name>'; además read_view resuelve semantics.path contra el project_root local, no contra el del store enlazado. Como sldb serve usa run_view, tampoco lo encuentra. Reproducción: `~/proyectos/SLDB_1/coord2-ccconfig/cc34/h9-repro/h9_repro.py` y `output.txt`; en deskops lo muestra `tests/test_view.py::test_a_store_without_the_viewdocs_is_an_error_envelope` y la medición c5 de abajo.
- (H10, de deskops) run_view solo ve documentos trackeados: desk/drawer/tasks no lo trackea ningún desk ni desk_declaration.yaml, desk/inbox no está en desk_declaration.yaml, y message send / promote escriben sin trackear.
- (H11, rendimiento) `run_view` compone en cada proceso el índice de aristas con todos los stores enlazados (`load_edge_index(include_linked=True)`: ~10 000 shards YAML de 6 stores en el desk de deskops), aunque las secciones de board solo seleccionan documentos locales; el índice compuesto no persiste entre procesos. Es el ~95 % del tiempo de `deskops view board` (perfil: run_view 38,4 s, proyección 0,6 s).
- (H13) en el proceso que escribió el store, `run_view` da otra `revision` para las mismas filas que un proceso nuevo o `sldb serve` (cachés de sldb en memoria); con datos iguales. El CLI y `sldb serve` son procesos propios, así que no afecta la guarda; el test c6 de graph_ui compara contra `sldb views run` en su propio proceso.
- (H12, menor) borrado `.sldb_cache`, `run_view` responde `Unknown view: board` (el índice sale vacío porque "reading never rebuilds") en vez de decir que el store no está construido; hace falta `sldb stores build`.

## Commits

- deskops `wt/cc34`: `d6e8a422` (goldens, a3), `8b644d8e` (implementación), `844a9835` (desk sin referencias a lo borrado: 3 materializations y el TaskDoc por `deskops edit`, autorizado), más el commit de este informe.
- graph_ui `wt/cc34-ui`: `55cfb45`.

## Validación (ACCEPTANCE, Validation y Done When)

Medido el 2026-11-11 con la máquina cargada (load average 12-16 en 6 núcleos). Tests de deskops desde la copia `/dev/shm/deskops-cc34/deskops`, uno por archivo con la guarda y `systemd-run MemoryMax=2G`; los de graph_ui desde `/dev/shm/deskops-cc34/ci/UIs/graph_ui` (deskops al lado, como en su CI).

| Línea | Evidencia |
|---|---|
| goldens capturados primero, en commit propio (a3) | `d6e8a422`, solo tests y `view_*.json`, capturados con `desk_view.py` |
| view board/task/drawer/inbox `--format json` idénticos a los goldens salvo revision y fechas (c4) | `tests/test_view_goldens.py`: 1 passed con el código nuevo, sin `--update-golden` |
| idénticos también en el desk real | worktree de deskops, misma caché en los dos lados: board idéntico, task idéntico salvo `revision`, drawer e inbox byte a byte |
| ayuda de view idéntica | `tests/test_output_goldens.py` (incluye `test_help_goldens`, 120 archivos): 7 passed |
| GET /views/board de sldb serve sobre el desk de prueba da el mismo payload (c6 con la precisión de la proyección) | graph_ui `test_board_comes_from_sldb_serve_and_projects_to_deskops_view`: `GET /views/board` == `sldb views run board`, `ETag` == `"revision"`, `project(...)` == `deskops view board --format json` == `/api/view/board`; en deskops `test_project_of_the_run_view_result_is_the_cli_payload` |
| graph_ui sirve board leyendo de sldb serve | mismo test; `test_each_view_route_returns_exactly_what_deskops_view_returns` |
| POST /api/desk/advance con ETag viejo da 409, probado editando la tarea | graph_ui `test_advance_with_the_etag_read_before_an_edit_is_409` (409 "cambió"; con el ETag fresco la guarda pasa y la regla de activación la retiene porque la edición dejó los recibos `changed`); `test_advance_delegates_to_desk_routes_with_revision_guard` |
| 502 si sldb serve no responde (b1) | graph_ui `test_sldb_serve_down_is_a_502_with_its_cause` |
| tests/test_desk_view.py reescrito sobre run_view y verde | `tests/test_view.py`: 14 passed |
| grep "desk_view\|DeskView" vacío en deskops/ y en UIs/graph_ui/frontends | 0 y 0 (`grep -rn` en `wt/cc34` y `wt/cc34-ui`); además `tests/test_view.py::test_the_old_view_service_is_gone` |
| tests de los archivos tocados (deskops) | test_view 14, test_view_goldens 1, test_cli 101, test_output_goldens 7, test_lifecycle_graph 9, test_operational 8, test_taskdoc_read_without_overlay 1, test_cli_grammar 2: todo verde |
| tests de graph_ui tocados | test_desk_ui_routes 13, test_mindmap_deskops 7, e2e_desk_ui 6, e2e_mindmap_deskops 1, test_ci_workflow 6: verdes |
| pasos de deskops (a8) en copia | `sldb stores build` ok; `sldb stores build --check --store .sldb` "PASS: the sources rebuild the store"; `scripts/ci-knowledge-check.sh .` rc 0 (antes de `844a9835` daba rc 1 con 10 `missing_declared_target` por el borrado); `deskops graph missing --root .` "No missing graph references found." |
| pasos de graph_ui en copia | `sldb stores build` (deskops y graph_ui) y `sldb stores build --check` rc 0 |
| deskops view board en los 6 desks (c5) | tabla de abajo |
| tiempo frío/caliente (c8) | sección de abajo |
| CHANGELOG, docs/deskops-ui.md | en `8b644d8e` |

Preexistente, no tocado: `tests/test_mindmap_workspace_reader.py` de graph_ui sigue rojo (2 failed: `test_get_on_stale_store_rejects_observably_and_never_rebuilds`, `test_no_file_is_opened_before_or_instead_of_its_guards`), espera el arreglo de seguridad de sldb. `wt/cc34-ui` parte de `wt/deskops-ui` (`12c4076`); cuando esa integración entre a master se rebasa sobre master.

### c5: `deskops view board --format json` en los 6 desks (código nuevo)

| Desk | Resultado |
|---|---|
| deskops (`wt/cc34`, su store trackea las ViewDoc) | exit 0, JSON con las claves del contrato. Con la caché que traía el worktree: 4 tareas, 0 errors, idéntico al código viejo. Tras `rm -rf .sldb_cache && sldb stores build`: 0 tareas y 4 errors "Ambiguous task selector", idéntico al código viejo: es el glob doble de TaskDoc preexistente (drawer de deskops `bcf090a8`, nota de sldb `6f9576a7`) |
| deskops (checkout principal, main sin las ViewDoc) | exit 1, `Unknown view: board` (H9: no las enlaza; las tendrá al integrar) |
| sldb | exit 1, `Unknown view: board` (H9: enlaza ../deskops/.sldb) |
| spec2viz | exit 1, `Unknown view: board` (H9) |
| scion | exit 1, `Unknown view: board` (H9) |
| pron | exit 1, `No desk board at .../pron/desk/tasks/Board.md` (preexistente: pron no tiene desk ni store; el código viejo daba lo mismo) |
| graph_ui | exit 1, `Unknown view: board` (H9) |

La parte de desks ajenos queda bloqueada por H9 (decisión DA4 → B del coordinador).

### c8: tiempo de `deskops view board --format json` en el desk real de deskops (`wt/cc34`)

`.sldb_cache` borrada no es un estado en el que la vista corra: `run_view` da `Unknown view: board` hasta `sldb stores build` (H12; 19,7 s). Por eso: frío = primera corrida tras `rm -rf .sldb_cache && sldb stores build`; caliente = corridas siguientes.

| | Código nuevo (run_view + proyección) | Código viejo (desk_view, misma caché, misma carga) |
|---|---|---|
| frío (proceso nuevo) | 40,9 s | 40,0 s |
| caliente (proceso nuevo) | 40,2 s; 41,1 s | 42,7 s |
| en un mismo proceso, 1.ª / 2.ª / 3.ª llamada | 35,7 s / 6,9 s / 6,1 s | — |

Perfil (proceso nuevo): `run_view` 38,4 s, de los cuales `load_edge_index(include_linked=True)` compone ~10 000 shards YAML de 6 stores (H11); la proyección de deskops 0,6 s. Meta caliente < 1 s: no se cumple hoy; la verifica CC52. Con la máquina menos cargada, el mismo board con el código viejo tardaba 4,3 s en el checkout principal esta mañana.
