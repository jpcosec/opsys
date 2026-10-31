## REFORMULACION

**Objetivo:** corregir cuatro afirmaciones documentales inexactas (más un punto 5 sobre ViewDoc) en dos auditorías authored, con citas a fuentes abiertas y sin afirmar nada ejecutado.

**Alcance:** editar solo `desk/drawer/plans/workspace-documental/auditoria/infraestructura.md` y `ui.md`; escribir `runs/subagents/20261031-correccion-ws03-ws04/result-summary.md`; añadir nota de supersesión en `runs/subagents/20261031-ws02-04-checkpoint/handoff.md`; validaciones, commits y closeout por el Supervisor; PASS de Tester independiente.

**Repo:** `deskops` (cwd); fuentes externas en `../sldb`, `../pron`, `../UIs/graph_ui`. Las rutas `../` son relativas a la raíz de `deskops`.

**Límites:** no tocar código, `dag.yaml`, `reconciliacion.md`, `brief.md`, WS02, WS06, otras filas ni reabrir cierres. Si algo no se comprueba leyendo, marcar «no ejecutado»/«fuera de alcance» nombrando el test futuro sin diseñarlo. Si la fuente contradice la revisión, reportar con cita, no corregir a ciegas.

## AMBIGUEDADES

1. «Corrige exactamente estos cuatro puntos» frente a Puntos 1–5 enumerados. Obliga a decidir si el Punto 5 entra; su detalle sugiere que sí, pero el cardinal lo niega.
2. Punto 2: «SPEC.md:79-82» y «connect-dialog.js:9-17» sin repo ni ruta. Obliga a inventar ubicación.
3. Punto 3: «línea de task.txt de ../UIs/graph_ui/runs/subagents/20261031-workspace-ui» sin número de línea. Obliga a elegir cuál.
4. Punto 3: «comprobar con git que f16fcd1 elimina o cierra la TaskDoc». «Elimina o cierra» no define criterio ni evidencia admisible.
5. Validación: «git diff --stat 2286b976..HEAD» sin definir qué es `2286b976` (¿base de la tarea?). Obliga a inventar la base.
6. Roles: «escribe el handoff nuevo» sin ruta. Obliga a inferir el destino.
7. «PASS» del Tester sin criterios observables; solo se pide lectura. Obliga a inventar el umbral.
8. Punto 5: «Enlazar WS18 y WS24 donde corresponda» sin regla de correspondencia.
9. «Línea de encabezado… bajo el título» sin precisar si sustituye o añade una línea existente.
10. Punto 4: rutas «pron/models/projection.py… bajo ../pron/src» admiten dos anidamientos (`../pron/src/models/...` o `.../src/pron/models/...`).
11. «Abrir cada archivo y citar las líneas reales» sin regla si el archivo no existe (solo hay regla para contradicción).
12. Validación usa opciones `--check` y `status` no evidenciadas en el encargo; si no existen, obliga a inventar equivalentes.

Las tareas asignadas a Executor, Supervisor y Tester son trabajo futuro, no lagunas.

## DRY-RUN

**Leería:** `review-source.md`; ambos handoffs; las dos auditorías; `http_server.py`, `save_routes.py`, `store/runtime_cache.py`, `store/runtime_cache_signature.py`; `pron/models/projection.py`, `world/projection_reader.py`, `world/lexicon.py`; `SPEC.md`, `connect-dialog.js`, `task.txt`; `frontends/mindmap/projection_views.py`, `views_routes.py`, `serve.py`, `tests/test_projection_views.py`, `tests/e2e_review_workbench_views.py`; `git show/log` de los cinco hashes.

**Entregable:** dos auditorías con filas y resumen corregidos y línea de encabezado «Corrección 2026-10-31»; `result-summary.md` con antes/después y citas; nota fechada de supersesión.

**Comandos posteriores (sin ejecutar):** `test -s` de ambas auditorías; `python build_plan.py --check`; `python validate_plan.py --check`; `python context_review.py status`; `git diff --stat 2286b976..HEAD -- …`; `git show` de los hashes.

**Resultado esperado:** validaciones en verde; diff limitado a las dos auditorías y evidencia; hashes confirman cierre/actualización descritos; Tester deja `tester-result-summary.md` con PASS.
