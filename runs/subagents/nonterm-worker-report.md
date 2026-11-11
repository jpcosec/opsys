# nonterm-worker: desk update migra a draft las tareas no terminales con history vacía

Task: `task-desk-update-migra-a-draft-las-tareas-no-terminales-con-history-vacía-desks-pre-cc31-y-deja-nota-de-m` (task.debug), rama `wt/nonterm-draft`, base `f21ab5c8`.

## Causa raíz

Reproducción del coordinador (`coord2-ccconfig/nonterm/repro.log`): dos tareas task.code en
`ritual-execution` con `status` `active` y `ready_for_testing` y `history: []`. `deskops desk
update` (dry-run y `--apply`) las lista en "Invalid task documents (not written)" con la
sugerencia fija, sale con rc 1 y salta el resto de las reparaciones (sldb no lee el store).

La tabla de migración es `deskops/models/task_lifecycle.py::legacy_state_migration`. Con history
vacía solo decide dos casos: `superseded` (añade el registro `history [superseded]`) y un status
de `LEGACY_RESOLVED_STATUSES | DRAWER_STATUSES` con nodo (vacía `current_node`). Cualquier otro
status, en particular uno no terminal como `active` o `ready_for_testing`, cae en la rama
`else: return None`, que `deskops/workspace.py::legacy_task_states` clasifica como no migrable.
Por eso `migrate_legacy_task_states` no lo escribe, queda un TaskDoc que el validador (CC37)
rechaza, `sldb stores check` falla y `desk update --apply` devuelve 1 sin hacer las demás
reparaciones. No hay error de lectura ni de escritura: es una fila que falta en la tabla.
