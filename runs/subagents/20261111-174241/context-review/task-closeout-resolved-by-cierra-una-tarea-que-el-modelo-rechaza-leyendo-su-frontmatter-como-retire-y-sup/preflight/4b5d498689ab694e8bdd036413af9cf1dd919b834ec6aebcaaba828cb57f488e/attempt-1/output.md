## REFORMULACION

El nodo debe modificar `deskops closeout resolved-by` para cerrar por CLI una tarea que el modelo `TaskDoc` rechaza, leyendo su frontmatter como ya hace `supersede`. Resultado: mismo commit, trailers (`Closeout-Mode: resolved-by`) y compuertas `--ref`/`--test` que una tarea válida; rama de respaldo compartida y no duplicada; con store y otra tarea inválida en el mismo modelo, rechazo previo a escribir, nombrando sldb H2 y vía manual. Repo/superficie: `deskops/services/closure.py`, `deskops/cli/commands/closeout.py`, `deskops/workspace.py`, `tests/`, `docs/operator-manual.md`, `docs/workflow-policy-reference.md`, `CHANGELOG.md`. Límites: no cerrar dos inválidas en el mismo modelo (depende de sldb H2, sin resolver); no escribir en sldb; la ruta de tareas válidas no cambia.

## AMBIGUEDADES

1. “escribe status resolved e history [..., <el evento de cierre que corresponda>]”: no se nombra el evento; obligaría a inventar su identificador exacto.
2. “con el mismo commit”: no se especifica si es HEAD, el commit de reproducción `60f1ec37` u otro; obligaría a elegir.
3. “CAUSA (a confirmar)”: no se indica cómo confirmarla ni dónde registrarla; obligaría a inventar el procedimiento.
4. “un mensaje que nombra sldb H2 y la vía manual”: no hay texto literal; obligaría a redactarlo.
5. “los 4 pasos del CI de deskops”: no se enumeran; obligaría a inventar cuáles son.
6. “con store y una sola inválida, cierra y stores check queda en rc 0”: “stores check” no se define; obligaría a asumir el comando.

## DRY-RUN

Lecturas previstas: `closure.py` (`close_resolved_by`, `close_superseded`), `closeout.py`, `workspace.py` (`rewrite_task_fields`), tests de closeout/legacy y goldens, docs y CHANGELOG. Cambios previstos: factorizar la rama de respaldo; aplicarla a `resolved-by`; añadir chequeo de store con mensaje H2; tests nuevos y actualización de docs/CHANGELOG. Dependencias: modelo `TaskDoc` para revalidar; reproducción del coordinador; sldb H2 solo limita el caso de dos inválidas. Validaciones futuras: tests nuevos de inválida sin/con store y de dos inválidas; `test_closeout`, `test_closeout_resolved_by`, `test_legacy_task_states` y goldens, de a uno; grep de closeout; CI de 4 pasos en clon limpio.

## FUTURO

El coordinador ejecuta los 4 pasos del CI y aporta/valida la reproducción. Otro nodo o un humano resuelve sldb H2 para el caso de dos inválidas. Un humano aprueba el texto exacto del mensaje y los cambios de docs/CHANGELOG.
