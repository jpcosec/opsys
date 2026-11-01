## REFORMULACION

- **Propósito**: agrupar WS32.1 y WS32.2 para unificar identidad de intento y cierre Scion sin un segundo pipeline: intento ≠ slug, dispatch intent/confirmed separados, manifiesto/RunDoc/cierre consistentes e idempotentes.
- **Resultado**: agregado no ejecutable. Se cumple cuando sus hijos cumplen su aceptación; sus salidas son las de WS32.1 y WS32.2.
- **Repo**: `deskops`.
- **Límites**: nodo `candidate`; promoción `not_authorized`; no dispatch/reply de red ni eventos Hub simulados; los estados Hub reales se prueban en WS34/37 bajo G_EXEC; el candidato de drawer citado no es ticket del Board.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

- **Lecturas**: `dag.yaml` (nodo WS32, gates, `external_references.scion`), `context-review-guide.md`, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `reconciliacion.md`.
- **Cambios previstos**: ninguno. Es un agregado y no se ejecuta; no modifica TaskDoc, Board ni archivos.
- **Dependencias**: WS05 (inventario Scion), WS12 (contrato de operaciones/registro), WS32.1 y WS32.2. Gates: G_CLOSEOUT `satisfied`; G_SCION `unverified`; G_WRITE_CONTRACT `pending`, evaluación `per_delta`. No se asume satisfacción de gates pendientes.
- **Validaciones futuras**: aceptación de ambos hijos; identidad/idempotencia local con operaciones reales sobre store temporal; correlación real solo en WS34/37; preflight task-only, archivos cambiados, pills/átomos/evidencia antes de cualquier promoción. Sin ejecución.

## FUTURO

- WS44 produce la evidencia de G_SCION; WS05 entrega el inventario; WS12 fija contrato y ubicación del registro por intento; WS32.1/32.2 implementan identidad e idempotencia; WS34/37 prueban dispatch y correlación reales bajo G_EXEC.
- La persona responsable autoriza la promoción y el TaskDoc de promoción fija archivos, escenarios y textos dentro de la aceptación.
- Nada de esto se decide ni se ejecuta en este nodo.
