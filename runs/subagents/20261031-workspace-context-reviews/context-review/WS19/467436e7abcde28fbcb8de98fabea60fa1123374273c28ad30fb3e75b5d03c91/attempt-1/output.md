REFORMULACION
WS19 es un nodo agregado de implementación en `graph_ui`: integrar la edición de campos con conflicto visible sobre el workspace `a1b2b22`, reutilizando editores/API y la precondición de escritura que fijen WS12/WS45; los campos protegidos por workflow no son editables por este canal. Incluye alta/baja de relaciones permitidas por contrato, sin crear semántica de relaciones en el componente. Resultado: no ejecutable por sí mismo; se cumple cuando WS19.1 y WS19.2 cumplen su aceptación. Límites: no cambia contratos, no edita campos protegidos, no duplica el ticket de edición y no ejecuta mutaciones sin sus gates. Depende de WS12 y de sus hijos.

AMBIGUEDADES
ninguna.

DRY-RUN
WS19 es un agregado no ejecutable: un ejecutor futuro no modifica archivos por WS19; verifica que sus hijos estén preparados y cerrados. WS19.1 cambiaría `frontends/mindmap/views/workspace/fields/` y `tests/`; WS19.2, `frontends/mindmap/views/workspace/relations/` y `tests/`. Ambos consumirían el contrato WS12 —endpoints, operaciones, precondición y whitelist— y los gates `G_PAYLOAD_PRECONDITION`, `G_HUMAN_READ`, `G_UI_WRITE` y `G_WRITE_CONTRACT` por delta. Si falta contrato, precondición o permiso, el ejecutor se detiene y registra el hueco con repo dueño, sin crear sustituto. La validación esperada: en WS19.1, guardar/recargar confirma el dato y una escritura obsoleta conserva el texto local y muestra conflicto; en WS19.2, alta/baja persisten tras recargar y una relación no permitida o revisión obsoleta se rechaza visiblemente. El agregado se valida cuando ambos hijos cumplen su aceptación.

FUTURO
WS12 fija la representación de la precondición, operaciones, escritores y whitelist; WS45 verifica la precondición; WS16 produce `G_HUMAN_READ`; el receptor P01 acepta `G_UI_WRITE` por delta. La promoción y el TaskDoc de WS19 y sus hijos quedan fuera de este nodo.
