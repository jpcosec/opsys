## REFORMULACION

**Objetivo:** corregir dos auditorías documentales (`infraestructura.md` y `ui.md`) para que reflejen seis hallazgos de revisión independiente, con citas a fuentes abiertas, sin afirmar ejecución y sin ampliar alcance.

**Alcance:** solo esos dos archivos, más evidencia en `runs/subagents/20261031-correccion-ws03-ws04/result-summary.md`. El Executor no toca handoff, commits ni validaciones: esas son tareas asignadas al Supervisor y al Tester, no lagunas.

**Repo:** `deskops` para las auditorías; lecturas en `../sldb/src/sldb`, `../pron/src`, `../UIs/graph_ui` y `../softfactory_spec/SPEC.md`.

**Límites:** no editar código de sldb, pron, graph_ui ni spec2viz; no tocar `dag.yaml`, `reconciliacion.md`, `brief.md`, WS02, WS06 ni otras filas; no reabrir cierres; lo no comprobable queda «no ejecutado: fuera de alcance», nombrando el test futuro sin diseñarlo.

## AMBIGUEDADES

1. **WS19.2 no definido.** Cita: «sin refutar al SPEC con WS19.2 sin un puente demostrado». No hay definición de WS19.2 ni del «puente». Obligaría a inventar qué es WS19.2 y qué evidencia constituiría puente.

2. **WS24 no definido.** Cita: «Enlazar WS18 y WS24 donde corresponda». Solo se describe WS18; WS24 no aparece en el bundle. Obligaría a inventar su identidad y el lugar del enlace.

3. **Uso de commits sin criterio.** Cita: «y los commits 0eb7dd7, b9ab83c y 2a15356». No dice qué debe citarse o verificarse de cada commit. Obligaría a inventar el formato de evidencia esperado.

4. **«su serve.py» sin ruta.** Cita: «citando que su serve.py sirve ese directorio sin ruta JS ni fallback». Podría ser `frontends/workspace/serve.py` o el `serve.py` de graph_ui. Obligaría a elegir un archivo no nombrado.

5. **Test futuro «sin diseñarlo».** Cita: «con el test futuro en sandbox propio que lo probaría, sin diseñarlo». No define qué cuenta como nombrar sin diseñar. Obligaría a inventar el límite entre nombrar y especificar.

## DRY-RUN

**Fuentes que leería:** task doc; `review-source.md`; `handoff.md`; ambas auditorías; rituales execution/testing/closeout; pills; `../sldb/src/sldb/cli/serve/http_server.py`, `save_routes.py`, `store/runtime_cache.py`, `store/runtime_cache_signature.py`; `../pron/src/pron/models/projection.py`, `world/projection_reader.py`, `world/lexicon.py`; `SPEC.md:79-82`; `connect-dialog.js:9-17`; `projection_views.py`, `views_routes.py`, `serve.py`, tests citados; `git show --stat` de los cinco commits.

**Entregable:** seis puntos corregidos en las dos auditorías, línea «Corrección 2026-10-31» en cada encabezado, y `result-summary.md` con antes/después y citas.

**Comandos posteriores (sin ejecutar):** `test -s` sobre ambas auditorías; `build_plan.py --check`; `validate_plan.py --check`; `context_review.py status`; `git diff --stat 2286b976..HEAD -- ...`; `git show --stat f16fcd1`, `134a665`, `0eb7dd7`, `b9ab83c`, `2a15356`; `rg` para localizar filas. **Esperado:** archivos no vacíos, checks en verde, diff restringido vacío, commits mostrando los cambios alegados y citas de línea verificables; lo no probado marcado como no ejecutado.
