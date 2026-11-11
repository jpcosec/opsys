## REFORMULACION

Propósito: retirar `DeskView` y servir board/task/drawer/inbox como `ViewDoc` semilla de sldb, con el mismo JSON salvo `revision`. Resultado: `deskops view <x> --format json` = `sldb.api.run_view` sobre `deskops/data/views/` + `render_text` y los agregados no-documento (agents, runs) en el CLI; `desk_view.py`, `task_revision`/`note_revision` y los alias privados borrados; graph_ui lee `GET /views/<v>` de sldb serve con ETag/409 sin importar DeskView. Repos: deskops (`wt/cc34`) y UIs/graph_ui (`wt/cc34-ui`). Límites: fuera proveedores computed (DA1) y `desk/views/` (DA4); gramática y formato del desk intactos; `desk_declaration.yaml` solo reserva.

## AMBIGUEDADES

1. "`deskops view agents` sigue existiendo como hoy" frente a "desk_view.py y sus helpers se borran": no se dice dónde vive `agents()` tras el borrado; obligaría a inventar su nueva sede y forma.
2. "Cada parte del contrato de docs/deskops-ui.md se lee como lo da el modelo": no se dice cómo salen `errors`, `counts`, `closeout`, `next` ni `markdown/excerpt/command` del drawer; obligaría a inventar el mapeo campo a campo.
3. "revision del payload = ETag de GD25" frente al `sha256(Board + tarea)` del doc: no se dice qué documentos cubre el ETag ni si un cambio del Board lo invalida; obligaría a inventar la equivalencia de la guarda.
4. "El coordinador integra primero graph_ui y después deskops" frente a "lee ... GET /views/<x> de sldb serve": graph_ui depende de las semillas y el store de deskops; obligaría a inventar cómo queda verde el paso intermedio.

## DRY-RUN

Lecturas: `desk_view.py`, `docs/deskops-ui.md`, `desk_declaration.yaml`, `view.py`, `operations.py`, `domain_tree.py`, `golden/output/`, `test_desk_view.py`; en graph_ui: `serve.py`, `deskops_routes.py`, `tests/`. Cambios: commit solo de goldens normalizados (b6); ViewDocs semilla declaradas con `sldb stores declare --write`; `view.py` = run_view + render_text + agents; borrado de `desk_view.py`, revisiones y alias; graph_ui con cliente GET /views y 409; tests, docs, CHANGELOG. Dependencias: sldb run_view/ETag (GD25), CC33/CC36 cerrados, store de graph_ui enlazado. Validaciones futuras: goldens salvo revision, GET /views/board, 409, grep vacío, 6 desks, 4 pasos de deskops + CI de graph_ui.

## FUTURO

El coordinador fija worktrees, integra en el orden acordado y corre suite completa, `sldb stores build` y e2e; decide las hipótesis no expresables con nota a sldb; CC52 mide el tiempo caliente.
