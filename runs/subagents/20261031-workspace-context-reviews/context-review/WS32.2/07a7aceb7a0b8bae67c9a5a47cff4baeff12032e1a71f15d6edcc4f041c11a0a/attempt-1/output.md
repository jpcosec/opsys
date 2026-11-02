## REFORMULACION
**Propósito:** hacer idempotente la finalización de un intento Scion, usando siempre el id de intento que cita el cierre, nunca agente o slug. **Resultado:** manifiesto, RunDoc y registros de closeout consistentes; repetir la finalización sobre el mismo id no crea registros nuevos y conserva identidad, hash de sesión y evidencia. **Repo:** deskops. **Límites:** solo persistencia local con operaciones reales sobre store temporal; sin dispatch/reply de red, sin confirmar eventos Hub no observados y sin fabricar hash o evidencia. Si falta artefacto/contrato de hash, se registra hueco y se bloquea la coincidencia antes de promoción.

## AMBIGUEDADES
1. «sin dispatch/reply de red ni confirmar evento Hub no observado; prueba runtime con Hub y correlación es WS34/37 bajo G_EXEC» frente a `requires: G_SCION`. G_SCION está `unverified` y significa «Scion accesible y contrato público comprobado», aunque este nodo declara trabajo local sin red. Obliga a inventar si el ejecutor debe detenerse por G_SCION o considerar que no aplica a la idempotencia local; ambas lecturas cambian si puede ejecutar y qué gate consume.

## DRY-RUN
Nodo ejecutable (`kind: implementation`), no agregado. Lecturas hipotéticas: `dag.yaml` de WS32.2, candidato externo Scion, `auditoria/scion.md` (WS05), `contratos/operaciones.md` (WS12), código/tests de WS32.1, `deskops/runtime/scion.py`, `models/run.py`, `services/closure.py` y pruebas de closeout.

Cambios previstos: persistencia idempotente por id de intento en `scion.py`/`closure.py`; campos de manifiesto/RunDoc en `models/run.py`; pruebas con store temporal que repitan la finalización y comprueben una sola identidad y evidencia coincidente.

Dependencias/gates: consume WS05, WS12 y WS32.1. G_CLOSEOUT está `satisfied`; G_WRITE_CONTRACT está `per_delta` y `accepted_scope_nodes` no incluye WS32.2; G_SCION está `unverified`. Si se aplica G_SCION, el ejecutor se detiene sin mutar. Errores: contrato, ubicación o artefacto de hash ausentes → registrar hueco con productor y no crear sustituto. Validación esperada: misma finalización → un registro, mismo id/hash/evidencia; ids distintos → registros separados. Sin ejecutar nada.

## FUTURO
WS05 aporta inventario de identidad/API; WS12 fija contrato, ubicación y artefacto de hash; WS32.1 entrega registro por intento; WS44 resuelve G_SCION; WS34/37 prueban Hub real bajo G_EXEC. La promoción fijará archivos, pruebas y recibo per_delta; no corresponde a este nodo.
