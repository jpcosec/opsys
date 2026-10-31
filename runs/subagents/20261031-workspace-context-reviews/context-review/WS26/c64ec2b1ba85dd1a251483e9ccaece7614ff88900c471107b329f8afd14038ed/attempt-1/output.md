## REFORMULACION

**Propósito:** WS26 es un nodo `aggregate` que vertebra la autoría explícita desde candidato (evidencia, dependencias, pills) y el contexto de tareas en graph_ui.

**Resultado:** agregado no ejecutable: sus salidas son las de WS26.1 (autorar tarea, evidencia y contexto) y WS26.2 (enrutar en Board y mostrar capa lista). Se considera cumplido cuando ambos hijos cumplen su aceptación.

**Repo dueño:** graph_ui, con endpoints autorizados por el contrato WS12.

**Límites:** no confundir Board route con ejecución; no implementar promoción nueva; si falta operación admitida por WS12, handoff y estado pendiente. G_HUMAN_READ habilita uso de mutaciones en UI, no bloquea desarrollo/pruebas aisladas de API. Promoción `not_authorized`; TaskDoc fijará archivos, pills y evidencias.

## AMBIGUEDADES

Ninguna. El nodo delega explícitamente el contenido operativo en WS26.1/WS26.2, cuyo alcance y aceptación están definidos. Los gates pendientes son intencionales y `per_delta`; el contrato de promoción y el comportamiento ante contrato ausente quedan resueltos por WS12, WS26.2 y las reglas comunes de alcance.md.

## DRY-RUN

**Lecturas:** guía de revisión, brief, alcance, decisiones, cobertura, entradas dag de WS26/WS26.1/WS26.2/WS12/WS22/WS30 y gates.

**Cambios previstos:** ninguno propio del agregado; cierre cuando terminen WS26.1 y WS26.2.

**Dependencias:** WS12 (contrato de operaciones/escritura), WS22 (Board navegable), WS26.1 y WS26.2. Gates: G_CLOSEOUT satisfecho; G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT pendientes por delta.

**Validaciones futuras:** aceptación de ambos hijos; recibo de recepción G_UI_WRITE para el delta concreto; contrato WS12 verificado; acta humana de lectura previa a habilitar mutaciones; recorrido UF04 en WS30.

## FUTURO

- WS12 publica el contrato y huecos asignados.
- WS22 entrega la representación de Board.
- WS26.1 y WS26.2 implementan autoría, enrutamiento y capa lista.
- El receptor P01 emite el acta por delta en el repo dueño.
- WS16 produce el acta de G_HUMAN_READ.
- WS30 valida autoría y revisión manual completas.
