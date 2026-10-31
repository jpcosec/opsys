## REFORMULACION
- **Propósito:** encargar una UI para leer mensajes del inbox, registrar ack y responder localmente dentro del mismo desk.
- **Resultado:** vista/UI en `graph_ui` y tests que persisten el ack, aplican permisos del contrato y solo habilitan respuesta si WS12 define esa operación.
- **Repo:** `graph_ui`.
- **Límites:** sin envío interdesk; ack no equivale a aprobación; no crear tarea implícita ni cron de triage; salidas en `frontends/mindmap/views/workspace/inbox/`, endpoints autorizados por WS12 y `tests/`.

## AMBIGUEDADES
ninguna.

## DRY-RUN
- **Lecturas:** nodo WS25.1 y fuentes suministradas; WS12/WS16 solo como dependencias, sin revisar sus contratos.
- **Cambios previstos:** UI de inbox y pruebas en el `output_scope` indicado; sin ejecución ni modificación de otros repos.
- **Dependencias:** WS12 aporta contrato, whitelist y capabilities; WS16 aporta `G_HUMAN_READ`; se requieren `G_UI_WRITE` y `G_WRITE_CONTRACT`.
- **Validaciones futuras:** con store temporal o corpus WS40, comprobar que el ack persiste tras recargar y muestra el mensaje origen; que la respuesta local solo aparece si WS12 la define y, si no, se declara no disponible; que se aplican permisos; que no se crea tarea implícita ni cron; que no hay envío interdesk.

## FUTURO
- WS12 produce el contrato de operaciones y determina si existe la operación de respuesta local.
- WS16 produce la aprobación humana `G_HUMAN_READ`.
- El responsable designado de `graph_ui` acepta el delta de `G_UI_WRITE`; la promoción fija TaskDoc, archivos, pills, atoms, evidencia y preflight.
- Un humano resuelve decisiones y gates pendientes; aquí no se aprueban.
