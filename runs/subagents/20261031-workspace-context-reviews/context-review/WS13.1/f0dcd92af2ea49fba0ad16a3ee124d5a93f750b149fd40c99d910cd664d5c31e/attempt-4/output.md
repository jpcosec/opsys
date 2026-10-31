## REFORMULACION
Propósito: convertir WS13.1 en un encargo ejecutable de lectura documental dentro de `graph_ui`. Resultado: documento/fuente en solo lectura, panel de contexto, navegación por enlaces y alternancia texto/grafo/código preservando el origen. Repo dueño: `graph_ui`. Límites: no crear otro workspace, no exigir índices nuevos, mantener rutas del host y usar las rutas/representaciones que fije WS11; promoción no autorizada.

## AMBIGUEDADES
1. «Code local con selección por documento/nodo». No define qué se selecciona ni qué efecto observable tiene. La aceptación solo exige «alternar entre texto/graph/code» y preservar origen, no comprobar la selección por documento/nodo. El ejecutor tendría que inventar si seleccionar un documento/nodo actualiza Code, si seleccionar Code cambia foco o si es solo estado visual, y cómo demostrarlo.

## DRY-RUN
Lecturas previstas: nodo WS13.1 y gates; brief/alcance; contrato y acta WS11; matriz WS09; estado del ticket workspace draft en `graph_ui`; reglas de P04/P07 aplicables a solo lectura.

Cambios previstos: vista de documento bajo `frontends/mindmap/views/workspace/document/`, panel de contexto, enlaces y alternancia texto/grafo/código, más tests. Sin tocar mutaciones, índices ni workspace paralelo.

Dependencias: WS11 y G_UI_READ; WS09/WS08 de forma transitiva; designación de responsable en WS07. Validaciones futuras: Markdown no modelado legible; identidad, relaciones y origen reales según WS11; enlaces preservan origen; no se requiere conocer ID; no se duplica el workspace; pruebas con store temporal real o corpus WS40.

## FUTURO
WS11 produce contrato de navegación, acta de aceptación y G_UI_READ; WS09 fija la matriz de representaciones; WS07 identifica al responsable de `graph_ui`. La promoción humana fija TaskDoc, archivos, escenarios y textos. WS13.2/WS13.3 dependen de esta entrega; WS16 valida lectura. La eventual integración en el ticket draft la decide el acta WS11.
