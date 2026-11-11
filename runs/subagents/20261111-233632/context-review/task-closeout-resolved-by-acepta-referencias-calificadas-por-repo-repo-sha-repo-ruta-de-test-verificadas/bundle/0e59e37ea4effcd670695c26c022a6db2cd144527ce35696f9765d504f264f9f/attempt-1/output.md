## REFORMULACION
Encargo (task.code, ejecutable por un worker, un solo repo: deskops): que `deskops closeout resolved-by` acepte referencias calificadas `<repo>:<sha>` y `<repo>:<ruta de test>`, resolviendo `<repo>` contra el registro del ecosistema y verificando el commit ancestro y el test en la raíz de ese repo, guardando la referencia tal cual en los trailers. Resultado esperado: c1–c5 (parseo, verificación, resolución por registro, ayuda CLI, tests, docs/CHANGELOG). Límites: fuera `closeout verify`/`commit`, la opción a (`task.external`) y `supersede`.

## AMBIGUEDADES
1. «una referencia calificada tiene la forma `<repo-id>:<valor>`… Una referencia sin prefijo, o con un prefijo que no es un repo registrado, se trata como hoy»: no dice dónde se corta (primer `:` o último) ni si un valor con `:` propio se admite; obliga a inventar el parseo.
2. «Si la raíz registrada no existe en la máquina, se rechaza con un error que nombra el repo y la ruta»: no fija texto, tipo de error ni código de salida; obliga a inventarlos.
3. «la resolución del repo por el registro (deskops/identity.py)»: no dice qué store/`ecosystem_root` usa `ClosureService` para cargar el registro (¿`.sldb` del root? ¿`--store`?); obliga a elegir.
4. «los tests gate… con las mismas reglas que reference_points_to_test» y «Los files de la tarea no amplían los tests de otro repo»: no aclara si `files` sigue ampliando las referencias sin prefijo mientras solo las calificadas lo ignoran; obliga a decidir.
5. «suite completa de a un archivo desde /dev/shm» y «4 pasos del CI de deskops»: no enumera comando ni pasos; obliga a inventarlos.

## DRY-RUN
Lecturas: TaskDoc, `closeout_gates.py`, `closure.py`, `identity.py`, `cli/commands/closeout.py`, `tests/` de resolved-by y closeout, `docs/operator-manual.md`, `CHANGELOG.md`. Cambios previstos: helper de parseo de referencia calificada y variantes de `reference_points_to_commit`/`reference_points_to_test` con raíz y `files` explícitos; `close_resolved_by` resuelve el registro y pasa la raíz del repo; help; tests con dos repos git en `tmp_path` registrados (cierre, sha no ancestro, test inexistente, repo no registrado, raíz ausente); docs y CHANGELOG. Dependencias: git, store/registro sldb, `RepositoryDoc`. Validaciones futuras (no ejecutadas): tests nuevos de a uno, tests existentes, suite completa archivo por archivo, 4 pasos de CI en clon limpio.

## FUTURO
El worker implementa y entrega; el coordinador corre los 4 pasos del CI; la decisión revisable de acotar a resolved-by y el ítem de drawer de la opción a los resuelve un humano.
