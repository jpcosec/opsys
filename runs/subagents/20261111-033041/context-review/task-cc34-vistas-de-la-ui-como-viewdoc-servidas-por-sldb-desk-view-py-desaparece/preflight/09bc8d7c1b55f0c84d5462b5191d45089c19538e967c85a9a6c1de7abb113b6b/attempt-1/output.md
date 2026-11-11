REFORMULACION
Propósito: retirar DeskView y servir las vistas de la UI como ViewDoc de sldb. Resultado: `deskops view board|task|drawer|inbox` = `sldb.api.run_view` sobre ViewDocs semilla de `deskops/data/views/`, con JSON igual al actual salvo `revision` (=ETag de GD25); graph_ui lee `GET /views/<v>` de sldb serve (sin importar DeskView; guarda por ETag: 409 con ETag viejo); se borran `desk_view.py`, `task_revision`/`note_revision` y alias privados. Repos: deskops (rama `wt/cc34`) y graph_ui (`wt/cc34-ui`); se integra graph_ui antes que deskops. Límites: formato del desk y gramática/ayudas del CLI invariantes; fuera: proveedores computed (DA1) y `desk/views/` (DA4). Es un nodo ejecutable de código, no un agregado.

AMBIGUEDADES
1. "deskops view board|task|drawer|inbox --format json idénticos a los goldens" frente a "task = una tarea por {id}": no se fija el id ni la invocación del golden de task; obliga a inventarlo.
2. "salvo el valor de revision" frente a b6 "normaliza los valores de revision y de fechas": ¿las fechas se comparan o se normalizan? Contradicción.
3. "deskops view board en los 6 desks responde": "responde" sin criterio (exit 0, JSON válido, no vacío).
4. "GET /views/board ... devuelve el mismo payload": ¿igual a `run_view` o a la salida del CLI, que añade agents?
5. "graph_ui lo pide a deskops en proceso como las acciones (DP4)" frente a b1 "No se usa la vía en proceso por CLI para leer vistas": dos transportes incompatibles.
6. "desk_declaration.yaml (solo si hace falta declarar las ViewDoc)": no se define "hace falta".
7. "meta caliente < 1 s, la verifica CC52": método de medición frío/caliente no definido.
8. "_repository_root si solo lo usa graph_ui": exige un inventario de usos no aportado.

DRY-RUN
Lecturas: TaskDoc, dag.yaml, alcance.md, docs/deskops-ui.md, `sldb.models.notation.view_doc`, `desk_view.py`, `view.py`, `operations.py`, `domain_tree.py`, `serve.py`, `deskops_routes.py`, goldens. Cambios previstos: capturar goldens en commit aparte; crear las 4 ViewDoc; reescribir `view.py` sobre `run_view`; borrar `desk_view.py` y helpers; ajustar alias; graph_ui como cliente HTTP con ETag; tests, docs y CHANGELOG. Dependencias: CC33/CC36 cerrados, GD25, `run_view`/`list_views`. Validaciones futuras: pytest por archivo, `stores build`/`--check`, `ci-knowledge-check`, CI completo de graph_ui, grep, 6 desks, tiempos y comparación de goldens.

FUTURO
El coordinador fija worktrees y orden de integración; el supervisor corre la suite completa; CC52 verifica el tiempo; sldb recibe hipótesis/nota si el modelo no expresa una parte; un humano decide si b2 basta (b3).
