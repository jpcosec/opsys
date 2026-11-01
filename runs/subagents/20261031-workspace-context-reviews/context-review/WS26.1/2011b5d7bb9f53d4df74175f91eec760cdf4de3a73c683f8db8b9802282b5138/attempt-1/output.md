## REFORMULACION

**Propósito:** planificar en graph_ui la autoría explícita de una tarea a partir de un candidato del drawer, con evidencia declarada, dependencias y pills de contexto vinculadas.

**Resultado:** un encargo implementable cuyo criterio es que, sobre un TaskDoc real, el candidato quede autorado con evidencia, dependencias y contexto visibles tras recargar; el avance de estado nunca se logra editando `status`; toda operación Git sin contrato o dueño queda en handoff declarado no disponible.

**Repo dueño:** graph_ui, con salidas en `frontends/mindmap/views/workspace/authoring/`, endpoints que autorice WS12 y `tests/`.

**Límites:** depende de WS12 y WS22; exige G_CLOSEOUT (satisfecho), G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT. G_HUMAN_READ solo condiciona el uso de mutaciones en UI; desarrollo y pruebas aisladas de API pueden avanzar con contratos/gates técnicos. No se diseña API nueva ni se implementa promoción no admitida.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas previstas (sin ejecutar):** contrato de operaciones WS12 y sus deltas; salidas de WS22 sobre Board/TaskDoc; TaskDoc real y candidato del drawer; recibos de G_CLOSEOUT; estado de G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT por delta.

**Cambios previstos:** componentes de autoría en graph_ui para crear/autorar desde candidato, declarar evidencia, fijar dependencias y vincular pills de contexto; invocaciones a endpoints autorizados por WS12; pruebas en `tests/`.

**Dependencias:** WS12 debe definir canal, campos, actor, revisión, efectos y errores de cada operación; WS22 debe abrir el mismo TaskDoc desde sus representaciones. Si falta contrato, API o dueño de una operación Git, se registra hueco y handoff, sin sustituto.

**Validaciones futuras:** recorrido UF04 sobre TaskDoc real; persistencia visible tras recarga de evidencia, dependencias y pills; verificación de que `status` no se edita para avanzar; handoff explícito ante operación Git no disponible; pruebas aisladas de API sin depender del acta humana de lectura.

## FUTURO

- WS12 produce el contrato/delta concreto y G_WRITE_CONTRACT correspondiente.
- WS16 produce el acta de G_HUMAN_READ antes de habilitar mutaciones en UI.
- P01 registra en graph_ui la recepción por delta de G_UI_WRITE.
- La promoción requiere preflight y autorización explícita; no está autorizada.
- Si aparece un hueco de contrato/API, un humano decide el productor y el nodo queda no disponible.
