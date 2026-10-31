## REFORMULACION
**Propósito:** entregar en `graph_ui` la UI para leer mensajes del inbox del desk y registrar ack o respuesta local mediante operaciones autorizadas.  
**Resultado:** inbox legible con ack persistente y mensaje origen visible; respuesta local disponible solo si el contrato WS12 la define; en caso contrario, se declara no disponible.  
**Repo dueño:** `graph_ui`; salida en `frontends/mindmap/views/workspace/inbox/` y `tests/`.  
**Límites:** sin envío interdesk; ack no equivale a aprobación; no crea tarea implícita ni cron de triage; permisos y endpoints según el contrato WS12.

## AMBIGUEDADES
ninguna.

## DRY-RUN
**Lecturas:** nodo WS25.1, aristas WS12/WS25, gates, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md` y guía. Sin ejecución.

**Cambios previstos:** componentes de lectura de inbox, ack y eventual respuesta local en `graph_ui`, invocando operaciones del contrato WS12; pruebas en `tests/`.

**Dependencias:** contrato WS12 por operación/campo/canal/permisos/efectos; gates `G_HUMAN_READ`, `G_UI_WRITE` y `G_WRITE_CONTRACT`, estos dos evaluados por delta.

**Validaciones futuras:** ack persiste tras recargar mostrando el mensaje origen; respuesta local solo si WS12 define la operación, declarándola no disponible en caso contrario; no se crea tarea implícita ni cron de triage; permisos del contrato aplicados.

## FUTURO
WS12 publica la whitelist y el contrato técnico por operación; si falta la operación de ack o de respuesta, se registra el hueco y la operación queda no disponible. P01 emite el acta de recepción por delta para `G_UI_WRITE`; WS16 produce el acta de `G_HUMAN_READ`. La promoción fijará TaskDoc, archivos, pruebas y textos dentro de la aceptación; no está autorizada en este nodo.
