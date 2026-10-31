## REFORMULACION

**Objetivo.** Corregir seis afirmaciones documentales inexactas detectadas por revisión independiente en `desk/drawer/plans/workspace-documental/auditoria/infraestructura.md` y `ui.md`, con citas abiertas de fuente, sin afirmar nada ejecutado y sin ampliar alcance.

**Alcance.** Solo esas dos auditorías y sus líneas de encabezado; nota de supersesión en `runs/subagents/20261031-ws02-04-checkpoint/handoff.md`; `handoff-correccion.md`; `result-summary.md`; `tester-result-summary.md`. Fuera: código de sldb/pron/spec2viz/graph_ui, `dag.yaml`, `reconciliacion.md`, `brief.md`, WS02, WS06, demás filas y reapertura de cierres.

**Repo.** Raíz de `deskops`; rutas `../` relativas a ella. CWD actual es `/home/jp/proyectos/SLDB_1/deskops`.

**Roles (tareas asignadas, no lagunas).** Executor edita dos archivos y escribe `result-summary.md`; Supervisor añade nota fechada, escribe handoff nuevo, valida, commitea y cierra; Tester independiente de solo lectura emite PASS.

**Límites.** Si la fuente contradice la revisión: reportar con cita, no corregir a ciegas. Lo no comprobable leyendo: «no ejecutado: fuera de alcance», nombrando el test futuro sin diseñarlo.

## AMBIGUEDADES

1. «la línea del encabezado de discrepancias (hoy ui.md:42)» frente a la precisión «Línea de encabezado: una línea de texto bajo el título». Hay dos usos de «encabezado»; obliga a inventar si la corrección del Punto 3 sustituye esa línea de tabla o si además se añade la línea bajo el título.
2. Referencias por número de línea («ui.md:42») tras insertar la línea de cabecera: obliga a decidir si el ancla es el número o el contenido citado.
3. «git diff --stat 2286b976..HEAD -- deskops/ … queda vacío (deskops/ es el paquete de código, no el repo)»: no se explicita en qué repo se ejecuta el diff ni cómo se concilia `deskops/` como ruta con el CWD dentro de `deskops`. Obliga a inferir la raíz git.
4. Los comandos de Validation se escriben con rutas relativas a la raíz (`desk/drawer/...`) pero no se declara el directorio de ejecución; obliga a asumir raíz del repo, no CWD.
5. «el archivo de la TaskDoc» en `git show --stat f16fcd1`: no se nombra el fichero; obliga a identificarlo por el stat.
6. «la lista de 35 nodos graph_ui»: si el conteo real difiere, la instrucción de añadir WS18 como nota/fila solo referencia queda sin criterio. Obliga a decidir entre mantener 35 o corregir el número.
7. Punto 1: base de rutas de `http_server.py` y `save_routes.py` («en ../sldb/src/sldb») no distingue subdirectorio; obliga a asumir que ambos están en `src/sldb/` y los `store/` en `src/sldb/store/`.
8. «sin diseñarlo» (test futuro): no define el umbral entre nombrar y diseñar.

## DRY-RUN

**Fuentes a leer:** `review-source.md`; `handoff.md`; ambos archivos de auditoría; en `../sldb/src/sldb`: `http_server.py`, `save_routes.py`, `store/runtime_cache.py`, `store/runtime_cache_signature.py`; `../softfactory_spec/SPEC.md:79-82`; `../UIs/graph_ui/.../connect-dialog.js:9-17`; `projection_views.py`, `views_routes.py`, `serve.py`, `tests/test_projection_views.py`, `tests/e2e_review_workbench_views.py`; en `../pron/src`: `models/projection.py:14`, `world/projection_reader.py:22`, `world/lexicon.py:137`; `context-review.md`.

**Entregable:** dos auditorías corregidas con citas y línea de corrección fechada; `result-summary.md` con antes/después por fila; nota de supersesión y `handoff-correccion.md`; `tester-result-summary.md` con PASS.

**Comandos posteriores (no ejecutados):** `test -s` de ambas auditorías → exit 0; `build_plan.py --check` y `validate_plan.py --check` → sin errores; `context_review.py status` → estado coherente; `git show --stat f16fcd1`, `134a665`, `0eb7dd7`, `b9ab83c`, `2a15356` en `../UIs/graph_ui` → confirmación de borrado/actualizaciones citadas; `git diff --stat 2286b976..HEAD ...` → vacío.
