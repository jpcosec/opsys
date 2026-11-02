REFORMULACION
WS13.1 «Leer documento, contexto y enlaces»: implementar en graph_ui un delta de solo lectura sobre el workspace a1b2b22 para que un Markdown modelado o no tenga fuente cruda íntegra y render con el mismo origen, panel de contexto (identidad, relaciones, origen), enlaces y Code local, y foco interno por documento compartido entre texto/graph/code solo donde WS11 defina correspondencia real. Repo: graph_ui; output_scope `views/workspace/` (reutilizar `node/workspace-view.js` y componentes), rutas de lectura WS11 y `tests/`. Límites: no escritura, no índices nuevos, no otro workspace, no inventar mapeo texto→código, no depender de un ID; sujeto a G_UI_READ y al contrato WS11 aún en borrador sin acta.

AMBIGUEDADES
1. «La selección por documento/nodo fija el foco del documento abierto» vs «C1-C3 solo cambian `selectedId` y navegan a otro documento». Obliga a inventar si seleccionar un nodo graph es navegación o foco interno y si conserva el documento activo.
2. «Markdown sin modelo tiene render de lectura y fuente cruda íntegra legibles (ambas), con mismo origen» vs «la reutilización con un descriptor y `model=None` se verifica al implementar WS13.1, y falta la ruta de graph_ui». Obliga a inventar qué render vale para no modelado o a bloquear.
3. «WS13.1 consume ese resultado y no lo implementa, y eso no crea una dependencia de WS13.1 hacia WS15.1» vs WS15.1 `depends_on: - WS13` y su cambio en `shell/api.js`. Obliga a inventar si WS13.1 usa el `request()` actual o espera un nodo posterior, con posible ciclo.

DRY-RUN
Sin ejecutar: leería contrato WS11, WS13.1 y código: `workspace_routes.py`, `sldb_adapter.py`, `workspace-view.js`, `workspace.mjs`, `document-ir.mjs`, `shell/api.js`. Cambios: ruta de fuente propia con guardias 3.3 y una sola lectura de bytes para fuente+IR; preservar `files`/`references` con campo y posición; enlaces con `parse_links`+`split_anchor`+autorización+`doc_status`/lectura protegida; foco por documento y callbacks en Document/Graph/Code; tests. Dependencias: WS11 (borrador), G_UI_READ, base a1b2b22/f16fcd1/134a665. Validación: acceptance WS13.1, mismo origen, sin copia, sin mapeo texto→código, acta G_UI_READ. Errores: documento ausente, lectura degradada y referencia rota.

FUTURO
WS11/Tester/root: PASS y acta; P01: recibo G_UI_READ; WS15.1: tipificar `request()` y E1-E3; WS13.3: foco/historia; WS41: multidesk y aliases; WS40: corpus; WS12: escritura.
