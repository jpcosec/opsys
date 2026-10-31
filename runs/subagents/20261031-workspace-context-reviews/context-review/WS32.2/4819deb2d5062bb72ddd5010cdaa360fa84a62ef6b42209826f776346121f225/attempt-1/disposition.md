# Disposición WS32.2, ronda 8

Propuestas de un agente Pi DeepSeek, revisadas por el coordinador antes de aplicar.

1. error_reviewer: Política de conflicto ante evidencia distinta es caso de borde de implementación y no impide ejecutar la aceptación. context-review-guide.md: «textos exactos de pantalla, nombres de archivo y casos de prueba detallados que el TaskDoc de promoción fijará».
2. error_reviewer: Origen y cálculo del hash son detalle de implementación; el cierre existente ya produce el hash de sesión (`deskops/services/closure.py`). alcance.md: «El TaskDoc de promoción fija archivos, escenarios de prueba y textos de pantalla dentro de lo que la aceptación del nodo pide».
3. error_reviewer: El ticket es un artefacto del repo con ruta y hash en external_references; sus campos adicionales se leen al ejecutar y no hay resultado indefinido. alcance.md: «Si al llegar a un nodo falta un contrato, API, dato o permiso que debía producir una dependencia: detenerse, registrar el hueco con repo dueño y no crear sustituto».
