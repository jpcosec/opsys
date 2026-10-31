## REFORMULACION
Propósito: definir WS25.1 como encargo de planificación para una UI que lea el inbox del desk y registre `ack` o una respuesta local mediante operaciones autorizadas por el contrato WS12.

Resultado esperado: piezas de UI en `graph_ui`, bajo `frontends/mindmap/views/workspace/inbox/`, más pruebas, capaces de mostrar mensajes, persistir `ack` y ofrecer respuesta local solo si WS12 define esa operación.

Límites: sin envío interdesk; `ack` no equivale a aprobación; no crear tareas implícitas ni cron de triage; no inventar endpoints, permisos ni operaciones ausentes. `G_HUMAN_READ` condiciona el uso de mutaciones en UI, no el desarrollo/pruebas aisladas de API con contratos técnicos.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Lecturas: guía de revisión, brief, alcance, decisiones, cobertura y nodos/aristas/gates relevantes del DAG. No se ejecuta nada.

Cambios previstos: UI de lectura de inbox, registro de `ack` y, condicionadamente, respuesta local; integración con endpoints autorizados por WS12; pruebas en `tests/`.

Dependencias: WS12 como productor del contrato; gates `G_HUMAN_READ`, `G_UI_WRITE` y `G_WRITE_CONTRACT`, evaluados por delta concreto.

Validaciones futuras: que `ack` persista tras recargar mostrando el mensaje origen; que la respuesta local solo exista si WS12 la define y, si no, se declare no disponible; que se apliquen permisos del contrato; que no se cree tarea implícita ni cron de triage.

## FUTURO
WS12 debe publicar el contrato de operaciones y los recibos técnicos aplicables. WS16 produce el acta de `G_HUMAN_READ`. WS25 cierra como agregado cuando sus hijos cumplan. La promoción fijará archivos, textos y pruebas en el TaskDoc. La aceptación por delta corresponde al actor humano designado.
