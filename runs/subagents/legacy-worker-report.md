# legacy-worker: tareas con status terminal heredado y history vacía (task.debug)

TaskDoc: `desk/tasks/task-tareas-con-status-terminal-heredado-y-history-vacía-desks-pre-cc31-desk-update-las-migra-y-doctor-de.md` (main `cd759192`).
Rama `wt/legacy-status`, base `cd759192`. sldb de main: `/dev/shm/sldb-main` en `84eb7f75`.

## Causa raíz (escrita antes del arreglo)

Reproducción propia en una copia de la del coordinador (`/dev/shm/repro-legacy/gw` → `/dev/shm/legacy-w/gw`, shared_llm-gateway `479b415`):
log `~/proyectos/SLDB_1/coord2-ccconfig/legacy/worker-before-gw.log`. Mismo resultado que `repro.log`: `sldb stores check`
cae con `Unexpected: 1 validation error for TaskDoc`, `doctor` da "SLDB store check crashed" sin nombrar el documento,
y `desk update` (dry-run) sale con `DeskopsEnvironmentError` sin reportar nada más.

Las cinco tareas, con `lifecycle_errors()` del frontmatter:

| tarea | status | current_node | history | error del validador |
|---|---|---|---|---|
| task-ci-propio-del-gateway | superseded | ritual-execution | [] | 'superseded' is not an entry status |
| task-workflow-check-obligatorio-del-gateway | superseded | ritual-execution | [] | ídem |
| task-tope-por-tipo-y-pedidos-bloqueados | deferred | ritual-execution | [] | 'deferred' is not an entry status |
| task-linea-base-de-lint-del-gateway | draft | ritual-closeout | [task_activates, task_hands_to_closeout] | status 'draft' does not follow history 'task_hands_to_closeout'; expected 'ready_for_testing' |
| task-logs-de-llm-gateway-servir-sin-pii | draft | ritual-closeout | [task_activates, task_hands_to_closeout] | ídem |

Las cinco están trackeadas como `TaskDoc` en el store.

**d1 (sin vía de migración).** El validador de CC37 (`deskops/models/task_lifecycle.py`, `lifecycle_errors`) acepta un
status terminal o de drawer con history vacía solo si `current_node` está vacío (`OUTSIDE_LIFECYCLE_STATUSES`), y
`superseded` solo con el registro `history [superseded]` (`CLOSEOUT_STATES`). Los desks migrados antes de CC31 dejaron
estas tareas con el `current_node` de entrada (`ritual-execution`) y sin history, un estado que ninguna transición
produce. Ninguna escritura de deskops las puede llevar a un estado válido: `advance` y `closeout` cargan la tarea con el
modelo, que la rechaza, y `desk update` (`workspace.migrate_task_types`) solo reporta las incoherentes como
"inconsistent task lifecycle ..., not written" sin una tabla para corregirlas. `cancelled` no está en ningún conjunto.

**d2 (doctor y desk update caen enteros).** El corte está en sldb: `sldb.store.diagnostics.diagnose_store` →
`_diagnose_model` → `_diagnose_doc` → `_fields_state` → `hashing.hash_fields_with_map` → `extract_model_data` construye
el modelo de cada documento sin guarda por documento, así que el `ValidationError` del primer documento inválido sale de
`check_store` y `sldb.cli.main` lo imprime como `Unexpected: ...` con rc 1 y sin JSON. deskops depende de ese JSON:
- `deskops/cli/commands/desk.py` (`update`) levanta `DeskopsEnvironmentError` cuando no hay JSON y no llega al registro
  de modelos ni a la migración de task_type;
- `deskops/cli/commands/doctor.py` (`_store_check`) registra solo la primera línea del stderr ("SLDB store check
  crashed") y no sabe qué documento es; el chequeo de modelos sí sigue, pero ningún hallazgo nombra la tarea.
deskops no lista ni valida las tareas por su cuenta: toda su lectura pasa por ese `stores check`.

**d3 (closeout retire).** `ClosureService.close_retired` lee la tarea con `doc_access.read_doc(task_path, TaskDoc)`
(extracción con el modelo, que la rechaza) y acepta solo `resolved, closed, done, complete`; la ayuda
(`deskops/cli/registry.py`) dice lo mismo.

## Arreglo

Superficie: solo `deskops desk update` (dry-run sin `--apply`; `--apply` migra). Sin subcomando propio (ronda 3 de pi).

- `deskops/models/task_lifecycle.py`: `cancelled` en `LEGACY_RESOLVED_STATUSES` (OUTSIDE es la unión);
  `legacy_state_migration(status, node, history)` aplica la tabla de d1 solo con history vacía y verifica el
  resultado con `lifecycle_errors`; `UNMIGRATABLE_SUGGESTION` es el texto fijo de b1.
- `deskops/workspace.py`: `legacy_task_states(root)` lee `desk/tasks/*.md` por frontmatter y valida cada una por
  separado (lifecycle y luego `TaskDoc`), así un documento inválido no corta el recorrido (b8);
  `migrate_legacy_task_states(root)` reescribe solo las líneas de la tabla en el frontmatter, revalida con
  `TaskDoc` y restaura byte a byte si sigue inválida.
- `deskops/cli/commands/desk.py` (`update`): con `--apply` migra antes de todo lo demás (antes del registro de
  modelos) e imprime `Migrating legacy task states...` y una línea b4 por campo; el reporte trae
  `Legacy task states to migrate` (dry-run) e `Invalid task documents (not written)` con la sugerencia de b1;
  si `sldb stores check` no da JSON y hay tareas inválidas nombradas, ya no levanta `DeskopsEnvironmentError`: se
  reporta como `Store check failed (...)` y `--apply` se salta las reparaciones del store (ver desvíos). Sin tareas
  inválidas sigue siendo error de entorno (exit 3), como fija `test_cli`. `--apply` sale 0 si
  migró todo o no había nada, 1 si queda algún no migrable. Las líneas `inconsistent task lifecycle ...` de la
  migración de task_type ya no se imprimen: las cubre el reporte nuevo.
- `deskops/doctor_findings.py`: `invalid_task_findings(root)`, una línea de error por tarea inválida
  (`Invalid task document: <archivo>: <lifecycle_errors>. ...`), con `Migrate it with deskops desk update --apply`
  si la tabla la decide y la sugerencia de b1 si no. `deskops/cli/commands/doctor.py`: una línea que la llama
  (más el import). Los demás chequeos corren igual (b9).
- `deskops/services/closure.py` (`close_retired`): lee el frontmatter (sin el modelo), acepta
  `LEGACY_RESOLVED_STATUSES` (con cancelled) y `superseded`, `deferred`, `candidate` con history vacía (y
  `superseded` con `history [superseded]`, lo que deja la migración); con store, rechaza antes de escribir nada
  si hay otra tarea inválida (ver desvíos). `Closeout-Mode: legacy-resolved` como hoy.
- `deskops/cli/registry.py`: la frase de status de la ayuda de retire; su golden es el único de ayuda que cambia.

Files sumados por el coordinador (autorización en el pane, revisable): `deskops/cli/commands/doctor.py` (solo la
llamada al helper) y `deskops/cli/registry.py` (solo la frase de status de retire).

## Hipótesis para sldb (b5: las abre el coordinador; el worker no escribe en sldb)

Todas verificadas sobre una copia del gateway en `/dev/shm` con sldb `84eb7f75`.

- **H1 (stores check aborta en el primer documento inválido).** `sldb.store.diagnostics.diagnose_store` →
  `_diagnose_model` → `_diagnose_doc` → `_fields_state` → `hashing.hash_fields_with_map` → `extract_model_data`
  no tiene guarda por documento: el `ValidationError` de un documento sale de `check_store` y `sldb.cli.main`
  imprime `Unexpected: ...`, rc 1, sin JSON. Lo esperable es un hallazgo por documento (nota `invalid` o similar)
  y el resto del diagnóstico. deskops lo esquiva leyendo las tareas por frontmatter.
- **H2 (toda escritura del store re-extrae todos los documentos del modelo).** `sldb.api.replace_text` dentro de
  `transaction`: el `untrack` del documento llama `untrack_document._forget` → `forget_document` →
  `edge_rebuild.rebuild_edges_indexes` → `edge_sync._sync_model_docs`, que extrae con el modelo cada documento del
  modelo y cae en cualquier otro inválido. Lo mismo `add_model`/herencia de modelos (`init_local_store`: "Inheriting
  ReviewDoc ... Error: 1 validation error for TaskDoc") y `closeout retire` (untrack de la tarea). Consecuencia: con
  dos tareas inválidas trackeadas en el mismo modelo no se puede escribir ninguna por la vía de documentos de b8.
- **H3 (rollback incompleto).** En el caso de H2 la transacción termina en
  `RollbackError: Rollback incomplete; not restored: .sldb/core/documents/TaskDoc/<...>.yaml, ...` y deja esos
  índices modificados en el árbol (visto en `git status` de la copia). Una transacción fallida no debería dejar el
  store a medio escribir.

## Hipótesis de b1 (comandos de la sugerencia sobre una tarea inválida)

- `deskops closeout supersede --task task-linea-base-de-lint-del-gateway ...` sobre la copia del gateway:
  `Validation error: 1 validation error for TaskDoc ... status: 'draft' does not follow history
  'task_hands_to_closeout'` (lee la tarea con el modelo). No opera sobre una tarea inválida.
- `closeout resolved-by` usa la misma lectura con el modelo (no se probó aparte); `closeout retire` no acepta
  `draft`. Para los dos draft del gateway, ningún comando de deskops puede hoy fijar su estado: el dueño tiene
  que editar el frontmatter. No se amplió el alcance (b1).
- La sugerencia fija de b1 usa `<id>` posicional (`deskops closeout supersede <id>`); la gramática real es
  `--task <id> --reason ... --ref ...`. Se dejó el texto de b1 tal cual; corregirlo es decisión del coordinador.

## Desvíos

1. **La migración no escribe por `desk_transaction` / `sldb replace_text` (b8).** Por H2, esa vía no puede
   escribir una tarea mientras otra del mismo modelo sea inválida, que es justo el caso del gateway y del kit. Se
   escribe el frontmatter directo (solo las líneas de la tabla), se revalida con `TaskDoc` y se restaura si sigue
   inválida; los índices del store se refrescan después con el resto de `desk update --apply` (stale hashes →
   `update_store_indexes`), y la tercera corrida da "Desk is up to date.".
2. **`desk update --apply` se salta las reparaciones del store mientras `stores check` no lee el store.** Intentar
   registrar modelos o trackear en ese estado deja el store a medio escribir (H2, H3). Se imprime
   `Skipped the store repairs (...)` y sale 1. Las reparaciones que no tocan el store (scaffold, migración) sí corren.
   "Registro de modelos incluido" (d2) se cumple en doctor (el chequeo de modelos corre) y en desk update como
   reporte; el registro efectivo espera a que no quede ningún inválido.
3. **`closeout retire` con store rechaza si hay otra tarea inválida** (mismo motivo), antes de escribir nada, y
   dice que corra `desk update --apply`. Además acepta `superseded` con `history [superseded]` (lo que deja la
   migración); sin eso, la tabla de d1 dejaba las superseded del kit fuera del alcance de retire. Decisión revisable.
4. **Copia del gateway: `stores check` rc 0 solo tras decidir los dos draft.** Ver abajo.

## Copia del gateway (`/dev/shm`): tabla aplicada, stores check

Log: `~/proyectos/SLDB_1/coord2-ccconfig/legacy/worker-gw-after.log` (copia de `/dev/shm/repro-legacy/gw`, borrada al final).

| tarea | antes | `desk update --apply` |
|---|---|---|
| task-ci-propio-del-gateway | superseded, ritual-execution, [] | `history [] -> [superseded]` |
| task-workflow-check-obligatorio-del-gateway | superseded, ritual-execution, [] | `history [] -> [superseded]` |
| task-tope-por-tipo-y-pedidos-bloqueados | deferred, ritual-execution, [] | `current_node ritual-execution -> ''` |
| task-linea-base-de-lint-del-gateway | draft, ritual-closeout, [task_activates, task_hands_to_closeout] | no migrable (b1) |
| task-logs-de-llm-gateway-servir-sin-pii | ídem | no migrable (b1) |

- Paso 3, `--apply`: tres líneas de migración, las dos draft reportadas, `Skipped the store repairs`, rc 1. El diff de
  `desk/` toca solo esas líneas.
- Paso 5, segunda corrida: ninguna línea de migración, solo los dos no migrables, rc 1, sin cambios.
- Paso 6, `sldb stores check`: rc 1, por las dos draft (H1).
- Paso 7: **simulación en la copia** de la decisión del dueño (las dos draft a `ready_for_testing`, coherente con su
  history; ningún comando de deskops puede hacerlo, ver b1).
- Paso 8, `--apply`: registra los modelos, retipa las tareas, trackea Board y phase, actualiza los índices, rc 0.
- Paso 9, `sldb stores check`: `PASS: store integrity — 60 documents in 26 models`, rc 0.
- Paso 10, tercera corrida: `Desk is up to date.`, rc 0. Paso 11, `doctor`: `Desk is healthy. No issues found.`, rc 0.

**No migrables que quedan en el gateway real:** `desk/tasks/task-linea-base-de-lint-del-gateway.md` y
`desk/tasks/task-logs-de-llm-gateway-servir-sin-pii.md` (draft tras `task_hands_to_closeout`; decide su dueño).

## doctor en la copia del gateway (capturas)

Antes (`worker-before-gw.log`, código de `cd759192`):
```
Errors (the desk is broken):
- Legacy desk detected: sldb stores check failed: Unexpected: 1 validation error for TaskDoc. Migrate with: deskops desk migrate --root <repo>.
- SLDB store check crashed (likely malformed documents): Unexpected: 1 validation error for TaskDoc
- Unregistered models: ReviewDoc, TaskAggregateDoc, ... Register them with deskops desk update --apply.
rc=1
```
Después (`worker-gw-after.log`, paso 2): las mismas tres líneas más una `Invalid task document: <archivo>: <texto del
validador>. ...` por cada una de las cinco tareas: `Migrate it with deskops desk update --apply` para las tres de la
tabla y la sugerencia de b1 para las dos draft. rc 1. El chequeo de modelos sigue corriendo.

## doctor en los 6 desks, antes y después (solo lectura, sobre copias en /dev/shm)

Capturas: `~/proyectos/SLDB_1/coord2-ccconfig/legacy/desks/<desk>.doctor-{before,after}.txt` (antes = worktree
detached en `cd759192`; después = este worktree). Las copias se hicieron con rsync (sin `.venv`, `node_modules` ni
`.sldb_cache`) y se borraron.

| desk | antes | después | diff |
|---|---|---|---|
| deskops | rc 0 | rc 0 | idéntico |
| sldb | rc 0 (25 alertas) | rc 0 | idéntico |
| spec2viz | rc 1 | rc 1 | idéntico |
| scion | rc 1 | rc 1 | idéntico |
| pron | rc 1 | rc 1 | idéntico |
| graph_ui | rc 1 | rc 1 | idéntico |

Ningún hallazgo nuevo de d2 en esos seis: ninguno tiene tareas en `desk/tasks` que el modelo rechace. Los rc 1 son
previos y no cambian.

## `deskops desk update` en dry-run sobre copias de todos los desks (precisión del overlord)

Sin `--apply`; nada se aplicó en ningún desk real. Salidas: `~/proyectos/SLDB_1/coord2-ccconfig/legacy/desks/<desk>.update-dry.txt`.

| desk | migraría | no migrable (decide el dueño) |
|---|---|---|
| /srv/repos/Chatbot_Infra (kit) | 19: 18 `history [] -> [superseded]` y 1 `current_node ritual-execution -> ''` (task-identidad-del-store-desde-store-manifest-de-sldb, deferred) | — |
| /srv/repos/Governance | 6: 5 cancelled `current_node ritual-execution -> ''` y 1 superseded | 1: task-rol-de-robocop-en-antonia-dev-y-mepu-dev-sin-llaves (active, history vacía) |
| /srv/repos/labchile_chatbots | 1: task-traer-selfix-desde-psp-agent (superseded) | — |
| /srv/repos/shared_llm-gateway | 3 (tabla de arriba) | 2 (las dos draft) |
| /srv/repos/mepu | — | 1: task-spec-2-spec-de-ingesta-del-sftp-de-teva-a-raw-stg-y-core-hoy-y-objetivo (closed tras `task_hands_to_closeout`) |
| ~/proyectos/SLDB_1/UIs/marcado | — | 59: `current_node: 'checklist-...'` sin history (53) e history con rutas de runs (6); forma pre-lifecycle de otro tipo, fuera de la tabla |
| ~/proyectos/SLDB_1/UIs/sldb-ui | — | 17: `current_node: 'checklist-...'` sin history |
| /srv/repos/antonia_gateway, ftcourier, manifest, plantilla_cliente, shared_etl-plataforma; deskops, sldb, spec2viz, scion, pron, graph_ui, marcado-ui | — | — |

El kit Chatbot_Infra coincide con b11 (19 heredadas). spec2viz y graph_ui tienen un `AtomDoc` inválido, ajeno a esta
tarea, que hace fallar `sldb stores check` (H1). La corrida de esta tabla (antes del rebase) lo reportaba como
`Store check failed (... AtomDoc)`. Tras el rebase, `test_cli::test_desk_update_exits_three_when_stores_check_has_no_json`
fija que un `stores check` sin JSON es un error de entorno (exit 3). Por eso `desk update` solo reporta y sigue cuando
hay tareas inválidas ya nombradas (d2); si no, levanta `DeskopsEnvironmentError` como antes. Para esos dos desks el
comportamiento queda como en main.

## Rebase sobre origin/main 4338f90b (CC33b)

**Causa raíz del choque en `deskops/services/closure.py`:** el choque está solo en el bloque de imports, y ambos lados agregan
líneas en el mismo lugar. CC33b sumó `from deskops import lifecycle` y `closeout_evidence_kinds` (la regla de cierre
`rule-closeout-<tipo>` y sus findings); esta rama sumó `DRAWER_STATUSES`, `LEGACY_RESOLVED_STATUSES` y `_frontmatter`
de `task_lifecycle`. Se conservan los dos lados. No hubo choque en `close_retired`: CC33b no lo tocó, y la regla de
cierre (`_gate_outcome` → `closeout_rule_findings`) solo corre en `_close` con `run_gates=True`. Retire sigue con
`run_gates=False`: sin regla de cierre, con `Closeout-Mode: legacy-resolved` y leyendo la tarea por frontmatter. No se
reintrodujo nada de lo que CC33b borró (`__closeout_evidence__`, `closeout_evidence_verified`, `_add_closeout_facts`
no aparecen en el diff de esta rama contra main). CHANGELOG se fusionó solo; `.sldb` no chocó (la rama no lo toca).

## Tests (de a uno, con la guarda; TMPDIR=/dev/shm, MemoryMax=2G)

Logs: `~/proyectos/SLDB_1/coord2-ccconfig/legacy/tests2/` (tras el rebase sobre 4338f90b) y `tests3/` (tras `7939bb54`).
Guarda de pytest: la ampliada por el coordinador (ignora integ-deskops, AntonIA, mepu y cwd fuera de SLDB_1//dev/shm).

| archivo | dónde | resultado |
|---|---|---|
| test_legacy_task_states | worktree (7939bb54) | 24 passed, rc 0 |
| test_task_lifecycle_validator | worktree (7939bb54) | 37 passed, rc 0 |
| test_closeout | worktree | 58 passed, rc 0 |
| test_closeout_atomless / _declared_evidence / _evidence_receipts / _gates / _resolved_by / _rules / _skill_links / _test_paths | worktree | 15 / 19 / 5 / 3 / 19 / 12 / 3 / 31 passed, rc 0 |
| test_cli | copia /dev/shm en 7939bb54 | 101 passed, rc 0 (en 78c6e779 fallaba `test_desk_update_exits_three_when_stores_check_has_no_json[-127]`; arreglado en 7939bb54) |
| test_output_goldens (incluye `test_help_goldens`) | copia /dev/shm en 78c6e779 | 7 passed, rc 0, sin `--update-golden` |
| test_command_registry, test_scaffold_golden | copia /dev/shm | 3, 3 passed, rc 0 |
| test_retire_cli, test_doctor_alerts, test_doctor_unmodeled_surfaces, test_doctor_model_registration, test_desk_sync, test_task_types, test_federated_models, test_lifecycle_graph, test_activation_rules, test_doc_readability, test_cli_grammar | worktree (78c6e779) | 11, 5, 4, 8, 8, 16, 2, 9, 10, 6, 2 passed, rc 0 |

**Antes del arreglo** (`tests/test_legacy_task_states.py` sobre un worktree detached en `cd759192`, con la tabla
nueva reemplazada por un stub; log `t-legacy-before.log`): 24 failed. Los tests de comportamiento fallan por el
defecto: `desk update` dry-run y `--apply` salen con 3 (caen con `'sldb stores check' failed`), doctor nombra 0 de las
7 tareas inválidas, y retire no rechaza por adelantado. Los 19 unitarios fallan porque la tabla no existe.

## Aceptación, línea por línea

| línea | evidencia |
|---|---|
| Causa raíz escrita y commiteada antes del arreglo | commit `f045f583` (antes `85f034c5`), anterior al arreglo `817278bc` |
| Test de reproducción sobre tmp_path con las 7 fixtures de b6: antes falla | `t-legacy-before.log`: 24 failed (desk update exit 3, doctor sin hallazgos por tarea) |
| ...después `desk update --apply` migra según la tabla con las líneas de b4 | `test_desk_update_apply_migrates_by_the_table_...`: 5 líneas `<archivo>: <campo> <antes> -> <después>`; golden `tests/fixtures/golden/output/desk_update_legacy_migration.text` |
| ...reporta los no migrables con rc 1 | mismo test: las 2 draft con el texto del validador y la sugerencia de b1, rc 1 |
| ...una segunda corrida no migra nada | mismo test: sin líneas de migración, archivos byte-idénticos, solo los no migrables |
| doctor con una tarea inválida la reporta y sigue (registro de modelos incluido) | `test_doctor_reports_each_invalid_task_and_runs_every_other_check`: 7 líneas `Invalid task document`, rc 1, "the desk is broken", `_check_models` corre; golden `doctor_invalid_task.text` |
| Goldens de ayuda idénticos salvo retire; los de salida, salvo los mensajes nuevos con golden propio | `test_output_goldens` 7 passed sin `--update-golden`; solo cambió `help/deskops_closeout_retire.txt` (la lista de status); dos goldens nuevos de b5 |
| closeout retire de superseded, cancelled, deferred y candidate; coherente en ritual-execution sigue rechazado | `test_closeout.py::test_closeout_retire_removes_a_pre_cc31_task_the_model_rejects[4 status]`, `..._refuses_a_coherent_task_at_ritual_execution`; con store: `test_retire_waits_while_another_task_is_invalid_then_retires_the_migrated_task` |
| Copia del gateway: `desk update --apply` y luego `stores check` rc 0 | `worker-gw-after.log`: rc 0 tras simular en la copia la decisión del dueño sobre los 2 no migrables (listados arriba); sin esa decisión, rc 1 por H1 |
| doctor en los 6 desks antes y después | tabla de arriba, idéntico en los seis; sin hallazgos nuevos de d2 |
| 4 pasos del workflow en clon limpio | los corre el coordinador (b2) |
| doc y CHANGELOG | `docs/operator-manual.md` (doctor, desk update, retire); `CHANGELOG.md` (Fixed) |

## Limpieza

Borradas las copias en `/dev/shm/legacy-w` y el worktree `/dev/shm/deskops-legacy-base`; los worktrees de goldens
`/dev/shm/deskops-legacy` se quitaron al terminar cada cola. Nada aplicado en desks reales; nada escrito en sldb.
