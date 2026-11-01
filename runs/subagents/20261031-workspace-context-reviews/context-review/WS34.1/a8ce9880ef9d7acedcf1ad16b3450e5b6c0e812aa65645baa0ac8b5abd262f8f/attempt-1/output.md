## REFORMULACION

WS34.1 es un nodo de implementación en `deskops` cuyo propósito es exponer un adaptador público restringido para dispatch hacia Scion: confirmación observada del Hub, identidad de intento, timeout/errores y autoridad del coordinador. El resultado exigido es demostrar con un agente real un dispatch aceptado y otro rechazado o vencido, correlacionados con el id de intento local de WS32.1 y los registros de WS32.2. Límites: solo `runtime/`, `cli/commands/runtime.py` o la API que fije WS12, y `tests/`; no shell arbitrario, no duplicar transporte, no elegir umbrales de timeout propios y no mandar mensajes durante la planificación. Depende de WS33 y WS12; requiere G_EXEC, G_SCION y G_WRITE_CONTRACT. La promoción no está autorizada.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

Un ejecutor futuro leería el contrato WS12 ya verificado para este delta (canal público, autoridad del coordinador, representación de confirmación y política/umbral de timeout), la salida de WS33 y los registros/intentos de WS32.1–WS32.2, el probe público de WS44/G_SCION y la autorización de escenario de G_EXEC. Comprobaría que G_WRITE_CONTRACT incluye WS34.1 en `accepted_scope_nodes`; si falta la política de timeout, se detendría y registraría el hueco, sin inventar un umbral.

Cambios previstos: adaptador de dispatch en `runtime/`, entrada CLI/API en `cli/commands/runtime.py` o la que fije WS12, y pruebas con agente real. Validaría: dispatch aceptado correlacionado con id de intento y registros; dispatch rechazado o timeout clasificado sin convertir ausencia de confirmación en éxito o fallo remoto; ausencia de shell arbitrario y de transporte duplicado; errores y timeout conforme al contrato. G_SCION/G_EXEC deben pasar antes. Si el Hub no responde, el resultado queda no confirmado, no exitoso.

## FUTURO

WS12 debe producir, al preparar este delta, la sección de política de timeout y autoridad; WS44 aporta el probe y el operador; un humano resuelve G_EXEC; WS34.2 consume este adaptador para reply; la promoción debe fijar TaskDoc, archivos exactos, pills y evidencia. Nada de esto se ejecuta aquí.
