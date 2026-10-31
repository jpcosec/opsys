## REFORMULACION

**Propósito:** implementar en `graph_ui` la lectura de inbox y el registro de ack o respuesta local dentro del mismo desk, usando solo operaciones autorizadas por el contrato WS12; ack no equivale a aprobación.

**Resultado:** vista en `frontends/mindmap/views/workspace/inbox/` donde el ack persiste tras recargar mostrando el mensaje origen; la respuesta local existe solo si WS12 la define y, si no, se declara no disponible; sin tarea implícita ni cron de triage.

**Repo:** `graph_ui`. **Límites:** sin envío interdesk, permisos del contrato aplicados, promoción no autorizada.

## AMBIGUEDADES

Ninguna. El nodo nombra repo, resultado, límites, dependencias y aceptación comprobable; la condicionalidad de la respuesta y el comportamiento ante contrato ausente quedan cubiertos por WS12 y por `alcance.md` («detenerse, registrar el hueco... La operación queda no disponible»). No hay frase que obligue al ejecutor a inventar.

## DRY-RUN

**Lecturas:** guía, brief, alcance, decisiones, cobertura, nodo WS25.1, edges WS12/WS16/WS25 y gates.

**Cambios previstos:** ninguno en esta revisión; la ejecución futura tocaría la vista inbox, la integración de operaciones y tests.

**Dependencias:** WS12 produce contrato/whitelist y `G_WRITE_CONTRACT`/`G_UI_WRITE`; WS16 produce `G_HUMAN_READ`. Gates pendientes intencionales; `G_UI_WRITE` exige acta del responsable `graph_ui`. No se asume contrato existente.

**Validaciones futuras:** el TaskDoc de promoción fijará archivos y pruebas; ack persistente; respuesta condicional; permisos aplicados; ausencia de tarea/cron.

## FUTURO

WS12 entrega el contrato y resuelve sus gates; WS16 produce la aprobación humana de lectura; el solicitante/humano designa al responsable `graph_ui` y decide P01/P04/P07/P08/P09 vía WS07; la promoción autoriza y fija el TaskDoc; WS25 cierra cuando WS25.1 y WS25.2 cumplen.
