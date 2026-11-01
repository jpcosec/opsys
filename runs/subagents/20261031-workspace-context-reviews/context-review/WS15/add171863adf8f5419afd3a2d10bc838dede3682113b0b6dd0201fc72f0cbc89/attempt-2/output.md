## REFORMULACION

WS15 es un agregado no ejecutable de `graph_ui`: agrupa el resultado «mostrar errores de lectura y modo degradado» mediante WS15.1 (errores de lectura, backend/CDN) y WS15.2 (orientación de proyecto sin desk). Propósito: que el lector explique fallos sin fingir vacío y oriente el arranque. Resultado conjunto: salidas de ambos hijos. Límites: no implementa otro lector ni guardado, no promete offline, no inicializa por GET; depende de WS13 y consume contrato WS11.

## AMBIGUEDADES

ninguna.

## DRY-RUN

Un ejecutor futuro no ejecutaría WS15, sino sus hijos:

- **WS15.1**: consumiría el contrato WS11 y la lectura Markdown de WS13.1; cambiaría `frontends/mindmap/views/workspace/errors/` y `tests/`. Validaría referencia rota, documento ausente, modelo no importable, backend caído, diagnóstico CDN sin recuperación offline, y reintento que conserva pestañas/foco/historia. Transfiere a WS15 y WS16 su salida de errores.
- **WS15.2**: consumiría WS13 y el `deskops init` existente; cambiaría `views/workspace/orientation/` y `tests/`. Validaría orientación sin mutación, ruta absoluta y comando, y refresco tras init externo. Transfiere a WS15 y WS16 la orientación UF10.
- **Agregado**: no toca archivos. Cierra cuando ambos hijos cumplen su aceptación, no solo al ejecutarse. La validación conjunta es WS16 con el corpus WS40: errores de lectura/diagnóstico y UF10 sin mutar, además de las pruebas propias de cada hijo. `G_UI_READ` es `per_delta`: cada hijo requiere su recibo; el estado global pendiente no impide cerrar el otro. Si faltan WS11 o la lectura de WS13.1, se detiene y registra el hueco según alcance.md; la operación queda no disponible.

## FUTURO

WS11 produce el contrato de errores y estados de red. WS13.1 entrega la lectura Markdown reutilizable. El receptor P01 emite el acta por delta de `G_UI_READ` en graph_ui. WS40 prepara el corpus y WS16 ejecuta la validación humana. `deskops init` ya existe; no lo produce este nodo.
