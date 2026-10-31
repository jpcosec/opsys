REFORMULACION
Propósito: agrupar la entrega de UI para leer/ack de inbox y captura interna en drawer o protoátomo, sin confundir ack con aprobación. Resultado: nodo agregado no ejecutable; se cierra cuando WS25.1 y WS25.2 cumplen su aceptación, y sus dependientes siguen dependiendo de WS25. Repo dueño: graph_ui. Límites: solo operaciones permitidas por el contrato WS12; sin envío interdesk; sin tarea implícita ni cron de triage; ack no equivale a aprobación; promoción no autorizada; no se ejecuta aquí.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas: guía de revisión, brief, alcance, decisiones, cobertura, nodo WS25, hijos WS25.1/WS25.2, aristas WS12/WS16/WS30 y gates G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT. Cambios previstos: ninguno; esta revisión no modifica archivos ni promueve el nodo. Dependencias: WS12 aporta contrato de operaciones y gates de escritura; WS16 aporta G_HUMAN_READ; WS25.1 y WS25.2 son hijos que materializan inbox/ack y captura. Validaciones futuras: aceptación de cada hijo, cierre agregado de WS25 y validación humana de WS30 sobre UF02/03/04/05; G_UI_WRITE incluye WS25 y sus hijos.

FUTURO
WS12 produce whitelist, canal, efectos y G_WRITE_CONTRACT/G_UI_WRITE; WS16 produce el acta humana de G_HUMAN_READ; WS25.1/WS25.2 implementan y prueban sus alcances; WS30 valida el recorrido manual; una persona resuelve Pxx, acepta deltas y autoriza la promoción. Nada de esto es ambigüedad del encargo actual.
