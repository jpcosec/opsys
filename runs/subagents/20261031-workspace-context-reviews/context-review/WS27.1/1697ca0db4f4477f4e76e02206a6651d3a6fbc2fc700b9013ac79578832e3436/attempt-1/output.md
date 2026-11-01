## REFORMULACION
WS27.1 encarga implementar en `graph_ui`, bajo `frontends/mindmap/views/workspace/diff/` y `tests/`, una vista read-only de diff Git e historial junto a la TaskDoc. El resultado es diff real e historial por repo y tarea, usando `TaskDoc.references` como commits y `TaskDoc.files` como rutas; sin commits, diff working tree→HEAD limitado a esas rutas. Debe resolver repo/rutas con el contrato WS11 —registry/aliases—, mostrar root explícito y una sección por repo alcanzado; una ruta sin repo resoluble queda no disponible. Límites: no escribir ni revertir; no mostrar hallazgos de integridad del store, que son de WS29; no asociar a intento, que se añade en WS35; no adivinar ni escribir cruzado. Depende de WS13 y WS12; requiere G_UI_READ; promoción no autorizada.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Un ejecutor futuro leería el `task_file`, `dag.yaml`, el modelo TaskDoc, el contrato WS11 y la whitelist/contrato WS12; reutilizaría el registro de vistas y la integración de WS13. Cambiaría archivos en `graph_ui/frontends/mindmap/views/workspace/diff/` y `tests/`.

Implementaría: resolución de repo/rutas vía WS11; selección de commits de `TaskDoc.references` resolubles, ordenados por fecha y limitados a `TaskDoc.files`; render por repo con root declarado; estado “sin historial referenciado” y diff working tree→HEAD cuando no haya commits; estado “no disponible” para ruta sin repo. Consumiría G_UI_READ mediante acta por delta en graph_ui; si falta el contrato WS11, se detendría y registraría el hueco, sin sustituto.

Errores previstos: contrato WS11 ausente → no ejecutar; commit no resoluble → no historial referenciado; ruta sin repo → no disponible; varios repos → una sección por repo. Validaría con repos Git temporales: commits acotados, sin commits, varias rutas/repos, ruta irresoluble y ausencia de escritura/revert. Resultado esperado: diff e historial acotados, read-only y sin efectos laterales.

## FUTURO
WS11 produce el contrato de rutas/repos; WS12, la whitelist/contrato aplicable; WS13, la integración del lector. WS35 añade la asociación a intento; WS29 cubre integridad del store. P01, como humano, acepta G_UI_READ por delta con acta en graph_ui. La promoción fijará archivos, pills y evidencia.
