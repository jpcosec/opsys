REFORMULACION
Propósito: exponer en deskops un adaptador público restringido para dispatch/reply Scion, con confirmación, identidad de intento, timeout/errores y autoridad del coordinador. Resultado: nodo agregado `WS34`; no produce artefacto propio: su `output_scope` son las salidas de WS34.1 y WS34.2. Repo dueño: deskops. Límites: agregado no ejecutable; no shell arbitrario, no duplicar transporte, no autoaprobación/simulación; depende de WS33, WS12 y ambos hijos; requiere G_EXEC, G_SCION y G_WRITE_CONTRACT. No autoriza promoción.

AMBIGUEDADES
Ninguna. El umbral de timeout, la política del coordinador y la precondición/errores se delegan a WS12; la confirmación y la identidad de intento se concretan en los hijos y WS32/WS33. Nada obliga a WS34 a inventar un resultado o aceptación distintos de la conjunción de sus hijos.

DRY-RUN
No ejecutable: un ejecutor futuro no modificaría archivos por WS34. Leería el contrato WS12 por delta (canal, timeout, errores, autoridad), los vínculos WS33 y las evidencias de WS34.1/WS34.2. Primero WS34.1, tras WS12 y WS33, implementaría el adaptador de dispatch en `runtime/`, `cli/commands/runtime.py` o la API fijada por WS12, y `tests/`; validaría con agente real un dispatch aceptado y otro rechazado/vencido, correlacionado al intento local WS32.1 y registros WS32.2. Transfiere a WS34.2 el adaptador de dispatch y la correlación de intento. Luego WS34.2, consumiendo también WS34.1, implementaría reply en la misma base; validaría respuesta vinculada al intento correcto y timeout como fallo sin confirmación. WS34 cerraría solo cuando ambas aceptaciones y G_WRITE_CONTRACT por delta consten; la validación conjunta es el par dispatch confirmado → reply al mismo intento, no un artefacto agregado nuevo. Si falta la sección de timeout o un gate, cada hijo se detiene y registra el hueco; no elige umbral ni crea sustituto.

FUTURO
WS12 fija la política/umbral por delta; WS44/operador resuelve G_SCION; el humano externo resuelve G_EXEC; WS34.1 y WS34.2 ejecutan; WS36 integra el adaptador. La recepción/aceptación por delta queda fuera de WS34.
