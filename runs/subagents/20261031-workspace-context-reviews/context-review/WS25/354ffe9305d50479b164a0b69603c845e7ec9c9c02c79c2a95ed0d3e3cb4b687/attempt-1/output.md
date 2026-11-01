REFORMULACION
Propósito: añadir a la UI de graph_ui la lectura/ack de mensajes del desk y la captura interna a drawer o protoátomo mediante operaciones autorizadas por el contrato WS12. Resultado: agregado no ejecutable cuyas salidas son las de WS25.1 (inbox) y WS25.2 (capture); se cumple cuando ambos hijos cumplen su aceptación, y sus dependientes siguen colgando de WS25. Repo dueño: graph_ui. Límites: no confundir ack con aprobación; no crear tarea implícita ni cron de triage; captura sin exigir tarea; no inventar API, modelo ni wrapper; los gates pendientes son intencionales y G_HUMAN_READ no bloquea desarrollo/pruebas aisladas.

AMBIGUEDADES
Ninguna.

DRY-RUN
Al ser agregado no hay ejecución propia. WS25.1 leería WS12 y gates; tocaría `frontends/mindmap/views/workspace/inbox/` y `tests/`; consumiría endpoints autorizados; validaría que el ack persiste tras recarga mostrando el mensaje origen, que la respuesta local solo existe si WS12 la define —si no, se declara no disponible—, que no se crea tarea implícita ni cron y que se aplican permisos. Entregaría la UI de inbox. WS25.2 tocaría `frontends/mindmap/views/workspace/capture/` y `tests/`; consumiría el canal de captura que fije WS12 y probaría por separado drawer y protoátomo; validaría persistencia tras recarga en el destino elegido, origen tipado (ruta o mensaje) visible y sin tarea implícita, y que una colisión no se sobrescribe en silencio. Entregaría la UI de captura. No hay arista entre hermanos: ambos consumen WS12 y no se transfieren nada; la integración conjunta se comprueba al validar la conjunción de ambas aceptaciones. WS30 usará luego WS25 en la validación manual de UF02. Si falta contrato u operación, se detiene y registra el hueco con repo dueño, sin sustituto; errores esperados: operación no definida, permiso denegado, colisión.

FUTURO
WS12 decide y publica el contrato por delta: canal de drawer, operación de respuesta, representación del origen y permisos. El receptor P01 emite el acta G_UI_WRITE por delta; WS16 produce la evidencia humana de G_HUMAN_READ. El TaskDoc de promoción fija archivos, pruebas y textos. WS30 ejecuta la validación humana de UF02.
