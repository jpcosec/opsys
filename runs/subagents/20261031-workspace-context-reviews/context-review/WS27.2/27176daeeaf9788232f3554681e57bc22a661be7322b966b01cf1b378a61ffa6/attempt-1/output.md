## REFORMULACION

WS27.2 es un nodo de implementación en `graph_ui` que añade, junto a la TaskDoc, una vista de evidencia con tres estados: declarada (`closeout_evidence`), encontrada (artefactos resolubles en `references/files`) y verificada (resultado de `deskops closeout verify`). Debe abrir el soporte si es Markdown dentro del workspace; si no, mostrar ruta y declarar no soportado. No crea modelo de comentarios ni infiere tipos por extensión: la correspondencia la fija WS12. Límites: solo lectura, sin mutaciones, sin closeout propio; depende de WS13 y WS12 y requiere G_UI_READ por delta.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

Un ejecutor futuro leería el contrato WS11 para rutas de lectura, la sección de WS12 que fija correspondencia por tipo de evidencia, artefactos de soporte y salida pública de `deskops closeout verify`, además del registro de vistas existente en `shell/registry.js` y la estructura real de TaskDoc en `graph_ui`. Cambiaría archivos bajo `frontends/mindmap/views/workspace/evidence/` y añadiría pruebas en `tests/`: un componente que, para una TaskDoc, lea `closeout_evidence`, resuelva `references/files`, consuma el reporte de verificación y renderice los estados sin colapsarlos. No tocaría el modelo de comentarios ni inferiría tipos por extensión.

Consumiría G_UI_READ mediante el recibo per-delta del receptor P01 para este nodo; sin recibo, se detendría y registraría el hueco, sin sustituirlo. También consumiría el contrato WS12; si falta la correspondencia o la salida pública, aplicaría la regla común: detenerse y registrar hueco con repo dueño.

Casos de error: reporte ausente o fallo de comando → estado “no verificable” con error, nunca “verificado”; evidencia declarada sin artefacto → declarada sin artefacto; artefacto resoluble no declarado → encontrada no declarada; verificación fallida → fallida, distinta de no verificable; soporte no Markdown o fuera del workspace → ruta visible y “no soportado”.

Validación esperada: pruebas con TaskDocs fixture que cubran los estados y sus combinaciones, comprobando que no se colapsan y que “abrir soporte” solo abre Markdown dentro del workspace. La aceptación se cumple cuando todos los estados y la apertura se comportan así con datos reales del reporte.

## FUTURO

El agregado WS27 cierra cuando WS27.1 y WS27.2 cumplen su aceptación. El TaskDoc de promoción fijará archivos exactos, pruebas y textos. El receptor P01 emite el acta G_UI_READ por delta; WS12 y WS11 producen los contratos consumidos.
