REFORMULACION
WS34.1 es un nodo de implementación, no un agregado. Su encargo es exponer en `deskops` un adaptador público restringido para dispatch de Scion, con confirmación observada, identidad de intento, timeout/errores y autoridad del coordinador según WS12. Resultado previsto: `runtime/`, `cli/commands/runtime.py` o la API que fije WS12, y `tests/`. Límites: no shell arbitrario, no duplicar transporte, no enviar mensajes en planificación y no fijar un umbral propio de timeout; solo avanza con la política de timeout de este delta en WS12, verificada por G_WRITE_CONTRACT. Promoción no autorizada.

AMBIGUEDADES
ninguna.

DRY-RUN
Un ejecutor futuro leería `dag.yaml`, la sección de dispatch/timeout del contrato WS12, las salidas de WS33 y los ids/registros WS32.1–WS32.2, la evidencia G_SCION de WS44 y la autorización G_EXEC; revisaría `runtime/` y CLI existentes. Cambios previstos: añadir el adaptador de dispatch en `runtime/`, exponerlo por CLI/API fijada por WS12 y crear pruebas en `tests/` para aceptado, rechazado y timeout. Dependencias y gates: WS33 y WS12 son prerrequisitos; G_EXEC y G_SCION deben pasar; G_WRITE_CONTRACT se evalúa por delta con la política de timeout de WS34.1. Errores: si falta la política WS12, detenerse y registrar el hueco; sin G_EXEC/G_SCION, no ejecutar; el timeout se reporta como fallo sin confirmación y se correlaciona al intento; el rechazo solo se declara si la respuesta Hub lo observa. Validación esperada: agente real con un dispatch aceptado y otro rechazado o vencido, ids correlacionados con WS32.1 y registros WS32.2, sin shell ni transporte duplicado.

FUTURO
Producen otros nodos: WS12 la política/umbral de timeout y la API/operaciones por delta; WS32.1–WS32.2 la identidad de intento y sus registros; WS33 los vínculos mensaje/resultado/decisión; WS44 la verificación de Scion. Decide un humano: G_EXEC, mediante autorización explícita de ejecución/comunicaciones, y la promoción del TaskDoc con archivos, pills y evidencia; G_SCION y G_WRITE_CONTRACT se verifican por evidencia, no por esta revisión.
