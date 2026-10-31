# Disposición WS27.1, ronda 3

Propuestas de un agente Pi DeepSeek, revisadas por el coordinador antes de aplicar.

1. corregido: WS27.1.acceptance -> sin escribir ni revertir nada
2. error_reviewer: context-review-guide.md: «casos de prueba detallados que el TaskDoc de promoción fijará». Rango, profundidad, filtro y renames del historial son detalle delegado.
3. error_reviewer: context-review-guide.md: «textos exactos de pantalla, nombres de archivo y casos de prueba detallados que el TaskDoc de promoción fijará». El filtro de referencias y el fallo ante hash ausente o clon shallow son detalle de implementación.
4. error_reviewer: alcance.md: «El TaskDoc de promoción fija archivos, escenarios de prueba y textos de pantalla dentro de lo que la aceptación del nodo pide.» La resolución ruta→repo usa las rutas del contrato WS11; el detalle queda delegado.
5. error_reviewer: context-review-guide.md: «casos de prueba detallados que el TaskDoc de promoción fijará». Archivos no rastreados y repos sin HEAD son casos de borde delegados.
6. error_reviewer: El nodo monta su propia vista (output_scope views/workspace/diff/) y WS13 ya abre TaskDoc como documento; montaje y archivos son detalle delegado por alcance.md: «El TaskDoc de promoción fija archivos, escenarios de prueba y textos de pantalla».
