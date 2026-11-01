REFORMULACION
Encargo de planificación para WS25.1: definir una UI de graph_ui que permita leer mensajes del inbox y registrar ack o respuesta local usando solo operaciones autorizadas por el contrato WS12. Resultado esperado: pieza UI en `frontends/mindmap/views/workspace/inbox/`, endpoints autorizados y tests, sin envío interdesk ni confundir ack con aprobación. Límites: no crear tarea implícita ni cron de triage; la respuesta local queda no disponible si WS12 no define la operación. Repo dueño: graph_ui.

AMBIGUEDADES
ninguna

DRY-RUN
Lecturas: nodo WS25.1; guía, brief, alcance, decisiones y cobertura; contexto de vecinos WS12, WS25 y gates, sin revisarlos. Cambios previstos: ninguno ahora; a futuro, implementación limitada a la UI de inbox, endpoints autorizados y tests dentro del `output_scope`. Dependencias: WS12 produce el contrato de operaciones/permisos; los gates G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT se aplican según su alcance. Validaciones futuras: ack persiste tras recargar y muestra el mensaje origen; respuesta local solo si el contrato la define, declarando no disponible en caso contrario; no se crea tarea implícita ni cron; se aplican permisos del contrato. No se ejecuta nada.

FUTURO
WS12 debe publicar las operaciones, campos, permisos, errores y pruebas aplicables al inbox, incluida la existencia o ausencia de respuesta local. El receptor humano P01 decide la recepción por delta de G_UI_WRITE; WS16 produce la evidencia de G_HUMAN_READ; WS12 resuelve G_WRITE_CONTRACT. La promoción fijará archivos exactos, TaskDoc, pills, átomos, evidencia y preflight task-only. WS25, como agregado, solo termina cuando WS25.1 y WS25.2 cumplan su aceptación.
