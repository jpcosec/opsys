## REFORMULACION

**Resultado:** un contrato fuente único (RoleDoc + plantilla Scion generada) para que el coordinador Scion recupere el desk configurado, ejecute trabajo autorizado rutinario, seleccione una tarea "reviewed ready unowned", despache ejecutor/tester frescos y reconcilie closeout antes de continuar. Superficies: `deskops/runtime/scion.py` (nuevo `--context-file` JSON y kwarg de contexto; `--mode` admite `tester` con instrucciones propias; autodetección del RoleDoc tester), `deskops/cli/registry.py` si el modo tester requiere elección, `desk/roles/deskops-supervisor.md`, átomo durable nuevo, `tests/test_scion_runtime.py`, golden de help si cambia elección, `docs/operator-manual.md`, `CHANGELOG.md`.

**Repo:** deskops (worktree `deskops-wt-scion-autonomy`).

**Límites:** sin motor de ciclo de vida nuevo, sin decisiones automáticas de política, sin pi-subagents, sin tareas CC ajenas. No implementa el supervisor; corrige fuente y regenera. Contexto: claves `project, workspace_root, desk_root, source_root, sldb_root` absolutas bajo `workspace_root` salvo `project`; emite `DESKOPS_DESK_ROOT, DESKOPS_SOURCE_ROOT, DESKOPS_SLDB_SOURCE_ROOT, DESKOPS_WORKSPACE_ROOT, DESKOPS_SCION_PROJECT, PYTHONPATH` y volumen `source=workspace_root target=workspace_root`; sin secretos; preserva comportamiento sin contexto.

## AMBIGUEDADES

1. Valor exacto de `PYTHONPATH` ("Emit ... `PYTHONPATH`"): no se define qué rutas lo componen (¿`source_root`? ¿`sldb_root/src`?).
2. Comportamiento ante claves de contexto faltantes o fuera de `workspace_root` ("context keys ... are absolute paths within workspace_root except project"): no dice si error, omisión o default.
3. Superficie y formato del "run intent" previo ("write run intent BEFORE start"): ¿RunDoc `in_progress` existente? ¿qué archivo?
4. Criterio de "existing matching Scion child" en la reconciliación ("reconcile existing matching Scion child"): ¿coincidencia por nombre derivado, por label de tarea/rol, ambos?
5. Algoritmo determinista de nombres ("Deterministic task+contract-derived agent names"): semilla/plantilla del slug no especificada.

## DRY-RUN (hipotético, sin ejecutar)

- **Lectura:** `deskops/runtime/scion.py`, `deskops/cli/registry.py`, `desk/roles/deskops-supervisor.md` y `deskops-tester.md`, `tests/test_scion_runtime.py`, golden `tests/fixtures/golden/help`, `docs/operator-manual.md`, `CHANGELOG.md`, átomo referenciado.
- **Cambios:** añadir `--context-file` + kwarg; emitir bloque env/volumen en plantilla; ampliar `--mode` a `tester`; autodetectar RoleDoc tester; bloques separados de alcance/completitud tester; instrucciones coordinador (recover→check→skip owned/blocked→select→intent→dispatch→reconcile).
- **Validaciones:** `pytest tests/test_scion_runtime.py -q`; regenerar y revisar golden de help; comprobar que sin `--context-file` la plantilla no cambia.

## FUTURO (comprobaciones de implementación)

Verificar que sin contexto no cambian bytes de plantilla; que sin secretos y con rutas absolutas se cumple; que modo tester materializa instrucciones distintas; integración real desatendida coordinador→ejecutor→tester→closeout→reinicio sin duplicar hijo; que un tester fail no cierra.
