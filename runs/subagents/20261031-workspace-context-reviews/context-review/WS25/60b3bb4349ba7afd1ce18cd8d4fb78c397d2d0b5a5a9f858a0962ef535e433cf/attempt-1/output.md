## REFORMULACION

**Propósito:** revisar WS25 como encargo de planificación: nodo agregado que integra en la UI de graph_ui la lectura/ack de inbox y la captura interna en drawer o protoátomo, sin confundir ack con aprobación.

**Resultado:** agregado no ejecutable; se cumple cuando WS25.1 y WS25.2 cumplen su aceptación. Sus dependientes siguen dependiendo de WS25.

**Repo:** `graph_ui` (`output_base: graph_ui:repository_root/`).

**Límites:** solo operaciones permitidas por el contrato WS12; sin envío interdesk; sin crear tarea implícita ni cron de triage; mutaciones en UI solo con G_HUMAN_READ; G_UI_WRITE y G_WRITE_CONTRACT por delta concreto.

## AMBIGUEDADES

Ninguna.

El título menciona «triage», pero el alcance concreto se reparte en los hijos («mensaje/ack y captura interna de drawer/protoátomo») y la aceptación agregada delega en ellos; no obliga a inventar un comportamiento adicional. La dependencia redundante de los hijos con WS12 junto a la del padre no crea trabajo ni resultado indefinido.

## DRY-RUN

**Lecturas previstas (sin ejecutar):** nodo WS25 en `dag.yaml`, nodos WS25.1/WS25.2, aristas WS12 y WS30, gates G_HUMAN_READ/G_UI_WRITE/G_WRITE_CONTRACT; guía, brief, alcance, decisiones y cobertura ya suministrados.

**Cambios previstos:** ninguno. WS25 es `node_role: aggregate` y no se ejecuta; no procede promoción (`promotion: not_authorized`). Si se promoviera, solo coordinaría a sus hijos.

**Dependencias:** contrato WS12 (canal público, operaciones por campo/actor/efectos) y gates asociados por delta; WS30 como validación humana aguas abajo.

**Validaciones futuras:** aceptación de WS25.1 (ack persiste tras recarga, respuesta local solo si el contrato la define, permisos aplicados) y de WS25.2 (captura persiste en destino elegido, origen tipado ruta/mensaje visible tras recarga, sin tarea implícita); acta humana de lectura; recepción por delta en graph_ui.

## FUTURO

- WS25.1 y WS25.2 producen la evidencia de aceptación que cierra el agregado.
- WS12 produce el contrato de operaciones y los recibos G_UI_WRITE/G_WRITE_CONTRACT por delta.
- WS16 produce el acta que satisface G_HUMAN_READ.
- WS30 registra la validación humana de autoría y revisión.
- El responsable humano acepta deltas en graph_ui; nada de esto es ambigüedad del nodo.
