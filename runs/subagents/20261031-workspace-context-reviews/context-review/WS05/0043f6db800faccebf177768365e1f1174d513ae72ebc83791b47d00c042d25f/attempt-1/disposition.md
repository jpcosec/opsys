# Disposición WS05, ronda 5

Propuestas de un agente Pi DeepSeek, revisadas por el coordinador antes de aplicar.

1. error_reviewer: WS33 es un nodo del DAG con scope propio (referencias Hub/proyecto/conversación/mensaje/intento); WS05 delega en WS32/WS33 qué capabilities consumen y el ejecutor las lee de sus contratos. Cita: context-review-guide.md, «dag.yaml es la fuente de IDs, aristas y gates».
2. error_reviewer: Pide versión y precedencia entre documentación y SDK exportado; es un caso de borde del inventario, no un resultado indefinido. Cita: context-review-guide.md, «No cuentan: ... detalles que el nodo delega a su promoción (archivos exactos, TaskDoc, pills)»; el scope ya fija «endpoints/SDK documentados o exportados; no tablas ni funciones internas».
3. error_reviewer: Las equivalencias slug/dispatch/conversación se obtienen al inventariar el runtime y la API de Scion, que el scope manda leer; no son términos del glosario del workspace. Cita: context-review-guide.md, «No cuentan: ... detalles que el nodo delega a su promoción (archivos exactos, TaskDoc, pills)».
