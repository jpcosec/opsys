## REFORMULACION

**Resultado:** un contrato fuente coherente —RoleDoc supervisor más plantillas Scion generadas— que haga al coordinador recuperar el desk configurado, comprobar estado canónico/DAG/ownership, elegir una hoja ready revisada y no poseída, despachar ejecutor y tester independiente con identidad determinista, reconciliar antes de arrancar, validar evidencia, ejecutar closeout y continuar. Un tester fallido no puede cerrar.

**Repo/superficies:** `deskops/runtime/scion.py`, `deskops/cli/registry.py`, `deskops/cli/commands/runtime.py`, `desk/roles/deskops-supervisor.md`, átomo de workflow, `tests/test_scion_runtime.py`, golden de help, `docs/operator-manual.md` y `CHANGELOG.md`.

**Límites:** sin motor de lifecycle nuevo, scheduler/registro paralelo ni pi-subagents; el supervisor no implementa; sin decisiones automáticas de política; sin secretos en el contexto; sin `--context-file` se preserva el comportamiento actual; nombres y labels deterministas; reconciliación exacta de proyecto+nombre+labels+RunDoc; reintentos técnicos acotados a 2 por input y 2 ciclos corrección/test; `ask_user` solo para decisiones humanas reales.

**Validación declarada:** `pytest tests/test_scion_runtime.py`, goldens afectados si el modo tester añade una opción, e integración real unattended coordinador→ejecutor→tester→closeout/continuación.

## AMBIGUEDADES

1. **`contract_sha256` no está definido.** Se usa en “SHA256(task_id + NUL + contract_sha256 + NUL + role)” y en “labels deskops.contract_sha256”, pero falta qué documento/bytes/versionado exacto se hashean.
2. **Valor de `role` en el hash.** “role-specific prefix deskops-e o deskops-t … + NUL + role” y “deskops.role”; también “distinct role identity”. Falta si `role` es `executor`/`tester`, el id completo del RoleDoc u otro literal.
3. **Significado de `source_root`.** “context keys project, workspace_root, desk_root, source_root, sldb_root son rutas absolutas…” y “PYTHONPATH is source_root + os.pathsep + sldb_root”; solo se aclara que “sldb_root already names its src directory”. Falta si `source_root` es la raíz del repo o el directorio src/padre del paquete `deskops`.
4. **Alcance real de la integración unattended.** “runtime task supplies hooks/bootstrap and unattended integration” frente a Validation (“real unattended … integration”) y Done When (“live integrated experiment”). Falta si esta tarea depende/bloquea en esa tarea runtime.
5. **Regla de autodetección del tester.** “auto-detect tester RoleDoc” y “mode literal is tester”; falta el criterio exacto (nombre contiene `tester`, id `role-deskops-tester`, etc.).

## DRY-RUN

**Lecturas hipotéticas:** TaskDoc, `AGENTS.md`, Board, rituales execution/testing/closeout/context-review, roles supervisor y tester, `runtime/scion.py`, registry/commands runtime, tests, golden help, átomo citado, operator-manual y CHANGELOG.

**Cambios hipotéticos:** corregir el RoleDoc vía SLDB; añadir kwarg de contexto y `--context-file` con validación cerrada; emitir variables, volumen y PYTHONPATH; añadir modo tester y su separación de instrucciones; escribir RunDoc `in_progress` antes de start; nombres/labels deterministas; reconciliación; ejemplos CLI correctos; átomo antes de docs; tests.

**Validaciones hipotéticas:** pytest focalizado; help golden si cambian choices; casos contexto omitido/válido/faltante/desconocido/relativo/fuera de workspace; ausencia de secretos; PYTHONPATH sin rutas heredadas; no duplicar child; tester fallido no cierra; integración real.

## FUTURO

Comprobar al implementar: definir `contract_sha256`, `role` y `source_root` antes de codificar; validar contexto antes de generar; salida byte-idéntica sin `--context-file`; volumen/env sin secretos; tester con identidad distinta del ejecutor; reconciliación proyecto+nombre+labels+RunDoc; reintentos = 2; closeout solo tras tester verde; goldens solo si cambian opciones.
