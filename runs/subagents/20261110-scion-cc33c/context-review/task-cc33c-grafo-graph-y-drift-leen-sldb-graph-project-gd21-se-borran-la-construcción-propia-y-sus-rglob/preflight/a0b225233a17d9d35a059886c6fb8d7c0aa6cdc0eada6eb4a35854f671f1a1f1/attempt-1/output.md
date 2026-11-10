## REFORMULACION
Nodo ejecutable `task.code`, no agregado ni paquete. **Propósito:** migrar las superficies `graph build|neighbors|missing|reflect` y, si corresponde, `drift` de deskops para que lean `sldb.api.project_graph(store)` con la configuración de `deskops/graph/desk_graph.py`, eliminando la construcción propia. **Resultado:** paridad semántica de `neighbors` y `missing` con el oráculo v1; borrado de `graph/snapshot.py` y de los `rglob` según b14/b15; borrado posterior de `tests/graph_oracle_v1/`; goldens idénticos; `doctor` sin hallazgos nuevos; CHANGELOG y evidencia de líneas. **Repo:** deskops, worktree fijado por el coordinador, base origin/main `ba982a45`. **Límites:** no closeout/CC33a-b, selectores, escrituras, `closure.py`, CLI `sldb graph project` ni regeneración de goldens; `drift` solo se toca si lee `snapshot.py` o hace `rglob`; la excepción `declared_target_is_a_file` solo se borra si b14 confirma ambos nodos.

## AMBIGUEDADES
ninguna. Las condiciones sobre `drift`, `rglob`, oráculo, goldens, doctor, workflow y precedencias están resueltas en b5-b18.

## DRY-RUN
Hipotéticamente: leer TaskDoc, pills, `desk_graph.py`, `snapshot.py`, `checks.py`, `self_reflection.py`, `graph.py`, `drift.py`, tests y goldens; registrar SHA; copiar `desk/` y `.sldb/` a `/dev/shm`; ejecutar `project_graph` para la evidencia b14; inspeccionar `drift.py`; implementar la lectura única; borrar snapshot y rglobs según b14/b15; adaptar tests; correr tests de archivo uno a uno; comparar `neighbors`/`missing` con el oráculo; registrar `wc -l`; actualizar CHANGELOG/docs; commit de implementación y commit separado que borra el oráculo. Dependencias: `sldb.api.project_graph`, configuración de `desk_graph.py`, copia real del desk. Validaciones futuras: goldens idénticos, grep, `doctor` en 6 desks y 4 pasos del workflow. Sin ejecutar nada.

## FUTURO
El coordinador fija el worktree y corre suite completa, 4 pasos y `doctor`; el supervisor decide revisiones y aceptación; CC33a/b integra closeout; sldb resuelve el rendimiento de `rule_graph`; si b14 no crea los nodos, el worker para y el coordinador decide la hipótesis para sldb; si cambia un golden, un humano revisa el diff.
