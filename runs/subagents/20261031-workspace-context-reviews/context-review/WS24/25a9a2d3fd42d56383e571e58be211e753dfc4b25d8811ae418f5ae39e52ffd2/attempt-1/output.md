REFORMULACION  
WS24 es un nodo de implementación en `graph_ui` para integrar conocimiento y grafo local reutilizando el grafo existente y una vista genérica registrada en `shell/registry.js`. El resultado esperado es navegación ida/vuelta por fuentes y backlinks, Markdown no modelado visible con su ruta de origen, clasificación por tipo/tags y vecindad de hasta 2 hops, preservando Code local. Límites: no crear un renderer obligatorio por clase, no inferir tags por carpeta, no duplicar el lector de WS13 y no conectar ViewDoc antes de G_SPEC_VIEW.

AMBIGUEDADES  
ninguna.

DRY-RUN  
Un ejecutor futuro leería `dag.yaml`, el contrato WS11, el catálogo WS09, las salidas de WS13/WS13.1/WS13.2, el inventario WS03, la vista y rutas actuales del workspace, y la API de grafo de sldb documentada. Cambios previstos: crear/ajustar `frontends/mindmap/views/workspace/graph/`, modificar el panel Context de `node/workspace-view.js`, registrar la vista genérica en `shell/registry.js` y añadir pruebas. Consumiría WS13 para lector/explorador y Markdown no modelado, WS09 para el catálogo, WS03/WS11 para tags y backlinks, y G_UI_READ por delta. WS18/G_SPEC_VIEW solo sería extensión opcional. Si falta un contrato requerido, se detendría y registraría el hueco con repo dueño, sin sustituto. Validaría con store temporal real: Markdown sin modelo navegable con ruta de origen, backlinks entrantes por API de grafo, vecindad de 2 hops, tipo/tags declarados, Code preservado y ausencia de clasificación ficticia. G_UI_READ pendiente es intencional; no bloquea desarrollo aislado, pero sí la aceptación del delta concreto.

FUTURO  
WS13 entrega lector/explorador y soporte Markdown no modelado; WS09 el catálogo de renderizaciones; WS11 el contrato de navegación/tags/backlinks; WS03 el inventario de infraestructura. El receptor humano P01 emite G_UI_READ por delta concreto. WS18 y G_SPEC_VIEW son opcionales y no bloquean WS24.
