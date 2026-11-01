## REFORMULACION
**Propósito:** hacer idempotente la persistencia local de manifiesto, RunDoc y cierre sobre el id de intento correcto. **Resultado:** finalizaciones repetidas no crean registros nuevos y manifiesto/RunDoc/closeout coinciden en id de intento, hash de sesión y evidencia. **Repo:** deskops (`runtime/scion.py`, `models/run.py`, `services/closure.py`, `tests/`). **Límites:** sin dispatch/reply de red ni evento Hub simulado; prueba Hub y correlación en WS34/37 bajo G_EXEC; promoción no autorizada.

## AMBIGUEDADES
1. «según el ticket de external_references.scion» — otras fuentes lo llaman «candidato de drawer» y la referencia externa declara `observed_source_not_gate_acceptance`. Obligaría a decidir si se trata como ticket autoritativo o solo como fuente observada.
2. «Una finalización repetida sobre el mismo id de intento» — no se nombra la operación concreta cuya repetición debe ser idempotente (`close_from_run`, cierre, otra). Obligaría a inventar qué operación se prueba y qué cuenta como “registro nuevo”.

## DRY-RUN
**Lecturas previstas:** nodo WS32.2, referencia externa Scion (sha256 declarado), contrato WS32.1, inventario WS05, contrato WS12, código actual de `scion.py`, `closure.py`, `models/run.py` y pruebas existentes.
**Cambios previstos:** persistencia idempotente en `runtime/scion.py` y `services/closure.py`; modelo/registro en `models/run.py`; pruebas en `tests/`.
**Dependencias:** WS05 aporta artefacto de sesión, fuente/ algoritmo de hash e identidad de run si la API la expone; WS12 fija campo/ algoritmo de hash y ubicación del registro por intento; WS32.1 materializa identidad y registro. Gates: G_CLOSEOUT satisfecho; G_SCION no verificado (WS44); G_WRITE_CONTRACT pendiente por delta.
**Validaciones futuras:** repetir finalización sobre store temporal real; comprobar ausencia de registros nuevos y coincidencia de id de intento, hash de sesión y evidencia; ante falta de artefacto/contrato, registrar hueco y bloquear la coincidencia.

## FUTURO
WS05 entrega el inventario de identidad/API y el artefacto de sesión; WS12 publica contrato, campo/ algoritmo de hash y ubicación del registro; WS32.1 materializa el registro por intento. WS44 produce G_SCION; WS34/37 prueban Hub real y correlación bajo G_EXEC. Un humano autoriza la promoción del nodo.
