## REFORMULACION
**Propósito:** implementar en la UI la lectura de mensajes del inbox y el registro de `ack` o respuesta local dentro del mismo desk.  
**Resultado:** vista de inbox en `graph_ui` con lectura, ack persistente y respuesta solo si WS12 la define; pruebas incluidas.  
**Repo dueño:** `graph_ui`; salida acotada a `frontends/mindmap/views/workspace/inbox/`, endpoints autorizados por WS12 y `tests/`.  
**Límites:** sin envío interdesk; ack no equivale a aprobación; no crea tareas implícitas ni cron de triage; no inventa operaciones ausentes del contrato.

## AMBIGUEDADES
Ninguna.

La eventual “respuesta local” queda condicionada por el contrato WS12 y su ausencia tiene salida explícita: “si no se declara no disponible”. El source del inbox, permisos concretos y endpoints quedan delegados al contrato/dependencia, no al ejecutor.

## DRY-RUN
**Lecturas previstas:** nodo WS25.1, guía, alcance y contrato producido por WS12 cuando exista; evidencia de gates.  
**Cambios previstos:** componentes de inbox bajo el `output_scope`, consumo de endpoints autorizados y tests.  
**Dependencias:** WS12 aporta whitelist/capacidades; WS16 aporta `G_HUMAN_READ`; `G_UI_WRITE` y `G_WRITE_CONTRACT` deben estar resueltos.  
**Validaciones futuras:** ack persiste tras recarga y muestra mensaje origen; respuesta local solo aparece si WS12 define la operación; permisos aplicados; no se crea tarea ni cron; no hay envío interdesk.

## FUTURO
WS12 produce el contrato técnico de operaciones y permisos. WS16 produce la aceptación humana de lectura. El responsable humano/graph_ui acepta el delta de `G_UI_WRITE`. La promoción fijará archivos exactos, textos y escenarios de prueba. La autorización de ejecución y el cierre del agregado WS25 corresponden a otro nodo/humano, no a este revisor.
