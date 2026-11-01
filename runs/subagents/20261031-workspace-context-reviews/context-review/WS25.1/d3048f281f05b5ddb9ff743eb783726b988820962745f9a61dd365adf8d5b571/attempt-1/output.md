## REFORMULACION
El nodo encarga construir en `graph_ui` la UI de inbox del mismo desk: leer mensajes y registrar ack o respuesta local usando solo operaciones autorizadas por el contrato WS12. Resultado: vista/componente en `frontends/mindmap/views/workspace/inbox/` con lectura, ack persistente y respuesta condicionada. Repo dueño: `graph_ui`. Límites: sin envío interdesk; ack no es aprobación; no crea tarea implícita ni cron de triage; respuesta solo si WS12 la define; mutaciones de UI sujetas a G_HUMAN_READ.

## AMBIGUEDADES
ninguna.

## DRY-RUN
Un ejecutor leería el TaskDoc promovido, `contratos/operaciones.md` de WS12 (canal público, whitelist ack/respuesta, precondición y errores) y la evidencia de gates. Crearía o modificaría componentes en `frontends/mindmap/views/workspace/inbox/` y `tests/`: listado/lectura de mensajes, acción ack que invoca el adapter autorizado, rama de respuesta solo si el contrato la define (si no, mostrar «no disponible»), estados de error/vacío. No tocaría tareas ni añadiría cron. Consumiría WS12 como prerrequisito (con WS11/WS08 detrás). Si falta la operación ack o su adapter, se detendría, registraría el hueco con repo dueño y declararía la operación no disponible, sin inventar sustituto. Gates: G_WRITE_CONTRACT por delta para ack/respuesta; G_UI_WRITE por delta (acta P01); G_HUMAN_READ antes de habilitar uso de mutaciones, aunque desarrollo/pruebas aisladas pueden avanzar. Errores esperados: contrato ausente, permiso denegado o fallo de precondición/escritura, mostrados honestamente. Validación: prueba de ack con recarga que conserva el ack y muestra el mensaje origen; prueba de la rama respuesta disponible/no disponible; verificación de permisos; comprobación de ausencia de tarea implícita y cron.

## FUTURO
WS12 produce el contrato/whitelist y adapter de ack/respuesta; WS16 produce el acta G_HUMAN_READ; el receptor P01 en `graph_ui` produce el acta G_UI_WRITE del delta. WS25.2 cubre captura drawer/protoátomo; WS25 (agregado) cierra cuando ambos hijos cumplen. El TaskDoc de promoción fija archivos, textos y pruebas; la persona decide la aceptación del delta.
