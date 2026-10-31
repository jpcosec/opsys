# Disposición WS05, ronda 8

Propuestas de un agente Pi DeepSeek, revisadas por el coordinador antes de aplicar.

1. error_reviewer: WS33 existe en el DAG (Vincular mensajes, resultados y decisiones) con scope propio que define lo que consume; el ejecutor no inventa su alcance, lo lee del plan. Cita: context-review-guide.md, «dag.yaml es la fuente de IDs, aristas y gates».
2. error_reviewer: La precedencia cuando documentación y exports discrepan, y el borde de un símbolo auxiliar exportado, son casos de borde del inventario; el scope ya fija el criterio «endpoints/SDK documentados o exportados; no tablas ni funciones internas». Cita: context-review-guide.md, «No cuentan: ... detalles que el nodo delega a su promoción (archivos exactos, TaskDoc, pills)».
