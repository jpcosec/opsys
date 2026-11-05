REFORMULACION

PC03 es un agregado no ejecutable del plan `gates-por-tipo`. Propósito: que un plan como este se promueva nodo a nodo y su DAG quede en el grafo de deskops. Resultado: `parent_id`, `children` y `task.aggregate` con regla propia; promoción desde `dag.yaml` con tipo, padre y dependencias; `deskops graph` leyendo aristas de sldb. Repo dueño: deskops. Límites: no se promueve ni ejecuta; termina cuando cierran sus hijos; no toca sldb salvo `deskops message send`; no sustituye con Python reglas de sldb. Dependencias: GC09 (GC01, GC05), GC10 (GC03, GC09), GC11 (GC09); PC03 no declara `requires`. Aceptación conjunta: promoción con `add task --from-drawer ... --node` deja tipo, `parent_id` y `depends_on` como aristas del store; el agregado no activa hasta cerrar hijos; `graph neighbors` lista `parent_id`, `children` y `depends_on` desde el índice de sldb.

AMBIGUEDADES

ninguna.

DRY-RUN

PC03 no ejecuta: no tiene lecturas, cambios ni validaciones propias. Un ejecutor futuro recorrería sus hijos. GC09 construye el modelo de composición y la regla de activación de `task.aggregate`; transfiere a GC10 y GC11 los campos `parent_id`/`children` y la semántica de agregado. GC10 usa eso para `add task --from-drawer --node`, crea el agregado padre, resuelve tipo, `parent_id`, `depends_on`, gates pendientes y `promoted`; no transfiere nada a GC11 porque no hay arista entre hermanos. GC11 usa de GC09 las aristas de referencia y cambia el snapshot de `graph` al índice de sldb; no debe asumir el mapa `promoted` de GC10. Validación conjunta: las aceptaciones de GC09 y GC10 cubren composición, promoción, bloqueo/activación y `closeout verify`; GC11 cubre `graph neighbors`, roles, ausencia de aristas por prosa, `graph missing` y goldens.

FUTURO

Quedan para otros nodos o el dueño: `G_TYPES` (GC01), `G_RECEIPTS` (GC03), `G_CONSUMER` (GC05); gates `G_SLDB_*` pendientes en sldb; confirmación de `--evidence`, DC7, `task.external` y Scion; nota a sldb desde GC03/GC05.
