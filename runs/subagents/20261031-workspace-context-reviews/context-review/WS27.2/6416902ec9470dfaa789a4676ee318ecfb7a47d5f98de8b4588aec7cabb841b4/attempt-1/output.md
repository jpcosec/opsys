REFORMULACION
Propósito: revisar WS27.2 como encargo de planificación, no como producto ni ejecución. Resultado esperado: una vista que muestre evidencia declarada, encontrada y verificada junto a la TaskDoc, con estados diferenciados y apertura de soporte. Repo dueño: `graph_ui`. Límites: sin modelo de comentarios nuevo; sin mutaciones; abrir solo Markdown dentro del workspace; fuera de ese caso, mostrar ruta y declarar no soportado; `G_UI_READ` sigue pendiente.

AMBIGUEDADES
1. «Declarada = closeout_evidence de la TaskDoc; encontrada = artefactos resolubles en las references/files de la TaskDoc; verificada = resultado de `deskops closeout verify`». Obliga a inventar la regla de correspondencia entre una evidencia declarada y un artefacto encontrado —ruta, identificador, nombre u orden— y si los estados son por evidencia o del conjunto. Sin esa regla no puede decidirse «declarada sin artefacto», «artefacto no declarado» ni atribuir una verificación fallida.
2. «una evidencia ausente se ve como ausente; declarada sin artefacto, artefacto no declarado y verificación fallida se muestran como estados distintos». Obliga a inventar si «ausente» es un cuarto estado —sin evidencia declarada— o el mismo caso de «declarada sin artefacto». La aceptación no fija esa taxonomía ni el caso vacío.

DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura, nodo WS27.2, contratos vecinos WS13/WS12/WS27 y gate `G_UI_READ`. Cambios previstos: implementar la vista en `frontends/mindmap/views/workspace/evidence/` y sus tests, consumiendo el lector de WS13 y el contrato de operaciones de WS12. Dependencias: WS13, WS12, rutas de lectura de WS11 y `G_UI_READ`. Validaciones futuras: pruebas con store temporal real, corpus WS40 para validación humana, aceptación del delta `G_UI_READ` y fijación de archivos/escenarios por el TaskDoc de promoción. No se ejecuta nada.

FUTURO
WS07 resuelve decisiones humanas P01/P04; WS11 produce rutas y acta de `G_UI_READ`; WS12 fija la capability exacta de `deskops closeout verify`; WS13 entrega el lector; la promoción autorizada por humano genera el TaskDoc. Nada de ello se decide aquí.
