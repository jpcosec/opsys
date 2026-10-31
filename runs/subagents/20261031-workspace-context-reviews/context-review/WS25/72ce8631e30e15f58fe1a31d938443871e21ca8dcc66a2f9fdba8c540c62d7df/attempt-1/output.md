REFORMULACION
Revisar WS25 como encargo de planificación: comprobar si propósito, resultado, repo dueño, límites, dependencias y aceptación son comprensibles. WS25 es `aggregate` no ejecutable; su resultado son las salidas de WS25.1 y WS25.2. Repo dueño: `graph_ui`. Límites: solo input explícito, sin ejecutar, sin revisar los bloques `edge` vecinos.

AMBIGUEDADES
Ninguna. El nodo declara agregado no ejecutable, hijos, repo, dependencias, gates y aceptación por cumplimiento de hijos. Las concreciones de destinos, origen, permisos y respuesta local están delegadas a WS25.1/WS25.2 y al contrato WS12, sin obligar a inventar al ejecutor de este agregado.

DRY-RUN
Lecturas: guía de revisión; nodo WS25; contratos vecinos WS12, WS16, WS25.1, WS25.2 y WS30; gates; brief, alcance, decisiones y cobertura. Cambios previstos: ninguno; esta revisión no modifica el plan. Dependencias: WS12 aporta contrato y gates `G_UI_WRITE`/`G_WRITE_CONTRACT`; WS16 aporta `G_HUMAN_READ`; WS25.1/WS25.2 son hijos que materializan el agregado. Los gates pendientes son intencionales. Validaciones futuras: aceptación de ambos hijos, evidencia de gates, validación humana WS30 y preflight de promoción; nada se ejecuta aquí.

FUTURO
WS12 debe producir el contrato de operaciones y las aceptaciones de escritura; WS16 debe obtener la aprobación humana de lectura; WS25.1/WS25.2 implementan inbox/ack y captura; WS30 valida los flujos; el responsable de `graph_ui` y el solicitante resuelven promoción y decisiones Pxx. No son ambigüedades de este nodo.
