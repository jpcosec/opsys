REFORMULACION
Nodo de implementación en graph_ui: mostrar errores de lectura y modo degradado sin borrar historial, pestañas ni foco, y sin fingir vacío. Resultado: panel afectado para referencia rota, documento ausente, modelo no importable, backend caído y fallo CDN; reintento tras restaurar backend; límite read-only visible cuando falte capacidad de edición. Repo dueño: graph_ui. Depende de WS13; requiere G_UI_READ, evaluado por delta con acta del receptor P01. Límites: no implementar otro lector ni guardado, no prometer offline, no inventar respuesta del backend ausente; contrato de errores y rutas de lectura en WS11; promoción no autorizada.

AMBIGUEDADES
ninguna.

DRY-RUN
Un ejecutor futuro leería primero WS13.1/WS13.3 ya entregados, el contrato WS11 de errores y estados de red, y el código actual de `views/workspace/` y sus tests. Consumiría el recibo G_UI_READ específico de WS15.1; si falta, no promovería. Cambios previstos: añadir bajo `frontends/mindmap/views/workspace/errors/` el panel y la normalización de estados de error; conectar detección de fallo CDN y reintento de backend conservando URL, pestañas, foco e historia; distinguir error de API de red sin respuesta; mostrar límite read-only de fuente sin tratarlo como fallo; añadir pruebas en `tests/`. No tocaría el lector Markdown de WS13.1 ni introduciría guardado u offline. Validaciones futuras: pruebas de cada error en panel afectado sin borrar estado; reintento con backend restaurado; diagnóstico CDN y prueba de no recuperación offline; límite read-only visible. Errores esperados: si WS11 no define un error o una ruta, detenerse y registrar el hueco con repo dueño conforme a alcance.md; si WS13.1 no está disponible, bloquear la reutilización. Sin ejecución ahora.

FUTURO
WS16 podrá validar el lector completo; el receptor humano P01 emitirá el acta G_UI_READ por delta; WS15 se cerrará cuando cumplan WS15.1 y WS15.2; la promoción fijará TaskDoc, archivos y pruebas.
