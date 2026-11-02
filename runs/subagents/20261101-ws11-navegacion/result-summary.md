# Resultado del Executor de WS11 — contrato de navegación e identidad

Fecha: 2026-11-01. Escribí solo `desk/drawer/plans/workspace-documental/contratos/navegacion.md` (creé el directorio `contratos/`) y este archivo. Sin commits, closeout, revisiones, build, validate, suite, servidores, Scion ni credenciales. No toqué `dag.yaml`, auditorías ni repos hermanos.

## Qué leí

Con Read o `sed` completos: la TaskDoc de WS11, `preflight-disposition.md`, `root-approval.md` de WS09, `result-summary.md` de WS09, `borradores/vistas.md` (448 líneas), `borradores/user-flows.md`, `decisiones.md`, `reconciliacion.md` (hasta la línea 214, que es el final), `alcance.md`, `brief.md`, `auditoria/ui.md` (195 líneas), `auditoria/infraestructura.md` (174 líneas). De `auditoria/deskops.md` (266 líneas) leí completas las líneas 175-266 (secciones B, C, C2-C4, D y resumen) y, por línea y sin truncar, las filas 33-35, 38-41, 43, 45, 48-49, 62-63, 72-73, 76, 82, 93, 100-102, 160 y 166. No leí las demás filas de A1/A2 de `deskops.md`.

De `dag.yaml` leí por tramos: líneas 1-306 (cabecera y todos los gates, incluidos G_UI_READ y G_SPEC_VIEW), WS11, WS12 (681-796), WS13 a WS13.3 (797-973), WS15.1 (1052-1092), WS17 y WS18 (1170-1257), WS33 (2276-2312), WS40 y WS41 (2672-2744). Para WS14, WS15, WS22-WS29, WS35, WS39, WS42, WS43, etc. usé solo `depends_on`, `requires` y `owner_repo` calculados con un script de lectura de `dag.yaml` (`python3 -I`, sin escribir). No leí los cuerpos de WS15.2, WS14, WS22, WS23, WS24 ni WS27-WS29 directamente.

## Código abierto exactamente

graph_ui `134a665` (árbol con solo untracked; `git status` no muestra tracked modificados):
- `frontends/mindmap/workspace_routes.py`: completo, 1-617.
- `frontends/mindmap/serve.py`: líneas 40-160, 312-330, 500-520 y un `grep` del archivo (workspace, SLDB_STORE, remote, 501, `make_server`).
- `frontends/mindmap/deskops_routes.py`: completo, 1-137.
- `frontends/mindmap/views/workspace/node/workspace.mjs`: completo (96 líneas).
- `frontends/mindmap/views/workspace/node/workspace-view.js`: líneas 1-232 y 322-380, más `grep` de símbolos (`updateUrl`, `popstate`, `handleSelectNode`, `focus`). No leí 233-321 ni 381-588 completos (JSX de cabecera, grafo, Code y contexto).
- `frontends/mindmap/projection_views.py` (1-140), `views_routes.py` (1-87), `sldb_adapter.py` (170-215), `shell/api.js` (completo), `shell/registry.js` (completo), `shared/document-ir.mjs` (líneas 11-36), `views/specs/notation/notation-view.js` (línea 356 por `grep`), `index.html` (líneas 7-8 por `grep`; búsquedas de `onerror`/`import(` sobre `index.html`, `app.js`, `shell/*.js`).
- No abrí `tests/*` de graph_ui, `workspace.css`, `apps/review-workbench/` ni `frontends/workspace/`.

sldb `77bd6d0097f46efdec5e7eeb0e58d71d70b98be5`: `api/documents/document_serialization.py` (24-32), `document_ir_serialization.py`, `document_ast.py`, `document_render.py` (19-39), `document_history.py` (18-30), `document_edges.py`, `document_edge.py`, `rebuild_edges.py` (1-40), `edge_reading.py` (14-26), `api/records/build_ir.py` (1-110), `utils.py` (10-19), `flatten.py`, `resolve.py`, `api/stores/open_store.py`, `store_discovery.py` (1-40, 67-76), `doc_ref.py`, `doc_status.py`, `doc_ref_status.py`, `store_links.py`, `api/search.py` (20-40), `cli/serve/routes.py` (55-110), `document_routes.py` (1-80), `render_routes.py` (1-60), `ast_routes.py`, `lint_routes.py` (20-60), `links/parser.py`, `links/recovery.py`, `links/resolver.py` (completo), `links/audit.py`, `store/edge_index/declared_references.py` (25-70), `store/edge_index/records.py`, `store/models/edge_record.py`, `store/query.py` (70-125), `core/ir/*` (listado y `meaning_node.py`/`document_ir.py` por `grep`).

deskops (este repo, HEAD `c19c6c0d`, no `215bf624`): `deskops/models/repository.py` (completo), `deskops/identity.py` (55-110 y 256-270), `deskops/operations.py` (360-396, 1196-1210), y por `grep` los campos de `models/inbox.py`, `materialization.py`, `pill.py`, `step.py`, `faq.py`, `ritual.py`.

## Símbolos de auditoría que no coincidieron

- `ui.md` (y `reconciliacion.md` C-07/C-08) dicen que la vista Specs no tiene fila de auditoría y `vistas.md` F18a la trata como «nombrada por la visión, sin productor». **La vista existe en graph_ui**: `notationView` con label «Specs» (`views/specs/notation/notation-view.js:356`, `shell/registry.js:16`). No hay discrepancia de código; hay un hueco de auditoría. Lo que sigue sin productor es integrarla al lector.
- `workspace_routes.py:3` declara «Strictly read-only»; `_build_graph_neighborhood` llama `document_edges` (`workspace_routes.py:356-359`), que reconstruye el índice de aristas bajo lock (`document_edges.py:30`, `rebuild_edges.py:34`). Por lectura, no es solo lectura en derivados. No lo ejecuté.
- La auditoría `ui.md:55` y `reconciliacion.md` C-02 sitúan el filtro de aristas en `workspace.mjs: filterGraphEdges` y el hash en `workspace_node`: ambos coinciden. `reconciliacion.md` C-45 cita `sldb/links/parser.py:6-7` y `audit.py:10`: coinciden. `recover_links` **no** está reexportada por `sldb.api` (solo por `sldb.links`); las auditorías hablan de `docs recover` y `/lint` sin precisarlo.
- La auditoría `deskops.md` fija `215bf624`; leí deskops en `c19c6c0d` y no comparé los archivos entre ambos commits.
- `ui.md:60` dice que el fallo de CDN es «sin manejo observado»: coincide con mis búsquedas (`index.html:7-8` es un importmap con `esm.sh`; sin `onerror`/`import(` en `index.html`, `app.js` ni `shell/*.js`).
- Ningún otro símbolo citado por las filas que usé dejó de aparecer en el código que abrí. No verifiqué los símbolos de filas que no cité (p. ej. `ConnectDialog`, `models_service.py`, `persistence.py:85,102`).

## Hallazgos que cambian cómo se escribe el contrato

1. Hoy no hay estado de foco en graph_ui (`focus` no aparece en `workspace_routes.py` ni en `views/workspace/`). El único dominio de correspondencia con soporte en código es identidad de documento (nodo, relación, catálogo) y entrada de `files`/`references` ↔ tarjeta Code.
2. sldb ya entrega, dentro del IR que graph_ui recibe, el rango de líneas por sección y los nodos `surface` con texto y rango; los campos no tienen rango (`build_ir.py:68-77` no asigna `span`). La UI no los usa como foco ni muestra el texto con líneas.
3. sldb guarda el campo que declara cada arista (`declared_references.py:68`), pero `DocumentEdge` y la ruta de graph_ui lo omiten.
4. `files` y `references` se concatenan en la ruta y se pierde el campo de origen de cada tarjeta Code (`workspace_routes.py:441-446`).
5. `GU/views_routes.py:29-33` acepta del cliente cualquier directorio `.sldb`; el registro de deskops acepta absolutas y `..` sin contención (`identity.py:256-262`); `recover_links` resuelve también contra `Path(destino)` arbitrario (`resolver.py:32-37`). Ninguno sirve como lista de permitidos; el contrato lo dice.
6. `recover_links` no resuelve enlaces `[[alias:ref]]`; `doc_status` resuelve referencias `alias:ref` entre stores enlazados directos, no enlaces de texto.
7. Campos de los modelos que las auditorías decían «no leídos» (RepositoryDoc, InboxNoteDoc, MaterializationContractDoc, PillDoc, StepDoc, DeskFAQDoc) leídos en `deskops/models/*.py`; quedan en la sección 13, punto 5 del contrato.

## Huecos (resumen; tabla completa en la sección 11 del contrato)

Con productor en el DAG: H-01 fuente propia (WS13.1), H-02 explorador y lista de permitidos (WS13.2), H-03 y H-03b campo de origen y campo↔arista (WS13.1), H-04 foco por sección/campo (WS13.1), H-06 seguir `[[…]]` (WS13.1, WS15.1), H-07 pestañas (WS13.3), H-08 y H-09 CDN y estados de red (WS15.1), H-10 manifiesto (WS40), H-12 ruta por alias (WS41), H-13 diff Git (WS27.1), H-14 lectura sin escritura derivada del segundo desk (WS41), H-17 enlaces entre desks del corpus (WS40/WS17), H-18 a H-24 (WS22, WS23, WS24, WS14, WS15.2). H-25 (todo hueco de escritura) remitido a WS12.

**Sin productor en el DAG**: H-05 rango de líneas por campo (sldb; no comprometido); H-11 conjunto de aliases autorizados del desk real (deskops); H-14 para el store propio; H-16 resolver enlaces de texto entre desks (sldb); H-21 progreso de paso (deskops; no comprometido); candidaturas de `vistas.md` (consulta guardada, búsqueda por significado, edición de RoleDoc/RuntimeProfileDoc, navegación de FAQ, lista de issues en UI, renderer de roles, Specs en el lector), que siguen como candidaturas.

## Decisiones que requieren cambio de alcance (no las tomé)

1. **WS13.1, foco compartido**: la aceptación literal («seleccionar en Code, texto o graph actualiza ese foco») excede lo que los mapeos actuales soportan (C4b-C14). Opciones: dejar los huecos con WS13.1 como productor, o acotar la aceptación al dominio de la sección 6.1. Decide root.
2. **WS41, enlaces authored entre desks**: ninguna operación pública de sldb los resuelve y WS41 es de graph_ui. O se compone `parse_links` + `doc_status` en graph_ui (a probar al promover) o root amplía el alcance a sldb. También falta fijar la sintaxis de esos enlaces en el corpus de WS40.
3. **WS18**: no hay evidencia que fije la selección mínima ni la notación; el contrato declara que su promoción se detiene. Para reanudarla hace falta una decisión de producto o de root.
4. **Desk real en multidesk**: no hay productor del conjunto cerrado de aliases autorizados; WS41 solo cubre los dos stores de WS40.

## Qué no verifiqué

- Ningún comportamiento de runtime: no ejecuté servidores, tests, `sldb`, `deskops` ni el navegador. Todas las afirmaciones son por lectura de código. En particular: reconstrucción de índices por `document_edges` (no medida), que `surface` reconstruya el texto íntegro, qué hace `fetch` ante backend caído (deducido del estándar), efectos de `open_store`/`migrate_store_layout`, y que `[[alias:ref]]` no se resuelva (solo vi `resolver.py`, no probé).
- No abrí el JSX de `workspace-view.js` fuera de los tramos indicados, ni `workspace.css`, ni `tests/` de graph_ui, ni `apps/review-workbench/`.
- No verifiqué `spec2viz` (ViewDoc, `resolve_documents`): todo sobre ese repo viene de `infraestructura.md` y `reconciliacion.md`. Tampoco `pron`.
- No leí `vision.md` completo (solo la línea 36 por `sed`), `cobertura.md`, `validacion-humana.md`, `manual.md` ni los demás cuerpos de nodos de `dag.yaml`.
- No verifiqué que exista o no un acta de recepción fuera de `runs/subagents/workspace-documental-acceptance/` de graph_ui (ausente) y de una búsqueda de `G_UI_READ` en `*.md` de graph_ui (sin resultados); no busqué en otros repos.
- No corrí los checks de la TaskDoc (`test -s`, `build_plan --check`, `validate_plan --check`, `context_review status`) ni dejé el contrato congelado: eso es del Supervisor. El contrato queda como borrador sin revisión.

## Resumen breve

El contrato tiene las 13 secciones en orden. Fija la identidad de Markdown no modelado como `(repo, ruta)` con modelo opcional, el mecanismo de resolución explícita por alias cerrado (sin valores inventados) y el criterio de rutas seguras tomado de `_inspect_file_reference`. La tabla de correspondencias solo marca soportado lo que el código muestra: identidad de documento y entrada de referencia ↔ tarjeta Code. El resto es hueco con productor, o requiere decisión de alcance de root (WS13.1 foco, WS41 enlaces entre desks, WS18 selección). Los 10 dependientes directos de WS11 y los 18 nodos de G_UI_READ están mapeados con «sin acta registrada». Nada se ejecutó y nada se afirma como aceptado.

## Revisión del Supervisor antes de congelar

Claude Opus 5.5, pane `w3Y:p1`, 2026-11-01, sin Executor. Leí el contrato completo. Comprobé contra código, por grep y lectura de líneas: los IDs de WS y gates; los 18 nodos de `G_UI_READ`; los símbolos de `workspace_routes.py`; `document_edges` llama a `rebuild_edges(..., wait=True)` en la línea 30; `recover_links` resuelve también por ruta (`resolver.py:32-37`); `_store` de `views_routes.py` acepta cualquier store del cliente; `identity.py:256-262` no impone contención; `focus` no aparece en `workspace_routes.py` ni en `views/workspace`; `[[` y `recover_links` no aparecen en código del workspace (coincidencias solo en notación y una regex de `contract.py`). No edité el contrato. El Tester independiente es quien coteja el resto.
