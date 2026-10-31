# Disposición WS04, ronda 7

Propuestas de un agente Pi DeepSeek, revisadas por el coordinador antes de aplicar.

1. error_reviewer: El universo ya es verificable en dag.yaml: los nodos que tocan graph_ui son los de `owner_repo: graph_ui`, que coinciden con todos los scope_nodes de G_UI_READ/G_UI_WRITE. Cita: context-review-guide.md, «dag.yaml es la fuente de IDs, aristas y gates».
2. error_reviewer: Path y hash de una entrada de Board sin archivo de tarea son formato de la auditoría, no un resultado indefinido. Cita: context-review-guide.md, «textos exactos de pantalla, nombres de archivo y casos de prueba detallados que el TaskDoc de promoción fijará».
3. error_reviewer: La evidencia de reclamación de archivos es un caso de borde de la observación de sesiones. Cita: context-review-guide.md, «No cuentan: ... detalles que el nodo delega a su promoción (archivos exactos, TaskDoc, pills)».
4. error_reviewer: La granularidad de la reconciliación con el SPEC es formato del informe. Cita: context-review-guide.md, «textos exactos de pantalla, nombres de archivo y casos de prueba detallados que el TaskDoc de promoción fijará»; alcance.md, «El TaskDoc de promoción fija archivos, escenarios de prueba y textos de pantalla dentro de lo que la aceptación del nodo pide».
