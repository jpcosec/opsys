## REFORMULACION
Propósito: revisar WS25 como encargo de planificación para integrar captura y triage en la UI. Resultado: nodo `aggregate` cuya aceptación se cumple cuando cumplen sus hijos WS25.1 y WS25.2; su salida es el agregado de ambas, sin ejecución propia. Repo dueño: `graph_ui`. Límites: UI para mensaje/ack y captura interna de drawer/protoátomo solo mediante operaciones permitidas por contrato; ack no equivale a aprobación; no se revisan aquí los contratos de nodos vecinos.

## AMBIGUEDADES
ninguna.

## DRY-RUN
Lecturas: guía de revisión, brief, alcance, decisiones, cobertura y nodo WS25 en `dag.yaml`; bloques de vecinos solo como contexto, no revisados. Cambios previstos: ninguno; es revisión, no promoción ni ejecución. Dependencias: WS12 (contrato de operaciones/escritura), WS16 (validación humana de lectura) y agregación de WS25.1/WS25.2; gates `G_HUMAN_READ`, `G_UI_WRITE` y `G_WRITE_CONTRACT`, pendientes de forma intencional. Validaciones futuras: aceptación de ambos hijos; WS30 validará UF02. No se ejecuta nada.

## FUTURO
WS12 produce la whitelist/capabilities y las evidencias de `G_UI_WRITE` y `G_WRITE_CONTRACT`; WS16 produce el acta de `G_HUMAN_READ`; WS25.1 y WS25.2 implementan y prueban inbox/ack y captura; WS30 valida el recorrido manual. La promoción y las decisiones Pxx quedan a un humano; no son ambigüedad de este nodo.
