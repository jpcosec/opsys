## REFORMULACION

**Propósito:** traducir los deltas y capacidades del plan a una correspondencia con repos dueños y tickets existentes, clasificando cada uno como ya cubierto (capacidad observable en código, con referencia), extensión de ticket (incluido un draft del Board) o delta nuevo.

**Resultado:** `reconciliacion.md` con una matriz agrupada por repo dueño, conservando el tratamiento ya registrado de la fila Scion RunDoc/cierre (WS32/33), sin requerir WS05.

**Repo dueño:** deskops.

**Límites:** no notificar, despachar ni modificar el Board de graph_ui; no produce gates de aceptación ni aprueba deltas aún indefinidos; la aceptación específica por repo receptor queda en WS11/12.

## AMBIGUEDADES

1. «responsable por designar» (acceptance) frente a «el responsable receptor ya designado en P01» (scope) y P01 en decisiones.md. Contradicción entre fuentes suministradas: obliga a inventar si el ejecutor debe designar responsable, dejarlo pendiente o limitarse a registrar la designación ya existente.

2. «Una matriz por implementación» frente a «una fila por delta o capacidad propuesta, agrupada por repo dueño». Unidad de fila indefinida: obliga a inventar si una implementación con varios deltas produce una fila o varias, y cómo deduplicar capacidades ya cubiertas repetidas entre nodos.

3. «capacidad observable en código implementado, con referencia». No fija qué constituye referencia suficiente (path, commit, hash, salida de comando); obliga a inventar el criterio de comprobación de la columna «ya cubierto».

## DRY-RUN

- **Lecturas previstas:** `reconciliacion.md` vigente, `dag.yaml`, `decisiones.md`, `cobertura.md`, `brief.md`, `alcance.md`, y las salidas de WS02 (`auditoria/deskops.md`), WS03 (`auditoria/infraestructura.md`) y WS04 (`auditoria/ui.md`).
- **Cambios previstos:** solo `reconciliacion.md`; ningún archivo de graph_ui ni del Board.
- **Dependencias:** WS02–WS04 como insumos; P01 como designación registrada; WS11/12 como receptores de la aceptación por delta.
- **Validaciones futuras:** una fila por delta/capacidad, agrupación por repo dueño, conservación de la fila Scion, ausencia de gates y de aprobaciones nuevas.

## FUTURO

- WS02/WS03/WS04 entregan sus auditorías como insumo.
- WS11/WS12 obtienen la aceptación específica por repo receptor.
- WS07 verifica y reutiliza el registro de decisiones sin repetir preguntas.
- El solicitante o el humano confirma cualquier designación pendiente; no es ambigüedad de este nodo si el registro P01 se considera suficiente.
