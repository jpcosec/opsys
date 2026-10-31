REFORMULACION
Propósito: revisar si WS13.2 se entiende como encargo de planificación. Resultado: un explorador en `graph_ui` que lista y abre documentos modelados del store y Markdown no modelado del desk, según el contrato WS11, sin exigir IDs ni índices nuevos, y que refleja altas en el store temporal de prueba sin cambiar código. Repo: `graph_ui`. Límites: salidas en `frontends/mindmap/views/workspace/explorer/`, rutas de lectura del contrato WS11 y `tests/`; depende de WS11 y WS13.1; requiere G_UI_READ; no se ejecuta nada ni se revisan los nodos vecinos.

AMBIGUEDADES
Ninguna. La fuente del árbol y la resolución store/desk se delegan explícitamente a WS11; el uso de un store temporal real está cubierto por `alcance.md`; los archivos, pruebas y textos exactos quedan al TaskDoc de promoción.

DRY-RUN
Lecturas: nodo WS13.2, WS11, WS13, WS13.1, gate G_UI_READ, guía y fuentes suministradas. Cambios previstos: ninguno; solo revisión. Dependencias: contrato WS11 —rutas de lectura, store y desk—, salida de WS13.1 y acta G_UI_READ pendiente. Validaciones futuras: abrir desde el explorador un documento modelado y uno no modelado sin conocer ID ni usar índices nuevos; comprobar que un documento añadido al store temporal aparece sin cambio de código; preflight task-only y fijación de archivos/pruebas por TaskDoc.

FUTURO
WS11 produce el contrato de navegación y el acta que resuelve G_UI_READ; el solicitante o WS07 designa al responsable de `graph_ui`; el TaskDoc de promoción fija archivos y escenarios; la validación humana puede apoyarse en el corpus WS40 cuando exista. La promoción de WS13.2 no está autorizada.
