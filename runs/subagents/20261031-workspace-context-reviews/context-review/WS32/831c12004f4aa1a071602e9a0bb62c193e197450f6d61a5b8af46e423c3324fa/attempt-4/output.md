## REFORMULACION
- **Propósito:** agrupar la revisión del ticket Scion para unificar identidad de intento —no slug—, separar dispatch `intent`/`confirmed` y dejar manifiesto/RunDoc/cierre consistentes e idempotentes.
- **Resultado:** agregado no ejecutable; salidas de WS32.1 y WS32.2.
- **Repo dueño:** deskops.
- **Límites:** «sin segundo pipeline»; `node_role: aggregate`; `promotion: not_authorized`; gates G_CLOSEOUT, G_SCION y G_WRITE_CONTRACT.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
- **Lecturas:** `dag.yaml` —nodo WS32, `external_references.scion` y gates—; `auditoria/scion.md` de WS05; `contratos/operaciones.md` de WS12; salidas de WS32.1/WS32.2; `decisiones.md`, `reconciliacion.md` y `cobertura.md`.
- **Cambios previstos:** el agregado no ejecuta ni edita código por sí mismo. Los hijos prevén `deskops/runtime/scion.py`, `models/run.py`, `services/closure.py` y `tests/`.
- **Dependencias:** WS05 y WS12; hijos WS32.1 y WS32.2; gates G_CLOSEOUT, G_SCION y G_WRITE_CONTRACT.
- **Validaciones futuras:** aceptación de hijos —dos intentos del mismo agente y un dispatch fallido con identidades distintas; finalización repetida sobre el mismo id de intento sin registros nuevos—; preflight de promoción; evidencia de gates.

## FUTURO
WS05 produce el inventario; WS12, el contrato de operaciones; WS44, el probe de G_SCION; el resolver externo de G_CLOSEOUT, su evidencia. WS33, WS34 y WS36 consumen el resultado. WS07 y las decisiones P01/P04/P08 son humanas. El TaskDoc de promoción fijará archivos, pills, átomos y evidencia. Nada de ello es ambigüedad del encargo.
