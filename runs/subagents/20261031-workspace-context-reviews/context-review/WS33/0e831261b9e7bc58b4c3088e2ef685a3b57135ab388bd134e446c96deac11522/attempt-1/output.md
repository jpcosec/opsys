REFORMULACION
Propósito: cerrar el delta documental que vincula mensajes, resultados y decisiones humanas al intento, sin editor UI. Resultado: agregado WS33 compuesto por WS33.1 (vínculo de mensajes/resultados con deduplicación y procedencia) y WS33.2 (registro de decisión humana explícita). Repo dueño: deskops (`runtime/`, modelos/reportes, `tests/`). Límites: backend documental; no tocar tablas Scion; sin dispatch/reply de red; WS33.1 no atribuye una conversación completa a un intento; WS33.2 no escribe estados validado/cerrado; promoción no autorizada; G_SCION y G_WRITE_CONTRACT por delta.

AMBIGUEDADES
ninguna.

DRY-RUN
WS33 es un agregado no ejecutable: no produce artefacto propio y termina cuando WS33.1 y WS33.2 cumplen su aceptación. Un ejecutor futuro esperaría WS32 (identidad/RunDoc/cierre idempotente), el contrato WS11 declarado en el agregado, el contrato WS12 por operación/actor, G_SCION producido por WS44 y G_WRITE_CONTRACT del delta.

WS33.1: lee de WS32 la identidad de intento y del contrato público Scion (WS05/WS44) los campos de mensaje/resultado. Añade el adaptador en `runtime/` según contrato, modelos/reportes y tests; importa con claves Hub+proyecto+conversación+mensaje y Hub+proyecto+intento+fuente; los mensajes sin intento resoluble quedan como hueco de procedencia. No modifica tablas Scion. Valida que una importación repetida no duplique ni atribuya la conversación completa a un intento.

WS33.2: consume de WS33.1 las referencias al intento y de WS12 la operación y el actor humano. Escribe la decisión con actor, intento, tarea y resultado aprobar/pedir corrección (esta con texto); `completed` del agente nunca se registra como aprobado. Tests propios.

Errores: si falta el contrato Scion o la operación de decisión de WS12, se detiene y registra el hueco con dueño; un gate pendiente impide avanzar. La validación conjunta exige ambas aceptaciones, sin duplicar pipeline, con commit/blob verificable en deskops.

FUTURO
WS34 consume WS33 para dispatch/reply; WS35 lo consume para mostrar trazabilidad; WS12 produce el contrato de actor/operación; WS44 produce G_SCION; el humano decide promoción y aceptación por delta. Nada de esto se ejecuta aquí.
