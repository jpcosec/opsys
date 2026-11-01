## REFORMULACION
**Propósito:** WS23 es un nodo de implementación en `graph_ui` que debe renderizar RitualDoc/StepDoc/lifecycle como procedimiento navegable y de solo lectura.
**Resultado:** una vista bajo `frontends/mindmap/views/workspace/procedure/` con pasos y fuentes navegables, más pruebas.
**Repo dueño:** `graph_ui`.
**Límites:** depende de WS13 (lector integrado) y WS09 (catálogo de renderizaciones); requiere `G_UI_READ`; no escribe estado, no invoca avance ni mutaciones y no inventa progreso. No duplica la base del workspace.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
**Lecturas previstas:** contrato WS11 (vía WS13), catálogo WS09 (`vistas.md`), auditorías WS02–WS04 para campos/APIs reales, corpus WS40 o store temporal, y código actual de `workspace_routes.py`/`workspace-view.js`.
**Cambios previstos:** crear el módulo de procedimiento, registrarlo en el host del workspace y añadir pruebas. No se toca escritura ni avance de lifecycle.
**Dependencias y gates:** WS13 debe estar integrado; WS09 debe haber entregado sus filas. `G_UI_READ` es `per_delta`: el receptor P01 debe emitir acta del delta concreto en `graph_ui`. Si falta, se registra el hueco y no se sustituye.
**Errores esperados:** sin campo/API real de progreso, los pasos quedan inertes; sin documento o soporte, error visible; backend ausente, límite declarado, sin inventar disponibilidad.
**Validación futura:** abrir un procedimiento y comprobar documentos/soporte; verificar que leer no marca pasos; comprobar que las transiciones solo muestran origen/destino/condición y no hay controles de avance; prueba de no peticiones de escritura.

## FUTURO
El receptor P01 emite el acta `G_UI_READ` por delta en `graph_ui`; WS09 fija las filas de renderización y WS11 el contrato de navegación; WS40 aporta el corpus; WS16/WS30 realizan aceptación humana; la promoción fija archivos, pills y pruebas exactas en el TaskDoc. Nada de esto es ambigüedad del nodo.
