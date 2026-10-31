## REFORMULACION

**Objetivo:** corregir cuatro afirmaciones documentales inexactas en dos auditorías, con citas abiertas en la fuente y sin ampliar alcance.

**Alcance:** P1 `infraestructura.md` §2.1 (expected/payload por carga runtime sujeta a cache, límite de frescura, citar `http_server.py`, `save_routes.py`, `runtime_cache.py`, `runtime_cache_signature.py`; no afirmar cache fresca; mantener no-CAS y expected como comparación optimista pública por valor). P2 `ui.md` (+Add relation vs `SPEC.md:79-82` y `connect-dialog.js:9-17` → capacidad no cubierta/no comprobada, sin refutar el SPEC). P3 `ui.md` línea de `task.txt` como snapshot histórico, verificando `f16fcd1` y `134a665`. P4 `infraestructura.md` consultas guardadas vs `pron.ProjectionDoc` (`projection.py:14`, `projection_reader.py:22`, `lexicon.py:137`). Más una línea de encabezado fechada por archivo y `result-summary.md` con antes/después.

**Repo:** `/home/jp/proyectos/SLDB_1/deskops`; lecturas en `../sldb/src`, `../pron/src`, `../UIs/graph_ui`.

**Límites:** el Executor edita solo esos dos `.md`; sin código, `dag.yaml`, `reconciliacion.md`, `brief.md`, WS02/WS06, otras filas ni reabrir cierres. Lo no comprobable queda «no ejecutado/fuera de alcance» con test futuro nombrado, sin diseñarlo. Contradicción de fuente → reportar con cita, no corregir a ciegas.

**Tareas futuras asignadas (no lagunas):** nota de supersesión fechada y handoff nuevo por el Supervisor; validaciones, commits y closeout por el Supervisor; PASS por Tester de solo lectura.

## AMBIGUEDADES

1. «git diff --stat 2286b976..HEAD sobre deskops, tests, dag.yaml y reconciliacion.md vacío»: el entregable vive dentro de `deskops/desk/drawer/...`, y no se dice si «deskops» excluye `desk/drawer` ni qué commit es `2286b976`. Obligaría a inventar una exclusión de ruta y la base del diff.
2. «python desk/drawer/plans/workspace-documental/build_plan.py --check» junto a «Agregar a cada archivo una línea en su encabezado»: no consta si las auditorías son fuente o artefacto generado; si son generadas, la línea manual se pierde o rompe `--check`. Obligaría a inventar su provenance.
3. «las filas de cache y resumen» y «una nota de supersesión fechada»: no se define qué filas componen «cache», ni el formato/fecha de la nota en `handoff.md`. Obligaría a inventar alcance de filas y sintaxis de la nota.

## DRY-RUN

**Leería:** task doc, `review-source.md`, `infraestructura.md`, `ui.md`, los cuatro archivos de sldb citados, `SPEC.md:79-82`, `connect-dialog.js:9-17`, `projection.py:14`, `projection_reader.py:22`, `lexicon.py:137`, `task.txt` de graph_ui; `git show --stat` de `f16fcd1` y `134a665`.

**Entregable:** dos `.md` con solo las filas de los cuatro puntos y su encabezado fechado, más `result-summary.md` con antes/después y citas, sin afirmar nada ejecutado.

**Comandos después (no ejecutados):** `test -s` de ambos `.md` → existen; `build_plan.py --check`, `validate_plan.py --check`, `context_review.py status` → exit 0; `git show --stat f16fcd1 134a665` → cierre de TaskDoc y actualización de Board; `git diff --stat 2286b976..HEAD -- tests dag.yaml reconciliacion.md` → vacío (sujeto a ambigüedad 1).
