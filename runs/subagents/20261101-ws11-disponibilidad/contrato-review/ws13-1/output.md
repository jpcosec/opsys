## REFORMULACION

**Propósito**: entregar el nodo WS13.1, «Leer documento, contexto y enlaces»: lectura de solo lectura del documento y su fuente Markdown (modelada y no modelada), panel de contexto, seguimiento de enlaces, Code local y foco interno por documento.

**Resultado**: delta conciliado en graph_ui sobre el workspace existente, con rutas de lectura conformes a WS11 y tests; no un workspace nuevo.

**Repo**: graph_ui (`views/workspace/`, rutas de lectura, `tests/`).

**Límites**: solo lectura; nada de guardado/escritura (WS12); no duplicar el workspace ni crear índices nuevos; no inventar mapeo texto→código; gate `G_UI_READ` y acta de recepción pendientes; el contrato WS11 sigue en borrador y sin aceptar.

## AMBIGUEDADES

1. «las relaciones que declare el contrato WS11» (acceptance): WS11 no enumera un conjunto cerrado para el panel; obligaría a inventar cuáles mostrar.
2. «No depender de conocer un ID» (acceptance): no aclara si habla de la persona, la URL o el cliente; obligaría a inventar el criterio.
3. «en las representaciones que el catálogo WS09 (borradores/vistas.md) y el contrato WS11 declaren soportadas» (acceptance): remite a un documento externo no incluido; obligaría a inventar el conjunto soportado.
4. «La base a1b2b22 es punto de partida reutilizable» (dag.yaml) frente a «graph_ui `134a665`» (contrato §1): dos bases citadas; obligaría a decidir cuál es la referencia sin más dato.

## DRY-RUN

**Lecturas**: `GU/workspace_routes.py`, `GU/sldb_adapter.py`, `GU/views/workspace/node/workspace-view.js`, `workspace.mjs`, `shared/document-ir.mjs`, `shell/api.js`; referencias sldb citadas en WS11.

**Cambios previstos**: ruta de fuente propia que devuelva texto y revisión de una sola lectura (H-01); pestaña de texto con spans del IR (H-04); preservar campo/posición de `files`/`references` antes de concatenar (H-03); estado de foco por documento; resolución de enlaces con `parse_links`+`split_anchor`+autorización+`doc_status(store,"local:"+resto)` (H-06); `include_linked=False`.

**Dependencias**: contrato WS11 (borrador), datos de `ir` y `load_edge_index`, guardias de §3.3. No modificar `request()` (lo tipifica WS15.1).

**Errores/validación esperada**: E5 y estados de Code; 400/404/503 existentes; tests de fuente+render con misma revisión, ausencia de mutación del store (H-14), contención de rutas y enlaces rotos visibles. Sin ejecutar.

## FUTURO

- WS15.1 tipifica estados HTTP/red sobre `api.js`.
- WS13.2 aporta explorador y lista de permitidos; WS13.3, pestañas e historia.
- WS41 resuelve multidesk/alias y H-16; WS40 aporta el corpus.
- P01/root registra actas y decide la base y el alcance de WS18.
