## REFORMULACION
Propósito: implementar en graph_ui la presentación de errores de lectura y modo degradado del lector workspace. Resultado: el panel afectado muestra referencia rota, documento ausente, modelo no importable y backend caído sin borrar historial ni fingir vacío; fuente sin permiso/capacidad de edición es límite read-only, no fallo; fallo CDN se declara límite actual sin prometer offline. Repo: graph_ui; salidas en `frontends/mindmap/views/workspace/errors/`, rutas del contrato WS11 y `tests/`. Límites: reutilizar lectura Markdown de WS13.1, no otro lector ni guardado, sin recuperación offline; G_UI_READ es per_delta.

## AMBIGUEDADES
1. «fallo CDN tiene diagnóstico visible y prueba de no carga, sin exigir recuperación offline»: si el CDN caído es el que carga la aplicación, no hay UI en ejecución que muestre el diagnóstico; obligaría a inventar si es fallback estático, mensaje de consola o diagnóstico solo parcial.
2. «Fuente sin permiso/capacidad de edición es límite read-only visible, no fallo de lectura»: no se nombra qué produce esa señal ni cómo distinguirla de un 401/403 del backend; WS11 solo cubre «errores de API y estados de red». Obligaría a inventar origen y clasificación.

## DRY-RUN
Lecturas: lectura Markdown de WS13.1, contrato WS11 (errores de API y estados de red) y estado de G_UI_READ. Cambios previstos: módulos de error bajo `views/workspace/errors/`, integración en el panel del lector y pruebas en `tests/`. Dependencias: WS13 (con WS11 transitivo); G_UI_READ per_delta pendiente hasta acta del receptor P01. Si falta la lectura de WS13.1 o la taxonomía de WS11, detenerse y registrar el hueco con repo dueño, sin crear sustituto (alcance.md). Validación esperada: pruebas que distingan error de API de red sin respuesta; reintento tras restaurar backend conservando pestañas/foco/historia; prueba de no carga CDN con diagnóstico visible; casos de referencia rota, documento ausente, modelo no importable y fuente read-only.

## FUTURO
WS13.1 entrega la lectura Markdown reutilizable; WS11 fija la taxonomía de errores y estados; WS16 valida con el corpus WS40; el receptor P01 emite el acta de G_UI_READ por delta. Nada de esto es ambigüedad de este nodo.
