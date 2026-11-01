REFORMULACION
WS13 es un agregado de implementación en `graph_ui` que integra el lector workspace: documento/fuente solo lectura, contexto, enlaces, selección por documento/nodo, explorador de documentos modelados y Markdown no modelado, dos documentos lado a lado, pestañas e historia. No se ejecuta: su resultado es la suma aceptada de WS13.1, WS13.2 y WS13.3. Límites: reutilizar el workspace a1b2b22 y Code local, conservar rutas del host, no exigir índices nuevos, no duplicar implementación; cada delta requiere su recibo G_UI_READ y el contrato WS11.

AMBIGUEDADES
1. «organización de contenido procede de documentos/consultas». Ningún hijo define qué es una consulta, quién la produce ni cómo organiza el lector; el brief además dice que no se promete modelo de consulta guardada. El ejecutor tendría que decidir si organiza por documentos, por consultas o ambas, y con qué API, pudiendo exceder el alcance.

DRY-RUN
WS13 no se ejecuta. WS13.1 lee el contrato WS11, el catálogo WS09, la matriz WS06 y el workspace a1b2b22; cambia `views/workspace/node/` y tests; entrega lector, fuente cruda/render, contexto, enlaces y foco compartido. WS13.2, tras WS11 y WS13.1, cambia `explorer/` y tests; consume ese lector para abrir documentos modelados y no modelados sin conocer ID y refrescar el catálogo. WS13.3, tras WS11 y WS13.1, cambia `layout/` y tests; consume el mismo lector para pestañas, divisiones, foco e historia. WS13.2 y WS13.3 no tienen arista entre sí: no se entregan nada; su integración se valida conjuntamente.

Validaciones: WS13.1 exige fuente cruda íntegra y render con mismo origen, contexto real y foco compartido; WS13.2 exige alta en store temporal visible tras refresco sin cambiar código; WS13.3 exige abrir/cerrar pestañas, dos documentos y volver conservando foco e historia. La integración conjunta abre un modelado y un no modelado sin ID, alterna fuente/render, sigue enlaces y usa pestañas/divisiones. Cada hijo consume su recibo G_UI_READ; el gate global sigue pendiente y `accepted_scope_nodes` vacío. Si falta WS11, API o recibo, se detiene y registra el hueco, sin sustituto.

FUTURO
WS11 produce el contrato de navegación; el receptor P01 emite actas por delta; la promoción fija TaskDoc, archivos y pruebas. WS14/22/23/24/27/39/41 consumirán WS13; WS40 aporta corpus y WS16 la validación humana.
