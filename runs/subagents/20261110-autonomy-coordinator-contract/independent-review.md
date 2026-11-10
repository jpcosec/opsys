# Revisión independiente (solo lectura): task-scion-autonomy-coordinator-contract

Worktree: /mnt/ssd/proyectos/SLDB_1/deskops-wt-scion-autonomy. No modifiqué ningún archivo ni store, y no corrí tests.

## Veredicto

No encontré ningún bug real que viole el contrato.

## Qué revisé

- **Contexto source/data:** `validate_scion_context` (`deskops/runtime/scion.py`) exige las 5 claves y rechaza claves desconocidas, rutas relativas y rutas fuera de `workspace_root`. También comprueba que existan `desk/`, `deskops/` y `sldb/`. La CLI (`deskops/cli/commands/runtime.py`) carga el JSON antes de generar nada. `PYTHONPATH` es solo `source_root + os.pathsep + sldb_root`, y el volumen va con `source` = `target` = `workspace_root`. Si se omite `--context-file`, el comportamiento anterior no cambia.
- **Módulo heredado:** `task_contract_sha256` usa `hash_fields_with_map(TaskDoc, md)` y `contract_hash` de SLDB. Los 7 subtipos de TaskDoc, incluido `TaskCodeDoc`, tienen el mismo `__contract__` que `TaskDoc`, así que el digest no cambia con el `task_type`. Con el venv, `deskops` se importa del worktree y `sldb` de `sldb-runtime/src`.
- **Idempotencia e intento:** el intento solo puede ser 1 o 2 (se rechazan bool y 3), y el 2 añade `-a2`. `record_scion_run` ya no sobrescribe una RunDoc existente; antes hacía `write_doc`. `run_id = run-<agent>` es único por identidad de rol e intento. El resumen dice "intent, not proof of start".
- **Labels nativos (≤63 caracteres ASCII imprimibles):** `contract_sha256[:63]`; un `task_id` de hasta 63 caracteres ASCII imprimibles va tal cual, y si no, `t-` más 61 hex (63 en total). `role` y `attempt` son cortos. El nombre del hijo usa el `task_id` y el digest completos (64 hex).
- **Campos canónicos:** `scion_child_identity` devuelve `name`, `task_id`, `contract_sha256` (64 hex), `role`, `attempt` y los labels `deskops.task_id`, `deskops.contract_sha256`, `deskops.role` y `deskops.attempt`. `scion_start_argv` lleva `--type`, `--project`, `--workspace`, `--harness-auth api-key`, `--non-interactive` y un `--label` por cada label.
- **Modo:** un `--mode` explícito manda. Si no, se decide por el nombre o id del rol: termina en `-tester` → tester, contiene supervisor/coordinator → coordinador, y si no, executor. `registry.py` añade `tester` a las opciones de `--mode`.
- **Evidencia:** `validation-native-labels.log` termina con 33 passed. `native-label-constraint.md` es coherente con la implementación.

## Riesgo sin verificar (no lo cuento como hallazgo)

`record_scion_run` solo rechaza si ya existe `run.md` en ese mismo `run_dir`. Si la misma identidad de intento 1 se registra en otro `run_dir`, el rechazo del id duplicado (`run-<agent>`) depende de la store de SLDB: no vi una comprobación de duplicados en `Transaction.create` / `transaction_ops.create` y no lo ejecuté. Sin store (`tx is None`), escribiría el archivo sin comprobar el id.
