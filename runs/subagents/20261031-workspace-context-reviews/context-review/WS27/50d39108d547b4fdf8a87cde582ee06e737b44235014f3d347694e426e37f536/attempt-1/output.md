## REFORMULACION
WS27 es un **agregado no ejecutable** de graph_ui: integra, junto a la TaskDoc, la revisión read-only de cambios Git y la evidencia. Resultado: salidas de WS27.1 (diff/historial por repo y tarea) y WS27.2 (evidencia declarada/encontrada/verificada). Depende de WS13, WS12 y ambos hijos; requiere G_UI_READ. Límites: no escribe, no revierte, no hace commit/closeout y su promoción no está autorizada.

## AMBIGUEDADES
Ninguna. La aceptación agregada queda definida por el cumplimiento de WS27.1 y WS27.2; el gate pendiente es intencional y no hay resultado conjunto distinto que inventar.

## DRY-RUN
No habría ejecutor de WS27: termina cuando terminan sus hijos.

- **WS27.1**: lee `TaskDoc.references` y `TaskDoc.files`, resuelve repo/rutas mediante WS11 y muestra diff/historial read-only. Sin commits, declara ausencia de historial y usa working tree→HEAD limitado a esas rutas. Ruta sin repo resoluble: no disponible. Cambios previstos en `frontends/mindmap/views/workspace/diff/` y `tests/`; consume WS12 y WS13; requiere recibo G_UI_READ de su delta.
- **WS27.2**: lee `closeout_evidence`, references/files y la salida de `deskops closeout verify`; muestra declarada, encontrada y verificada como estados distintos, y abre soporte Markdown dentro del workspace o declara no soportado. Reporte ausente/fallo: no verificable con error. Cambios en `frontends/mindmap/views/workspace/evidence/` y `tests/`; mismas dependencias y gate por delta.

No hay arista entre WS27.1 y WS27.2: no se transfieren secuencialmente. Ambos consumen WS13/WS12 y sus salidas se integran junto a la TaskDoc. El resultado conjunto se valida por la aceptación de ambos hijos, sin criterio agregado adicional. Si falta contrato, API o permiso de una dependencia, se detiene y registra el hueco; no se crea sustituto. La promoción exigiría TaskDoc, archivos/pills/evidencia y preflight, hoy no autorizados.

## FUTURO
El receptor humano P01 emite actas G_UI_READ por delta concreto en graph_ui. La promoción fija TaskDoc y archivos. WS28 y WS35 consumirán WS27 cuando sus hijos estén aceptados.
