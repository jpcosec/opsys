REFORMULACION
- **Propósito**: integrar en el lector de graph_ui la alternancia fuente/render según `source_mode` (`editable`), conservando mismo origen, revisión y buffer sucio.
- **Resultado**: UI que alterna fuente/render, conserva el buffer y no lo descarta sin confirmación; en editable permite edición fuente mediante API autorizada de WS20 y edición de campos vía WS19; una composición escribe solo en el documento dueño o queda read-only declarada.
- **Repo**: graph_ui (`frontends/mindmap/views/workspace/; tests/`).
- **Límites**: no implementa la API raw-source de sldb/WS20, no define el contrato de operaciones (WS12), no crea composición no soportada, no duplica el ticket `editing` y no ejecuta; promoción no autorizada.

AMBIGUEDADES
ninguna.

DRY-RUN
- **Lecturas**: dag.yaml (WS21, WS19, gates, `parameters.source_mode`), decisiones P01/P04/P07, brief (source_mode, composición, revisión, buffer), alcance (reglas comunes), reconciliación C-15/C-39–C-42 y cobertura.
- **Cambios previstos, sin ejecutar**: en `views/workspace/` integrar alternancia fuente/render, conservación de buffer, guardado fuente por API autorizada en editable y guardado de campos con precondición; pruebas en `tests/`.
- **Dependencias**: WS19 completo; la variante editable añade WS20 y G_SOURCE; gates G_PAYLOAD_PRECONDITION (WS45), G_UI_WRITE (acta P01 por delta) y G_WRITE_CONTRACT (WS12). `source_mode=editable`; con `pending` no se prepara ni promueve; read_only no añade dependencias.
- **Validaciones futuras**: roundtrip, conflicto y campos protegidos vía G_SOURCE; edición de campos vía WS19; buffer conservado si no hay confirmación; composición limitada al documento dueño o declarada read-only; acta G_UI_WRITE; validación humana WS30 y manual.

FUTURO
- WS12 fija el contrato de operaciones y la representación de revisión; WS45 produce G_PAYLOAD_PRECONDITION; WS20 produce G_SOURCE y la API raw-source; WS19 entrega la edición de campos; P01 receptor emite el acta G_UI_WRITE por delta; WS30/WS31 validan y documentan. Nada de ello es ambigüedad del nodo ni autoriza ejecución.
