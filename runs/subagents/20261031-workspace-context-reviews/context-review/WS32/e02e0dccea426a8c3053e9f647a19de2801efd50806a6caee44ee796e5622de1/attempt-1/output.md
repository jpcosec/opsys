## REFORMULACION
WS32 es un agregado no ejecutable cuyo propósito es unificar la identidad de intento y el cierre Scion sin crear un segundo pipeline. El resultado son las salidas conjuntas de WS32.1 y WS32.2; el ID agregado sigue siendo dependencia de sus consumidores. Repo dueño: `deskops`. Límites: solo identidad, persistencia local, manifiesto/RunDoc/cierre idempotentes; sin dispatch/reply de red, sin eventos Hub inventados y sin crear almacenamiento ad hoc. WS05 inventaría y WS12 fija contrato/ubicación; los estados Hub reales corresponden a WS34/37 bajo G_EXEC. Promoción no autorizada; G_SCION sigue sin verificar y G_WRITE_CONTRACT es por delta.

## AMBIGUEDADES
ninguna

## DRY-RUN
Un ejecutor futuro no ejecutaría WS32 directamente: verificaría WS05 y WS12 y recorrería sus hijos. WS32.1 consumiría el inventario y el contrato para separar intento de slug, registrar `intent`/`confirmed` como hechos distintos y materializar el registro por intento mediante operaciones locales reales sobre store temporal; modificaría `deskops/runtime/scion.py`, `models/run.py`, `services/closure.py` y `tests/`, sin red. Entregaría a WS32.2 ese registro y las identidades ya probadas.

WS32.2 consumiría el registro de WS32.1 para convertir manifiesto, RunDoc y cierre en idempotentes sobre el mismo id de intento. Validaría dos intentos con IDs distintos, ausencia de confirmación Hub sin evidencia y finalización repetida sin registros duplicados; comprobaría coincidencia de id de intento, hash de sesión y evidencia. Si falta artefacto o contrato de hash, registraría el hueco con dueño WS12/WS05 y bloquearía esa coincidencia antes de promoción.

La validación conjunta sería que ambos hijos acepten y que el resultado agregado conserve una sola identidad de intento hasta el cierre, sin segundo pipeline. G_CLOSEOUT está satisfecho; G_SCION no; G_WRITE_CONTRACT debe evaluarse por delta. No hay cambios ni pruebas ejecutadas en esta revisión.

## FUTURO
WS05 produce el inventario Scion; WS12, el contrato y ubicación del registro; WS44, la evidencia de G_SCION; WS34/37 prueban Hub real bajo G_EXEC y autorización humana. La promoción y designación del operador Scion quedan fuera de este nodo.
