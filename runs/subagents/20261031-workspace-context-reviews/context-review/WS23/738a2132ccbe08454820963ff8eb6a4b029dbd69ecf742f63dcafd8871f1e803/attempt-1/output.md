REFORMULACION
El nodo encarga, en graph_ui, una vista de procedimiento que renderice RitualDoc, StepDoc y el lifecycle del desk: pasos y fuentes navegables, documentos abribles y transiciones declaradas (origen, destino, condición) solo representadas. El resultado vive en `frontends/mindmap/views/workspace/procedure/` con pruebas. Depende de WS13 (lector agregado) y WS09 (catálogo de renderizaciones); requiere G_UI_READ. Límites: la vista no escribe estado, no auto-marca pasos por leerlos, no ofrece controles de avance/mutación ni inventa progreso; si WS02/WS09/WS11 no identifican campo/API real, los pasos quedan inertes. Pruebas con corpus WS40 o store temporal real. No depende de ViewDoc.

AMBIGUEDADES
ninguna

DRY-RUN
Lecturas: `dag.yaml` (nodo, aristas, gate), salida de WS09 (`borradores/vistas.md`), contrato WS11 y resultados de WS13.1–3, reconciliación C-18/C-51, y código actual de `workspace_routes.py`, `views/workspace/`, `deskops_routes.py`, `serve.py` y `workspace.mjs`; artefactos RitualDoc/StepDoc/lifecycle de un store real. Cambios previstos: componentes de procedimiento bajo `views/workspace/procedure/`, su registro en el host del workspace y, solo si la lectura de artefactos no existe, la ruta de lectura mínima; tests que monten un store temporal real (o WS40) con procedimiento, pasos, documentos/soporte y transiciones. Dependencias: WS13 completo y WS09; G_UI_READ se consume como acta per-delta al preparar/promover, no como aceptación global. Errores: si falta catálogo WS09, contrato WS11 o lectura real de artefactos, detenerse y registrar el hueco con repo dueño; si no hay StepDoc en el corpus, usar store temporal; si no hay campo/API de progreso, no mostrarlo. Validación esperada: abrir documentos y soporte, mostrar transiciones sin controles, comprobar pasos no auto-marcados y prueba de ausencia de peticiones de escritura.

FUTURO
WS30 valida el manual con WS23; el receptor humano P01 emite el acta G_UI_READ del delta; WS09/WS11 producen catálogo y contrato; WS40 puede aportar corpus. La aceptación de producto no se decide aquí.
