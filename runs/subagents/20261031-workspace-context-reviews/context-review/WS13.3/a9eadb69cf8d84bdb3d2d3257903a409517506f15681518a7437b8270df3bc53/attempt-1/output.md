REFORMULACION
WS13.3 encarga, en graph_ui, implementar o conciliar un delta para abrir documentos en pestañas y divisiones, con documento activo, foco e historia. Resultado: pestañas y dos documentos lado a lado; cambiar de pestaña/división no altera el foco guardado de cada documento; volver restaura documento, foco y origen en orden inverso de navegación. Límites: disposición local de sesión de navegador, sin persistencia tras recarga; foco no compartido entre usuarios; no crear otro workspace; usar rutas de lectura del contrato WS11 y la base de WS13.1; requiere G_UI_READ por delta.

AMBIGUEDADES
ninguna

DRY-RUN
Un ejecutor leería el contrato WS11, la aceptación/salida de WS13.1, `workspace_routes.py`, `workspace-view.js`, el registro de vistas y los tests existentes. Cambiaría, bajo `frontends/mindmap/views/workspace/layout/` y reutilizando la vista workspace, el estado local de pestañas/divisiones, documento activo, foco por documento e historia; añadiría pruebas en `tests/`. Consumiría de WS11 identidad, origen y rutas de lectura; de WS13.1 la lectura y foco por documento; de G_UI_READ el acta del delta concreto. Validaría abrir, cambiar y cerrar pestañas; abrir dos documentos en divisiones; alternar el activo; volver en orden inverso restaurando documento, foco y origen; y que recargar no exija persistir la disposición. Si falta el contrato/ruta de WS11 o la base de foco de WS13.1, se detendría registrando el hueco en el repo dueño, sin sustituirlo. No ejecutaría nada durante esta revisión.

FUTURO
El TaskDoc de promoción fijará archivos exactos, pills, evidencia y pruebas detalladas. El receptor P01 en graph_ui emitirá el acta G_UI_READ del delta. WS13 solo cerrará cuando WS13.1, WS13.2 y WS13.3 cumplan; la integración conjunta se valida por sus aceptaciones, sin secuencia entre hermanos. La aceptación humana del delta corresponde al receptor, no a este revisor.
