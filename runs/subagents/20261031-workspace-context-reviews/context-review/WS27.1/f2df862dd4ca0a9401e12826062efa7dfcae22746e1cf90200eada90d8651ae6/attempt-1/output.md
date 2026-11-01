REFORMULACION
WS27.1 es un nodo de implementación en graph_ui que añade al workspace una vista read-only de diff Git e historial junto a una TaskDoc. Propósito: mostrar cambios reales por repo y tarea sin escribir ni revertir. Resultado: una sección por repo alcanzado por TaskDoc.files, con root declarado; historial de commits resolubles de TaskDoc.references, ordenados por fecha y limitados a TaskDoc.files; sin commits, diff working tree→HEAD en esas rutas; ruta sin repo resoluble no disponible. Repo: graph_ui; salida en frontends/mindmap/views/workspace/diff/ y tests. Límites: depende de WS13 y WS12; G_UI_READ por delta; quedan fuera asociación a intento (WS35) e integridad del store (WS29). WS27 es agregado: no se ejecuta; termina con WS27.2.

AMBIGUEDADES
1. «sin commits se declara que no hay historial referenciado y se usa diff working tree→HEAD». No distingue references vacías, referencias no resolubles y referencias que no tocan TaskDoc.files; obliga a inventar si se declara ausencia, se muestra historial parcial o se activa el fallback.
2. «Diff Git e historial read-only» / «Repo/rutas se resuelven por contrato WS11». No nombra el canal o API que ejecuta git log/diff ni quién lo produce; WS12 es contrato de operaciones, pero el nodo solo atribuye a WS11 la resolución de repo/rutas. Obliga a inventar endpoint/CLI y autorización.

DRY-RUN
Leería task_file, modelo TaskDoc, contratos WS11/WS12, registry/alias y host graph_ui. Crearía en frontends/mindmap/views/workspace/diff/: resolución de files a repos, lectura de references/files, historial y diff, estados vacío/no disponible. Por repo leería commits y ejecutaría `git diff HEAD -- <rutas>` cuando corresponda; no escribiría. Consumiría G_UI_READ (acta por delta) y salidas WS13/WS12; si falta contrato, API o repo, pararía registrando el hueco. Validaría con fixtures: varios repos, con/sin commits, references no resolubles, ruta sin repo; comprobaría read-only, secciones por repo y exclusión de WS29. Un canal Git no cubierto por WS12 bloquearía el nodo.

FUTURO
WS35 añade asociación a intento; WS29 integridad. El receptor P01/humano emite el acta G_UI_READ y decide la promoción; el TaskDoc de promoción fijará archivos, pills y evidencia. Un humano o nodo productor resolvería el canal Git si falta.
