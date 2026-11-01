## REFORMULACION

Propósito: dotar a la UI del workspace de lectura de mensajes de inbox y registro de ack o respuesta local dentro del mismo desk, usando solo operaciones autorizadas por el contrato WS12. Resultado: vista en `frontends/mindmap/views/workspace/inbox/` que muestra mensajes, persiste el ack tras recargar y, solo si WS12 define esa operación, permite respuesta local; si no, la declara no disponible. Repo dueño: `graph_ui`. Límites: sin envío interdesk; ack no es aprobación; no crea tarea implícita ni cron de triage; permisos del contrato aplicados; desarrollo y pruebas aisladas de API pueden avanzar, pero el uso de mutaciones en UI queda tras `G_HUMAN_READ`; promoción no autorizada.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

Un ejecutor futuro, tras promoción autorizada y TaskDoc, cambiaría archivos bajo `frontends/mindmap/views/workspace/inbox/` y `tests/`: añadiría la vista de lectura, la acción de ack contra el endpoint que fije WS12, el estado deshabilitado para respuesta local si el contrato no la define, y pruebas. Consumiría el contrato WS12 para canal, campos, permisos y errores; `G_WRITE_CONTRACT` por delta, `G_HUMAN_READ` antes de habilitar mutaciones en UI y `G_UI_WRITE` como recibo del delta concreto. Casos de error: operación de ack ausente en WS12 → detenerse y registrar hueco con repo dueño; permiso denegado → mostrar rechazo; backend caído → modo degradado declarando el límite; fallo de ack → no mostrar éxito falso. Validación esperada: prueba con store temporal real donde el ack persiste tras recarga mostrando el mensaje origen; respuesta local disponible solo si el contrato la define; ninguna tarea ni cron creados; permisos aplicados. Validación humana, cuando corresponda, sobre el corpus WS40.

## FUTURO

WS12 decide si existe la operación de respuesta local y fija su canal, campos, permisos y errores. WS16 produce el acta de `G_HUMAN_READ`. El receptor P01 emite el recibo `G_UI_WRITE` por delta. La promoción fija archivos, textos y pruebas concretas. WS25.2 cubre la captura; WS25 cierra cuando ambos hijos cumplen.
