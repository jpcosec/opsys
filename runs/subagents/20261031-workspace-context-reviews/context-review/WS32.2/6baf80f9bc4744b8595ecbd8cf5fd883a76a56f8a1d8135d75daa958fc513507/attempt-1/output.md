REFORMULACION
- **Propósito**: fijar WS32.2 como encargo de planificación para hacer idempotentes manifiesto, RunDoc y cierre sobre el id de intento.
- **Resultado**: una finalización repetida del mismo intento conserva identidad y evidencia sin crear registros nuevos; manifiesto, RunDoc y closeout coinciden en id de intento, hash de sesión y evidencia.
- **Repo dueño**: deskops. `output_scope`: `runtime/scion.py`, `models/run.py`, `services/closure.py`, `tests/`.
- **Límites**: sin dispatch/reply ni red, sin simular Hub, sin hash fabricado; si falta artefacto o contrato de hash, registrar hueco con WS12/WS05 y bloquear esa coincidencia. Promoción no autorizada. Depende de WS05, WS12 y WS32.1; requiere G_CLOSEOUT (satisfecho), G_SCION y G_WRITE_CONTRACT (pendientes).

AMBIGUEDADES
ninguna.

DRY-RUN
- **Lecturas previstas**: `dag.yaml` (nodo, gates y aristas), ticket de `external_references.scion`, inventario WS05, contrato WS12, evidencia de G_CLOSEOUT y código/pruebas actuales de `scion.py`, `run.py` y `closure.py`.
- **Cambios previstos**: registro idempotente por intento en esos archivos y pruebas asociadas; sin red ni dispatch.
- **Dependencias**: WS05, WS12 y WS32.1; G_SCION y G_WRITE_CONTRACT pendientes; G_CLOSEOUT disponible.
- **Validaciones futuras**: store temporal real, repetición de finalización, ausencia de duplicados y coincidencia de id/hash/evidencia; bloqueo y registro de hueco si falta contrato de hash; preflight de promoción.

FUTURO
- WS05 produce el inventario de identidad/API Scion; WS12 el contrato de registro y operaciones; WS32.1 el registro por intento; WS44 produce G_SCION; WS34/37 prueban Hub y correlación bajo G_EXEC. Un humano autoriza promoción/ejecución y el receptor P01 emite acta por delta.
