## REFORMULACION
WS25 es un nodo agregado no ejecutable de `graph_ui` cuyo encargo es integrar en la UI la captura y el triage: leer mensajes, registrar ack o respuesta local, y capturar en drawer o protoátomo mediante operaciones permitidas por el contrato WS12. El resultado es el agregado de las salidas de WS25.1 y WS25.2. Límites: no hay envío interdesk; ack no es aprobación; no se crea tarea implícita ni cron de triage; no se diseña API o modelo por reflejo; las mutaciones en UI requieren G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT, aunque desarrollo y pruebas aisladas de API pueden avanzar con contratos técnicos.

## AMBIGUEDADES
ninguna

## DRY-RUN
WS25 no se ejecuta: termina cuando terminan WS25.1 y WS25.2. Un ejecutor futuro leería el contrato WS12 (`contratos/operaciones.md`), las actas de gates por delta y la aceptación de cada hijo. WS12 es prerrequisito común; WS25.1 y WS25.2 son hermanos sin arista entre sí y pueden consumir WS12 en paralelo.

WS25.1 cambiaría archivos bajo `frontends/mindmap/views/workspace/inbox/` y sus tests; transferiría ack persistente tras recarga, mensaje origen visible y respuesta local solo si WS12 define la operación, declarándola no disponible en caso contrario.

WS25.2 cambiaría archivos bajo `frontends/mindmap/views/workspace/capture/` y sus tests; transferiría captura persistente en el destino elegido, origen tipado (ruta o mensaje) y colisión controlada, sin tarea implícita. Si WS12 no fija canal para drawer, se registra hueco y no se inventa sustituto.

Errores esperados: operación ausente en WS12 → hijo declara no disponible; gate o acta per_delta ausente → no se habilitan mutaciones en UI; fallo de persistencia → no se acepta el hijo. Validación conjunta: aceptación de ambos hijos más recorrido UF02 en WS30; WS25 no añade validación propia.

## FUTURO
WS12 produce el contrato de operaciones y sus recibos por delta; WS16 produce el acta de G_HUMAN_READ; el receptor P01 emite el acta G_UI_WRITE del delta concreto; WS30 realiza la validación humana de UF02. La promoción de WS25 exige autorización humana y TaskDoc con archivos, pills y evidencia.
