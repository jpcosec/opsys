REFORMULACION

WS13 es un nodo agregado, no ejecutable, cuyo propósito es integrar el lector del workspace con lectura de documento/fuente, contexto, enlaces, Code local, selección por documento/nodo, explorador de documentos modelados y no modelados, pestañas, divisiones e historia. El resultado es la aceptación conjunta de WS13.1, WS13.2 y WS13.3, reutilizando el workspace integrado a1b2b22 y el registro de vistas existente. Repo dueño: graph_ui. Límites: solo lectura; mantener rutas del host y Code local; no exigir índices nuevos; no crear otro workspace independiente; no duplicar implementación ni inferir cierre por commit. Depende de WS11 y de sus tres hijos; requiere recibo de lectura por delta.

AMBIGUEDADES

ninguna.

DRY-RUN

Un ejecutor futuro no modificaría código en WS13: leería `dag.yaml`, el contrato de WS11 y las aceptaciones/evidencias de WS13.1–WS13.3. WS11 debe entregar identidad, origen, rutas de lectura/seguridad y errores; si falta, se detiene y registra el hueco. WS13.1 produce lectura de documento y fuente cruda, contexto, enlaces, Code local y foco. WS13.2 consume ese lector para el explorador de documentos modelados y Markdown no modelado. WS13.3 consume lector y foco para pestañas, dos documentos lado a lado e historia. WS13.2 y WS13.3 no tienen arista entre sí: integran conjuntamente explorador y pestañas sobre el mismo lector y foco, sin entregarse uno al otro. Cada hijo consume su propio recibo de lectura. La validación conjunta exige las tres aceptaciones, misma base a1b2b22, rutas del host, ausencia de workspace nuevo e índices nuevos, y solo lectura. No hay cambios propios de WS13 ni validaciones que ejecute por sí mismo.

FUTURO

WS11 debe cerrar su contrato de navegación. El receptor humano P01 emite en graph_ui las actas de recepción por delta concreto. La promoción fija TaskDoc, archivos, pruebas y textos de pantalla de cada hijo. WS16 valida la lectura sobre el corpus Taller.
