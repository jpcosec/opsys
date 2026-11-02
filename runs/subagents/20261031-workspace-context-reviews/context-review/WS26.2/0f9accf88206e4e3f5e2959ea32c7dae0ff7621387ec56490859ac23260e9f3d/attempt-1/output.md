## REFORMULACION
WS26.2 encarga, en `graph_ui`, enrutar en Board una tarea creada desde el candidato y representar la capa lista. Propósito: que la UI distinga tarea enrutada, en ejecución y lista. Resultado: vista/controlador en `frontends/mindmap/views/workspace/routing/`, endpoints solo si WS12 los autoriza y pruebas. Límites: autorizar, crear la tarea activa y enrutarla es una operación conjunta W01 posterior a WS26.1; no hay operación parcial ni efecto oculto. No se implementa promoción nueva: se invoca la operación completa de WS12 o se prepara handoff. La capa lista excluye dependencias pendientes y archivos solapados según `files`; glob dudoso no se marca lista. `G_HUMAN_READ` habilita uso de mutaciones en UI, no el desarrollo ni pruebas aisladas.

## AMBIGUEDADES
1. «revisión supervisor antes de marcar lista»: no se nombra quién es el supervisor, cómo registra la revisión ni cómo se comprueba. Obliga a inventar actor, evidencia y efecto sobre la capa lista.
2. «Enrutar un TaskDoc ya existente no tiene operación pública con precondición (HO-12)»: no fija si debe usarse una operación sin precondición, quedar no disponible o pasar a handoff. Obliga a inventar el comportamiento y su aceptación para ese recorrido.

## DRY-RUN
Un ejecutor futuro leería el nodo, el contrato WS12, la representación Board de WS22, la preparación de WS26.1, la admisión de WS48 y el código actual de `graph_ui`. Añadiría la vista de enrutamiento y el cálculo de capa lista, consumiría la operación W01 y el estado real de deskops, y escribiría pruebas en `tests/`. Errores esperados: contrato/operación ausente → handoff y estado pendiente; solapamiento dudoso → no comprobado y revisión; falta de admisión WS48 → lectura/handoff. Validaría que `deskops show board` muestra la tarea, que la UI distingue enrutada/en ejecución y que la capa lista separa dependencias y solapamientos. Los gates pendientes no bloquean pruebas aisladas, pero sí la habilitación de mutaciones UI.

## FUTURO
WS12 produce W01, precondición, política de commits previos y expansión de `files`; WS22 aporta Board/lifecycle; WS26.1 prepara candidato/evidencia; WS48 aporta admisión. WS16 y P01 producen las actas de `G_HUMAN_READ` y `G_UI_WRITE`; WS12 verifica `G_WRITE_CONTRACT` por delta. El TaskDoc de promoción fija archivos, textos y pruebas.
