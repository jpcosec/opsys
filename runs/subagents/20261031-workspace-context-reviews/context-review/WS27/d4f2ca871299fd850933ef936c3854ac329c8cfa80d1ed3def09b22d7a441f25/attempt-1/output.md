## REFORMULACION

WS27 es un **agregado no ejecutable** (`node_role: aggregate`) de graph_ui: reúne WS27.1 (diff Git e historial read-only junto a la TaskDoc) y WS27.2 (evidencia declarada/encontrada/verificada). Propósito: dejar disponibles ambas lecturas bajo el mismo contexto de TaskDoc para que WS28 (cierre) y WS35 (trazabilidad) las consuman. Resultado: sus salidas. Límites: solo lectura (`G_UI_READ` por delta), sin escribir/revertir, sin hallazgos de integridad (WS29), sin modelo de comentarios nuevo; promoción no autorizada.

## AMBIGUEDADES

Ninguna. Dependencias, repo dueño, aceptación agregada y delegaciones a WS11/WS12 tienen productor y conducta ante faltantes definidos en el input.

## DRY-RUN

No se ejecuta: termina cuando ambos hijos cumplen su aceptación. Prerrequisitos compartidos: contrato WS11 (rutas/repos por registry/aliases) y contrato WS12 (correspondencia por tipo de evidencia), más el lector WS13.

- **WS27.1**: leería `TaskDoc.references` y `TaskDoc.files`; resolvería repo por WS11; sin commits mostraría working tree→HEAD limitado a esas rutas y declararía ausencia de historial; ruta sin repo resoluble → no disponible. Cambios en `views/workspace/diff/` y tests. Consume el recibo `G_UI_READ` de WS27.1. Transfiere a WS28 un diff/historial anclado a TaskDoc con repo declarado, y a WS35 la advertencia de que la asociación a intento se añade allí.
- **WS27.2**: consumiría la correspondencia WS12, `closeout_evidence`, artefactos resolubles y salida de `deskops closeout verify`; cambios en `views/workspace/evidence/` y tests. Consume el recibo `G_UI_READ` de WS27.2. Distingue declarada/encontrada/verificada; fallo o reporte ausente → no verificable. Abre Markdown por WS13; fuera de ahí, ruta y “no soportado”.

Entre hermanos no hay arista: la integración conjunta es co-presencia en el workspace bajo la misma TaskDoc, sin secuencia ni entrega mutua. Validación conjunta: pruebas de ambos hijos sobre store temporal real o corpus WS40, misma TaskDoc mostrando diff y evidencia, sin escrituras cruzadas; WS27 cierra al aceptar ambos hijos y WS28 recibe el conjunto.

## FUTURO

Recibos per-delta de `G_UI_READ` los emite el receptor P01 en graph_ui al preparar cada delta; el estado global pendiente es intencional. WS28 y WS35 consumen WS27. La promoción fijará archivos, pruebas y textos. WS12/WS11 deben publicar sus contratos; su ausencia se registra como hueco, no se sustituye.
