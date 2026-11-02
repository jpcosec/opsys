REFORMULACION
WS15.1 es un nodo de implementación en graph_ui. Encargo: mostrar en el panel afectado errores de lectura —referencia rota, documento ausente, modelo no importable, backend caído— y modo degradado, sin borrar historial/foco ni fingir vacío; declarar el fallo CDN como límite actual, no offline. Resultado: estados de error y reintento que recupera lectura conservando pestañas/foco/historia. Repo dueño graph_ui; depende de WS13 y G_UI_READ. Límites: reutilizar la lectura Markdown de WS13.1, no implementar otro lector ni guardado, y no prometer empaquetado/recuperación offline.

AMBIGUEDADES
1. «Fuente sin permiso/capacidad de edición es límite read-only visible, no fallo de lectura». WS11 solo se nombra para «errores de API y estados de red», no para decidir esa capacidad; el ejecutor tendría que inventar la fuente de verdad (¿respuesta de lectura?, ¿source_mode de WS21?) y el criterio para no tratarlo como error.

DRY-RUN
Hipotético: leería WS11, WS13/WS13.1 y el código actual de `workspace_routes.py`, `workspace-view.js` y `shell/api.js`. Modificaría `views/workspace/errors/` y `shell/api.js` para tipificar HTTP/red/JSON conservando `status`, `body` y compatibilidad; añadiría tests. No tocaría el lector Markdown ni guardado. Consumiría WS13 (lectura, foco, historia) y G_UI_READ por delta: sin acta no declararía aceptación; gate pendiente no es defecto. Si WS11 no define estados o WS13.1 no expone lectura, se detendría y registraría el hueco. Validaría: backend ausente vs JSON/red, reintento con pestañas/foco/historia, CDN con diagnóstico y prueba de no carga, sin offline. No ejecuto.

FUTURO
WS11 produce el contrato de errores/red/CDN; WS13.1 la lectura reutilizable; WS16 la validación humana con corpus WS40; el receptor P01 emite el acta G_UI_READ por delta en graph_ui. El TaskDoc de promoción fija archivos, pruebas y textos.
