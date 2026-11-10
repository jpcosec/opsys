REFORMULACION
Propósito: sustituir en deskops la construcción propia del grafo por la lectura del grafo de proyecto de sldb (GD21), configurado con `deskops/graph/desk_graph.py`, en `graph build|neighbors|missing|reflect` y `drift`, borrando el código viejo en el mismo paso (invariante 3). Resultado: `neighbors` y `missing` equivalentes al oráculo v1, sin `rglob` en `deskops/graph/`, `snapshot.py` borrado, goldens intactos, CHANGELOG y, tras aceptación, borrado de `tests/graph_oracle_v1/`. Repo: deskops, worktree en robocop2 fijado por el coordinador. Límites: fuera closeout (CC33a/b), selectores y escrituras; no cambia formato del desk ni gramática CLI; nada a mano en `desk/` ni `.sldb/`.

AMBIGUEDADES
1. «Depende de CC38 (en main)» frente a `depends_on: []`: ¿la dependencia está satisfecha o debe verificarse? Obligaría a inventar el criterio de bloqueo.
2. «sldb.api.project_graph (o sldb graph project)»: dos superficies distintas; obligaría a elegir API Python o CLI sin dato.
3. «Este nodo decide si el grafo de sldb ya crea esos nodos» (a4): no fija evidencia ni qué significa "crear"; obligaría a inventar la prueba y el destino de la excepción.
4. «el enlace atom/materialization que usa el closeout (CC33a) se lee de ese grafo cuando este nodo entra»: "entra" no está definido y closeout está fuera de alcance; obligaría a inventar si este nodo toca CC33a.
5. «dan lo mismo que el oráculo v1 sobre el desk real» vs «copia en /dev/shm» (a3): no fija fixture ni si "lo mismo" es semántico o byte a byte.
6. «goldens de ayuda y salida idénticos»: si cambia la fuente del grafo, no aclara qué diferencias serían aceptables; obligaría a inventar el criterio.

DRY-RUN (hipotético, sin ejecutar)
Lecturas: `desk_graph.py`, `snapshot.py`, `checks.py`, `self_reflection.py`, `cli/commands/graph.py` y `drift.py`, `tests/graph_oracle_v1/`, goldens y CHANGELOG. Cambios previstos: reemplazar el snapshot por GD21 en los comandos; borrar `snapshot.py` y los `rglob`; adaptar `checks`/`self_reflection`; actualizar tests y CHANGELOG. Dependencias: GD21 en main, gate G_GD21, ~30 s por comando. Validaciones futuras: comparación con oráculo, grep de `rglob` vacío, tests de a uno, goldens desde `/dev/shm`, doctor en 6 desks, 4 pasos del workflow y borrado del oráculo en commit propio.

FUTURO
El supervisor corre suite completa y workflow; el coordinador fija worktree y decide a4; sldb corrige `rule_graph` (a6); CC33a consume el enlace; un humano acepta el borrado del oráculo.
