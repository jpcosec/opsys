REFORMULACION
El nodo encarga implementar en graph_ui una vista read-only de diff Git e historial junto a la TaskDoc: propósito, hacer revisable el cambio de una tarea sin salir del workspace. Resultado: secciones por repo alcanzado por `TaskDoc.files`, con root explícito; historial desde commits de `TaskDoc.references` ordenados por fecha; sin commits, diff working tree→HEAD acotado a esas rutas; lo no resoluble se declara no disponible. Repo dueño: graph_ui. Límites: solo lectura, sin escribir/revertir, sin hallazgos de integridad (WS29), sin asociación a intento (WS35); depende de WS13 y WS12 y requiere G_UI_READ por delta; promoción no autorizada.

AMBIGUEDADES
1. «Base: commits listados en TaskDoc.references y rutas en TaskDoc.files (campos del modelo TaskDoc de deskops)» y «commits de TaskDoc.references resolubles». No se define forma/versión de esos campos ni quién entrega su esquema, ni qué hace «resoluble». Obligaría a inventar el parser de references, el criterio de resolución y el tratamiento de referencias no-commit o parcialmente resolubles.
2. «ordenados por fecha de commit, limitados a TaskDoc.files». No aclara si se filtran commits que tocan esas rutas o si solo se recorta el diff de cada commit. Obligaría a inventar la semántica del historial y qué commits aparecen.

DRY-RUN
Un ejecutor futuro leería el esquema TaskDoc disponible, el contrato WS11, el contrato WS12, la integración WS13 y el registry/aliases. Crearía la vista en `frontends/mindmap/views/workspace/diff/` y pruebas en `tests/`; ejecutaría `git log`/`git diff` read-only por repo. Consumiría WS13 para el contenedor y WS12 para operaciones permitidas; sin contrato o esquema, se detendría registrando el hueco en el repo dueño, sin sustituto. G_UI_READ exigiría acta del delta concreto antes de promover. Errores esperados: repo/ruta no resoluble ⇒ no disponible; sin HEAD o sin archivos ⇒ estado honesto. Validaría con repos fixture y store temporal real o corpus WS40, comprobando diff/historial reales, ausencia de escritura Git y de hallazgos WS29. No se ejecuta nada.

FUTURO
WS11 publica resolución registry/aliases; WS12, whitelist/operaciones; el dueño del modelo TaskDoc, el esquema de campos; P01 emite el acta G_UI_READ; WS35 añade asociación a intento; WS29, integridad; el TaskDoc de promoción fija archivos y textos; WS40 aporta corpus de validación.
