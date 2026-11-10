## REFORMULACION
Propósito: corregir en deskops dos defectos: d1, falta de migración de tareas heredadas con estado terminal y `history` vacía; d2, caída completa de `doctor` y `desk update` ante documentos inválidos. Resultado: `desk update --apply` migra según la tabla de d1, reporta lo no decidible y es idempotente; `doctor` y `desk update` reportan documento a documento sin abortar. Repo de trabajo: deskops, según rutas `deskops/...`; verificación contra una copia de `shared_llm-gateway`. Límites: no relajar el validador salvo sumar `cancelled` a `LEGACY_RESOLVED_STATUSES`; no tocar desks de AntonIA; no cambiar la gramática del CLI; no escribir a mano en `desk/` ni `.sldb/`; no `git add -A`. Es una tarea ejecutable única, no un agregado.

## AMBIGUEDADES
1. “informe runs/subagents/<worker>-report.md”: el marcador `<worker>` no está resuelto; obligaría a inventar el slug del worker o el nombre exacto del archivo.
2. “Goldens de ayuda idénticos; los de salida, salvo los mensajes nuevos con golden propio”: no se identifican qué goldens de salida existen ni cuáles mensajes nuevos requieren golden propio; obligaría a inventar ese mapeo.
3. “doctor y desk update reportan los documentos inválidos uno por uno sin caer” y b9 solo fija el veredicto de `doctor`: falta el código de salida de `desk update` cuando hay hallazgos no migrables; obligaría a inventar su rc.

## DRY-RUN
Lecturas: tarea, `task_lifecycle.py`, `desk.py`, `workspace.py`, `closure.py`, `closeout.py`, `doctor_findings.py`, tests, docs y CHANGELOG. Cambios previstos: helper de migración por tabla; escritura por ruta de documentos (`desk_transaction`/`sldb replace_text`), revalidación y reversión; `desk update --apply` listando frontmatter y validando por documento; `doctor` con hallazgos por documento y exit distinto de 0; tests con las fixtures b6; docs y CHANGELOG. Dependencias: `lifecycle_errors`, `OUTSIDE_LIFECYCLE_STATUSES`, `CLOSEOUT_STATES`, `LEGACY_RESOLVED_STATUSES` y la ruta de documentos CC35a/CC35d. Validaciones futuras: pytest por archivo con TMPDIR y guarda pgrep; cuatro pasos del workflow en clon limpio; copia del gateway con `stores check` rc 0; goldens.

## FUTURO
El coordinador ejecuta los cuatro pasos, abre la nota a sldb y decide el nombre del informe. Los dueños de AntonIA corren `desk update --apply`. Un humano revisa la decisión revisable de sumar `cancelled` y acepta o rechaza los hallazgos no migrables.
