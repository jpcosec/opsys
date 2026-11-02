## REFORMULACION

Nodo WS13.1 (implementation, owner graph_ui, depende de WS11, gate G_UI_READ): añadir al workspace lectura de solo lectura de Markdown modelado y no modelado, con render y fuente cruda íntegra del mismo origen, panel de contexto con identidad/relaciones/origen, seguimiento de enlaces, Code local y foco compartido solo donde WS11 fije correspondencia real. Base reutilizable a1b2b22/134a665; sin escritura, índices nuevos ni otro workspace; `promotion: not_authorized`.

## AMBIGUEDADES

1. «Estado: borrador… No está revisado» frente a «según contrato WS11» y «el contrato WS11 declaren soportadas»: obliga a decidir si el borrador es normativo y con qué hash (`context_review` cita `358c…`).
2. «según contrato WS11 y recibo externo del delta» frente a «sin acta registrada» (12.1): obliga a decidir si el recibo es precondición para implementar o solo para cerrar.
3. `output_scope` «frontends/mindmap/views/workspace/ (reutilizar node/workspace-view.js…); … tests/» frente a las rutas que el contrato exige tocar (`workspace_routes.py`, `sldb_adapter.py`, `shell/api.js`): obliga a decidir si se permite editar servidor fuera del scope.
4. «seleccionar en Code, texto o graph actualiza ese foco y las demás representaciones del mismo documento lo comparten» frente a C11b/C12 «sin soporte, sin productor» y 6.1 «solo la correspondencia que existe»: obliga a fijar qué representaciones comparten foco y si H-03/H-03b (campo, posición, multiplicidad de aristas) entran en este nodo; la aceptación no los nombra.
5. «No depender de conocer un ID» frente a identidad `Model:name` o `(repo, ruta)` (2.2): obliga a inventar la clave de selección y de sesión.

## DRY-RUN

Leería contrato, `dag.yaml` y workspace en 134a665; tocaría `GU/workspace_routes.py` (fuente cruda y revisión de la misma lectura), `GU/sldb_adapter.py` (IR), `views/workspace` (contexto, enlaces, foco), `shared/document-ir.mjs` y tests. Consumiría WS11 y G_UI_READ; sin acta se detendría antes de escribir. Errores previstos: E1-E9 y referencias rotas. Validaría fuente+render con igual revisión, enlaces con origen, foco solo donde hay mapeo, cero mutación del store (H-14), sin índices ni workspace duplicado.

## FUTURO

Root/P01 debe aprobar WS11 y fijar su hash; P01 registra el recibo del delta; WS13.2 aporta la lista de permitidos; WS15.1 los estados de error; WS41 multidesk y WS40 el corpus.
