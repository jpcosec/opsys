## REFORMULACION
Nodo ejecutable (`task.code`), no agregado, en el repo `deskops`. Propósito: retirar las guardas de deskops que esquivaban H1-H3 de sldb, para que retire, supersede y resolved-by cierren por CLI varias tareas inválidas del mismo modelo, y `desk update --apply` repare un desk con documentos inválidos. Resultado: g1-g5, tests con caché fría/caliente, docs/CHANGELOG y baja del ítem 75e33dab. Límites: no cambiar sldb; conservar migración de estados heredados y su escritura por frontmatter; fuera el listado de tareas inválidas del doctor (pero ver ambigüedad 2).

## AMBIGUEDADES
1. "variable de entorno SLDB_SRC si la tarea de SLDB_SRC ya entró, o la ruta hermana en la copia": no define cómo detectar si entró ni cuál ruta hermana; obliga a inventar el mecanismo de selección.
2. "el listado de tareas inválidas del doctor" figura fuera de alcance, pero g3 pide que "el doctor listan los documentos inválidos por el hallazgo store/doc-invalid"; hay que decidir si se modifica; obliga a resolver el conflicto.
3. "sin duplicarlos": no fija clave ni prioridad de deduplicación; obliga a inventarla.
4. "Si stores check falla de verdad (sin informe y sin documentos inválidos que lo expliquen)": no define "de verdad" ni cómo distinguirlo; obliga a inventar la condición.
5. "las dos funciones si quedan sin uso": exige verificar todos los llamadores, no listados; obliga a asumir el alcance del borrado.
6. "siempre con caché frío además del caliente": no dice qué tests ni cómo preparar caché fría; obliga a inventar el harness.

## DRY-RUN
Lecturas: `closure.py`, `desk.py`, `doctor_findings.py`, tests, `operator-manual.md`, `CHANGELOG.md`; verificar `store/doc-invalid` en sldb. Cambios previstos: g1 quitar llamadas/funciones; g2 no saltar reparaciones; g3 deduplicar listados; g4 reescribir tests H2 y añadir fríos; g5 docs/CHANGELOG. Dependencias: sldb main corregido, `SLDB_SRC`/ruta hermana, `/dev/shm`. Validaciones futuras: tests de closeout/heredados, suite por archivo contra sldb corregido y 4 pasos CI. No se ejecuta nada.

## FUTURO
Otro nodo/equipo entrega sldb corregido y confirma `store/doc-invalid`; el coordinador ejecuta los 4 pasos CI; el worker ejecuta pruebas; un humano o la CLI da de baja el ítem 75e33dab.
