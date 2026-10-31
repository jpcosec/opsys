# REFORMULACION

**Objetivo:** corregir cuatro afirmaciones inexactas en `auditoria/infraestructura.md` y `auditoria/ui.md`, con citas abiertas en fuente, sin ampliar alcance; commit propio y evidencia en `runs/subagents/20261031-correccion-ws03-ws04/result-summary.md`.

**Alcance:** solo las filas de los cuatro puntos, el resumen afectado y una línea de encabezado por archivo. El Supervisor añade nota de supersesión en `handoff.md` (sin borrar lo original), escribe handoff nuevo, valida, commitea y cierra. Tester de solo lectura verifica. Fuera: código de sldb/pron/spec2viz/graph_ui, `dag.yaml`, `reconciliacion.md`, `brief.md`, WS02, WS06, demás filas y reabrir cierres.

**Repo:** `/home/jp/proyectos/SLDB_1/deskops`; fuentes hermanas `../sldb`, `../pron`, `../UIs/graph_ui`.

**Límites:** nada afirmado como ejecutado; lo no comprobable leyendo queda «no ejecutado»/«fuera de alcance» nombrando el test futuro sin diseñarlo; si la fuente contradice la revisión, reportar con cita en `result-summary.md`.

# AMBIGUEDADES

1. «git diff --stat 2286b976..HEAD sobre deskops, tests, dag.yaml y reconciliacion.md vacío» — `deskops` incluye los dos archivos que se editan; obliga a inventar el criterio de exclusión (¿vacío salvo los `.md` editados y `result-summary.md`?).
2. «Agregar a cada archivo una línea en su encabezado» — no se muestra frontmatter ni formato/posición de esa línea.
3. «§2.1 fila Verificación optimista en HTTP, filas de cache y resumen» — «resumen» no se identifica: ¿sección Resumen, fila de resumen de tabla?
4. «Comprobar con git que f16fcd1 elimina… y que 134a665 actualiza Board» — no indica en qué repositorio (¿`graph_ui`? ¿`deskops`?).
5. «nota de supersesión fechada» — sin formato de fecha ni ubicación (¿`history` YAML? ¿texto libre?).
6. Rutas `../sldb/src/sldb` y `../pron/src` — asumen layout hermano no verificado en el encargo.
7. «Un Tester independiente da PASS» — no se define quién lo designa ni si su PASS bloquea el closeout pese a figurar ya en Validation.

**Tareas futuras asignadas (no lagunas):** nota en `handoff.md`, handoff nuevo, commits, closeout y `tester-result-summary.md`.

# DRY-RUN

**Fuentes que leería:** `review-source.md`; `infraestructura.md` (§2.1, filas cache y Consultas guardadas, resumen) y `ui.md` (fila + Add relation, línea `task.txt`); `handoff.md`; `context-review.md`; en `../sldb/src/sldb`: `http_server.py`, `save_routes.py`, `store/runtime_cache.py`, `store/runtime_cache_signature.py` (buscar `new_operation`); en `../pron/src`: `pron/models/projection.py:14`, `world/projection_reader.py:22`, `world/lexicon.py:137`; en `graph_ui`: `SPEC.md:79-82`, `connect-dialog.js:9-17`, `runs/subagents/20261031-workspace-ui/task.txt`; `git show f16fcd1` y `134a665`.

**Entregable:** dos `.md` editados (solo filas afectadas + encabezado) y `result-summary.md` con antes/después por fila y citas.

**Comandos después (no ejecutados):** los seis de Validation (`test -s` ×2, `build_plan.py --check`, `validate_plan.py --check`, `context_review.py status`, `git diff --stat 2286b976..HEAD`) más `grep -rn saved_query`. **Resultado esperado:** archivos no vacíos, checks OK, diff limitado a los dos `.md`, `result-summary.md` y handoff; Tester PASS.
