## REFORMULACION
WS13 es un agregado de implementación en `graph_ui`: integrar en el workspace existente (`a1b2b22`) lectura solo lectura de documento/fuente y contexto, enlaces, foco por documento/nodo, explorador de modelados/no modelados, dos documentos lado a lado y pestañas/historia. Resultado: salidas conjuntas de WS13.1–WS13.3, reutilizando Code local, rutas del host y `shell/registry.js`, sin índices nuevos ni segundo workspace. Límites: solo lectura; contrato WS11 y recibo G_UI_READ por delta; no ejecuta por sí mismo.

## AMBIGUEDADES
1. «organización de contenido procede de documentos/consultas»: no se define qué son esas «consultas» ni quién las produce. Obligaría a inventar si WS13 debe organizar contenido mediante un modelo/API de consulta, una vista derivada o los documentos existentes, y a asignarle productor y aceptación, ninguno presente en los hijos.

## DRY-RUN
Agregado no ejecutable: termina cuando terminan WS13.1, WS13.2 y WS13.3. Lecturas previstas: `dag.yaml`, contrato WS11 —identidad, rutas, foco y APIs reales—, catálogo WS09 y estado del workspace `a1b2b22`. Cambios: ninguno propio; WS13.1 toca `views/workspace/node/` y tests (lectura de fuente/render, contexto, enlaces, foco); WS13.2 añade `views/workspace/explorer/` y tests (abrir modelados/no modelados sin ID, refresco); WS13.3 añade `views/workspace/layout/` y tests (pestañas, divisiones, historia). Dependencias: WS11 antes de los tres; WS13.1 antes de WS13.2 y WS13.3; G_UI_READ por delta. Transferencia: WS13.1 entrega lector, fuente, contexto y semántica de foco; WS13.2 lo usa para abrir documentos; WS13.3 conserva foco/historia al cambiar pestaña o división. Validación conjunta: aceptación de cada hijo sobre store temporal real; no hay prueba agregada adicional definida. Si falta WS11 o su API, se detiene y registra el hueco, sin sustituto.

## FUTURO
WS11 produce el contrato de navegación; WS09 el catálogo de representaciones. El receptor humano P01 emite el acta G_UI_READ de cada delta. WS14, WS15, WS22, WS23, WS24, WS27 y WS41 consumen el lector integrado.
