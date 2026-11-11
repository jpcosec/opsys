## REFORMULACION
Nodo ejecutable de código, no agregado. Propósito: sustituir `DeskView` por ViewDoc semilla y `sldb.api.run_view`, de modo que `deskops view board|task|drawer|inbox` conserve su JSON (salvo revision) y graph_ui lea las vistas por sldb serve sin importar `DeskView`. Resultado: semillas en `deskops/data/views/`, CLI sobre `run_view`, borrado de `desk_view.py`/helpers/alias, graph_ui con `GET /views/<vista>` y ETag, tests, docs y CHANGELOG. Repos: deskops y `UIs/graph_ui` (ramas `wt/cc34` y `wt/cc34-ui`). Límites: no proveedores computed, no `desk/views/`, no reimplementar reglas; goldens primero; deskops se integra antes que graph_ui; acciones siguen por CLI en proceso.

## AMBIGUEDADES
1. «board = sección de tareas … con transitions …, rules … y edges» y «Sin proveedores computed (DA1)» frente a `gates`, `closeout` y `next` del contrato. No se dice si salen de ViewDoc, `run_view` o agregados del CLI; mapearlos obligaría a inventar su fuente.
2. «agents de Herdr, runtime/, P4» no define «P4»; si no es agents/runs, obligaría a inventar un agregado.
3. «idénticos … salvo el valor de revision» frente a c4 «revision y fechas»: la aceptación no nombra fechas; sin c4 obligaría a decidir qué normalizar.

## DRY-RUN
Leer TaskDoc, `docs/deskops-ui.md`, `desk_view.py`, `view.py`, `operations.py`, `domain_tree.py`, `desk_declaration.yaml`, CHANGELOG y los archivos de graph_ui citados. Capturar goldens en `tests/fixtures/golden/output/` con desk `tmp_path` determinista. Crear ViewDoc semilla board/task/drawer/inbox; adaptar `view.py` a `run_view` + `render_text`; borrar `desk_view.py`, `task_revision`/`note_revision` y alias; ajustar `domain_tree.py`; graph_ui: servir `/views/<vista>` con ETag y 502, acciones por CLI, tests 409; actualizar tests, docs y CHANGELOG. Depende de `sldb.api.run_view`, modelo ViewDoc, ETag GD25, store enlazado y recibos CC33. Validaciones futuras: las seis de Validation, sin ejecutar.

## FUTURO
El coordinador integra deskops y luego graph_ui, corre CI en clones limpios y decide si `desk_declaration.yaml` hizo falta; el supervisor corre la suite completa; CC52 verifica el tiempo; si el modelo no expresa una parte, el worker deja hipótesis y nota a sldb; si un paso intermedio queda rojo, para y avisa.
