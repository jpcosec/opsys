# Disposición WS26.2, ronda 3

Propuestas de un agente Pi DeepSeek, revisadas por el coordinador antes de aplicar.

1. corregido: WS26.2.acceptance -> el canal de promoción respeta commits previos y estado real; la capa lista se muestra separada de tareas en ejecución y de tareas con dependencias pendientes o archivos s
2. error_reviewer: context-review-guide.md: «textos exactos de pantalla, nombres de archivo y casos de prueba detallados que el TaskDoc de promoción fijará». La regla exacta de solapamiento es detalle de implementación delegado.
3. error_reviewer: alcance.md: «Si al llegar a un nodo falta un contrato, API, dato o permiso que debía producir una dependencia: detenerse, registrar el hueco con repo dueño y no crear sustituto. La operación queda no disponible.» La promoción depende del contrato y de G_CLOSEOUT; su comprobación exacta es detalle del TaskDoc.
4. error_reviewer: context-review-guide.md: «detalles que el nodo delega a su promoción (archivos exactos, TaskDoc, pills)». El mapeo de estados de dependencia a la capa lista es detalle delegado.
