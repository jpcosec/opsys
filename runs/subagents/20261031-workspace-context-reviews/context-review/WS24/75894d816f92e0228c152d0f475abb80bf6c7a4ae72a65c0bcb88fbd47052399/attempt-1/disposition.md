# Executor comparison — WS24

State: requires_contract_correction_rereview

## Reformulación examinada

## REFORMULACION
WS24 es un nodo de implementación en `graph_ui` que debe integrar conocimiento y grafo local reutilizando el gráfico existente y una vista única de documento genérica registrada en `shell/registry.js`, con átomos/protoátomos/crossroads, materializaciones, pills, clasificación, vecindad de hasta 2 hops y backlinks derivados de la API de grafo de sldb. Resultado esperado: navegación ida/vuelta por fuentes y backlinks, soporte Markdown sin modelo visible con ruta de origen, clasificación y vecindad, preservando Code local del workspace `a1b2b22`. Límites: depende de WS13 y WS09; requiere G_UI_READ por delta; ViewDoc WS18 es opcional y no bloquea; no exige un renderer nuevo por clase; promoción no autorizada.

##

## Comparación con intención / hallazgos

1 tags provienen payload/semantic_tags públicos según WS03/WS11; 2 no modelados heredados de WS13.1/13.2 vía WS13, sin segundo lector; 3 Context ruta existente node/workspace-view.js y registry explicitados.

Se leyó reformulación, ambigüedades, dry-run y futuro del output completo. Se compara propósito/resultado/repo/límites, secuencia/autoridad, aceptación y decisiones con contrato suministrado. No se inyecta este output o disposición al siguiente modelo.
