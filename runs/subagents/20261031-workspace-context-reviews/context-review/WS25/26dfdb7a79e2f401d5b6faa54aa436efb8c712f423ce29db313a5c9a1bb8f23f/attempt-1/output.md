## REFORMULACION
**Propósito:** integrar en la UI la lectura de mensajes/ack y la captura interna en drawer o protoátomo, sin confundir ack con aprobación. **Resultado:** nodo agregado no ejecutable; se cumple cuando WS25.1 y WS25.2 cumplen su aceptación, y sus salidas constituyen el agregado. **Repo dueño:** `graph_ui`. **Límites:** operar solo mediante operaciones permitidas por el contrato de WS12; no envío interdesk; no crear tarea implícita ni cron de triage; promoción no autorizada.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
- **Lecturas previstas:** WS25, sus dependencias declaradas, gates `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`, y fuentes de alcance/decisiones; sin revisar contratos de nodos vecinos ni ejecutar.
- **Cambios previstos:** ninguno; el nodo es `aggregate` y no produce cambios por sí mismo.
- **Dependencias:** WS12 aporta contrato/whitelist; WS16 aporta aprobación humana de lectura; WS25.1 y WS25.2 aportan las salidas agregadas.
- **Validaciones futuras:** aceptación de ambos hijos; resolución de gates por sus productores; cobertura UF02 en WS30. No se ejecutan aquí.

## FUTURO
- WS12 produce la whitelist/capabilities y resuelve `G_UI_WRITE`/`G_WRITE_CONTRACT`; WS16 produce `G_HUMAN_READ`.
- WS25.1 y WS25.2 implementan y prueban inbox/ack/respuesta local y captura, respectivamente.
- WS30 valida el recorrido UF02 con humano real.
- La promoción futura fijará archivos, TaskDoc y evidencia; requiere autorización y preflight, no lo decide este nodo.
