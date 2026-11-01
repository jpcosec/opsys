REFORMULACION
- **Propósito**: revisar WS23 como encargo de implementación en graph_ui: representar RitualDoc/StepDoc/lifecycle como procedimiento navegable dentro del lector workspace.
- **Resultado**: vista en `frontends/mindmap/views/workspace/procedure/` con pasos y fuentes navegables, sin escritura de estado; pruebas asociadas en `tests/`.
- **Repo dueño**: graph_ui (`output_base: graph_ui:repository_root/`).
- **Límites**: solo lectura; no auto-marcar pasos por leerlos; no inventar progreso; transiciones representadas sin controles de avance ni mutaciones; pruebas sobre corpus WS40 o store temporal real.
- **Dependencias**: WS13 (lector agregado) y WS09 (catálogo de renderizaciones); requiere G_UI_READ, pendiente y por delta. WS40 no es dependencia directa: el nodo admite store temporal real.

AMBIGUEDADES
Ninguna. La aceptación condiciona el progreso a que WS02/WS09/WS11 identifiquen campo/API real de deskops y fija el fallback —“si no, pasos authored son inertes y no hay progreso inventado”—, por lo que no obliga a inventar. La fuente de datos de procedimiento queda dentro de referencias reales y del contrato de navegación; los detalles de archivos, textos y pruebas los fija el TaskDoc de promoción.

DRY-RUN
- **Lecturas previstas**: WS23, WS13/WS13.x, WS09, contrato WS11, auditorías WS02/WS04, `reconciliacion.md`, `alcance.md` y, si se usa, corpus WS40 o store temporal.
- **Cambios previstos**: crear renderer de procedimiento bajo la ruta declarada y sus pruebas; ninguna escritura de estado ni endpoint de avance.
- **Dependencias**: WS13 debe estar cumplido por sus hijos; WS09 debe aportar catálogo; G_UI_READ necesita recibo por delta del receptor P01; WS40 solo si se elige ese corpus.
- **Validaciones futuras**: abrir un procedimiento y sus documentos/soporte; comprobar que leer no marca pasos; verificar transiciones con origen/destino/condición declarados; prueba de ausencia de peticiones de escritura.

FUTURO
La promoción no está autorizada: otro nodo/TaskDoc fijará archivos, pruebas y textos exactos; el receptor P01 emitirá el acta G_UI_READ por delta; WS09/WS11 determinarán si existe campo/API real para mostrar progreso; WS13 cerrará por sus hijos; WS30 podrá validar el flujo manualmente.
