# CC37 worker report: cerrar vías de escape del ciclo de vida

Worker: `cc37-worker` (robocop2). Worktree `deskops-wt-cc37`, rama `wt/cc37`, base `45198785`.
Logs: `~/proyectos/SLDB_1/coord2-ccconfig/cc37/`. Sin push.

## Qué cambió

| archivo | antes (wc -l) | después |
|---|---:|---:|
| `deskops/models/task_lifecycle.py` (nuevo) | 0 | 146 |
| `deskops/models/task.py` | 208 | 219 |
| `deskops/lifecycle.py` | 371 | 371 |
| `deskops/workspace.py` (autorizado, d1) | 728 | 748 |
| `deskops/cli/commands/desk.py` | 432 | 441 |
| `tests/test_task_lifecycle_validator.py` (nuevo) | 0 | 326 |
| `tests/test_lifecycle_graph.py` | 197 | 201 |
| `tests/test_closeout*.py` (fixtures) | | ver D5, D8 |
| `CHANGELOG.md` | | +1 entrada |

- **Validador** (`TaskDoc._lifecycle_is_coherent`, `model_validator(mode="after")`): llama a
  `deskops/models/task_lifecycle.py:lifecycle_errors(status, current_node, history)`. La tabla
  (`lifecycle_table()`, cacheada) se lee del paquete: las tres `RelationDoc` de
  `deskops/data/lifecycle/` (relation_type → destino, `sets.status`; `terminal` → `complete`) y el
  `entry_node` de `deskops/spec/workflows/task_lifecycle.yaml`. Mensaje:
  `Task <id> lifecycle is inconsistent: <campo>: '<valor>' ...; expected '<valor>'` (una o dos
  causas, unidas por `; `).
- **advance** (`lifecycle.advance`): `apply_effects` recibe en un solo `sets` el `status` de la
  arista, la `history` con la arista añadida y el `current_node` destino. Antes validaba un payload
  intermedio (status nuevo con nodo e historia viejos) que el validador rechaza.
- **desk update** (d1, autorizado por coord2): `_task_type_migration_plan` marca cada tarea con
  `lifecycle_errors`; `migrate_task_types` y `pending_task_type_migration` la saltan y devuelven
  `inconsistent task lifecycle in <path>, not written: <errores>`. `desk.py` la saca del conteo de
  migración y la lista bajo `- Inconsistent task lifecycles (not written): N task(s)`. Si la tarea
  inconsistente está trackeada, `sldb stores check` aborta (ver hipótesis H1); `desk.py` ahora
  añade el stderr de sldb al error (`'sldb stores check' failed ... exit code 1: Unexpected: ...
  Task <id> lifecycle is inconsistent: ...`, exit 3), sin escribir nada.

## Estados válidos (a2, b2, b5, c1, c2, c5)

1. **Entrada** — `history` vacía, `current_node` = `ritual-execution` (o vacío, que `advance`
   lee como el nodo de entrada) y `status ∈ ENTRY_STATUSES = {"draft"}`.
2. **Tras transición** — el último de `history` es el `relation_type` de una arista;
   `current_node` = su destino y `status` = su `sets.status`:
   `task_activates → (ritual-testing, active)`, `task_hands_to_closeout → (ritual-closeout,
   ready_for_testing)`, `task_completes → (complete, closed)`.
3. **Cierre** (`CLOSEOUT_STATES`, constante de pares): `closed` ↔ `task_completes` (solo en
   `complete`), `superseded` ↔ `superseded` y `resolved` ↔ `resolved-by` (desde cualquier nodo,
   como los escribe `closure.py:163-164` y `:274-275`).
4. **task_type** — cada modelo tipado acepta solo su `Literal` (ya lo hacía; test
   `test_task_type_matches_the_typed_model`). `TaskDoc` genérico acepta cualquier string (vacío,
   legacy como `code`, o un tipo registrado): ver desvío D3.
5. **Fuera del ciclo de vida** (desvío D2) — con `current_node` vacío e historia vacía también se
   aceptan `deferred` (`DRAWER_STATUSES`) y `resolved|closed|done|complete`
   (`LEGACY_RESOLVED_STATUSES`).

### Conjunto de entrada (b2/c1)

`{"draft"}`. Justificación: es el `status_default` de `TaskDoc` que pone `compile_task_spec`
(`specs/compiler.py:49`), y es el status de las 11 tareas en estado de entrada de los 6 desks:

| desk | tarea | status | current_node | history | task_type |
|---|---|---|---|---|---|
| deskops | task-cc30-… | draft | ritual-execution | [] | task.refactor |
| deskops | task-cc33a-… | draft | ritual-execution | [] | task.code |
| deskops | task-cc36-… | draft | ritual-execution | [] | task.refactor |
| deskops | task-cc37-… | draft | ritual-execution | [] | task.code |
| deskops | task-cc38-… | draft | ritual-execution | [] | task.refactor |
| deskops | task-main-en-verde-… | draft | ritual-execution | [] | task.debug |
| sldb | task-diseño-jerarquía-… | draft | ritual-execution | [] | task.docs |
| sldb | task-diseño-set-bootstrap-… | draft | ritual-execution | [] | task.docs |
| sldb | task-gd27-… | draft | ritual-execution | [] | task.code |
| graph_ui | task-edicion-contextual-… | draft | ritual-execution | [] | code (legacy → TaskDoc) |
| graph_ui | task-vista-changes-… | draft | ritual-execution | [] | code (legacy → TaskDoc) |

spec2viz, scion y pron no tienen tareas en `desk/tasks/`. Ningún valor legacy se agrega al
conjunto. `add task` con un payload JSON que trae otro status (`{"status": "active", ...}`) hoy
queda rechazado por el modelo (antes se escribía).

## Inventario de vías (a3, b4)

| vía | pasa por transición | la cubre el validador | test |
|---|---|---|---|
| `deskops add task` (`compile_task_spec` + transacción) | no (creación en estado de entrada) | sí: el payload se valida al escribir; un `status` no de entrada en el JSON se rechaza | `test_entry_state_*`; sandbox: `add task '{"status":"active",...}'` → `Invalid value: Task task-bad lifecycle is inconsistent ...`, sin archivo |
| `deskops add task --from-drawer` | no | sí (igual que add task; el drawer no aporta status) | `test_add_task_from_drawer` (3 passed) |
| `deskops edit task` | no | rechaza `status/current_node/history/task_type/closeout_evidence` antes de escribir (GC06); el resto se valida al escribir | `test_cli_escape_hatches` |
| `deskops advance task` | sí (`lifecycle.advance`, `apply_effects` con el estado completo) | sí: `apply_effects` valida contra el modelo del tipo; la transición terminal no se persiste | `test_lifecycle_graph`, `test_lifecycle_end_to_end`, `test_activation_rules`, `test_state_after_each_transition_is_valid` |
| `deskops closeout commit` (`close_with_run/close_manual/close_auto`) | sí: cierre; borra la tarea (DC6), no escribe status | lectura con `TaskDoc` (validada) | `test_closeout`, `test_lifecycle_end_to_end` |
| `deskops closeout supersede` | cierre: `(superseded, superseded)` | sí (par de cierre) | `test_closeout` (supersede), `test_closeout_records_are_valid_from_any_node` |
| `deskops closeout resolved-by` | cierre: `(resolved, resolved-by)` | sí (par de cierre) | `test_closeout_resolved_by` |
| `deskops closeout retire` | no escribe; borra una tarea pre-ciclo | sí: estado «fuera del ciclo» (D2) | `test_closeout` (retire), `test_a_task_resolved_before_the_lifecycle_is_valid_only_outside_it` |
| `deskops promote inbox-to-drawer-task` | no (crea un `TaskDoc` `deferred` en el drawer) | sí: estado «fuera del ciclo» (D2) | `test_a_drawer_task_outside_the_lifecycle_may_be_deferred`, `test_inbox_promote_cli_gaps` (20 passed), `test_promotion_nesting` (2 passed) |
| `deskops desk update --apply` (`migrate_task_types`) | no (reescribe `task_type` legacy y re-trackea) | sí: salta y reporta la tarea inconsistente (d1); una trackeada inconsistente aborta en `stores check` con el mensaje | `test_desk_update_reports_an_inconsistent_task_and_does_not_write_it`, `test_desk_update_names_a_tracked_inconsistent_task_and_writes_nothing` |
| servicios internos (grep de a5) | ver a5 | sí (todas escriben por la transacción, que valida) | a5 |
| graph_ui (`UIs/graph_ui`, solo lectura del código) | no | sí: escribe solo por `sldb serve` `POST /save` (`apps/knowledge-workbench/src/api/sldb.ts:190`, `apps/review-workbench/.../sldb-provider.ts:69`) | los tests de `/save` |
| `sldb fields update` | no | sí (`render_checked` → roundtrip construye el modelo) | `test_sldb_fields_update_of_status_to_closed_at_ritual_execution_is_rejected`, `test_sldb_fields_update_of_current_node_without_a_coherent_status_is_rejected` |
| `sldb docs update` | no | sí | `test_sldb_docs_update_with_the_inconsistent_payload_is_rejected` |
| `sldb serve` `/save` (simple y batch) | no | sí | `test_sldb_serve_save_with_the_inconsistent_payload_is_rejected[False/True]` (llama a `sldb.cli.serve.save_routes.save_request`, la función que el handler HTTP de `/save` ejecuta; sin levantar servidor) |
| `sldb.api.transaction` (deskops `doc_access.write_doc`) | — | sí | cubierto por todas las anteriores de deskops |
| escritura directa coherente sin transición (DA6) | no | aceptada a propósito | `test_a_consistent_direct_write_is_accepted` |

## Aceptación, línea por línea

Logs en `~/proyectos/SLDB_1/coord2-ccconfig/cc37/` (`run-r1.log`, `run-r2.log`, `queue-q2.log`,
`nodes-n1.log`, `validator-2.log`). Cada pytest con el comando del brief (`timeout 900`,
`systemd-run MemoryMax=2G`, `TMPDIR=/dev/shm`, uno a la vez). Los archivos lentos (H2) se corrieron
por nodo (D6).

| línea (a8 / Done When) | evidencia | estado |
|---|---|---|
| un test por cada caso de a2, válidos e inválidos, construyendo el modelo | `tests/test_task_lifecycle_validator.py`: entrada (válido; status fuera del conjunto; nodo posterior sin historia), tras transición (las 3 aristas; status ≠ sets.status; nodo ≠ destino; último de history desconocido), cierre (superseded/resolved desde cualquier nodo; par equivocado; closed fuera de `complete`), task_type (Literal tipado; TaskDoc genérico), fuera del ciclo (drawer `deferred`, pre-ciclo resueltas) — archivo completo 36 passed (`r1-1`), más los 2 tests editados después por nodo (`run-r2`) | verde |
| `sldb fields update` de status a `closed` en `ritual-execution` rechazado con el mensaje del validador | `test_sldb_fields_update_of_status_to_closed_at_ritual_execution_is_rejected`; archivo sin cambios | verde |
| `sldb fields update` de current_node sin status coherente rechazado | `test_sldb_fields_update_of_current_node_without_a_coherent_status_is_rejected` | verde |
| `sldb docs update` y `/save` con el mismo payload inconsistente rechazados | `test_sldb_docs_update_with_the_inconsistent_payload_is_rejected`, `test_sldb_serve_save_with_the_inconsistent_payload_is_rejected[False/True]` (`save_request`, simple y batch con `expected`) | verde |
| escritura coherente sin transición aceptada (DA6) | `test_a_consistent_direct_write_is_accepted` | verde |
| tareas de los 6 desks pasan o desk update las reporta sin escribirlas | sección «6 desks»: 11/11 OK; reporte probado en `test_desk_update_reports_an_inconsistent_task_and_does_not_write_it` y `test_desk_update_names_a_tracked_inconsistent_task_and_writes_nothing` | verde |
| advance y closeout commit siguen funcionando | `test_lifecycle_graph` 9/9 por nodo; `test_lifecycle_end_to_end` 5/5 por nodo; `test_closeout` 49 passed; `test_closeout_resolved_by` 19, `_declared_evidence` 19, `_gates` 7, `_skill_links` 3, `_atomless` 15, `_test_paths` 31 | verde |
| grep de a5 limpio (patrón fijado) | sección «Grep de a5» | verde |
| inventario en el TaskDoc | tabla «Inventario de vías» (b4: la copia al TaskDoc la hace el coordinador) | listo para copiar |
| `test_cli_escape_hatches` | 9/9 por nodo (`nodes-n1`) | verde |
| `test_activation_rules` | 10/10 por nodo (`nodes-n1`, `run-r1`) | verde |
| `test_model_validators` | 14 passed | verde |
| `test_task_types` | 16 passed | verde |
| otros tocados por el cambio | `test_add_task_from_drawer` 3, `test_inbox_promote_cli_gaps` 20, `test_desk_view` 10 (1 skip previo), `test_promotion_nesting` 2, `test_desk_sync` 8 | verde |
| `test_cli` y `test_output_goldens` desde `/dev/shm`, sin `--update-golden` | **no corridos** (pausa de pytest y luego cierre pedido por coord2) | **pendiente** |
| tabla `wc -l` antes y después | sección «Qué cambió» | hecho |
| CHANGELOG | `CHANGELOG.md`, `### Changed`, entrada CC37 | hecho |
| doc en `docs/` y rituales (regla común 5) | no hecho: `docs/` no está en `files` del TaskDoc | pendiente (fuera de files) |

## Grep de a5

Patrón: `grep -rnE '\["(status|current_node)"\]\s*=|"(status|current_node)":' deskops/` sobre
`79441973`.

Payloads de TaskDoc (c3):

| hit | dónde | clase |
|---|---|---|
| `lifecycle.py:288` `payload["current_node"] = node` | `advance`, rama bloqueada (vuelve a poner el mismo nodo; no se persiste) | advance |
| `lifecycle.py:301` `"current_node": target` en `sets` | `advance` → `apply_effects` | advance |
| `services/closure.py:163` `payload["status"] = "superseded"` | `close_superseded` | closeout |
| `services/closure.py:274` `payload["status"] = "resolved"` | `close_resolved_by` | closeout |
| `specs/compiler.py:49` `"status": ...status_default...` | `compile_task_spec` | creación |
| `specs/compiler.py:69` `task_payload["current_node"] = ... entry_node` | `compile_task_spec` | creación |
| `services/drawer.py:268` `"status": "deferred"` | `_render_drawer_task` (promote inbox-to-drawer-task) | creación (drawer) |
| `services/tasks.py:237`, `:275`, `:276` | `next_action_report`: dicts de salida, no se escriben | lectura |
| `services/tasks.py:313` `restored = {...}` | `advance_task`, transición terminal: no se escribe | lectura |
| `doc_access.py:121`, `:122` | `_TASK_OWNED_FIELDS`: textos del rechazo de `edit task` | lectura |
| `doc_access.py:905` | `_task_route_summary`: resumen de rutas de repos | lectura |
| `models/task.py:44` | `__reference_models__` | declaración |

Otros modelos (una línea cada uno): `specs/compiler.py:131` (`compile_artifact_spec`, atom/materialization/…; las tareas usan `compile_task_spec`); `cli/commands/message.py:102,177,201,328` (notas de inbox/mensajes); `cli/commands/repo.py:45` (RepositoryDoc); `cli/commands/runtime.py:43,175,205` y `runtime/grouping.py:49,66` (runtime); `cli/commands/review.py:77` (nombre de subcomando); `services/issues.py:139` (issues); `services/desk_view.py:236,237,368,418` (filas de la vista, lectura); `cli/model_introspection.py:208` (introspección de campos del CLI).

Ninguna escritura de `status`/`current_node` de TaskDoc queda fuera de advance, closeout o la
creación. No hizo falta tocar `services/` ni `closure.py`.

## 6 desks (a6, c4)

Copias de los 6 desks con el código de la rama y cwd neutro
(`~/proyectos/SLDB_1/coord2-ccconfig/cc37/desks6.sh`, basado en `cc35a/doctor6.sh`; salidas en
`cc37/desks6/`). Para cada desk: `doctor` main vs rama sobre copias intactas, `view board`,
`desk update` (seco), `desk update --apply` dos veces, sha256 de `desk/tasks/*.md` antes y después,
y cada tarea validada con su modelo (`TASK_TYPE_MODELS[task_type]` o `TaskDoc`).

| desk | tareas | validador | inconsistentes reportadas | `--apply` 1 / 2 | doctor main vs rama |
|---|---:|---|---:|---|---|
| deskops | 6 | 6 OK | 0 | 0 / 0 (2.ª: «Desk is up to date.») | idéntico |
| sldb | 3 | 3 OK | 0 | 0 / 0 (2.ª: «Desk is up to date.») | idéntico |
| spec2viz | 0 | — | 0 | 3 / 3 (H1: `AtomDoc` de CC38) | idéntico |
| scion | 0 | — | 0 | 0 / 0 | idéntico |
| pron | 0 | — | 0 | 0 / 0 (2.ª: «Desk is up to date.») | idéntico |
| graph_ui | 2 (`code`, legacy → `TaskDoc`) | 2 OK | 0 | 3 / 3 (H1: `AtomDoc` de CC38) | idéntico; `desk/tasks` sin cambios (sha256) |

Ninguna tarea real deja de pasar el validador (c4 no se dispara). El exit 3 de spec2viz y
graph_ui es previo: con el código de main (`45198785`) `desk update` en una copia de spec2viz
también sale con 3 (`'sldb stores check' failed ... exit code 1`); la rama solo añade la razón de
sldb (`atom id must follow slug convention atom-<slug>: atom-ast-compilers-for_whom`). Por eso las
2 tareas legacy `code` de graph_ui no llegan a migrarse en la copia; validadas directamente pasan
(`TaskDoc`). `view board` sale con 0 en todos menos pron, que no tiene `desk/tasks/Board.md`
(igual en main). `doctor` sale con 1 en sldb, spec2viz, scion, pron y graph_ui con salida
idéntica a main.

## Hipótesis para sldb

- **H1. `sldb stores check` aborta en el primer documento que su modelo rechaza** (`Unexpected: 1
  validation error ...`, exit 1, sin JSON) en vez de reportarlo como hallazgo. Con validadores de
  modelo (CC38, CC37) un documento trackeado inválido deja a `deskops desk update` sin poder
  diagnosticar el resto (exit 3). Hoy ya pasa en spec2viz y graph_ui por el validador de `AtomDoc`
  de CC38 (`atom-ast-compilers-for_whom`, `atom-actionssection-for_whom`), no por CC37.
- **H2. Lectura lenta del store**: cada comando CLI de deskops tarda ~30 s en un desk recién
  creado (también con el código de main, 33 s para `add task`); el perfil marca
  `yaml constructor.get_single_data` (9 834 llamadas) y `deepcopy`/`model_copy` de pydantic
  (~266 000) dentro de sldb. `desk update` gasta ~33 s en cada `sldb stores check`. Por eso los
  archivos de test con subprocesos (`test_lifecycle_end_to_end`, `test_activation_rules`,
  `test_cli_escape_hatches`) no caben en el `timeout 900` por archivo; los corrí por nodo.
- **H3 (opcional)**: un campo «solo por transición» no se pide (DA6), como dice el TaskDoc.

## Desvíos

- **D1 (autorizado por coord2)**: `deskops/workspace.py`, fuera de `files`: el filtro en
  `_task_type_migration_plan`/`migrate_task_types`/`pending_task_type_migration`
  (`_task_lifecycle_errors`, `_inconsistent_task_line`). Nada más de ese archivo.
- **D2 (decisión reversible, para el coordinador)**: estado «fuera del ciclo de vida». Con
  `current_node` vacío e historia vacía el validador acepta, además de `draft`, `deferred` (lo que
  escribe `promote inbox-to-drawer-task`; 34 TaskDoc `deferred` de drawer en los desks, ninguno trackeado,
  pero `deskops view drawer` y `promote` los construyen con `TaskDoc`) y
  `resolved|closed|done|complete` (las tareas pre-ciclo que `closeout retire` borra; sin esto
  `retire` no podía leer su tarea: 6 tests de `test_closeout` rojos). b2 hablaba solo del estado
  con `current_node = entry_node`; esto es otro estado, y una escritura por sldb que deje
  `current_node` vacío con uno de esos status queda aceptada. Si se prefiere cerrarlo, la
  alternativa es leer el drawer y la tarea de `retire` sin validar (toca `drawer.py`,
  `desk_view.py` y `closure.py`).
- **D3**: `TaskDoc` genérico acepta también un `task_type` registrado (p. ej. `task.code`). c5
  dice «vacío o cualquier string no registrado», pero deskops lee y escribe todas las tareas con
  `TaskDoc` (`closure.py`, `services/tasks.py`, `doc_access`), y sldb las valida con el modelo
  trackeado (`TaskCodeDoc`…), cuyo `Literal` ya exige su tipo. Rechazar tipos registrados en
  `TaskDoc` rompería supersede/resolved-by/advance; queda la coherencia por el `Literal`.
- **D4**: `tests/test_lifecycle_graph.py::test_changing_sets_on_the_relation_doc_changes_what_advance_writes`
  (CC31) pasa a `test_a_desk_edge_whose_sets_differ_from_the_package_is_refused_by_the_task_model`:
  por a1 la tabla es la del paquete, así que una arista del desk editada a `in_review` hace que
  `advance` rechace la transición con el mensaje del validador y no escriba.
- **D5**: fixtures de tests de closeout que escribían tareas `status: active` sin historia (o en
  `ritual-execution`) pasan a `current_node: ritual-testing` + `history: [task_activates]`, el
  estado que `advance` deja con `active` (`test_closeout`, `_resolved_by`, `_skill_links`,
  `_gates`, `_declared_evidence`).
- **D6**: tests lentos corridos por nodo (un pytest por test, uno a la vez, mismo comando del
  brief) por H2.
- **D8**: fixtures de `test_promotion_nesting` y `test_desk_sync` (tareas `active` sin ciclo) pasan a `draft`.
- **D7**: `desk.py` añade el stderr de `sldb stores check` al error cuando falla (antes solo el
  exit code).
- No se tocó `doc_access`, la resolución, `services/` ni `closure.py`; ni `desk/` ni `.sldb/`.

## Fallos que no son míos

- spec2viz y graph_ui: `desk update` exit 3 por `AtomDoc` (CC38) en `sldb stores check` (H1), igual en main.
- pron: `view board` exit 1 (sin Board), igual en main.
- Lentitud general de los comandos (H2), igual en main.
