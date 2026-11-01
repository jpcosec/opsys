## REFORMULACION
WS34.1 encarga, en `deskops`, implementar un adaptador público restringido para dispatch Scion: confirmación como respuesta de la API Scion, identidad de intento, timeout/errores y autoridad del coordinador según WS12. Resultado: operación de dispatch acotada, correlacionada con el intento local previo WS32.1 y los registros WS32.2, con pruebas. Límites: no shell arbitrario, no duplicar transporte, no elegir umbral propio; depende de WS33/WS12 y exige G_EXEC, G_SCION y G_WRITE_CONTRACT.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Un ejecutor futuro leería `dag.yaml`, la sección de WS12 para este delta —política y umbral de timeout, autoridad del coordinador—, el probe de WS44/G_SCION, la autorización G_EXEC y los registros WS32.1/WS32.2. Cambiaría `runtime/` y `cli/commands/runtime.py` o la API que fije WS12, más `tests/`. Concretamente: expondría una sola operación de dispatch con intento obligatorio, aplicaría la política de timeout de WS12, mapearía la respuesta del Hub a confirmado/rechazado/timeout sin inferir éxito o fallo remoto, y verificaría la autoridad del coordinador. Errores: gates o sección de timeout ausentes → detenerse y registrar hueco con repo dueño; rechazo → correlacionar y no marcar confirmado; timeout → sin confirmación, no éxito; fallo de transporte → error declarado sin reintento duplicado. Validaría con agente real un dispatch aceptado y otro rechazado o vencido, comprobando la correlación con el intento local y los registros. Resultado esperado: evidencia observable y ninguna mutación fuera del adaptador.

## FUTURO
WS34.2 (reply) depende de este nodo; WS34 cierra como agregado cuando ambos hijos cumplen. WS12 debe producir la sección de timeout al preparar el delta; WS44/operador y el humano resuelven G_SCION/G_EXEC; WS32.2 aporta registros y el receptor verifica G_WRITE_CONTRACT por delta.
