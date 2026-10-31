# REFORMULACION

**Propósito:** encargo de planificación para integrar edición de campos y relaciones en el workspace de graph_ui, con revisión (before-image/CAS), conflicto visible y campos workflow-protegidos excluidos del canal.

**Resultado:** nodo agregado; no ejecutable por sí mismo. Su resultado es la suma de WS19.1 (campos) y WS19.2 (relaciones).

**Repo dueño:** `graph_ui`; base `graph_ui:repository_root/`, sobre ticket draft de edición, sin duplicarlo.

**Límites:** no crear semántica de relaciones en el componente; mutación solo en desk manual exclusivo (P03); consumir endpoints del contrato WS12 sin modificarlo; promoción `not_authorized`; gates pendientes no se satisfacen aquí.

# AMBIGUEDADES

1. **`kind: implementation` frente a `node_role: aggregate` y “Agregado no ejecutable: se cumple cuando todos sus hijos cumplen su aceptación.”** El nodo declara naturaleza de implementación y estimación M, pero su aceptación lo declara no ejecutable. Esto obliga al ejecutor a inventar si WS19 produce artefactos propios (código, tests, evidencia) o solo coordina a sus hijos; una lectura literal de `kind` podría exceder el alcance agregado.

# DRY-RUN

- **Lecturas previstas:** nodo WS19 y sus hijos WS19.1/WS19.2; vecinos WS12 (contrato/whitelist y G_UI_WRITE, G_WRITE_CONTRACT), WS16 (G_HUMAN_READ), WS21 y WS42 como consumidores; guía, brief, alcance, decisiones, cobertura, reconciliación; `task-ws19.md` al promoverse.
- **Cambios previstos:** ninguno en este nodo agregado. Al promoverse, los hijos tocarían `frontends/mindmap/views/workspace/fields/` y `.../relations/` más `tests/`, consumiendo endpoints WS12.
- **Dependencias:** WS12 y WS16 pendientes; WS11/WS06 llegan transitivamente; gates G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT en `pending`.
- **Validaciones futuras:** aceptación de cada hijo (guardar/recargar, conflicto sin pérdida de texto local, rechazo de relación no permitida o revisión obsoleta); actas de gates; pruebas técnicas separadas de la aprobación humana. Sin ejecución.

# FUTURO

- WS16 produce el acta de G_HUMAN_READ.
- WS12 produce whitelist, capability exacta y aceptación del delta en graph_ui (G_UI_WRITE/G_WRITE_CONTRACT), incluida la tarea receptora sin solapamiento.
- WS19.1 y WS19.2 implementan; WS21 y WS42 consumen el resultado.
- El humano resuelve P01/P03/P04/P06 y WS07 designa responsables; el concilio no aprueba nada de esto.
