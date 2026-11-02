REFORMULACION
WS24 es un encargo de implementación en `graph_ui`, aún candidato y sin promoción autorizada. Propósito: reutilizar el grafo y una vista de documento genérica registrada en `shell/registry.js` para átomos, protoátomos, crossroads, materializaciones y pills, con clasificación y vecindad de hasta 2 hops; preservar Code local e heredar Markdown no modelado de WS13. Resultado: delta o ticket existente en `frontends/mindmap/views/workspace/graph/`, panel Context de `node/workspace-view.js`, `shell/registry.js` y `tests/`. Límites: depende de WS13 y WS09; exige G_UI_READ por delta; ViewDoc de WS18 solo tras G_SPEC_VIEW y no bloquea; no crear segundo lector, no inferir tags por carpeta ni clasificación ficticia, ni exigir renderer nuevo por clase.

AMBIGUEDADES
Ninguna.

DRY-RUN
Un ejecutor futuro leería el nodo WS24, el TaskDoc promovido, el contrato WS11, el catálogo WS09, las salidas de WS13, la auditoría WS03 y el código de `graph_ui` (`workspace_routes.py`, `workspace-view.js`, `shell/registry.js`, tests). Verificaría el recibo G_UI_READ de WS24; sin él no habilitaría el delta. Cambios previstos: registrar o ajustar la vista genérica, integrarla en Context, consumir la API de grafo de sldb para relaciones entrantes/backlinks y tags públicos, mostrar tipo/tags y vecindad de 2 hops, conservar Code y recibir Markdown de WS13. Dependencias: WS13 aporta lector, explorador y foco; WS09 aporta fichas por tipo con contrato, renderer, acción, error y estado. Si falta API, contrato de tags o renderer, se detendría y registraría el hueco con repo dueño; la operación quedaría no disponible, sin sustituto. Validación esperada: pruebas con store temporal real o corpus WS40 sobre ida/vuelta, ruta de origen, tags declarados, ausencia de tags ficticios, 2 hops y Code; después acta G_UI_READ y validación humana WS30. ViewDoc no se conecta sin G_SPEC_VIEW.

FUTURO
WS13 produce lector y explorador; WS09 el catálogo; WS11 el contrato; WS03 el inventario de grafo/tags; el receptor P01 emite el acta G_UI_READ. WS30 valida uso; WS29 y WS42 consumen este resultado. Nada de eso se ejecuta aquí.
