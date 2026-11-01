## REFORMULACION

WS19.2 es un nodo de implementación en `graph_ui`: añadir alta y baja de relaciones permitidas por contrato en el workspace, usando API real y la precondición de escritura que fije WS12, sin introducir semántica de relaciones en el componente. Resultado: relaciones que persisten y se confirman tras recarga, y rechazo visible de una relación no permitida o una revisión obsoleta. Repo dueño: `graph_ui`; salida bajo `frontends/mindmap/views/workspace/relations/`, endpoints autorizados por WS12 y `tests/`. Límites: solo relaciones de la whitelist WS12; no crear endpoints, semántica ni campos; promoción no autorizada. El desarrollo y las pruebas aisladas de API pueden avanzar con contratos técnicos, pero el uso de mutaciones en UI queda tras G_HUMAN_READ.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

Lecturas: definición del nodo y gates en `dag.yaml`; contrato WS12 cuando exista; `task_file` del nodo; código actual de `views/workspace/` y endpoints de edición. Cambios previstos: componentes de alta/baja de relaciones, llamada a los endpoints autorizados por WS12, mapeo de errores a mensaje visible y pruebas. Dependencias consumidas: WS12 fija whitelist, operaciones, representación de la precondición y errores; WS45 produce G_PAYLOAD_PRECONDITION; WS16 produce G_HUMAN_READ; el receptor P01 produce G_UI_WRITE por delta; WS12 produce G_WRITE_CONTRACT por delta. Si falta contrato, endpoint o precondición, el ejecutor se detiene, registra el hueco con repo dueño y declara la operación no disponible; no crea sustituto. Validación esperada: con store temporal real, alta y baja persisten y se confirman tras recargar; relación no permitida y revisión obsoleta se rechazan con error visible; pruebas automatizadas cubren ambos caminos. Los gates pendientes no bloquean pruebas aisladas de API, pero sí habilitar mutaciones en UI.

## FUTURO

WS12 entrega el contrato de operaciones y escritura. WS45 verifica la precondición de payload. WS16 produce el acta de G_HUMAN_READ. El receptor P01 emite el acta G_UI_WRITE del delta concreto. La promoción fijará archivos exactos, pills, átomos y evidencia y exigirá preflight específico de tarea; no está autorizada.
