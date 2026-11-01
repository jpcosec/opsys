REFORMULACION

WS26 es un agregado de planificación en `graph_ui`: integrar autoría explícita desde candidato, evidencia, dependencias y contexto/pills con el enrutamiento en Board y la capa lista. No se ejecuta: su resultado es la suma aceptada de WS26.1 y WS26.2, sin confundir ruta de Board con ejecución ni crear promoción nueva. Límites: usar solo operaciones admitidas por WS12; si faltan, handoff y estado no disponible; no editar `status` para avanzar.

AMBIGUEDADES

ninguna.

DRY-RUN

WS26 no produciría cambios directos. Un ejecutor futuro leería `dag.yaml` (WS26, WS26.1, WS26.2), sus aristas WS12/WS22/WS30 y `task-ws26.md`. WS26.1 consumiría WS22 (TaskDoc, selección y links del lector) y WS12 (endpoints autorizados); modificaría `frontends/mindmap/views/workspace/authoring/`, endpoints autorizados y `tests/`, dejando un candidato autorado con evidencia, dependencias y pills visibles tras recargar. Si una operación Git no tiene contrato/dueño, produciría handoff explícito, no una acción terminada. WS26.2 consumiría WS22, WS12 y el TaskDoc resultante de WS26.1; modificaría `frontends/mindmap/views/workspace/routing/`, endpoints autorizados y `tests/`, mostrando la tarea enrutada en `deskops show board`, separada de ejecución, y la capa lista separada de tareas con dependencias pendientes o archivos solapados. No implementaría promoción: invocaría solo la operación completa admitida por WS12 o dejaría handoff. La validación conjunta sería la aceptación de ambos hijos; WS30 haría después la validación humana UF04/UF05. Gates: G_CLOSEOUT ya satisfecho; G_HUMAN_READ pendiente (WS16) bloquea uso de mutaciones en UI, no desarrollo/pruebas aisladas; G_UI_WRITE y G_WRITE_CONTRACT pendientes por delta.

FUTURO

WS12 debe publicar el contrato de operaciones y precondiciones; WS22, la representación de Board; WS16, el acta de lectura para G_HUMAN_READ; el receptor P01, las actas por delta de G_UI_WRITE; y WS12, la evidencia de G_WRITE_CONTRACT. WS30 decidirá la aceptación humana posterior.
