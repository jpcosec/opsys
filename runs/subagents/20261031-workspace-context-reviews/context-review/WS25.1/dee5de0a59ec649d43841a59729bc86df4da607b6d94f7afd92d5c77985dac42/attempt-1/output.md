## REFORMULACION

**Propósito:** encargar la UI de lectura del inbox y el registro de ack o respuesta local dentro del mismo desk, usando solo operaciones autorizadas por contrato.

**Resultado:** ack persistente tras recargar, mostrando el mensaje origen; respuesta local únicamente si el contrato WS12 define esa operación, y declarada no disponible en caso contrario; sin creación implícita de tareas ni cron de triage; permisos del contrato aplicados.

**Repo dueño:** `graph_ui`.

**Límites:** salida en `frontends/mindmap/views/workspace/inbox/`, endpoints autorizados por WS12 y `tests/`; sin envío interdesk; ack no equivale a aprobación. Promoción no autorizada.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

- **Lecturas previstas:** nodo WS25.1, guía de revisión, brief, alcance, decisiones, cobertura y gates; en ejecución futura, contrato de operaciones de WS12 y acta de WS16.
- **Cambios previstos:** componentes de lectura de inbox, ack y, condicionada al contrato, respuesta local; pruebas en `tests/`.
- **Dependencias:** WS12 produce whitelist/capabilities y resuelve `G_UI_WRITE` y `G_WRITE_CONTRACT`; WS16 produce `G_HUMAN_READ`. Ambas figuran como prerrequisitos.
- **Validaciones futuras:** ack visible tras recarga con mensaje origen; respuesta solo con operación contractual o declaración de no disponibilidad; ausencia de tarea implícita y cron; permisos aplicados; ningún envío interdesk.
- **Sin ejecución:** no se modifica código, no se promueve la tarea ni se crean archivos.

## FUTURO

- WS12 debe entregar el contrato con operaciones, canales y efectos, y aceptar el delta de `graph_ui`.
- WS16 debe producir el acta humana de `G_HUMAN_READ`.
- El solicitante humano debe designar responsables y aprobar los gates pendientes.
- La promoción posterior fijará archivos, pills, átomos, evidencia y preflight task-only; hasta entonces el nodo no es tarea ejecutable.
- WS25 cerrará como agregado cuando sus hijos cumplan su aceptación.
