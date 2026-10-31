## REFORMULACION

**Propósito:** encargo de planificación para una vista que represente RitualDoc/StepDoc/lifecycle como procedimiento navegable sobre referencias reales.

**Resultado:** renderer de pasos, transiciones y fuentes navegables; el estado de paso solo se lee de deskops y no se escribe desde la vista.

**Repo:** `graph_ui`, con salidas en `frontends/mindmap/views/workspace/procedure/` y `tests/`.

**Límites:** depende de WS13 y WS09; sujeto a `G_UI_READ` pendiente; pruebas con corpus WS40 o store temporal real; integración como delta o ticket existente, sin duplicar trabajo.

## AMBIGUEDADES

1. «pasos, transiciones y fuentes navegables» frente a «El estado de un paso solo viene de deskops; esta vista no lo escribe.» No aclara si las transiciones son solo representadas o también accionables (por ejemplo, avanzar un paso). Obligaría a inventar si existe mutación, qué contrato/permiso la habilita y qué ocurre al activar una transición.

2. «RitualDoc/StepDoc/lifecycle sobre referencias reales» y «Un procedimiento abre sus documentos y soporte». No nombra el inventario o API que provee los rituales ni el criterio para seleccionar el procedimiento mostrado; «referencias reales» no fija su resolución ni el comportamiento si una referencia falta. Obligaría a inventar la fuente de datos, el conjunto mostrable y el tratamiento del hueco.

## DRY-RUN

**Lecturas:** guía, brief, alcance, decisiones, cobertura, reconciliación, nodo WS23, contexto de WS13/WS09 y gate `G_UI_READ`. Sin ejecución.

**Cambios previstos:** crear el renderer de procedimiento, registrarlo en el mecanismo de vistas existente y añadir pruebas; sin escribir estado de pasos.

**Dependencias:** WS09 aporta el contrato por fila del catálogo; WS13, el lector integrado; WS11 resuelve `G_UI_READ`; la matriz WS06 llega de forma transitiva; el estado proviene de deskops; pruebas con corpus WS40 o store temporal.

**Validaciones futuras:** comprobar `G_UI_READ` antes de despachar; abrir procedimiento, documentos y soporte; verificar que leer no marca pasos como realizados; confirmar ausencia de escritura; validación humana en WS30.

## FUTURO

WS11 debe emitir `G_UI_READ` con identidad y fecha del responsable. WS12 definirá privilegios y efectos de mutación. La promoción fijará archivos, pills y evidencia. WS30 validará el recorrido humano. El solicitante debe resolver P01/P02/P04/P07 y designar al actor receptor. Nada de esto es ambigüedad del nodo.
