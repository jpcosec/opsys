## REFORMULACION

Encargo del nodo WS27 (agregado, `node_role: aggregate`, repo dueño `graph_ui`): reunir bajo un mismo ID la integración en el workspace de la revisión de cambios y de la evidencia de una TaskDoc, materializada en dos hijos: WS27.1 (diff Git e historial read-only por repo y tarea) y WS27.2 (evidencia declarada, encontrada y verificada). Resultado esperado: que ambos hijos cumplan su aceptación; WS27 no produce archivos propios ni se ejecuta. Límites: solo lectura (`requires: G_UI_READ`), sin escribir ni revertir, sin hallazgos de integridad del store (WS29) y sin modelo de comentarios nuevo; `promotion: not_authorized`. Depende de WS13 (lector integrado con historia/foco) y WS12 (contrato de operaciones y rutas de lectura), además de sus hijos; de él dependen WS28 y WS35.

## AMBIGUEDADES

Ninguna. El nodo es agregado y su aceptación remite explícitamente a la de sus hijos; alcance, repo, gate y dependencias están fijados. Los detalles de archivos, textos y pruebas quedan delegados a la promoción/TaskDoc, y las rutas de lectura al contrato WS11/WS12, sin obligar a inventar nada.

## DRY-RUN

Nodo agregado, no ejecutable: un ejecutor futuro no abriría diff ni escribiría archivos en nombre de WS27. Cumpliría sus hijos:

- **WS27.1**: cambiaría `frontends/mindmap/views/workspace/diff/` y `tests/`; leería TaskDoc (`references`, `files`) y resolvería repo/rutas por el contrato WS11 (registry/aliases). Consume WS13 (lector) y WS12 (rutas de lectura); requiere recibo propio de G_UI_READ. Errores: sin commits → diff working tree→HEAD limitado a `TaskDoc.files`, declarando ausencia de historial; ruta sin repo resoluble → no disponible, sin adivinar ni escribir cruzado. Validación esperada: diff real acotado, sección por repo declarado, cero escrituras.
- **WS27.2**: cambiaría `frontends/mindmap/views/workspace/evidence/` y `tests/`; consumiría la correspondencia por tipo de evidencia fijada en WS12 y `deskops closeout verify`. Errores: reporte ausente o comando fallido → no verificable con error, nunca verificado. Validación: declarada/encontrada/verificada y ausente visibles como estados distintos.

El padre cierra cuando ambos recibos existen; no hay validación conjunta adicional.

## FUTURO

El receptor P01 emite el acta G_UI_READ por cada delta hijo; la promoción fija archivos, escenarios y textos en el TaskDoc; WS28 y WS35 consumen el resultado; la aceptación humana decide el cierre.
