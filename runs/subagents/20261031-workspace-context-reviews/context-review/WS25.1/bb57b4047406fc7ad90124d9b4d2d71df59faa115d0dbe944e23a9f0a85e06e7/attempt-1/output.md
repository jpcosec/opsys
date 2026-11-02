## REFORMULACION
**Propósito:** entregar en graph_ui la UI de inbox para leer mensajes y registrar ack o respuesta local dentro del mismo desk, usando solo operaciones autorizadas por el contrato WS12.
**Resultado:** vista y acciones en `frontends/mindmap/views/workspace/inbox/`, con ack persistente y respuesta condicionada al contrato, más pruebas.
**Repo:** graph_ui.
**Límites:** sin envío interdesk; no crear tarea implícita ni cron de triage; ack no equivale a aprobación. Depende de WS12 y WS48; gates G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT.

## AMBIGUEDADES
Ninguna. La condición «respuesta local solo si el contrato WS12 define esa operación, y si no se declara no disponible» nombra productor y salida alternativa; los gates pendientes son intencionales.

## DRY-RUN
Un ejecutor futuro leería el contrato WS12 (operaciones, permisos, campos, errores), el módulo común de admisión de WS48, la vista de inbox existente y el TaskDoc de promoción. Cambiaría componentes de lectura de mensajes, acciones de ack/respuesta y pruebas en `tests/`, sin tocar envío interdesk.

Consumiría de WS12 los endpoints y la whitelist autorizados; si falta la operación de respuesta, la declararía no disponible. Antes de toda mutación consultaría la admisión de WS48; un rechazo produciría lectura/handoff con causa, no escritura.

Validaría con store temporal: ack visible y persistente tras recargar, mostrando el mensaje origen; permisos del contrato aplicados; respuesta local solo si existe operación contractual; ausencia de tarea implícita o cron. Errores esperados: fallo de persistencia, operación no autorizada, admisión denegada o consulta de evidencia fallida. No se ejecuta nada en esta revisión.

## FUTURO
WS12 debe publicar el contrato por delta; WS48 debe entregar el punto único de admisión; el receptor humano P01 debe emitir el acta G_UI_WRITE del delta concreto. G_HUMAN_READ habilitará el uso de mutaciones en UI. El agregado WS25 cerrará cuando WS25.1 y WS25.2 cumplan. La promoción fijará archivos, pills y evidencias en el TaskDoc.
