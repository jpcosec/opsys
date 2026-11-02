REFORMULACION

WS25.1 encarga en `graph_ui` una UI de inbox para leer mensajes, registrar `ack` y, solo si el contrato WS12 define esa operación, responder localmente dentro del mismo desk. El resultado es una pantalla operativa con `ack` persistente, permisos aplicados y estados de no disponibilidad. Repo: `graph_ui`; salidas en `frontends/mindmap/views/workspace/inbox/`, endpoints autorizados por WS12 y `tests/`. Límites: sin envío interdesk; `ack` no equivale a aprobación; no crea tarea implícita ni cron de triage; la promoción no está autorizada.

AMBIGUEDADES

ninguna

DRY-RUN

Un ejecutor futuro leería el TaskDoc promocional, las secciones de WS12 sobre operaciones/permisos y el mecanismo de admisión de WS48, además de la vista, endpoints y pruebas existentes de inbox en `graph_ui`. No es agregado: es un nodo `delivery`; no hay secuencia con su hermano WS25.2.

Cambios previstos: añadir o modificar la vista de inbox, conectar listado/lectura, `ack` y respuesta local condicionada a WS12; toda escritura pasaría por la admisión de WS48. Añadiría estados de error, lectura/handoff y “no disponible” para respuesta local. Pruebas en store temporal o corpus WS40.

Dependencias y gates: consumiría WS12 como contrato de canal, campos, permisos y operación de respuesta; WS48 como punto único de admisión. `G_WRITE_CONTRACT` y `G_UI_WRITE` son `per_delta`; `G_HUMAN_READ` se exige antes de habilitar mutaciones en UI, no para desarrollo/pruebas aisladas.

Errores esperados: si falta contrato, canal o permiso, el ejecutor debe detenerse, registrar el hueco con repo dueño y no crear sustituto; si WS12 no define respuesta local, se declara no disponible. Validación: `ack` persiste tras recargar mostrando el mensaje origen, no se crea tarea/cron, permisos aplicados y respuesta local solo aparece si el contrato la autoriza.

FUTURO

WS12 produce el contrato y la eventual operación de respuesta; WS48 produce la admisión de escritura. El receptor P01 en `graph_ui` produce el acta de `G_UI_WRITE` por delta; WS16 produce la evidencia de `G_HUMAN_READ`. El TaskDoc fijará archivos, textos y casos de prueba. La promoción requiere autorización futura.
