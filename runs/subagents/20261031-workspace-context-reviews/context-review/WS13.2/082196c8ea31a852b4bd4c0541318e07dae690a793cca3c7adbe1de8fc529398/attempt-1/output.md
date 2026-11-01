## REFORMULACION
WS13.2 encarga a `graph_ui` un explorador para abrir documentos modelados del store y Markdown no modelado del desk sin conocer su ID, y que las altas aparezcan tras refresco explícito del catálogo. Resultado esperado: código en `frontends/mindmap/views/workspace/explorer/`, rutas de lectura según WS11 y pruebas. Límites: depende de WS11 y WS13.1; exige G_UI_READ por delta; no crea índices nuevos, otro workspace ni API de store; puede reutilizar catálogo/filtro existente para modelados. Es candidato, sin promoción autorizada.

## AMBIGUEDADES
Ninguna. El nodo nombra resultado, repo, dependencias y aceptación comprobable; la API/seguridad para Markdown no modelado y la resolución de origen quedan delegadas a WS11, con regla de parada en `alcance.md` si falta el contrato.

## DRY-RUN
Un ejecutor futuro leería el nodo WS13.2, `contratos/navegacion.md` de WS11, las salidas de WS13.1, el código existente del workspace y la matriz de reconciliación. Comprobaría que WS11 define rutas y seguridad para documentos no modelados y que WS13.1 permite abrir/fijar foco; si falta, se detendría registrando el hueco con repo dueño, sin inventar API.

Cambios previstos: crear el explorador bajo `frontends/mindmap/views/workspace/explorer/`, con listado de documentos modelados desde el catálogo del store y de Markdown no modelado desde el desk; añadir acción de refresco que recargue el catálogo sin reiniciar servidor; reutilizar catálogo/filtro para modelados; pruebas en `tests/`. No introducir índices nuevos ni duplicar el workspace.

Dependencias consumidas: contrato WS11, lector/foco WS13.1 y recibo G_UI_READ específico de WS13.2, con actor P01, alcance, efecto y commit; no requiere recibos de otros deltas. Validación esperada: abrir un modelado y un no modelado sin ID; añadir un documento al store temporal real o al corpus WS40 y verlo tras refresco; añadir Markdown al desk y verlo igual; confirmar que no hay reinicio ni cambio de código y que el filtro existente sigue operando. Errores esperados: contrato WS11 ausente o ruta no resuelta → detenerse y registrar hueco; fallo de lectura → error honesto, no sustituto.

## FUTURO
WS11 produce el contrato de navegación; WS13.1 aporta lectura y foco; el receptor P01 emite el acta G_UI_READ del delta en graph_ui. La promoción fija archivos, pruebas y textos de pantalla en el TaskDoc. WS13 cierra por sus hijos y WS06 reconcilia con la matriz.
