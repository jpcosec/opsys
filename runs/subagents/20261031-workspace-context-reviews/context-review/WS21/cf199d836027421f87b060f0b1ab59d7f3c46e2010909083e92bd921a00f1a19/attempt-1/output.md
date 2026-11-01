REFORMULACION
Propósito: integrar en el workspace de graph_ui la alternancia fuente/render del mismo documento según `source_mode=editable` (P04), conservando buffer sucio y usando el guardado fuente autorizado. Resultado: fuente y render con origen y revisión, buffer conservado con confirmación, y composición que escribe solo en el documento dueño de cada campo. Repo: graph_ui (`frontends/mindmap/views/workspace/; tests/`). Límites: no define el contrato WS12 ni implementa WS20; no sustituye la precondición de payload; no promociona el nodo ni ejecuta la variante `read_only`; no habilita mutaciones UI sin `G_UI_WRITE`.

AMBIGUEDADES
ninguna

DRY-RUN
Lecturas: nodo WS21, guía, brief, alcance, decisiones, gates y vecinos del DAG. Cambios previstos: alternancia fuente/render, conservación del buffer y confirmación explícita, consumo del guardado de WS20 en editable, y composición limitada al origen trazable. Dependencias: WS19; en editable, WS20; gates `G_PAYLOAD_PRECONDITION`, `G_UI_WRITE`, `G_WRITE_CONTRACT` y `G_SOURCE`. Validaciones futuras: pruebas de edición/conflicto/roundtrip, conservación de buffer, composición de solo lectura si no hay soporte; acta `G_UI_WRITE` por delta y validación manual WS30. Sin ejecutar.

FUTURO
WS20 produce `G_SOURCE`; WS45 produce `G_PAYLOAD_PRECONDITION`; WS12 fija el contrato de composición y operaciones; el receptor P01 emite el acta `G_UI_WRITE`; WS30 valida manualmente. La promoción fijará TaskDoc, archivos, pills y evidencia. La variante `read_only` no aplica con `source_mode=editable`.
