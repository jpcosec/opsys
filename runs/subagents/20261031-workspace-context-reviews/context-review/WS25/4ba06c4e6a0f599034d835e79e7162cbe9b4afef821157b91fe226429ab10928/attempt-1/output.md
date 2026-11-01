## REFORMULACION
WS25 es un nodo agregado (`node_role: aggregate`) de implementación en `graph_ui` cuyo encargo es integrar en la UI la lectura de inbox con ack/respuesta local y la captura interna hacia drawer o protoátomo, usando únicamente operaciones permitidas por el contrato WS12. El resultado son las salidas de WS25.1 y WS25.2. Límites: no se ejecuta por sí mismo; no confunde ack con aprobación; sin envío interdesk; no crea tarea implícita; requiere G_HUMAN_READ (solo para habilitar mutaciones en UI), G_UI_WRITE y G_WRITE_CONTRACT por delta.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
WS25 no es ejecutable: termina cuando WS25.1 y WS25.2 cumplen su aceptación. Un ejecutor futuro de WS25.1 leería el contrato WS12 (`deskops:contratos/operaciones.md`, whitelist por operación/campo/canal) y modificaría `frontends/mindmap/views/workspace/inbox/` más `tests/`, consumiendo solo endpoints autorizados; errores: operación no definida en contrato → declarar «no disponible» sin sustituto; ack que no persiste → test falla; permisos no aplicados → test falla. Validación esperada: ack persiste tras recarga mostrando mensaje origen; respuesta local solo si el contrato la define; sin tarea implícita ni cron. WS25.2 modificaría `frontends/mindmap/views/workspace/capture/` y `tests/`, con origen tipado (ruta/mensaje) fijado por WS12; errores: contrato sin canal de captura → registrar hueco con dueño, no inventar API; colisión no controlada → test falla. Validación esperada: captura persiste tras recarga en el destino elegido, con origen visible, sin tarea implícita y sin sobrescritura silenciosa. Gates de ambos hijos: G_WRITE_CONTRACT per_delta (solo el delta concreto), G_UI_WRITE per_delta y G_HUMAN_READ para habilitar uso de mutaciones.

## FUTURO
WS12 publica contrato, whitelist y matriz de capacidades/huecos; WS16 produce el acta de G_HUMAN_READ; el receptor P01 emite actas G_UI_WRITE por delta en el repo dueño; WS30 valida UF02 con registro humano; WS43 publica entradas reales del desk tras corpus y gate manual.
