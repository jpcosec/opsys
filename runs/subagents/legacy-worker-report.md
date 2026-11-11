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
