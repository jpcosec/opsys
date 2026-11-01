## REFORMULACION
- **Propósito:** encargar la UI para leer mensajes del inbox del desk, registrar `ack` y, solo si el contrato lo define, responder localmente.
- **Resultado:** vista y acciones en `graph_ui`, con persistencia del `ack`, mensaje origen visible y permisos del contrato aplicados; sin tarea implícita ni cron de triage.
- **Repo:** `graph_ui`; `output_scope: frontends/mindmap/views/workspace/inbox/; endpoints autorizados por el contrato WS12; tests/`.
- **Límites:** sin envío interdesk; `ack` no equivale a aprobación; respuesta local condicionada a WS12 y, si falta, “se declara no disponible”; desarrollo/pruebas aisladas pueden avanzar, pero las mutaciones UI requieren `G_HUMAN_READ`.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
- **Lecturas previstas:** nodo WS25.1, contrato WS12, gates `G_HUMAN_READ`/`G_UI_WRITE`/`G_WRITE_CONTRACT` y reglas de alcance ya suministradas.
- **Cambios previstos:** solo en `graph_ui`, bajo `frontends/mindmap/views/workspace/inbox/` y `tests/`; endpoints según WS12.
- **Dependencias:** WS12 —y por alcance WS11/WS08—; contrato de operaciones, permisos y efectos; recibos por delta de `G_UI_WRITE` y `G_WRITE_CONTRACT`.
- **Validaciones futuras:** `ack` persiste tras recargar y muestra el mensaje origen; respuesta local definida por WS12 o declarada no disponible; no se crea tarea ni cron; permisos aplicados; pruebas en `tests/`; acta humana de lectura antes de habilitar mutaciones UI. `G_HUMAN_READ` pendiente es intencional.

## FUTURO
WS12 decide si existe la operación de respuesta local y fija canal, permisos y efectos. WS16 produce el acta de `G_HUMAN_READ`. El receptor P01 emite recibos por delta para `G_UI_WRITE` y la verificación de contrato. La promoción, aún no autorizada, fijará archivos exactos, pills y pruebas en el TaskDoc. WS25 cerrará cuando lo hagan sus hijos.
