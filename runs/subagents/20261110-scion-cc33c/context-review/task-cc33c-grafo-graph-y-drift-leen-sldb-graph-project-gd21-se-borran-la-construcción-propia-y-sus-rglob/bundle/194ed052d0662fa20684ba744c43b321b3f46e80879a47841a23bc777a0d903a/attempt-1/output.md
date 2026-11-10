## REFORMULACION

Encargo del nodo CC33c (plan `deskops-como-config`, dag rev 4; parte 4 del agregado CC33), en el repo `deskops`: hacer que `graph build|neighbors|missing|reflect` y `drift` lean el grafo de proyecto de sldb (GD21) mediante `sldb.api.project_graph(store)` y la configuración de `deskops/graph/desk_graph.py`. Resultado: `snapshot.py` y su construcción propia borrados; `rglob` de `checks.py` y `self_reflection.py` eliminados; `neighbors` y `missing` semánticamente iguales al oráculo v1 sobre copia de `desk/` y `.sldb/` en `/dev/shm`; oráculo borrado después, en commit propio; goldens y gramática CLI idénticos; `deskops doctor` sin hallazgos nuevos en los 6 desks; CHANGELOG y tabla de líneas antes/después. Límites: no se toca closeout (`closure.py`), no se invoca el CLI `sldb graph project`, no se regeneran goldens, no se inventa migración de `drift` si no lee `snapshot.py` ni hace `rglob`, y b14/b15 mandan sobre el borrado de `declared_target_is_a_file`.

## AMBIGUEDADES

Ninguna: las tensiones del contrato están resueltas por precisiones posteriores y con precedencia declarada.

1. «drift leen el grafo de proyecto» frente a b10/b16, que lo condicionan a inspeccionar `drift.py`; resuelto por b16.  
2. «se borra el rglob de checks.py» frente a b14/b15, que ordenan PARAR y conservar la excepción si `project_graph` no crea los dos nodos; resuelto por b15.  
3. «el enlace atom/materialization que usa el closeout… se lee de ese grafo» frente a b4, que prohíbe editar `closure.py`; resuelto por b4.

## DRY-RUN

Lecturas: TaskDoc, pills 008–011 y drift, `graph.py`, `drift.py`, `desk_graph.py`, `snapshot.py`, `checks.py`, `self_reflection.py`, tests y oráculo v1.  
Cambios previstos: ejecutar `project_graph` sobre la copia de `ba982a45` y registrar los nodos de `dag.yaml` y `model_contract_hashes.json`; migrar comandos a `sldb.api.project_graph`; borrar `snapshot.py` y `rglob`; decidir la excepción según b14; actualizar tests y CHANGELOG.  
Dependencias: `sldb.api.project_graph`, configuración de `desk_graph.py`, CC38 cerrada.  
Validaciones futuras, sin ejecutar: paridad semántica con el oráculo; tests de a uno; goldens desde `/dev/shm`; `wc -l`; `doctor` en 6 desks; cuatro pasos del workflow; commit final que borra `tests/graph_oracle_v1/`.

## FUTURO

El coordinador ejecuta los cuatro pasos en clon limpio, decide la parada de b14 y valida doctor; el supervisor corre la suite completa. Si la excepción queda, se envía hipótesis a sldb. CC33a/b coordinan si el closeout leía `snapshot.py`.
