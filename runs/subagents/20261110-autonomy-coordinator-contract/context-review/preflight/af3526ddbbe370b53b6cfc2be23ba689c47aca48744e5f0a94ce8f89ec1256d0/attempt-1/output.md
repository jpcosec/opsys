## REFORMULACION

**Resultado:** un contrato fuente coherente para el coordinador Scion: recuperar estado configurado, progresar trabajo rutinario autorizado, seleccionar una tarea hoja revisada y lista sin dueño, despachar ejecutor/tester independiente y reconciliar cierre antes de continuar.

**Repo/superficie:** `deskops`; toca `deskops/runtime/scion.py`, `deskops/cli/registry.py`, `deskops/cli/commands/runtime.py`, `desk/roles/deskops-supervisor.md`, átomo de workflow, tests, golden de help, manual y CHANGELOG. Fuera de alcance: motor de ciclo de vida sustituto, decisiones automáticas de política, pi-subagents y tareas CC no relacionadas.

**Límites:** el supervisor puede modelar mutaciones CLI del workflow, pero no implementar. Solo escala decisiones de owner no resueltas, conflictos reales de ownership o credenciales/permisos externos. No repite una review aceptada con input sin cambios; limita reintentos técnicos y ciclos corrección/test, y reporta bloqueos exactos. El CLI runtime-template gana `--context-file` JSON opcional con claves `project`, `workspace_root`, `desk_root`, `source_root`, `sldb_root`; todas absolutas y dentro de `workspace_root` salvo `project`. Emite `DESKOPS_DESK_ROOT`, `DESKOPS_SOURCE_ROOT`, `DESKOPS_SLDB_SOURCE_ROOT`, `DESKOPS_WORKSPACE_ROOT`, `DESKOPS_SCION_PROJECT`, `PYTHONPATH` sin rutas heredadas y volumen `source=workspace_root target=workspace_root`. Sin secretos. Sin contexto, comportamiento intacto. Añade modo `tester`, autodetección de su RoleDoc e instrucciones separadas. Identidad determinista `deskops-e`/`deskops-t` + 12 hex de SHA256(task_id+NUL+contract_sha256+NUL+role), labels `deskops.task_id`, `deskops.contract_sha256`, `deskops.role`. RunDoc `in_progress` como intención antes de start; reconciliar proyecto+nombre+labels+RunDoc; hijo running se observa, stopped se reanuda, completed se revisa; nunca duplicar. Secuencia: ejecutor → tester independiente → coordinador valida evidencia → closeout → reconcile → recuperar/seleccionar. Tester fallido no cierra. Espera con notificaciones Scion; solo decisiones humanas reales usan `ask_user`.

## AMBIGUEDADES

- No se define qué hashea `contract_sha256`: «SHA256(task_id + NUL + contract_sha256 + NUL + role)». Falta fuente y canonización (bytes del task, contrato fuente, YAML normalizado).
- «Bound technical retries to 2 per unchanged input» no aclara si son 2 intentos totales o 2 reintentos tras el inicial.
- «selects one reviewed ready leaf» no define desempate si hay varias hojas elegibles.
- «auto-detect tester RoleDoc» no fija precedencia si existen varios RoleDoc candidatos.

## DRY-RUN

**Lecturas hipotéticas:** task, `e58ee061`, `tests/test_scion_runtime.py`, RoleDoc supervisor, átomo, runtime/CLI, goldens de help, manual y CHANGELOG.

**Cambios hipotéticos:** RoleDoc vía SLDB; validación y paso de contexto; kwarg de generador; env/volumen; modo tester y detección; prompts/ejemplos; tests, goldens, docs y changelog.

**Validaciones:** pytest focalizado; goldens de help; rechazo de claves faltantes/desconocidas/rutas relativas/fuera de workspace; ausencia de secretos; no-context sin cambios; nombres/labels deterministas; reconcile antes de start; no duplicado; tester fallido no cierra; límites de reintento; integración real coordinador→ejecutor→tester→closeout.

## FUTURO

Comprobar al implementar: help/ejemplos reales coinciden; nombres exactos de env; `PYTHONPATH` sin rutas obsoletas; contención de rutas; `project` slug/UUID no path; literal `tester`; RunDoc antes de start; identidad recalculable; reconciliación exacta; contadores de reintento; preguntas rutinarias no van a `ask_user`; no aparece scheduler/registro nuevo; tests y experimento live pasan. No apruebo aún: el documento está `draft` y el contrato depende de `task-scion-autonomy-review-status`.
