## REFORMULACION

**Propósito:** convertir RitualDoc, StepDoc y lifecycle en una vista de procedimiento legible dentro del lector de workspace.
**Resultado:** renderer en `graph_ui` que abre documentos y soporte del procedimiento, muestra pasos y fuentes navegables, y representa transiciones sin ejecutarlas.
**Repo dueño:** `graph_ui`, con salida acotada a `frontends/mindmap/views/workspace/procedure/` y `tests/`.
**Límites:** no escribe estado, no auto-marca pasos por leerlos, no ofrece controles de avance ni mutaciones y no inventa progreso si falta campo/API real. Depende de WS13 (lector) y WS09 (catálogo), y requiere G_UI_READ por delta.

## AMBIGUEDADES

Ninguna.

Las condiciones de aceptación delimitan el resultado y los límites; el nodo no exige archivos, textos ni pruebas detalladas, que quedan al TaskDoc de promoción. La ausencia de API real de progreso está prevista: pasos authored inertes, sin progreso inventado.

## DRY-RUN

Un ejecutor futuro leería el lector integrado de WS13, el catálogo de WS09, el contrato de navegación de WS11 —transitivo vía WS13—, los RitualDoc/StepDoc/lifecycle reales de deskops y el corpus WS40 o un store temporal real. Añadiría el renderer de procedimiento en el `output_scope`, su registro en la navegación del workspace y pruebas de lectura de documentos/soporte, transiciones representadas y ausencia de peticiones de escritura. Consumiría WS13 y WS09 como dependencias entregadas; si falta su salida, se detendría y registraría el hueco sin sustituirla. Verificaría el recibo G_UI_READ del delta concreto; al estar pendiente, no lo daría por aceptado. Errores esperados: soporte roto → error visible; lifecycle sin campo/API de estado → pasos inertes; intento de control de avance → prueba fallida. Validación: abrir un procedimiento y sus fuentes, comprobar que leer no marca pasos, que las transiciones muestran origen/destino/condición declarados y que no hay POST ni avance.

## FUTURO

WS30 valida el recorrido manual e integra WS23. El solicitante P01 emite el acta G_UI_READ por delta. La promoción fija TaskDoc, archivos y pruebas; WS11 enlaza el contrato de navegación.
