## REFORMULACION
Encargo: en el repo deskops, migrar los comandos `graph build|neighbors|missing|reflect` y `drift` para que lean el ProjectGraph de sldb vía `sldb.api.project_graph(store)` usando la configuración de `deskops/graph/desk_graph.py` (GD21). Resultado: `graph/` sin construcción propia (`snapshot.py`), sin `rglob` (`checks.py`, `self_reflection.py`) y sin excepción de targets declarados si GD21 crea esos nodos; `neighbors`/`missing` semánticamente iguales al oráculo v1 sobre copia en `/dev/shm` del desk real, y `tests/graph_oracle_v1/` borrado en commit propio posterior. Límites: no toca closeout (CC33a/b), selectores, escrituras, `closure.py` ni formato del desk/gramática CLI; goldens idénticos; `CHANGELOG.md` actualizado.

## AMBIGUEDADES
1. “`graph build|neighbors|missing|reflect`”; la aceptación solo exige igualdad para “`neighbors` y `missing`”. Obligaría a inventar el criterio de corrección de `build` y `reflect`.
2. “`drift` leen el grafo de proyecto” frente a b8: “solo cambia lo que lea el snapshot propio … o haga rglob”. Si no lee ninguno, obligaría a inventar si hay cambio real en `drift.py`.
3. “líneas de `graph/` antes y después” sin formato ni umbral: obligaría a inventar el reporte.
4. “`desk/` y `.sldb/` de main al despachar”: obligaría a fijar el SHA exacto de la copia.
5. “`deskops doctor` sin hallazgos nuevos en los 6 desks”: “nuevos” sin baseline explícito; obligaría a inventar la referencia.
6. “se borran … el rglob de `checks.py`” convive con a4/b3 (excepción condicional `declared_target_is_a_file`); obligaría a inventar qué se borra si GD21 no crea los nodos.

## DRY-RUN
Lecturas: `graph/snapshot.py`, `checks.py`, `self_reflection.py`, `desk_graph.py`, `cli/commands/{graph,drift}.py`, tests oráculo y goldens. Cambios: sustituir snapshot por `sldb.api.project_graph(store)`, eliminar `snapshot.py` y rglob, resolver a4 con evidencia, borrar oráculo en commit propio, `CHANGELOG.md`. Dependencias: GD21 en main, `sldb.api.project_graph`, store `.sldb`. Validaciones futuras: comparación semántica con oráculo, `grep rglob`, goldens sin regenerar, doctor en 6 desks, 4 pasos en clon limpio.

## FUTURO
Coordinador/supervisor: corre los 4 pasos del workflow en clon limpio y la suite; decide cold-bundle; coordina con CC33a/b si `closure` leía `snapshot.py`. Humano: promoción con `deskops add task --from-drawer`. Otro nodo: arreglo de rendimiento de `rule_graph` en sldb.
