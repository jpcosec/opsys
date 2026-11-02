## REFORMULACION
Encargo de planificación para WS26.1: preparar en la UI un candidato del drawer (UF04) con dos recorridos: escritura directa rastreada mediante `update` con precondición `expected` y guardas WS47/WS48, y propuesta no rastreada con handoff explícito a `deskops edit task` y lectura posterior de comprobación. Resultado: autoría limitada a campos autorizables, evidencia, dependencias, `files`, referencias, tags, pills y `closeout_evidence`; nunca `id`, `status`, `current_node`, `history` ni `from_drawer`; sin crear tarea activa ni ruta de Board (WS26.2). Repo dueño: `graph_ui`; alcance: `frontends/mindmap/views/workspace/authoring/`, endpoints autorizados por WS12 y `tests/`. Límites: sin API inventada, sin escritura HTTP en el recorrido no rastreado, sin marcar aplicado por generar un comando y handoff no disponible si falta contrato/dueño.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Un ejecutor futuro leería el contrato WS12 (sección 4.4 y whitelist), las salidas de WS22, las guardas WS47 y WS48, la evidencia de G_CLOSEOUT y el estado de G_PAYLOAD_PRECONDITION; inspeccionaría el módulo de autoría y los endpoints autorizados en `graph_ui`. Cambios previstos: extender/crear la vista de autoría, formulario de campos autorizables, envío rastreado con `expected`, integración de la guarda de contenido de WS47 y del punto de admisión de WS48, edición de pills con validación y conservación, propuesta y handoff a `deskops edit task`, refresco posterior y bloqueo de campos protegidos. Añadiría pruebas en `tests/`.

Dependencias y gates: consumiría WS12, WS22, WS47 y WS48; exigiría G_CLOSEOUT, G_HUMAN_READ para uso de mutaciones, G_PAYLOAD_PRECONDITION, G_UI_WRITE y G_WRITE_CONTRACT. Ante contrato/API ausente: detenerse, registrar hueco y declarar la operación no disponible; nunca inventar sustituto.

Errores y validación esperada: guardado obsoleto → 409 sin perder texto local; rechazo de WS47 sin cambios; campos protegidos no editables; selector que resuelve a tarea activa → no se ofrece comando; recorrido no rastreado sin escritura HTTP y con lectura posterior que refleja lo preparado fuera de la UI; persistencia visible tras recarga; botón deshabilitado no válido. Pruebas sobre store temporal real.

## FUTURO
WS26.2 crea la tarea activa y la enruta en Board. WS45 produce la precondición de payload. WS16 aporta el acta humana de lectura. La promoción fijará TaskDoc, archivos, pills, átomos y evidencia; la aceptación por delta queda en el repo receptor.
