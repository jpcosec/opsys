REFORMULACION  
WS26.1 encarga en graph_ui la preparación de un candidato del drawer (UF04) con dos recorridos: edición directa por campos con precondición `expected`, guarda WS47 y admisión WS48, y propuesta/handoff a `deskops edit task` sin escritura HTTP. El resultado es el módulo de autoría en `frontends/mindmap/views/workspace/authoring/` y `tests/`. Límites: solo campos autorables; nunca `id`, `status`, `current_node`, `history` ni `from_drawer`; no crea tarea activa ni ruta Board; no inventa API; los gates pendientes bloquean el uso, no el desarrollo aislado.

AMBIGUEDADES  
1. «El handoff se ofrece solo si una comprobación previa confirma que el selector no resuelve a una tarea activa» / «(nombre idéntico y prefijo)». No se define qué es «selector» ni qué «prefijo»; el ejecutor tendría que inventar la regla de coincidencia y cuándo suprimir el comando.  
2. «no amplía S06». S06 no aparece definido en el nodo ni en los contratos suministrados; el ejecutor tendría que inventar qué capacidad o alcance queda excluido.  
3. «una lectura posterior que refleja la preparación hecha fuera de la UI». «Refleja» no fija observación ni prueba; el ejecutor tendría que inventar cómo demostrar que esa lectura posterior refleja el cambio.

DRY-RUN  
Leería `task-ws26-1.md`, el contrato WS12 (sección 4.4), WS47, WS48, WS22 y el estado de los gates. Crearía la vista/módulo de autoría y sus pruebas; conectaría el guardado directo solo por endpoint autorizado con `expected`, guarda WS47 y admisión WS48; implementaría lista de pills y handoff CLI. Consumiría `G_PAYLOAD_PRECONDITION` (WS45) y `G_UI_WRITE` por delta. Si falta contrato, API o dueño, pararía y registraría el hueco. Errores previstos: 409 conserva el texto local; WS47 rechaza contenido no declarado; la admisión deniega la escritura; un selector que resuelve a tarea activa no ofrece comando. Validaría recarga de evidencia/dependencias/pills, 409, handoff sin HTTP, lectura posterior, y ausencia de edición de `status` o ruta Board.

FUTURO  
WS12 fija operación, precondición y whitelist; WS47 y WS48 fijan sus guardas; WS45 resuelve `G_PAYLOAD_PRECONDITION`; WS26.2 crea la tarea activa y la ruta Board; P01/WS16 expiden `G_UI_WRITE`/`G_HUMAN_READ`; la promoción fija archivos y pruebas exactas.
