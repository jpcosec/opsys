## REFORMULACION
Nodo ejecutable (`task.code`), no agregado. Encargo: en el repo deskops, migrar `deskops graph build|neighbors|missing|reflect` y `drift` para que lean el grafo de proyecto de sldb (GD21) usando la configuración de `deskops/graph/desk_graph.py`; borrar la construcción propia (`graph/snapshot.py`), el `rglob` de `checks.py` y los de `self_reflection.py`. Resultado: `neighbors` y `missing` equivalentes al oráculo v1 sobre el desk real; después se borra `tests/graph_oracle_v1/` en commit propio; sin `rglob` en `deskops/graph/`; goldens y doctor sin cambios no previstos. Límites: solo `deskops/graph/`, `cli/commands/graph.py`, `cli/commands/drift.py`, `tests/` y `CHANGELOG.md`; fuera closeout, selectores y escrituras; no cambia el formato del desk ni la gramática del CLI.

## AMBIGUEDADES
1. «sldb.api.project_graph (o sldb graph project)»: no fija la interfaz exacta; obligaría a inventar qué API o comando invocar.
2. «Este nodo decide si el grafo de sldb ya crea esos nodos… Si los crea… Si no…»: no da criterio ni evidencia de decisión; obligaría a inventar cómo determinarlo.
3. «goldens de ayuda y salida idénticos» frente a «su test cambia a «aparece como nodo»»: posible conflicto si cambia la salida de `graph missing`; obligaría a elegir precedencia.
4. «se conserva hasta la aceptación y luego se borra» frente a «en un commit propio»: no aclara si el borrado es parte de este nodo o un commit posterior; obligaría a inventar el momento.
5. «4 pasos del workflow en clon limpio»: no los enumera; obligaría a inventar cuáles son.
6. «drift leen el grafo de proyecto»: `drift.py` ejecuta varias comprobaciones; no aclara si migran todas o solo `drift_check_knowledge_surfaces`; obligaría a inventar el alcance.

## DRY-RUN
Lecturas: TaskDoc y contrato dag, `desk_graph.py`, `snapshot.py`, `checks.py`, `self_reflection.py`, `graph.py`, `drift.py`, oráculo v1, goldens y CHANGELOG. Cambios previstos: sustituir lecturas del snapshot propio por sldb; borrar `snapshot.py`, `rglob`s y pruebas obsoletas; ajustar tests y CHANGELOG. Dependencias: CC38 en main, GD21, API de sldb disponible, copia del desk real en `/dev/shm`. Validaciones futuras, sin ejecutar: comparar con oráculo v1; `grep -rn rglob deskops/graph/` vacío; `pytest` de archivos de a uno; `test_cli` y goldens desde `/dev/shm` sin `--update-golden`; 4 pasos del workflow; doctor en 6 desks; CHANGELOG.

## FUTURO
El supervisor decide revisiones en frío y corre la suite completa integrada; el coordinador fija worktree y ejecuta workflow/doctor; si la excepción de `a4` queda, se anota hipótesis para sldb. El closeout CC33a leerá el enlace atom/materialization de este grafo.
