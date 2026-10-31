# Disposición WS12, ronda 6

Propuestas de un agente Pi DeepSeek, revisadas por el coordinador antes de aplicar.

1. error_reviewer: El acto de aceptación ya está fijado por G_UI_WRITE: «Acta de aceptación del delta definido por contrato, con identidad/fecha ...; task receptora y no solapamiento confirmados», y WS11 ya resuelve la ausencia: «si no hay recepción, el contrato queda pendiente». Cita: dag.yaml#gates G_UI_WRITE y dag.yaml#edge:WS11, acceptance.
2. corregido: WS12.acceptance -> operaciones de autoría de tareas/cierre quedan bloqueadas por G_CLOSEOUT hasta evidencia
3. error_reviewer: El baremo de «comprobada» es parte de la verificación que produce el contrato; fijarlo en el plan es detalle de promoción. Cita: context-review-guide.md, «textos exactos de pantalla, nombres de archivo y casos de prueba detallados que el TaskDoc de promoción fijará»; alcance.md, «El TaskDoc de promoción fija archivos, escenarios de prueba y textos de pantalla dentro de lo que la aceptación del nodo pide».
