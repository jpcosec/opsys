REFORMULACION
Propósito: que un ejecutor futuro implemente en deskops el adaptador público restringido de respuesta (reply) vinculado al intento de un agente, con timeout/errores y autoridad del coordinador. Resultado: adaptador en `runtime/`, comando/API en `cli/commands/runtime.py` o la que fije WS12, y pruebas en `tests/`. Repo dueño: deskops (`output_base deskops:repository_root/`). Límites: no enviar mensajes durante planificación; sin la política y umbral de timeout que WS12 produce para este delta, detenerse y registrar el hueco sin elegir umbral propio; gates G_EXEC, G_SCION y G_WRITE_CONTRACT; promoción no autorizada; depende de WS33, WS12 y WS34.1.

AMBIGUEDADES
1. «con timeout/errores y autoridad del coordinador» (scope). El nodo no indica quién produce ni dónde se define la «autoridad del coordinador»; solo atribuye a WS12 el umbral de timeout («con el umbral de la política de timeout que WS12 produce para este delta»). Obligaría al ejecutor a inventar el modelo de autoridad —quién puede responder, sobre qué intento y con qué alcance— o a tomarlo de un bloque vecino que el input no declara aplicable.

DRY-RUN
Ejecutor hipotético: leería el nodo, la sección por delta de WS12 (timeout y autoridad), las salidas de WS33 y WS34.1, el probe de WS44 y la autorización G_EXEC. Cambiaría `runtime/` (adaptador reply), `cli/commands/runtime.py` o la API fijada, y `tests/`. Errores: política WS12 ausente → parar y registrar hueco con repo dueño; G_EXEC/G_SCION sin verificar → no ejecutar; respuesta no vinculada al intento → rechazo; timeout → fallo sin confirmación. Validaría con agente real: reply correlacionada al intento correcto y timeout reportado como fallo; esperado: ninguna confirmación falsa.

FUTURO
WS12 publica la política de timeout/autoridad por delta; WS44 aporta el probe de Scion; el humano resuelve G_EXEC; la promoción (TaskDoc, archivos exactos) y la recepción por delta las producen otros nodos o personas; WS34 agrega cuando WS34.1 y WS34.2 cierran; consumidores de UI (WS36/WS37) usan el adaptador.
