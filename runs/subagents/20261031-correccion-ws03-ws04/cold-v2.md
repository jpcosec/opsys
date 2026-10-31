REFORMULACION

**Objetivo:** corregir dos auditorías authored (`infraestructura.md` y `ui.md`) para que coincidan con las fuentes en los puntos 1–4 y el punto 5 (ViewDoc), con citas literales de líneas reales, sin afirmar nada ejecutado ni ampliar el producto.

**Alcance:** solo esos dos archivos; evidencia en `runs/subagents/20261031-correccion-ws03-ws04/result-summary.md` (antes/después por fila), línea de encabezado «Corrección 2026-10-31» en cada auditoría, nota de supersesión fechada en `runs/subagents/20261031-ws02-04-checkpoint/handoff.md` sin borrar el original, y `tester-result-summary.md` por Tester independiente de solo lectura con PASS.

**Repo:** deskops (`/home/jp/proyectos/SLDB_1/deskops`). Lectura en `../sldb`, `../pron` y `../UIs/graph_ui`.

**Límites:** no tocar código de sldb/pron/spec2viz/graph_ui, `dag.yaml`, `reconciliacion.md`, `brief.md`, WS02, WS06, otras filas ni cierres previos; no ejecutar tests de producto; lo no comprobado queda «no ejecutado» o «fuera de alcance» nombrando el test aislado futuro sin diseñarlo; si la fuente contradice la revisión, reportar con cita.

AMBIGUEDADES

1. **Cuatro vs. cinco puntos.** Rationale: «cuatro afirmaciones documentales inexactas»; Scope: «Corrige exactamente estos cuatro puntos»; luego «Punto 5, ViewDoc…»; Done When: «Los cuatro puntos están corregidos». Obliga a inventar si el punto 5 entra en el PASS del Tester y en el cierre, o queda fuera.

2. **Ruta del handoff nuevo.** «El Supervisor agrega en `runs/subagents/20261031-ws02-04-checkpoint/handoff.md` una nota de supersesión fechada, sin borrar el texto original, y escribe el handoff nuevo.» No se indica dónde va el handoff nuevo; obliga a inventar su ruta.

3. **Localización de fuentes incompletas.** «Abrir `http_server.py`, `save_routes.py`, `store/runtime_cache.py` y `store/runtime_cache_signature.py` en `../sldb/src/sldb`»; review-source solo cita `save_routes.py:38–40` sin subruta. Igual ocurre con «`SPEC.md:79-82`» y «`connect-dialog.js:9-17`», sin repo ni directorio. Obliga a asumir rutas para poder citar líneas reales.

4. **Commit base de validación no definido.** «`git diff --stat 2286b976..HEAD …` queda vacío». No se define qué es `2286b976` ni cómo obtenerlo si no existe; obliga a inventar el punto de comparación.

No son lagunas, sino tareas futuras asignadas: nombrar el test aislado futuro sin diseñarlo; enlazar WS18/WS24; elegir «nota o fila solo referencia»; mantener separados modelo/evaluador/renderer/notación; no anunciar aceptación del producto ampliado.

DRY-RUN

**Fuentes que leería:** task doc, `review-source.md`, rituales execution/testing/closeout, pills 001/005/007, ambas auditorías y handoff WS02–WS04; en `../sldb`: `http_server.py`, `save_routes.py`, `runtime_cache.py`, `runtime_cache_signature.py`; en `../pron`: `models/projection.py`, `world/projection_reader.py`, `world/lexicon.py`; en `../UIs/graph_ui`: `SPEC.md`, `connect-dialog.js`, `frontends/mindmap/projection_views.py`, `views_routes.py`, `serve.py`, `tests/test_projection_views.py`, `tests/e2e_review_workbench_views.py`, `runs/subagents/20261031-workspace-ui/task.txt`, y `git show` de `f16fcd1`, `134a665`, `0eb7dd7`, `b9ab83c`, `2a15356`.

**Entregable:** `result-summary.md` con antes/después y citas; encabezados fechados en ambas auditorías; nota de supersesión en handoff; `tester-result-summary.md` con PASS.

**Comandos posteriores:** `test -s` de ambas auditorías; `build_plan.py --check`; `validate_plan.py --check`; `context_review.py status`; `git diff --stat 2286b976..HEAD -- …`; `git show`/`git ls-files` para verificar commits y archivos; `deskops closeout verify/commit` según ritual.

**Resultado esperado:** checks OK, diff prohibido vacío, citas abiertas, Tester PASS, un único commit de cierre.
