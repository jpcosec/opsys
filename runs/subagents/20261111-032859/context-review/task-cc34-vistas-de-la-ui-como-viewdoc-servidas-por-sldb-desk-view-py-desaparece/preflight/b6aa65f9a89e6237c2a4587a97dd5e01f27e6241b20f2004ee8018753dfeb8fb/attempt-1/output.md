REFORMULACION
Propósito: retirar `DeskView` y servir board/task/drawer/inbox como ViewDoc semilla mediante `sldb.api.run_view`, conservando JSON y ayuda de `deskops view`. Resultado: CLI y graph_ui leen las vistas nuevas; `desk_view.py`, revisiones y alias privados desaparecen; el ETag mantiene la guarda optimista. Repos: deskops (principal) y UIs/graph_ui. Límites: sin proveedores computed (DA1), sin `desk/views/` (DA4); quedan fuera proveedores computed y esa carpeta; ningún agregado reimplementa reglas. Nodo ejecutable `task.code`, no agregado.

AMBIGUEDADES
1. “proxy o cliente directo, con ETag”: no fija cómo consume graph_ui; obliga a inventar proxy/cliente y manejo de errores.
2. “sldb serve las encuentra por un store de deskops enlazado”: no define el enlace; obliga a inventar configuración/registro del store.
3. “agents de Herdr, runtime/, P4) lo agrega deskops view”: no fija orden, colisiones ni mezcla; obliga a inventar semántica de agregación.
4. “deskops/data/desk_declaration.yaml (solo si hace falta declarar las ViewDoc)”: no decide si hace falta; obliga a inventar el criterio.
5. “desk de prueba fijo ... contenido determinista”: no enumera fixtures ni normalización; obliga a inventar el desk y cómo estabilizar `revision`.

DRY-RUN
Lecturas: TaskDoc, `docs/deskops-ui.md`, `desk_view.py`, `run_view`/`list_views`, rutas e imports de graph_ui, goldens y ayudas. Cambios previstos: commit solo de goldens; ViewDoc semilla board/task/drawer/inbox; `view.py` sobre `run_view` + `render_text` y suma de agents/runtime; borrado de `desk_view.py`, `task_revision`/`note_revision` y alias; tests reescritos; docs/CHANGELOG; graph_ui lee la vista con ETag y elimina `DeskView`/`_read_doc`/`_resolve_glob`/`show_task`; test 409. Dependencias: CC33 (recibos evidence), GD25 (ETag), store enlazado y orden graph_ui→deskops. Validaciones futuras: pytest por archivo, stores build/check, ci-knowledge, CI de graph_ui, greps vacíos, 6 desks, tiempos y comparación de payload/ETag.

FUTURO
El coordinador fija worktrees, integra primero graph_ui y después deskops, y corre las suites completas; un humano resuelve el enlace del store si sldb no lo soporta; CC52 verifica el tiempo caliente.
