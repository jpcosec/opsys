## REFORMULACION

Encargo del nodo CC34 (task.code, no agregado): migrar las vistas `board|task|drawer|inbox` de `DeskView` a ViewDoc semilla servidas por `sldb.api.run_view`, y borrar `deskops/services/desk_view.py`. Resultado: mismos JSON que hoy salvo `revision` (y fechas, c4), `graph_ui` lee por `GET /views/<vista>` de `sldb serve`, guarda optimista por ETag (409 con ETag viejo), grep de `desk_view|DeskView` vacío, 6 desks responden, CHANGELOG y doc. Repos: deskops (rama `wt/cc34`) y graph_ui (`wt/cc34-ui`); integra deskops primero (c1). Límites: sin proveedores computed, sin `desk/views/` (DA4), acciones por CLI en proceso (DP4), ningún agregado reimplementa reglas, no hay shim de compatibilidad.

## AMBIGUEDADES

1. Cita: «tests/test_desk_view.py reescrito sobre run_view y verde» frente a «grep de "desk_view\|DeskView" en deskops/ ... vacío». El archivo contiene `desk_view` y vive bajo `deskops/`; obliga a inventar si se renombra o si el grep excluye `tests/`.
2. Cita: «una fixture de tests arma el desk en tmp_path con ids, títulos y fechas fijas» y «El fixture lo define» (c3). No se dan ids, títulos ni número de tareas: obliga a inventarlos.
3. Cita: «Si el modelo no expresa una parte, hipótesis y nota a sldb» (b4) y «lo que no tenga fuente en el modelo, hipótesis y nota a sldb» (c9). Sin el modelo `view_doc` en el input, obliga a inventar el mapeo campo→fuente.
4. Cita: «el test de 409 de graph_ui lo prueba con el cambio que sí la invalida» (c9). Obliga a inventar qué cambio concreto invalida la revisión de `task`.

## DRY-RUN

Lecturas: TaskDoc, `dag.yaml` (CC34), `docs/deskops-ui.md`, `desk_view.py` (543 líneas), modelo `sldb.models.notation.view_doc`, `.sldb/store.yaml` de ambos repos, golden dir. Cambios: commit 0 con goldens en `tests/fixtures/golden/output/`; ViewDoc semilla en `deskops/data/views/` declaradas con `sldb stores declare`; `cli/commands/view.py` sobre `run_view`+`render_text`+agregados (agents, runs); `runtime/` recibe agents; borrado de `desk_view.py`, `task_revision/note_revision` y alias; `domain_tree.py` a `doc_access`; graph_ui `serve.py`/`deskops_routes.py` a GET `/views`; tests, doc, CHANGELOG. Dependencias: CC33/CC36, GD25, fixture b6, orden c1. Validaciones futuras: `pytest` por archivo, 4 pasos deskops, CI graph_ui, 6 desks, tiempos c8. Nada ejecutado.

## FUTURO

El coordinador fija worktree, integra deskops y luego graph_ui, corre suite completa/CI y decide si `desk_declaration.yaml` se toca (c7). CC52 mide la meta de tiempo. Si el modelo no expresa una parte, decide sldb.
