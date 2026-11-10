**REFORMULACION**

- **Resultado:** un contrato fuente coherente para que el coordinador Scion recupere estado configurado, avance trabajo autorizado rutinario, seleccione una hoja ready/reviewed sin dueño, despache ejecutor y tester independiente, valide evidencia, cierre y vuelva a recuperar/seleccionar. Incluye `--context-file` opcional, modo `tester`, identidad determinista, RunDoc de intención, reconciliación de hijos y límites de reintento.
- **Repo/tarea:** `deskops`; tarea `task-scion-autonomy-coordinator-contract`, dependiente de `task-scion-autonomy-review-status`.
- **Límites:** toca RoleDoc fuente, plantillas/prompts generados, `runtime/scion.py`, `cli/registry.py`, `runtime.py`, tests/goldens, docs/CHANGELOG y átomo. No crea motor lifecycle, scheduler/registry nuevo, decisiones automáticas de política, pi-subagents ni tareas CC no relacionadas. El supervisor puede modelar mutaciones CLI; no implementa.
- **Contrato clave:** `contract_sha256` se obtiene solo con `hash_fields_with_map` + `contract_hash` de SLDB. Nombres: `deskops-e|t` + 12 hex de `SHA256(task_id + NUL + contract_sha256 + NUL + role)`; labels `deskops.task_id`, `deskops.contract_sha256`, `deskops.role`, `deskops.attempt`. Intento 1 nombre base; intento 2 `-a2`; máximo 2 intentos totales. RunDoc `in_progress` en `run_dir` antes de lanzar; intención no prueba de arranque. Reconciliar proyecto+nombre+labels+RunDoc; running se observa, stopped se reanuda, completed se revisa; nunca duplicar; conflicto bloquea solo esa tarea.
- **Contexto:** cinco claves obligatorias (`project`, `workspace_root`, `desk_root`, `source_root`, `sldb_root`), todas rutas absolutas dentro de `workspace_root` salvo `project`; rechazar faltantes/desconocidas/inválidas/relativas/fuera antes de generar, sin defaults parciales. `project` es slug/UUID no ruta. `desk_root` contiene `desk/`; `source_root` contiene `deskops/`; `sldb_root` ya es `src`. Emitir variables `DESKOPS_*`, `PYTHONPATH=source_root + os.pathsep + sldb_root`, volumen `source=target=workspace_root`; sin secretos; sin contexto preserva comportamiento.

**AMBIGUEDADES**

- No se identifica la “declared setup runtime task” exigida para aceptación final: *“final unattended acceptance/phase integration requires the declared setup runtime task”*. Falta id/dependencia explícita; sin nombrarla no puede verificarse esa aceptación.

**DRY-RUN**

Leería RoleDoc supervisor/tester, `deskops/runtime/scion.py`, `registry.py`, `runtime.py`, tests/goldens, átomo y docs. Editaría vía SLDB el RoleDoc; añadiría validación de contexto y emisión de entorno/volumen; ampliaría `--mode` a `tester`, autodetección solo sobre el RoleDoc elegido y textos separados; añadiría helper de nombre/labels y ejemplos con `--project`, `--workspace`, `--type`, `--harness-auth api-key`, `--non-interactive` y `--root` correctos; actualizaría tests/goldens/docs/CHANGELOG desde el átomo. Validaría: `pytest tests/test_scion_runtime.py`; goldens de help; pruebas de digest canónico, identidad estable ante status/history/references y cambiante ante goal/scope/contract, intento inválido, contexto rechazado antes de escribir, modo tester y flags completos. Luego integración real coordinador→ejecutor→tester→closeout.

**FUTURO**

Comprobaré que no haya contradicción fuente/instalado; que contexto omitido preserve entorno y CLI; que no se filtren secretos; que `contract_sha256` no se reimplemente; que no exista intento 3 ni duplicado; que tester tenga identidad distinta; que los reintentos sean 2 totales; y que la aceptación no atendida espere la setup runtime task nombrada.
