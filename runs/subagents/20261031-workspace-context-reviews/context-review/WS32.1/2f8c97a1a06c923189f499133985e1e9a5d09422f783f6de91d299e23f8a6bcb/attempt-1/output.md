## REFORMULACION
WS32.1 es un nodo de implementación en deskops que refina el candidato de drawer Scion para separar identidad de intento y dispatch: un intento no es slug; dispatch (intención local registrada) y confirmed (solo respuesta Hub observada) son hechos distintos del RunDoc, registrados en el registro por intento que WS32.2 hará manifiesto canónico. El resultado previsto es código y pruebas en `deskops/runtime/scion.py`, `models/run.py`, `services/closure.py` y `tests/` que generan IDs de intento distintos y registran intent/no confirmado con operaciones reales del store temporal, sin red, sin dispatch/reply ni evento Hub fingido. Repo dueño: deskops. Límites: no inventa almacenamiento (contrato WS12), no usa tablas internas Scion, no afirma fallo/éxito de Hub, no crea segundo pipeline; promoción no autorizada.

## AMBIGUEDADES
1. «sin segundo pipeline: intento no es slug»: no identifica el pipeline existente ni qué cuenta como duplicarlo; el ejecutor tendría que inventar la frontera y podría crear o rechazar una persistencia paralela sin criterio.
2. «contrato de integración explícito»: no dice dónde se registra, qué contiene ni quién lo acepta; el ejecutor tendría que inventar artefacto, formato y responsable.

## DRY-RUN
Leería `dag.yaml` (nodo, dependencias, gates), el candidato de drawer citado, `runtime/scion.py`, `models/run.py`, `services/closure.py` y tests existentes; consumiría el inventario WS05 y el contrato WS12 sobre registro por intento. Cambiaría el modelo/registro local para crear IDs de intento distintos antes de dispatch, añadiría estados intent/no confirmado separados del RunDoc y pruebas con store temporal real, sin red ni Hub simulado. Verificaría G_CLOSEOUT (satisfecho) y esperaría G_WRITE_CONTRACT/G_SCION; si falta el contrato WS12 o el inventario WS05, se detendría y registraría el hueco con repo dueño, sin sustituto. Validaría dos intentos con IDs distintos, registro intent/no confirmado persistido, ausencia de etiquetas fallo/éxito Hub, registro/validación SLDB del modelo y edición de RunDoc por API/CLI, no Markdown ad hoc.

## FUTURO
WS05 produce el inventario de identidad/API Scion; WS12 fija contrato y ubicación del registro por intento; WS44 produce G_SCION; WS32.2 convierte el registro en manifiesto canónico; WS34/WS37 prueban dispatch real y correlación; una persona autoriza la promoción.
