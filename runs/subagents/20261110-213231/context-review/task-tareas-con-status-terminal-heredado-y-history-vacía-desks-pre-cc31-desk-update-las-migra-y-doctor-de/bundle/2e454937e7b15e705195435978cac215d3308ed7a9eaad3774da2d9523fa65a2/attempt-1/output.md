REFORMULACION

Propósito: corregir d1 (no hay vía de migración para tareas pre-CC31 con status terminal heredado y `history` vacía) y d2 (doctor y desk update caen enteros ante un documento inválido). Resultado: `desk update --apply` migra según la tabla de d1 (superseded→`history [superseded]` conservando `current_node`; closed/resolved/done/complete/cancelled→`current_node ''`; deferred/candidate→`current_node ''`; el resto no se escribe y se reporta con arreglo sugerido), idempotente y por ruta de documentos; doctor y desk update reportan los inválidos uno por uno sin abortar ni dejar de registrar modelos. Repo: deskops (los archivos de `files`). Límites: no relajar el validador más allá de `cancelled`, no tocar desks de AntonIA, no cambiar la gramática del CLI; TMPDIR=/dev/shm, guarda pgrep, nada a mano en `desk/` ni `.sldb/`, nunca `git add -A`; los 4 pasos los corre el coordinador.

AMBIGUEDADES

1. «las cinco formas de la reproducción»: la reproducción lista 5 tareas en 3 estados; obligaría a inventar si son tareas o formas.
2. «con history vacía y current_node no vacío» / «current_node se queda»: no cubre esos status con `current_node` vacío; obligaría a inventar si caen en «cualquier otro caso».
3. «el arreglo sugerido (deskops advance o closeout según el caso)»: sin mapeo; obligaría a inventar qué sugerir en active con `history` vacía frente a draft con `[task_activates, task_hands_to_closeout]`.
4. «deskops lo esquiva leyendo por la ruta de documentos»: sin mecanismo ni modelo; obligaría a inventar cómo lee y valida.
5. «doctor ... sin caer»: no dice si el inválido es error (exit≠0) o alerta; obligaría a inventar el veredicto.
6. «4 pasos del workflow»: no los nombra; obligaría a inventar cuáles.
7. La instrucción pide «los rituales enrutados por el Board, las pills ligadas, los átomos ligados», pero el TaskDoc trae `pills: []` y `atoms: []` y no incluye Board ni rituales; obligaría a inventar el enrutado.

DRY-RUN

Lecturas: `task_lifecycle.py`, `desk.py`, `workspace.py` (`_task_type_migration_plan`, `_task_lifecycle_errors`, `pending/migrate_task_types`), `doctor_findings.py`, `tests/`, `docs/operator-manual.md`, `CHANGELOG.md` y los archivos de `files`. Cambios previstos: `cancelled` en `LEGACY_RESOLVED_STATUSES`; plan/aplicación de migración de terminales heredadas por frontmatter antes de registrar modelos, una línea por tarea; `desk update` no aborta ante `stores check`; doctor lista inválidos uno por uno. Dependencias: sldb `stores check` (hipótesis), validador TaskDoc, tabla de ciclo de vida, goldens. Validaciones futuras: las cinco de Validation y los 4 pasos.

FUTURO

El coordinador corre los 4 pasos en clon limpio y escribe `runs/subagents/<worker>-report.md`. Los dueños de los desks (salvo AntonIA) ejecutan `desk update --apply`. La decisión revisable de `cancelled` y la elección advance/closeout quedan para el overlord/dueño. sldb decide si `stores check` reporta en vez de abortar.
