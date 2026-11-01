REFORMULACION
WS32 es un agregado de implementación, candidato, del plan. Propósito: unificar identidad de intento y cierre Scion desde el candidato de drawer citado (external_references.scion), sin segundo pipeline: intento no es slug, dispatch intent/confirmed son hechos separados, manifiesto/RunDoc/cierre consistentes e idempotentes. Resultado: salidas de WS32.1/WS32.2 en deskops (`runtime/scion.py`, `models/run.py`, `services/closure.py`, tests), con identidad/registro/idempotencia local sin dispatch/reply de red. Repo dueño: deskops. Límites: no es ticket del Board; sin eventos Hub simulados; estados Hub reales se prueban en WS34/37 bajo G_EXEC; promoción no autorizada. Depende de WS05 (inventario Scion), WS12 (contrato) y sus hijos. Gates: G_CLOSEOUT satisfecho; G_SCION no verificado; G_WRITE_CONTRACT pendiente per_delta.

AMBIGUEDADES
ninguna

DRY-RUN
WS32 es agregado no ejecutable: no produce cambios propios; se cumple con WS32.1 y WS32.2. Orden real: WS32.1 -> WS32.2 (WS32.2 depende de WS32.1); ambos consumen WS05 y WS12; WS32 espera a ambos.
WS32.1: lee inventario WS05 y contrato WS12; cambia `deskops/runtime/scion.py`, `models/run.py`, `services/closure.py` y tests; materializa registro local y dos IDs de intento distintos; registra intent/no confirmado con operaciones reales en store temporal, sin red ni mock. Transfiere a WS32.2 el id y el registro local.
WS32.2: consume WS32.1; mismos archivos/tests; hace manifiesto/RunDoc/cierre idempotentes sobre ese id; una finalización repetida conserva identidad, hash de sesión y evidencia sin duplicar. Si falta contrato/artefacto de hash, registra hueco con WS12/WS05 y bloquea.
Dependencias/gates: G_CLOSEOUT satisfecho; G_SCION no verificado no habilita dispatch/reply real; G_WRITE_CONTRACT per_delta pendiente. Si faltan WS05/WS12, detenerse y registrar hueco con dueño, sin sustituto. Validación conjunta: pruebas en store temporal real (IDs distintos; idempotencia sin duplicados); Hub real queda para WS34/37 bajo G_EXEC. El agregado se valida cuando constan ambas aceptaciones hijas.

FUTURO
WS05 produce el inventario de identidad/API Scion. WS12 fija contrato, ubicación del registro por intento y precondición de escritura; G_WRITE_CONTRACT se recibe por delta. WS44 produce G_SCION con probe real; el operador Scion se designa al abordar el ramal E. WS34/37 prueban dispatch/confirmación real y correlación bajo G_EXEC. Un humano decide la promoción (not_authorized; preflight task-only) y el acta de recepción que corresponda; WS06 mantiene la matriz.
