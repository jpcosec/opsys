REFORMULACION
Propósito: dotar a la UI de `graph_ui` de lectura de inbox y registro de ack/respuesta local mediante operaciones autorizadas por WS12. Resultado: vista/componentes en `frontends/mindmap/views/workspace/inbox/` y tests; ack persistente que muestra el mensaje origen; respuesta local solo si el contrato la define, y si no, declararla no disponible. Repo dueño: `graph_ui`. Límites: mismo desk, sin envío interdesk, ack no es aprobación, sin tarea implícita ni cron de triage; no define endpoints ni permisos propios. Es un nodo `implementation` hijo de WS25, no un agregado.

AMBIGUEDADES
ninguna.

DRY-RUN
Un ejecutor futuro leería el contrato WS12 (operaciones, permisos, errores y precondiciones), la estructura actual de `graph_ui`, los patrones de tests y el TaskDoc promovido. Cambios previstos: listado/detalle de inbox, acción de ack, acción de respuesta condicionada, estados de carga/vacío/error y tests de persistencia, permisos y ausencia de efectos prohibidos. Dependencias: consumir WS12; antes de habilitar mutaciones en UI, `G_HUMAN_READ`; `G_WRITE_CONTRACT` y `G_UI_WRITE` por delta. Si falta la operación de lectura/ack o el contrato, detenerse y registrar el hueco; si falta respuesta local, mostrarla no disponible. Los errores del contrato se muestran sin crear sustituto. Validación esperada: tras recargar, el ack persiste y muestra el mensaje origen; la respuesta cumple exactamente lo definido o queda no disponible; permisos aplicados; sin llamadas interdesk, sin tarea ni cron; pruebas con store temporal o corpus WS40.

FUTURO
El TaskDoc de promoción fijará archivos, pills, átomos y evidencia, con preflight task-only. WS12 publicará el contrato y verificará `G_WRITE_CONTRACT` por delta. WS16 producirá el acta de `G_HUMAN_READ`. El receptor P01 del repo emitirá el recibo `G_UI_WRITE` del delta concreto. La promoción requiere autorización humana; hoy figura como no autorizada.
