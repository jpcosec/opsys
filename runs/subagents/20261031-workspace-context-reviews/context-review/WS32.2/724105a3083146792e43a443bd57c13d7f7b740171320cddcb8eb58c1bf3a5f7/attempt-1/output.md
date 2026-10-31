## REFORMULACION

Propósito: encargo de planificación para hacer idempotente la persistencia local de manifiesto, RunDoc y cierre asociados al id de intento que cita el cierre. Resultado: una finalización repetida del mismo intento conserva identidad y evidencia sin crear registros nuevos, y manifiesto, RunDoc y closeout coinciden en id de intento, hash de sesión y evidencia. Repo dueño: `deskops`. Límites: solo operaciones locales reales sobre store temporal; sin dispatch/reply de red ni confirmar eventos Hub no observados; sin hash de proceso/slug ni valores fabricados. Depende de WS05, WS12 y WS32.1; gates: G_CLOSEOUT satisfecho, G_SCION no verificado, G_WRITE_CONTRACT pendiente por delta.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

Lecturas previstas: ticket de `external_references.scion`, auditoría WS05, contrato WS12, salidas de WS32.1, `deskops/runtime/scion.py`, `models/run.py`, `services/closure.py`, tests y evidencia de G_CLOSEOUT. Cambios previstos: persistencia idempotente por id de intento y pruebas de repetición; sin red. Dependencias: artefacto/contrato de sesión y hash de WS05/WS12, registro por intento de WS32.1 y gates declarados. Si falta artefacto o contrato de hash, corresponde registrar hueco y bloquear la coincidencia antes de promoción. Validaciones futuras: ejecutar tests locales con store temporal, repetir la finalización sobre el mismo id de intento, comprobar ausencia de duplicados y coincidencia de id, hash y evidencia; no invocar Hub.

## FUTURO

WS05/WS12 producen inventario, contrato y artefacto de sesión/hash; WS44 resuelve G_SCION; WS34/37 prueban dispatch/Hub real y correlación bajo G_EXEC; WS06 y la promoción fijan TaskDoc, archivos exactos y preflight; una persona autoriza la promoción. Nada de eso se decide en este nodo.
