REFORMULACION  
Propósito: definir un explorador para abrir documentos del store y Markdown no modelado del desk sin conocer IDs. Resultado: vista/explorer en graph_ui con catálogo refrescable y pruebas. Repo dueño: graph_ui. Límites: output_scope en `frontends/mindmap/views/workspace/explorer/`, rutas de lectura del contrato WS11 y `tests/`; depende de WS11/WS13.1; requiere G_UI_READ; no autoriza promoción ni ejecución.

AMBIGUEDADES  
1. Cita: «El árbol se obtiene de la API del store y del sistema de archivos del desk, según contrato WS11» y output_scope «rutas de lectura definidas por el contrato WS11». Obliga a inventar si «rutas de lectura» son URLs de UI o endpoints de API, si existe o debe crearse un endpoint para listar el filesystem del desk y quién lo implementa, ya que el output_scope solo cubre explorer/tests y WS11 es planificación.  
2. Cita: «Altas de documento modelado en store y Markdown no modelado en desk aparecen tras refresco explícito del catálogo sin reiniciar servidor ni cambiar código». Obliga a inventar qué es el «catálogo» para Markdown no modelado, si el refresco re-escanea el filesystem, refresca solo el store o ambos, y qué acción cuenta como refresco explícito; el comportamiento de aceptación no queda fijado.

DRY-RUN  
- Lecturas: nodo WS13.2, guía, brief, alcance, decisiones, reconciliación; contratos vecinos WS11/WS13.1 solo como dependencias.  
- Cambios previstos: crear explorer en graph_ui, reutilizar catálogo/filtro, abrir documentos modelados y no modelados, pruebas de alta/refresco; posiblemente registrar la vista sin ampliar alcance.  
- Dependencias: contrato WS11, lector WS13.1, catálogo/API existente, G_UI_READ por delta.  
- Validaciones futuras: alta en store temporal y Markdown en desk; apertura sin ID; aparición tras refresco sin reinicio ni cambio de código; revisión de recepción y solapamiento.

FUTURO  
WS11 produce el contrato/API y seguridad para no modelados; P01/receptor emite G_UI_READ por delta; WS06/Ws13 resuelven integración y cierre agregado; un humano decide el canal backend y la semántica de refresco antes de promover.
