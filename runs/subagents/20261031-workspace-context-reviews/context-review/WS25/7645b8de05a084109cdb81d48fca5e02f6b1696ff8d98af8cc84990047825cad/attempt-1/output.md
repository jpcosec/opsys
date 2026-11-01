## REFORMULACION

El encargo de WS25 es agrupar la implementación de UI para mensaje/ack y captura interna en drawer o protoátomo, usando solo operaciones permitidas por WS12 y sin confundir ack con aprobación. El resultado es el agregado de las salidas de WS25.1 y WS25.2. El repo dueño es `graph_ui`; el alcance excluye envío interdesk, creación implícita de tareas y diseñar API o modelo nuevos. Las mutaciones en UI quedan sujetas a `G_HUMAN_READ`, `G_UI_WRITE` y `G_WRITE_CONTRACT` por delta. La promoción no está autorizada.

## AMBIGUEDADES

Ninguna. WS25 es agregado no ejecutable: su aceptación queda definida por la aceptación de sus hijos y no introduce un resultado propio que obligue a inventar.

## DRY-RUN

No hay ejecución propia de WS25. Un ejecutor futuro trataría el nodo como cierre de agregado: leería `dag.yaml`, el TaskDoc y los contratos/evidencias de WS12 y de WS25.1–WS25.2; no modificaría código por WS25.

- **WS25.1**: implementaría la vista de inbox y ack/respuesta local en `frontends/mindmap/views/workspace/inbox/` y `tests/`, contra endpoints autorizados por WS12. Transferiría a WS25 evidencia de ack persistente, mensaje origen visible, permisos aplicados y respuesta local solo si el contrato la define.
- **WS25.2**: implementaría la captura con destino explícito en `frontends/mindmap/views/workspace/capture/` y `tests/`, también contra WS12. Transferiría persistencia tras recarga, origen tipado, ausencia de tarea implícita y control de colisiones.

Ambos hijos comparten repo y dependencia WS12, pero se validan por separado; no hay dependencia entre ellos. WS25 cerraría solo cuando ambos cumplan su aceptación y existan los recibos por delta de `G_UI_WRITE`/`G_WRITE_CONTRACT`; `G_HUMAN_READ` habilita el uso de mutaciones, no el desarrollo aislado. El resultado conjunto se validaría después en WS30.

## FUTURO

WS12 produce el contrato de operaciones y canal. WS25.1 y WS25.2 producen implementación y pruebas. WS16 produce el acta de `G_HUMAN_READ`; el receptor P01 decide/registra `G_UI_WRITE` por delta. WS30 verifica el recorrido manual completo.
