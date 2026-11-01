REFORMULACION

WS32.2 es implementación en deskops. Propósito: hacer consistentes e idempotentes manifiesto, RunDoc y cierre sobre el id de intento que cita el cierre, nunca por agente o slug. Resultado: una finalización repetida del mismo id conserva identidad y evidencia sin crear registros nuevos; manifiesto, RunDoc y registros de closeout coinciden en id de intento, hash de sesión y evidencia. Repo: deskops; output_scope: deskops/runtime/scion.py, models/run.py, services/closure.py, tests/. Límites: persistencia local en store temporal real; sin dispatch/reply de red ni confirmar evento Hub; no hash de proceso/slug/fabricado; Hub real y correlación son WS34/37 bajo G_EXEC. Depende de WS05, WS12 y WS32.1; requiere G_CLOSEOUT, G_SCION y G_WRITE_CONTRACT.

AMBIGUEDADES

Ninguna.

DRY-RUN

Leería dag.yaml/WS32.2, el candidato external_references.scion, el inventario WS05, el contrato WS12, el registro de WS32.1 y el código `runtime/scion.py`, `services/closure.py`, `models/run.py` y tests. Comprobaría gates: G_CLOSEOUT satisfecho; G_SCION no verificado; G_WRITE_CONTRACT pendiente y per_delta. Sin G_SCION no iniciaría. Si WS12 no define hash de sesión, registraría hueco con productor WS05/WS12 y bloquearía esa coincidencia. Con contrato, añadiría el manifiesto por intento en `models/run.py` (id de intento, agente, run si la API lo expone, timestamps, hash de sesión, evidencia, commit de cierre) y haría idempotentes persistencia/finalización en `runtime/scion.py` y `services/closure.py`, usando el id de intento como clave y el registro de WS32.1. Tests en `tests/` con store temporal real: repetir finalización mismo id, verificar cero registros nuevos y coincidencia manifiesto/RunDoc/closeout; id distinto, identidad distinta; sin red ni Hub. Errores: gate no satisfecho, contrato/artefacto de hash ausente, operación no idempotente. Validación focalizada, no suite global.

FUTURO

WS05 produce inventario y artefacto de sesión; WS12 contrato, ubicación, hash y recibo G_WRITE_CONTRACT; WS32.1 registro e identidades; WS44 G_SCION; WS34/37 prueban Hub bajo G_EXEC; WS32 cierra como agregado. Promoción/TaskDoc fija archivos y pruebas; humano/receptor decide recibos.
