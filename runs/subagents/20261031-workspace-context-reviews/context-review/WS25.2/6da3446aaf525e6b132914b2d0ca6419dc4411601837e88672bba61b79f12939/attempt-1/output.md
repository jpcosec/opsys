## REFORMULACION
Propósito: implementar en `graph_ui` la captura interna con destino elegido explícitamente —candidato de drawer o protoátomo— usando solo operaciones permitidas por WS12, sin exigir tarea. Resultado: flujo de captura persistente y probado por separado para cada destino, con origen tipado y control de colisiones. Repo dueño: `graph_ui`. Límites: no crear API/modelo por reflejo, no asumir el canal de drawer ni el de protoátomo, no habilitar mutaciones UI sin `G_HUMAN_READ`, no tocar otros repos y no convertir `ack` en aprobación.

## AMBIGUEDADES
ninguna

## DRY-RUN
Un ejecutor futuro, sin ejecutar ahora, modificaría archivos bajo `frontends/mindmap/views/workspace/capture/` y `tests/` en `graph_ui`: añadiría la UI de captura con selección explícita de destino, llamadas exclusivas a las operaciones autorizadas por WS12, registro y presentación del origen tipado —ruta o mensaje— y manejo de colisión según contrato. Consumiría el contrato WS12 para canal de drawer, canal de protoátomo, representación del origen, permisos y colisiones; `G_WRITE_CONTRACT` para las operaciones concretas; `G_UI_WRITE` mediante recibo por delta; y `G_HUMAN_READ` antes de habilitar mutaciones en UI, pudiendo avanzar desarrollo/pruebas aisladas de API con contratos técnicos. Si falta canal, API, dato o permiso, se detendría y registraría el hueco con repo dueño, sin sustituto. Casos de error: colisión no silenciosa según contrato; operación no autorizada rechazada; fallo de persistencia declarado. Validación esperada: cada destino, probado por separado, persiste tras recargar; origen ruta/mensaje visible; sin tarea implícita; permisos aplicados; colisión controlada.

## FUTURO
WS12 produce el contrato y los canales/representación de origen/colisiones/permisos. El receptor P01 emite el acta `G_UI_WRITE` del delta concreto; WS12 verifica `G_WRITE_CONTRACT` por operación. WS16 produce el acta `G_HUMAN_READ`. WS25 cierra como agregado cuando cumplen WS25.1 y WS25.2. La promoción sigue no autorizada y el TaskDoc fijará archivos, pruebas y textos exactos.
