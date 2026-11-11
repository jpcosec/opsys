REFORMULACION

Nodo de revisión cold-bundle, no ejecutable: no implementa ni ejecuta nada. Su propósito es reformular el encargo de `task-closeout-resolved-by...` y producir un DRY-RUN del cambio futuro, usando el TaskDoc, los rituales enrutados por el Board, las pills/átomos ligados y los archivos nombrados. Resultado: las secciones pedidas, en español. El encargo revisado: que `deskops closeout resolved-by` cierre por CLI una tarea que TaskDoc rechaza leyendo su frontmatter como supersede/retire, con el mismo commit y trailers y las compuertas de ref/test, y que rechace antes de escribir si hay otra inválida en el mismo modelo, nombrando sldb H2 y la vía manual. Repo: deskops. Límites: solo input; fuera cerrar dos inválidas en el mismo modelo y escribir en sldb.

AMBIGUEDADES

1. «depende de sldb H2 (nota de sldb 3895e9f7, sin resolver)»: H2 no se define; obliga a inventar qué hipótesis es y el texto exacto de la vía manual.
2. «las compuertas de --ref y --test son las de hoy»: “hoy” no fija commit ni versión; obliga a elegir una línea base.
3. «4 pasos del CI de deskops en clon limpio»: no se enumeran; obliga a inventar los comandos del CI.
4. «con store y una sola inválida, cierra» frente a r3 «si hay otra tarea inválida»: no aclara si la tarea cerrada cuenta como inválida; obliga a definir el alcance del chequeo.
5. «los mismos trailers (Closeout-Mode: resolved-by)»: no enumera el conjunto; obliga a decidir si incluye `Task-Id`, `Closeout-Reason`, `Closeout-Ref` y `Closeout-Test`.

DRY-RUN

Un ejecutor futuro leería `deskops/services/closure.py` (`close_resolved_by`, `close_superseded`), `deskops/cli/commands/closeout.py`, `deskops/workspace.py` (`rewrite_task_fields`, `_model_errors`, estados heredados), tests de closeout y goldens, docs y CHANGELOG. Factorizaría la rama de respaldo de supersede: si TaskDoc rechaza, leería `files` y frontmatter sin modelo, escribiría `status: resolved` e `history` con `resolved-by` mediante `rewrite_task_fields`, revalidaría y restauraría si falla. Aplicaría las mismas compuertas de `--ref`/`--test` usando los `files` del frontmatter. Con store, comprobaría otras tareas inválidas del mismo modelo antes de escribir y rechazaría nombrando sldb H2 y la vía manual. Añadiría tests sin store, con store y una inválida, y con dos inválidas; actualizaría docs y CHANGELOG. Validaría esos tests, luego `test_closeout`, `test_closeout_resolved_by`, `test_legacy_task_states` y goldens de a uno, y finalmente los 4 pasos del CI. Dependencia abierta: sldb H2 para el caso de dos inválidas.
