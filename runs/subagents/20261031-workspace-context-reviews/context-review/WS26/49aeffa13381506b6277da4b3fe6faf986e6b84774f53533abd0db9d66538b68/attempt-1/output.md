## REFORMULACION

**Propósito:** revisar WS26 como encargo de planificación: agregado que integra autoría desde candidato, evidencia, dependencias, contexto/pills y enrutamiento en Board con capa lista.

**Resultado:** nodo `aggregate` no ejecutable; cierra cuando WS26.1 y WS26.2 cumplen su aceptación. `output_scope` es el agregado de sus salidas.

**Repo:** `graph_ui`.

**Límites:** no confundir Board route con ejecución; promoción solo mediante canal autorizado que respete commits previos y estado real; sin editar status para avanzar; operaciones Git sin contrato quedan en handoff/no disponibles.

**Dependencias:** WS12, WS22, WS26.1, WS26.2; gates G_CLOSEOUT, G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT.

## AMBIGUEDADES

Ninguna.

El agregado no ejecuta: su aceptación remite a los hijos y su alcance queda cubierto por WS26.1/WS26.2. La frase «promoción solo cuando el contrato resuelve commits previos por canal autorizado» identifica el contrato en WS12 (whitelist/capabilities) y G_CLOSEOUT; no obliga a inventar otro. «El canal de promoción debe respetar commits previos y estado real» es criterio operativo delegado a WS12 y a la aceptación de WS26.2, no resultado indefinido para este nodo. La dependencia de WS26 respecto de sus propios hijos es coherente con la semántica de agregado indicada en la guía.

## DRY-RUN

**Lecturas (sin ejecutar):** `context-review-guide.md`, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, nodo WS26 y bloques edge WS12/WS22/WS26.1/WS26.2, gates.

**Cambios previstos:** ninguno; esta revisión no modifica el plan.

**Dependencias:** WS12 aporta contrato de operaciones/escritura; WS22 representación de Board; WS26.1 autoría/contexto; WS26.2 enrutamiento/capa lista. Gates pendientes son intencionales.

**Validaciones futuras:** aceptación de WS26.1 y WS26.2; cierre agregado de WS26; G_CLOSEOUT, G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT; cobertura UF04; validación humana WS30.

## FUTURO

WS12 debe producir/verificar contrato y aceptar deltas; WS16 produce G_HUMAN_READ; WS07 registra decisiones humanas P01–P09 y designaciones; WS26.1 y WS26.2 ejecutan y demuestran sus aceptaciones; WS30 valida el recorrido completo. Ninguna de esas tareas corresponde a este revisor.
