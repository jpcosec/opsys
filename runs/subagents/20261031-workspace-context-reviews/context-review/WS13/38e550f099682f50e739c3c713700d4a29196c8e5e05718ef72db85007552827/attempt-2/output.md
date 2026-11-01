REFORMULACION  
WS13 es un **agregado no ejecutable**: no implementa nada por sí mismo. Su propósito es integrar en `graph_ui` un lector de workspace con historia y foco sobre la base `a1b2b22`, reutilizando el registro de vistas existente. El resultado es la suma verificada de WS13.1, WS13.2 y WS13.3: lectura de documento/fuente, contexto, enlaces, Code local y foco; explorador de documentos modelados y Markdown no modelado; pestañas, divisiones e historia. Repo dueño: `graph_ui`. Límites: solo lectura de documento/fuente, conservar Code local y rutas del host, no exigir índices nuevos, no crear otro workspace, respetar contrato WS11 y recibo G_UI_READ por delta. Promoción no autorizada.

AMBIGUEDADES  
1. «organización de contenido procede de documentos/consultas». Obliga a decidir si «consultas» exige soporte de consulta derivada/guardada o solo selección de contenido existente; ningún hijo incluye esa capacidad en su aceptación. El ejecutor del agregado tendría que inventar su alcance o ignorarlo.

DRY-RUN  
Sin ejecutar nada: un ejecutor futuro del agregado no abriría código ni modificaría archivos; leería `dag.yaml` de WS13 y sus hijos, el contrato WS11, el catálogo WS09 y los recibos G_UI_READ. Cambios previstos: ninguno propio; WS13.1 aporta lector/fuente/contexto/enlaces/foco en `views/workspace/`; WS13.2 añade explorador y refresco de catálogo; WS13.3 añade pestañas, divisiones e historia conservando foco. WS13.1 precede a WS13.2 y WS13.3; ambos heredan WS11. Validación conjunta: aceptación y evidencia de cada hijo, con sus recibos por delta; WS13 cierra solo cuando los tres hijos cumplen, sin commit único ni nueva implementación agregada. Si falta WS11 o un recibo, se detiene y registra el hueco; no se sustituye.

FUTURO  
WS11 produce el contrato de navegación; el receptor P01 emite actas G_UI_READ por delta; WS09 fija las representaciones soportadas. La autorización de promoción y la aceptación humana quedan fuera de este nodo.
