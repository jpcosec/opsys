REFORMULACION
Propósito: ofrecer en la UI del workspace la lectura de mensajes del inbox del desk actual y el registro de ack, con respuesta local solo si el contrato la define. Resultado: vista en graph_ui (`frontends/mindmap/views/workspace/inbox/`) con tests. Repo dueño: graph_ui; endpoints únicamente los autorizados por WS12. Límites: sin envío interdesk; ack no equivale a aprobación; no crea tarea implícita ni cron de triage; gates G_HUMAN_READ (uso de mutaciones UI), G_UI_WRITE y G_WRITE_CONTRACT por delta; desarrollo y pruebas aisladas de API pueden avanzar bajo contrato. WS25 es agregado no ejecutable: termina cuando WS25.1 y WS25.2 cumplen.

AMBIGUEDADES
Ninguna. La ausencia de operación de respuesta está cubierta por la aceptación («si no se declara no disponible») y la regla común de ejecución de alcance.md; el contrato WS12 tiene productor nombrado.

DRY-RUN
Lecturas: `contratos/operaciones.md` de WS12 (operaciones de lectura/ack/respuesta, permisos, revisión y errores); API de inbox existente en SLDB; host de workspace de Mindmap; actas de G_HUMAN_READ y G_UI_WRITE; `accepted_scope_nodes` de G_WRITE_CONTRACT. Cambios previstos: componentes de vista de inbox, acción ack contra el endpoint autorizado, acción de respuesta condicionada al contrato, y pruebas en `tests/` usando store temporal real creado en el test. Dependencias: WS12 cerrado; si falta la operación de ack o la de respuesta, detenerse, registrar el hueco con repo dueño y declarar la operación no disponible. Errores esperados: conflicto/precondición (409), permisos denegados, fallo de red en modo degradado sin fingir persistencia. Validación: test de ack que tras recarga muestra el mensaje origen, verificación de que no se crea tarea ni cron, comprobación de permisos del contrato y caso de respuesta no disponible.

FUTURO
WS25.2 aporta captura drawer/protoátomo; WS16 produce el acta de G_HUMAN_READ; el receptor P01 emite acta per-delta de G_UI_WRITE para WS25.1; WS12 fija o deja ausente la operación de respuesta; el TaskDoc de promoción concreta archivos, pills y evidencia, sin autorización aún.
