## REFORMULACION

WS34 es un nodo **agregado no ejecutable** del plan de workspace documental. Su propósito es exponer, en el repo `deskops`, un adaptador público restringido para despacho y respuesta Scion, con confirmación, identidad de intento, timeout/errores y autoridad del coordinador. El resultado no es código propio: el agregado se cumple cuando WS34.1 (dispatch) y WS34.2 (reply) cumplen su aceptación; los dependientes siguen apuntando a WS34. Límites: depende de WS33 y WS12; requiere G_EXEC, G_SCION y G_WRITE_CONTRACT; no permite shell arbitrario, duplicar transporte ni enviar mensajes durante planificación. `output_base: deskops:repository_root/`.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

Un ejecutor futuro no tocaría archivos por WS34: lo trataría como agregado. Ejecutaría sus hijos:

- **WS34.1**: leería el contrato WS12 —sección de política/umbral de timeout de dispatch—, los registros WS33 y el inventario WS32. Cambiaría `runtime/`, `cli/commands/runtime.py` o la API que fije WS12, y `tests/`. Consumiría G_EXEC, G_SCION y el recibo per_delta de G_WRITE_CONTRACT. Si falta la política de timeout, se detendría y registraría el hueco sin elegir umbral. Validaría con agente real un dispatch aceptado y otro rechazado o vencido, correlacionados con el id de intento local y registros WS32.2; la ausencia de confirmación no se convertiría en éxito/fallo remoto.
- **WS34.2**: leería lo anterior más la salida de WS34.1. Cambiaría los mismos puntos para reply vinculado al intento y tests. Misma dependencia de política WS12 y gates; validaría respuesta al intento correcto y timeout reportado como fallo sin confirmación.

El agregado terminaría cuando ambos hijos tengan aceptación y recibos verificados. Errores comunes: gate pendiente, política ausente, intento no correlacionable, confirmación no observada. No habría shell arbitrario ni transporte duplicado.

## FUTURO

WS36 consumirá el adaptador WS34. WS12 debe producir, al preparar esos deltas, la política y umbral de timeout. WS44 aportará la comprobación de G_SCION; un humano autorizará G_EXEC. La promoción de WS34 sigue no autorizada y requerirá preflight y archivos/evidencia concretos.
