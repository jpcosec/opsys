**REFORMULACION**
- **Propósito:** preparar un candidato en el drawer (UF04, «preparar») sin crear la tarea activa ni enrutarla al Board; separa un recorrido rastreado de escritura directa por `update` con `expected`, y otro no rastreado de propuesta/handoff a `deskops edit task`.
- **Resultado:** UI de autoría en `graph_ui` (`frontends/mindmap/views/workspace/authoring/`), endpoints autorizados por WS12 y pruebas; evidencia, dependencias y pills persisten, o el handoff queda probado sin escritura HTTP.
- **Repo:** `graph_ui`. **Límites:** solo campos autorables; nunca `id`, `status`, `current_node`, `history` ni `from_drawer`; no crea tarea activa ni ruta Board (WS26.2); no inventa API ni Git sin contrato; documentos con contenido no declarado quedan bloqueados hasta WS47.

**AMBIGUEDADES**
Ninguna.

**DRY-RUN**
- **Lecturas:** `dag.yaml`/WS26.1, contrato WS12 §4.4, WS22, WS47, WS48, gates y código existente de authoring/reader en `graph_ui` y CLI deskops.
- **Cambios previstos:** módulo UI de preparación; ruta rastreada con `update`+`expected` y whitelist WS12; guarda de conservación WS47; admisión WS48; validación de pills/referencias; detección de colisión del selector; ruta no rastreada con propuesta y comando de handoff; lectura posterior; tests.
- **Dependencias/gates:** espera contrato/whitelist WS12, lector WS22, guarda WS47 y admisión WS48. `G_CLOSEOUT` está satisfecho; `G_PAYLOAD_PRECONDITION`, `G_UI_WRITE` y `G_WRITE_CONTRACT` pendientes por delta; `G_HUMAN_READ` pendiente para habilitar uso de mutaciones en UI, sin bloquear pruebas API aisladas.
- **Errores:** falta contrato/API → detener, registrar hueco y declarar operación no disponible; 409 conserva el texto local; colisión no ofrece comando; Git sin contrato → handoff/no disponible.
- **Validación esperada:** recarga muestra evidencia/dependencias/pills; 409 sin pérdida; ninguna escritura HTTP en el recorrido no rastreado; lectura posterior refleja la preparación externa; generar el comando no lo marca aplicado; caso de colisión no ofrece comando; evidencia vacía puede quedar pendiente.

**FUTURO**
WS12 fija contrato, whitelist y representación de precondición; WS47 produce la guarda; WS48 la admisión; WS45/`G_PAYLOAD_PRECONDITION` verifica la precondición; WS16/`G_HUMAN_READ` aporta acta de lectura; P01/`G_UI_WRITE` emite recibo por delta; WS26.2 crea la tarea activa y la enruta en Board.
