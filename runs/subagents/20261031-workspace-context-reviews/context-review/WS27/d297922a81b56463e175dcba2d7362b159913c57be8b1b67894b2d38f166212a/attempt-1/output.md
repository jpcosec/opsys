## REFORMULACION

WS27 es un agregado de implementación en `graph_ui` que integra, junto a la TaskDoc, la revisión de cambios y la evidencia: diff Git/historial read-only (WS27.1) y evidencia declarada/encontrada/verificada (WS27.2). No se ejecuta: termina cuando ambos hijos cumplen su aceptación. Límites: solo lectura, sin escribir ni revertir; no introduce modelo de comentarios ni juicios de integridad del store (WS29) ni asociación a intento (WS35). Depende de WS13 (lector/registro de vistas y resolución de rutas por WS11) y WS12 (contrato de operaciones y correspondencia de evidencia), y requiere G_UI_READ por delta. Promoción no autorizada.

## AMBIGUEDADES

Ninguna. El nodo declara rol agregado, hijos, repo y aceptación comprobable; no obliga a inventar resultado, alcance ni dependencias.

## DRY-RUN

Al ser agregado, no hay ejecución propia ni archivos del padre. Un ejecutor futuro abordaría WS27.1: leer TaskDoc (`references`, `files`) y resolver repo/rutas mediante WS13/WS11; producir vista en `frontends/mindmap/views/workspace/diff/` y tests; si no hay commits, diff working tree→HEAD acotado a esas rutas; ruta sin repo resoluble queda no disponible. WS27.2: consumir la correspondencia de WS12 y la salida de `deskops closeout verify`; mostrar declarada/encontrada/verificada como estados distintos y abrir Markdown en el lector cuando proceda; salida en `frontends/mindmap/views/workspace/evidence/` y tests. Dependencias: contrato WS11, contrato WS12 y lector WS13; gate G_UI_READ con acta por delta en graph_ui (receptor P01), sin aceptación conjunta. Errores: contrato/dato ausente → detenerse y registrar hueco con repo dueño, sin sustituto; reporte de verificación ausente o fallido → no verificable, nunca verificado. Validación conjunta: aceptaciones de WS27.1 y WS27.2 más recibos G_UI_READ de sus deltas; entonces se satisface WS27 y sus dependientes siguen apuntando a este ID.

## FUTURO

El TaskDoc de promoción fijará archivos, pruebas y textos dentro de la aceptación. El receptor P01 emitirá las actas por delta en graph_ui. WS11 y WS12 producirán sus contratos; WS35 añadirá la asociación a intento y WS29 la integridad del store.
