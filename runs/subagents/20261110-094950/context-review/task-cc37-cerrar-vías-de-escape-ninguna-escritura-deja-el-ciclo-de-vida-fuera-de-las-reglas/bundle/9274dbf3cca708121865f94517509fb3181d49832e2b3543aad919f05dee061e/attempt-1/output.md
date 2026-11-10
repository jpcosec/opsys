## REFORMULACION

**Propósito:** CC37, nodo del plan `deskops-como-config` (PF2, T3.7), cierra las vías de escritura que dejan una TaskDoc con ciclo de vida inconsistente.

**Resultado:** validador de TaskDoc (status/current_node/history/task_type coherentes con la tabla de RelationDoc del paquete) aplicado por sldb en toda escritura (fields update, docs update, /save, transacción); escrituras internas de lifecycle solo por `advance` y `closeout commit`; `desk update` reporta inconsistentes sin escribirlas; inventario de vías; tests y CHANGELOG.

**Repo:** deskops, worktree por nodo.

**Límites:** no toca sldb, ni DA6, CC33, CC35b, closeout resolved-by, ni la forma del desk.

## AMBIGUEDADES

1. **Conjunto de entrada dependiente de datos ausentes.** b2: «cada status que el inventario de a6 encuentre en tareas existentes de los 6 desks con current_node = entry_node e history vacía»; c1: «los status que el inventario de a6 encuentra en tareas reales». El bundle no trae los 6 desks: obliga a inventar/descubrir `ENTRY_STATUSES`.
2. **Función de /save no nombrada.** a4: «el worker usa la función de sldb que /save llama y lo explica». Obliga a inventar cuál es y cómo probarla sin servidor.
3. **Punto de partida contradictorio.** El TaskDoc declara `status: draft`, `history: []`, pero los archivos incluidos ya contienen CC37 (`workspace.py: _task_lifecycle_errors` «CC37»; CHANGELOG sección Changed con CC37). Obliga a inventar si se implementa desde cero o se verifica lo ya escrito.

## DRY-RUN

**Lecturas:** TaskDoc, `deskops/lifecycle.py`, `workspace.py`, `cli/commands/desk.py`, `models/`, `data/lifecycle/`, `tests/`, CHANGELOG.

**Cambios previstos:** crear `deskops/models/task_lifecycle.py` (`lifecycle_errors` leyendo las RelationDoc del paquete); `model_validator` en TaskDoc o su base; en `advance`, aplicar `sets` + `history` + `current_node` en un solo `apply_effects`; filtro en `_task_type_migration_plan`/`migrate_task_types` y reporte en `desk.py`; tests por caso a2 y por vía sldb (a4); grep a5; CHANGELOG.

**Dependencias:** `render_checked`/`validate_model_input_roundtrip` de sldb (`payload_save_steps.py:55-70`); `sets.status` de RelationDoc (CC31); rama `wt/closeout-resolved-by`.

**Validaciones futuras:** pytest uno a uno con `TMPDIR=/dev/shm`; copias de los 6 desks con `desk update --apply`; goldens sin `--update-golden`.

## FUTURO

El merge de `wt/closeout-resolved-by` aporta el par `(resolved, resolved-by)`; el coordinador copia el inventario al TaskDoc con `edit task` (b4) y decide si alguna tarea real no pasa el validador (c4); DA6 («solo por transición») y CC33/CC35b quedan fuera de este nodo.
