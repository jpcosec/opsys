## REFORMULACION

**Propósito:** reducir a ≤2,5 s el tiempo de `deskops view board` (store construido, proceso nuevo, mediana de 3) sin cambiar su salida, construyendo una vez por corrida lo que hoy se rehace por tarjeta: transiciones/gates, contexto de closeout, grafo del desk y snapshot de lectura, y abriendo el store menos veces.

**Resultado:** perfil antes/después con conteo de llamadas a `open_store`, `desk_graph` y `build_closeout_graph_context`; salida byte a byte idéntica de `view board` y `view task`; tests, suite completa y CI en verde; docs y CHANGELOG; si no se llega a 2,5 s, informe con la medición y qué parte corresponde a sldb.

**Repo/superficie:** deskops (`cli/commands/view.py`, `services/tasks.py`, `services/closeout_gates.py`, `lifecycle.py`, `graph/desk_graph.py`, `operations.py`, `tests/`, docs, CHANGELOG).

**Límites:** fuera sldb (memoizar `open_store`/`migrate_store_layout` es hipótesis para sldb), cambiar lo que muestra el board o el contrato de la vista, y `view task` salvo código compartido. Sin estado global que sobreviva a la corrida.

## AMBIGUEDADES

1. «mediana de 3, store construido, proceso nuevo» / «caché frío y caliente»: no se define si «construido» incluye `.sldb_cache` y la caché de composición. Obligaría a inventar qué estado de caché cuenta para el umbral.
2. «la tarea H11 de sldb está integrada en sldb main; esta tarea corre contra ese sldb»: no se indica checkout/commit ni ruta del paquete. Obligaría a inventar contra qué árbol de sldb medir.
3. «el layout del benchmark de H11»: se citan commits pero no dónde reside el layout ni cómo obtenerlo. Obligaría a inventar la ruta del banco de pruebas.
4. «las llamadas de deskops que abren el store por tarjeta se reducen a las necesarias, con el mismo manejo de errores»: «necesarias» y «mismo manejo» no fijan umbral ni conducta observable (hoy `_gates` traga excepciones y `_closeout` las registra). Obligaría a inventar cuántas llamadas y qué errores deben preservarse.
5. «un test la compara contra una corrida con el camino viejo, o con los goldens existentes si cubren el caso»: no se dice si los goldens cubren el caso y el «o» deja dos diseños. Obligaría a inventar el mecanismo de comparación.

## DRY-RUN

**Lecturas:** los seis archivos listados, tests de vista/goldens, informe del worker de H11 y CHANGELOG; verificar precondición H11 antes de medir. **Cambios previstos:** p1 perfil con cProfile y línea base commiteada; p2 construir grafo/closeout una vez y pasarlos por `ReadSnapshot` o parámetro explícito; p3 reducir aperturas del store conservando errores; p4 test/golden de igualdad de salida y de `view task`; p5 docs y CHANGELOG. **Dependencias:** sldb con H11 integrado; layout de H11; store construido. **Validaciones futuras:** benchmark mediana de 3 antes/después, perfil con conteos, igualdad byte a byte, suite de a un archivo desde /dev/shm, CI de 4 pasos (coordinador), `ci-knowledge-check` y `graph missing`.

## FUTURO

El coordinador ejecuta los 4 pasos del CI en clon limpio y decide si el umbral o el coste de sldb quedan explicados; el worker se detiene ante golden cambiado o precondición ausente.
