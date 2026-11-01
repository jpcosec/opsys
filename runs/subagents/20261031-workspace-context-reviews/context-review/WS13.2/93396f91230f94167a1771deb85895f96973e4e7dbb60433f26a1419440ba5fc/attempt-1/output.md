REFORMULACION
Propósito: añadir a graph_ui un explorador que permita descubrir y abrir documentos del store y Markdown no modelado del desk sin conocer IDs. Resultado: navegación y apertura de ambos tipos, con altas visibles tras refresco explícito. Repo dueño: graph_ui. Límites: `output_scope` en `frontends/mindmap/views/workspace/explorer/`, rutas de lectura y seguridad según contrato WS11, `tests/`; sin índices nuevos, sin workspace independiente y sin promoción autorizada.

AMBIGUEDADES
1. «El árbol se obtiene de la API del store y del sistema de archivos del desk» frente a una aceptación que solo exige «abrir un documento modelado y uno no modelado». No queda fijado si el resultado debe ser un árbol jerárquico navegable o basta una lista plana; el ejecutor tendría que inventar la forma del entregable y su comprobación.
2. «aparecen tras refresco explícito del catálogo» aplicado a «Markdown no modelado en desk»: el catálogo existente es de documentos del store; no se define si el refresco debe reconstruir también la exploración del sistema de archivos o si los no modelados tienen otro estado de actualización. Obligaría a inventar qué abarca el refresco y qué resultado observable se exige.

DRY-RUN
Lecturas: contrato WS11 (`contratos/navegacion.md`), salida de WS13.1, `workspace_routes.py` (`workspace_nodes`), `workspace-view.js`/`workspace.mjs` (`loadCatalog`, `filterCatalog`) y resolución del desk. Cambios previstos: crear `views/workspace/explorer/`; ruta de listado que combine API del store y recorrido seguro del desk según WS11; control de refresco que recargue catálogo y reexplore; tests. Dependencias y gates: contrato WS11 y lector WS13.1; G_UI_READ es `per_delta`, exige solo acta de WS13.2. Errores: si WS11 no fija API/seguridad de no modelados o falta el recibo, detenerse y registrar hueco en graph_ui, sin sustituto. Validación: store temporal real (test o corpus WS40), alta de documento modelado y archivo no modelado, apertura de ambos sin ID, refresco explícito sin reinicio ni cambio de código; reutilización del catálogo para modelados.

FUTURO
WS11 produce el contrato de rutas/seguridad; WS13.1 produce la lectura del Markdown no modelado; el receptor P01 emite el acta G_UI_READ por delta; WS16 valida con el corpus; el TaskDoc de promoción fija archivos y pruebas; una persona acepta el delta. WS13 cierra cuando cierran sus hijos.
