## REFORMULACION

WS41 es un nodo de implementación en graph_ui: habilitar lectura segura entre desks. Propósito: resolver aliases/roots explícitamente autorizados por el contrato WS11 usando APIs públicas de store, con cada request conservando su proyecto/store sin tocar la variable global `SLDB_STORE`. Resultado: leer un segundo desk del corpus WS40 y volver, sin mutaciones cruzadas, mostrando identidad/origen y siguiendo enlaces authored entre desks mediante la historia. Repo dueño: graph_ui (salidas en `frontends/mindmap/source/`, `views/workspace/`, `tests/`). Límites: rechazar roots arbitrarios/paths escapados, errores visibles para alias no autorizado/path escapado/store ausente, y no afirmar federación por copiar contenido. Depende de WS13 (lector con historia/foco), WS11 (contrato de navegación e identidad) y WS40 (corpus reproducible con segundo desk); requiere G_UI_READ, evaluado por delta.

## AMBIGUEDADES

Ninguna. Las rutas exactas, pruebas y textos visibles quedan delegados a la promoción; el contrato de aliases/roots y APIs lo produce WS11; el corpus y sus enlaces los produce WS40. G_UI_READ pendiente es intencional y per_delta.

## DRY-RUN

Un ejecutor futuro, tras promoción y con recibo G_UI_READ del delta WS41, leería: `contratos/navegacion.md` de WS11 (autorización de aliases/roots y APIs públicas citadas), el manifiesto JSON de WS40 (roots, stores, commits, documentos clave y enlaces entre los dos desks) y el código integrado de WS13 (historia, foco, registro de vistas). Cambios previstos: módulo de resolución de alias/root que valide contra el contrato WS11 y pase el store por petición; integración en `views/workspace/` del segundo desk con identidad/origen visibles y navegación de vuelta por historia; tests en `tests/` que levanten el corpus WS40 (o store temporal equivalente ya existente) y cubran lectura entre dos desks, retorno por historia, alias no autorizado, path escapado y store ausente. No mutará el segundo store (verificación de estado/commits intactos) ni escribirá global `SLDB_STORE`. Si falta el recibo G_UI_READ o el contrato/maniobra de WS11/WS40, se detiene y registra el hueco, sin sustituto. Validación esperada: pruebas en verde, errores visibles, ausencia de mutación cruzada, sin declaración de federación; gate humano posterior en WS16.

## FUTURO

WS16 ejecutará la validación humana de UF08 sobre el corpus WS40. El receptor P01 en graph_ui emitirá el recibo G_UI_READ del delta. La promoción fijará TaskDoc, archivos, pills, escenarios y textos. WS17 enriquecerá índices; el envío interdesk sigue fuera de alcance.
