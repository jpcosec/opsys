## REFORMULACION

WS13.1 es un encargo de implementación en **graph_ui**: ampliar el lector integrado a partir de la base a1b2b22 para que un documento —incluido Markdown sin modelo— tenga render de lectura y fuente cruda íntegra con el mismo origen, panel de contexto (identidad, relaciones y origen), seguimiento de enlaces y Code local, con foco por documento/nodo compartido entre representaciones solo donde WS11 defina correspondencia real. El resultado exigido es evidencia de aceptación de esas conductas, sin crear otro workspace ni requerir índices nuevos. Límites: solo lectura, reutilizar rutas/componentes existentes y el contrato WS11, no inventar mapeo texto→código ni depender de conocer un ID. Depende de WS11 y requiere G_UI_READ por delta.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

Leería el contrato de navegación de WS11, el catálogo WS09, `workspace_routes.py`, `views/workspace/node/workspace-view.js`, `workspace.mjs`, el registro de vistas y los tests existentes; comprobaría la base a1b2b22 y el recibo G_UI_READ de este delta. Cambios previstos: rutas de lectura en graph_ui para fuente Markdown modelada y no modelada con resolución WS11, componentes de contexto/enlaces y estado de foco por documento bajo `views/workspace/`, más pruebas en `tests/`. No tocaría escritura ni índices. Consumiría WS11 para identidad, rutas, relaciones y correspondencia de foco, y WS09 para las representaciones declaradas. Si falta una ruta, API o relación, o el catálogo no declara una representación, detendría el trabajo y registraría el hueco con repo dueño, sin crear sustituto. Validaría con store temporal real y Markdown del desk: render y fuente con mismo origen, contexto, enlace seguido y foco conservado al alternar texto/graph/code, sin copia ni dependencia de ID. Sin recibo G_UI_READ no cerraría ni promovería el delta.

## FUTURO

WS11 produce el contrato de navegación y el mapa de recepción; WS09, el catálogo de representaciones. El receptor P01 en graph_ui produce el acta G_UI_READ por delta. WS13.2 y WS13.3 aportan explorador y pestañas, sin ser dependencias directas de WS13.1. WS13 cierra como agregado cuando sus hijos cumplen. La promoción fijará TaskDoc, archivos exactos y pruebas.
