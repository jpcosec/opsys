REFORMULACION  
Propósito: encargo de planificación para que `graph_ui` oriente a quien abre un proyecto sin desk, muestre destino e init CLI, no inicialice por GET y refresque la lectura tras un init externo. Resultado: vista/componente en `frontends/mindmap/views/workspace/orientation/`, rutas de lectura según contrato WS11 y tests. Repo dueño: `graph_ui`. Límites: sin mutaciones ni init por GET; depende de WS13 y G_UI_READ pendiente; `promotion: not_authorized`; no se ejecuta nada.

AMBIGUEDADES  
1. «destino explícito» / «muestra orientación y destino». No se define qué es “destino”: ruta del proyecto, ubicación donde ejecutar init, comando, URL o siguiente paso. Obliga a inventar el contenido mostrado y el criterio de aceptación de ese elemento.  
2. «init CLI». No se indica comando, argumentos ni desde dónde ejecutarlo; el nodo tampoco declara de qué nodo/artefacto toma esa instrucción ni qué hacer si falta. Obliga a inventar la instrucción que la UI debe mostrar.

DRY-RUN  
Lecturas: `dag.yaml#node:WS15.2`, guía de revisión y fuentes suministradas; los bloques edge solo como contexto. Cambios previstos: UI de orientación y tests en `output_scope`; sin mutación ni GET de init. Dependencias: WS13, G_UI_READ pendiente, contrato de rutas WS11 e init CLI externo. Validaciones futuras: abrir proyecto sin desk y comprobar orientación/destino/sin mutación; ejecutar init fuera de la UI y refrescar para ver el desk real; aceptación G_UI_READ y preflight de promoción.

FUTURO  
WS11 produce rutas de lectura y resuelve G_UI_READ; WS13 aporta lector/contexto; WS07 o actor humano designa responsable de `graph_ui`; WS16 valida arranque; la promoción exige archivos/pills/evidencia y preflight task-only.
