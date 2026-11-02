REFORMULACION

WS25 es un nodo agregado de planificación en `graph_ui`: encarga integrar en la UI el triage de inbox —leer, ack y respuesta local— y la captura interna en drawer/protoátomo usando solo operaciones permitidas por WS12, sin confundir ack con aprobación. Su resultado no es una entrega propia: es la suma de las salidas aceptadas de WS25.1 y WS25.2. Límites: no envío interdesk, no tarea/cron implícitos, no API/modelo nuevo por reflejo; mutaciones UI solo tras G_HUMAN_READ y con G_WRITE_CONTRACT/G_UI_WRITE por delta; promoción no autorizada. Esta revisión no ejecuta.

AMBIGUEDADES

ninguna

DRY-RUN

El agregado no se ejecuta: no tiene archivos, comandos ni gates propios que consumir. Su cierre es la aceptación de ambos hijos; no hay arista entre ellos ni transferencia de artefacto entre hermanos, solo integración conjunta.

WS25.1: leerá el contrato WS12 y la salida de WS48; intervendrá `frontends/mindmap/views/workspace/inbox/` y `tests/`; implementará lectura/ack y, si WS12 define la operación, respuesta local; validará persistencia tras recarga, mensaje origen mostrado, permisos y ausencia de tarea/cron implícitos.

WS25.2: leerá WS12, WS46 y WS48; intervendrá `frontends/mindmap/views/workspace/capture/` y `tests/`; implementará captura a drawer/protoátomo con destino explícito; validará persistencia tras recarga, origen tipado ruta/mensaje, ausencia de tarea implícita y colisión no silenciosa; no podrá cerrar declarando no disponible.

Validación conjunta: WS25 cierra cuando constan ambas aceptaciones; WS30 recorre UF02. G_WRITE_CONTRACT y G_UI_WRITE se evalúan por ID/delta, y G_HUMAN_READ antes de habilitar mutaciones UI. Si falta una dependencia, se detiene y registra hueco con repo dueño, sin sustituto.

FUTURO

WS12 produce el contrato de operaciones/whitelist; WS46, la capacidad probada de captura con origen; WS48, su salida según arista. WS16 resuelve G_HUMAN_READ; el receptor P01 emite actas G_UI_WRITE por delta; WS12 resuelve G_WRITE_CONTRACT por delta. WS30 valida UF02. La promoción y el TaskDoc quedan para autorización humana/técnica posterior.
