## REFORMULACION

**Resultado:** `task-scion-autonomy-coordinator-contract` está en `status: draft`, tipo `task.code`, depende de `task-scion-autonomy-review-status`. El contrato exige una fuente coherente para que Scion: recupere estado actual configurado; avance trabajo rutinario autorizado; seleccione una tarea hoja revisada, lista y sin dueño; despache ejecutor y tester independiente; valide evidencia y cierre; y se recupere para continuar.

**Repo/superficie:** según rutas del input, `deskops-wt-scion-autonomy`; toca `deskops/runtime/scion.py`, `deskops/cli/registry.py`, rol supervisor, átomo de workflow, tests/goldens, manual, changelog y fixture de ayuda.

**Incluye:** corregir RoleDoc vía SLDB; permitir mutaciones CLI modeladas sin implementación del supervisor; añadir `--context-file` JSON opcional al comando runtime existente y kwarg del generador; emitir variables `DESKOPS_*` y `PYTHONPATH`, más volumen `source=workspace_root target=workspace_root`; preservar comportamiento sin contexto; añadir modo tester, autodetección de RoleDoc tester e instrucciones separadas; nombres deterministas derivados de tarea+contrato y etiquetas tarea/rol; escribir intención de ejecución antes de arrancar y reconciliar hijo Scion existente antes de uno nuevo; ejemplos con `--project`, `--workspace`, `--type`, `--harness-auth api-key`, `--non-interactive` y `--root` correctos.

**Límites:** revisión read-only del input suministrado; no ejecuté comandos ni verifiqué repositorio, tests, estado de dependencias ni documentación referenciada. No apruebo el contrato completo: solo lo reformulo.

## AMBIGUEDADES

- **Valor de `project`:** dice “context keys project, workspace_root, desk_root, source_root, sldb_root are absolute paths within workspace_root except project”. Falta decidir si `project` es nombre, ruta relativa o identificador, y cómo se deriva/valida.
- **Límite de reintentos/correcciones:** exige “bound technical retries” y “request bounded correction and fresh test”, pero no fija máximo, condición de parada ni qué cuenta como bloqueo definitivo.
- **Cadena exacta del modo tester:** pide “Include tester mode in existing --mode choices” sin fijar el literal aceptado; probablemente `tester`, pero es una decisión de contrato.
- **Criterio de reconciliación:** “reconcile existing matching Scion child” no define la clave exacta de coincidencia (nombre, etiquetas, RunDoc, worktree o combinación), aunque exige nombres deterministas y etiquetas.
- **Metadatos incompletos:** `summary: ''` y `Rationale: Not provided` dejan sin resumen contractual ni motivo; no bloquean la reformulación, pero faltan como decisión editorial.

## DRY-RUN

**Lecturas hipotéticas:** task file, referencias `e58ee061`, `tests/test_scion_runtime.py`, rol supervisor, átomo, goldens de help, manual, changelog.  
**Cambios hipotéticos:** `scion.py`, `registry.py`, RoleDoc, átomo, tests/fixtures, manual y changelog.  
**Validaciones hipotéticas:** `pytest tests/test_scion_runtime.py`; goldens de ayuda/salida si aparece `tester`; inspección de YAML/modos/contexto; ejemplos CLI reales; integración desatendida coordinador→ejecutor→tester independiente→cierre/continuación.

## FUTURO

Comprobar en implementación: comportamiento sin contexto intacto; rutas absolutas y ausencia de secretos; variables y `PYTHONPATH`; volumen correcto; autodetección tester; intención antes de arrancar; reconciliación y protección nativa de duplicados; notificaciones de bloqueo/completado; fallo de tester no cierra; corrección acotada con tester fresco; ejemplos con flags/root correctos; y que preguntas rutinarias no acaben en `ask_user`.
