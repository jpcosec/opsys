## REFORMULACION

**Propósito:** sustituir `deskops/services/desk_view.py` por ViewDocs semilla servidas por `sldb.api.run_view`, de modo que `deskops view board|task|drawer|inbox` y graph_ui lean la misma vista sin código propio de composición.

**Resultado:** los cuatro comandos devuelven el JSON actual salvo el valor de `revision` (ETag GD25); `GET /views/board` de `sldb serve` da el mismo payload; graph_ui sirve board sin importar `DeskView` y `POST /api/desk/advance` con ETag viejo da 409; `desk_view.py`, `task_revision`, `note_revision` y los alias privados de la fachada se borran.

**Repos:** deskops (`services/desk_view.py`, `data/views/`, `cli/commands/view.py`, `runtime/`, `operations.py`, tests, goldens, docs, CHANGELOG) y UIs/graph_ui (`frontends/desk/serve.py`, `frontends/mindmap/deskops_routes.py`, tests).

**Límites:** fuera proveedores computed (DA1) y `desk/views/` (DA4); formato del desk y gramática del CLI invariantes; goldens capturados antes en un commit solo (a3); graph_ui se integra antes que deskops (a2); cada superficie borra su código viejo en el mismo paso.

## AMBIGUEDADES

1. "deskops view <x> --format json en proceso, **o** GET /views/<x> de sldb serve con ETag" (a2): dos transportes alternativos; obliga a elegir uno, y la aceptación solo prueba el segundo.
2. "la ViewDoc lee por **edges o rules**": no se decide cuál; obliga a inventar la forma de la ViewDoc y su modelo (no aparece esquema alguno).
3. "lo que no es documento ni recibo (agents de Herdr, runtime/, P4) lo agrega deskops view sobre el resultado de run_view": la vista `agents` no figura en Goal ni en la aceptación (solo board|task|drawer|inbox); obliga a decidir si sobrevive y dónde.
4. "idénticos a los goldens ... sin fechas ni hashes variables **salvo revision**" (a3) frente a inbox, cuyas notas llevan `date` y `revision` por nota: obliga a decidir si el inbox queda fuera de los goldens deterministas.
5. "sldb serve las encuentra por un store de deskops enlazado" (a6): no se dice cómo se enlaza ni qué declara `desk_declaration.yaml`; obliga a inventar configuración de store.
6. "los alias privados de la fachada que CC30 conservó": `operations.py` marca cuatro, pero también nombra `domain_tree.py`; obliga a decidir el conjunto exacto.

## DRY-RUN

**Lecturas:** TaskDoc, `desk_view.py`, `view.py`, `operations.py`, `desk_declaration.yaml`, `docs/deskops-ui.md`, goldens existentes, `sldb.api.run_view`/`list_views`.

**Cambios previstos:** commit 1 captura goldens; commit 2 crea `data/views/{board,task,drawer,inbox}`; reescribe `view.py` como `run_view` + `render_text` + agents en CLI; borra `desk_view.py` y alias; actualiza docs y CHANGELOG; en graph_ui cambia `serve.py`/`deskops_routes.py` a la vista nueva.

**Dependencias:** CC33/CC36 cerrados; `sldb serve` con store enlazado; rama wt/ de graph_ui creada tras `wt/deskops-ui`.

**Validaciones futuras:** goldens salvo revision; `GET /views/board`; test 409; grep vacío; seis desks; cuatro pasos de deskops y CI de graph_ui en clones limpios.

## FUTURO

El coordinador fija worktrees, orden de integración y corre CI en clones limpios; CC52 mide el tiempo caliente; sldb aporta `run_view`/`list_views` y el enlace de store; un humano resuelve las ambigüedades 1–6.
