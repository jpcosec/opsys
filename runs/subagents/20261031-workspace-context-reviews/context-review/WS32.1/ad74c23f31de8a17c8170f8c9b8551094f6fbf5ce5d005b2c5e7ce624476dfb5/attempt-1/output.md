## REFORMULACION
**Propósito:** separar la identidad de intento del slug y registrar `dispatch` (intención) y `confirmed` (aceptación de Scion) como hechos distintos del RunDoc. **Resultado:** ids de intento generados por deskops antes del dispatch, estados de dispatch fallido conservados y pruebas de identidades distintas. **Repo:** deskops. **Límites:** refinar el ticket existente sin segundo pipeline; identidad pública de Scion solo según WS05/WS44; RunDoc mediante flujo SLDB/CLI sldb, no edición ad hoc; no duplicar trabajo de scion.

## AMBIGUEDADES
1. «un dispatch fallido (rechazo de la API o timeout, que deja confirmed desconocido hasta reconciliar)»: no se define qué es reconciliar, quién lo ejecuta, con qué evidencia ni cuándo el estado deja de ser desconocido. Obligaría a inventar el mecanismo, el actor y el criterio comprobable; también si un rechazo explícito debe quedar desconocido o como fallo confirmado.

## DRY-RUN
- **Lecturas:** input del nodo, guía, brief, alcance, decisiones, cobertura y reconciliación; bloques de contrato WS05/WS12/WS32/WS32.2 solo como vecinos.
- **Cambios previstos:** `deskops/runtime/scion.py`, `models/run.py`, `services/closure.py` y `tests/`; registro por intento, generación de id, estados dispatch/confirmed y pruebas de dos intentos y dispatch fallido.
- **Dependencias:** WS05 (inventario), WS12 (contrato), gates G_CLOSEOUT, G_SCION, G_WRITE_CONTRACT; WS32.2 consume el registro.
- **Validaciones futuras:** pruebas de identidad y fallo, evidencia de gates, probe WS44 e idempotencia de WS32.2.

## FUTURO
WS05 produce el inventario de API/identidad; WS44 produce G_SCION con probe; WS12 produce whitelist/capability; WS32.2 convierte el registro en manifiesto canónico; WS32 cierra como agregado; un humano autoriza la promoción y resuelve decisiones pendientes. Nada de esto se ejecuta aquí.
