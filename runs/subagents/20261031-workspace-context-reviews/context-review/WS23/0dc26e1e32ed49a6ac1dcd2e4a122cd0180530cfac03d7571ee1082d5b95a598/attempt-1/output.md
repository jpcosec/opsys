REFORMULACION

WS23 es un nodo de implementación en graph_ui: construir una vista de procedimiento que represente RitualDoc/StepDoc/lifecycle con pasos y fuentes navegables sobre referencias reales. El resultado es un renderer en `frontends/mindmap/views/workspace/procedure/` con pruebas. Límites: solo lectura; no escribe estado; no auto-marca pasos realizados por leerlos; no inventa progreso; las transiciones muestran origen/destino/condición sin controles de avance ni mutación. Depende de WS13 (lector integrado) y WS09 (catálogo de renderizaciones); requiere G_UI_READ.

AMBIGUEDADES

ninguna

DRY-RUN

Un ejecutor futuro leería el nodo, el borrador de WS09, el contrato WS11 a través de WS13, el lector workspace existente, las operaciones/rutas de deskops que exponen tarea y lifecycle (C-51/C-16) y las pruebas actuales. Cambios previstos: añadir el renderer de procedimiento bajo `procedure/` y sus tests; consumir WS13 y el catálogo WS09; comprobar si WS02/WS09/WS11 identifican campo/API real de estado de paso; si no, renderizar pasos authored inertes. Dependencias: recibo G_UI_READ por delta y WS13/WS09 disponibles. Si falta la ruta o contrato de lectura de RitualDoc/StepDoc/lifecycle, debe detenerse y registrar el hueco con repo dueño, sin crear sustituto. La promoción fijará archivos exactos y el punto de registro de la vista. Validaciones futuras: pruebas sobre corpus WS40 o store temporal real; apertura de documentos y soporte; transiciones con origen/destino/condición declarados y sin acciones; comprobación de no peticiones de escritura y de ausencia de estado o progreso inventado.

FUTURO

WS09 entrega `borradores/vistas.md`; WS11 produce el contrato de navegación; los hijos de WS13 entregan el lector; WS40 aporta el corpus; el receptor humano P01 emite el acta G_UI_READ por delta y WS30 realiza la validación humana. La promoción fijará archivos, pills y evidencia.
