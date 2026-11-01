## REFORMULACION
**Propósito:** unificar identidad de intento y cierre Scion, refinando el candidato de drawer de `external_references.scion` sin crear un segundo pipeline.
**Resultado:** agregado cuyas salidas son las de WS32.1 y WS32.2; este nodo no se ejecuta.
**Repo:** deskops (`owner_repo: deskops`, `output_base: deskops:repository_root/`).
**Límites:** sin dispatch/reply de red ni eventos Hub fingidos; identidad/registro/idempotencia solo local; la correlación Hub real queda para WS34/WS37 bajo G_EXEC. Depende de WS05 y WS12; requiere G_CLOSEOUT (satisfecho), G_SCION (unverified) y G_WRITE_CONTRACT (pending, per_delta).

## AMBIGUEDADES
Ninguna. El nodo es agregado y su aceptación delega explícitamente: «se cumple cuando todos sus hijos cumplen su aceptación». Los detalles de almacenamiento, campos y hash quedan atribuidos a WS12/WS05 en los hijos y en el contrato de vecinos, no a este nodo.

## DRY-RUN
Nodo `aggregate`: no ejecutable; lo cumplen sus hijos.
- **WS32.1** cambiaría, hipotéticamente, `deskops/runtime/scion.py`, `models/run.py`, `services/closure.py` y `tests/`: separar id de intento de slug, registrar `intent` y `confirmed` como hechos distintos, persistir vía operaciones reales del store temporal. Consume el inventario WS05 y el contrato WS12 (registro por intento); gates G_CLOSEOUT/G_SCION/G_WRITE_CONTRACT.
- **WS32.2** cambiaría los mismos archivos: manifiesto canónico por intento, RunDoc y closeout idempotentes, coincidencia de id, hash de sesión y evidencia. Consume WS32.1.
- **Errores:** si falta el artefacto/hash o el contrato de operación, detenerse y registrar hueco con productor WS12/WS05; si G_SCION no está verificado, no afirmar Hub ni ejecutar red; sin mock de respuesta.
- **Validación esperada:** dos intentos generan IDs distintos; finalización repetida no duplica registros ni evidencia. WS32 termina cuando ambos hijos aceptan.

## FUTURO
- WS05 produce el inventario de identidad/API Scion.
- WS12 produce contrato de operaciones y ubicación del registro por intento.
- WS44 produce G_SCION mediante probe real; el operador Scion lo designa un humano al abordar el ramal E.
- Un humano decide G_EXEC y acepta el delta en el repo dueño; la promoción sigue `not_authorized`.
