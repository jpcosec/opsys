REFORMULACION

Encargo: hacer idempotentes y consistentes manifiesto, RunDoc y cierre sobre el intento correcto, identificado por el id que cita el cierre, nunca por agente o slug. Resultado: una finalización repetida del mismo intento conserva identidad y evidencia sin crear registros nuevos, y manifiesto, RunDoc y registros de closeout coinciden en id de intento, hash de sesión y evidencia. Repo dueño: deskops (`runtime/scion.py`, `models/run.py`, `services/closure.py`, `tests/`). Límites: persistencia local con operaciones reales del store temporal, sin dispatch/reply de red ni confirmar eventos Hub; la prueba con Hub corresponde a WS34/37 bajo G_EXEC. Depende de WS05, WS12 y WS32.1; G_CLOSEOUT está satisfecho, G_SCION no verificado y G_WRITE_CONTRACT pendiente. Promoción no autorizada.

AMBIGUEDADES

1. «Una finalización repetida sobre el mismo id de intento conserva identidad y evidencia sin crear registros nuevos». No fija qué ocurre si la repetición aporta evidencia, commit o hash de sesión distintos: ¿rechaza, conserva el primer valor o actualiza el registro existente? Tampoco define si «evidencia» coincide por conjunto idéntico, por hash o por identificador declarado. El ejecutor tendría que inventar la política de conflicto/deduplicación y el criterio de aceptación.

DRY-RUN

Un ejecutor leería el TaskDoc, el candidato de drawer, la auditoría WS05, el contrato WS12 y la salida de WS32.1. Localizaría `close_from_run`, `record_scion_run` y el modelo RunDoc. Añadiría una clave por id de intento y deduplicación en `services/closure.py` y `models/run.py`; probaría con store temporal que la primera finalización crea registros y la segunda no crea nuevos, conservando id, hash de sesión y evidencia. G_WRITE_CONTRACT pendiente y G_SCION no verificado bloquearían la ejecución; si falta artefacto/contrato de hash, registraría hueco con WS12/WS05 y bloquearía esa coincidencia. Validaría repetición y comparación de los tres artefactos, sin red ni Hub.

FUTURO

WS05 aporta inventario e identidad; WS12, contrato, ubicación del registro y definición de hash; WS32.1, el registro por intento. WS44/G_SCION y WS34/37 prueban Hub real bajo G_EXEC. Un humano autoriza la promoción.
